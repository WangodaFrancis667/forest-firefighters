# autonomous_mavic.py Inspection

Date: Sun Jun 14 16:34:35 UTC 2026

## Important Code Locations
```text
11:    import cv2
13:    sys.exit("Warning: 'cv2' module not found.")
23:    # Vertical offset where the robot actually targets to stabilize itself.
31:    # Precision between the target position and the robot position in meters
32:    target_precision = 0.5
39:        self.water_to_drop = 0
42:        self.camera = self.getDevice("camera")
43:        self.camera.enable(self.time_step)
44:        self.imu = self.getDevice("inertial unit")
46:        self.gps = self.getDevice("gps")
47:        self.gps.enable(self.time_step)
48:        self.gyro = self.getDevice("gyro")
49:        self.gyro.enable(self.time_step)
51:        self.front_left_motor = self.getDevice("front left propeller")
52:        self.front_right_motor = self.getDevice("front right propeller")
53:        self.rear_left_motor = self.getDevice("rear left propeller")
54:        self.rear_right_motor = self.getDevice("rear right propeller")
55:        self.camera_pitch_motor = self.getDevice("camera pitch")
56:        self.camera_pitch_motor.setPosition(1.55)  # vertical PoV
57:        motors = [self.front_left_motor, self.front_right_motor,
58:                  self.rear_left_motor, self.rear_right_motor]
59:        for motor in motors:
60:            motor.setPosition(float('inf'))
61:            motor.setVelocity(1)
64:        self.target_position = [0, 0, 0]
65:        self.target_index = 0
67:        self.world_fire_quadrants = [0, 0]
68:        self.img_coord_fire = []
71:    def get_image_from_camera(self):
73:        Take an image from the camera and prepare it for OpenCV processing:
78:            image of the camera
80:        img = self.camera.getImageArray()
82:        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
83:        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
84:        return cv2.flip(img, 1)
94:    def move_to_target(self, waypoints, verbose_movement=False, verbose_target=True):
100:            verbose_target (bool): whether to print targets or not
106:        if self.target_position[0:2] == [0, 0]:  # Initialisation
107:            self.target_position[0:2] = waypoints[0]
108:            if verbose_target:
109:                print("First target: ", self.target_position[0:2])
111:        # if the robot is at the position with a precision of target_precision
112:        if all([abs(x1 - x2) < self.target_precision for (x1, x2) in zip(self.target_position, self.current_pose[0:2])]):
114:            self.target_index += 1
115:            if self.target_index > len(waypoints)-1:
116:                self.target_index = 0
117:            self.target_position[0:2] = waypoints[self.target_index]
118:            if verbose_target:
119:                print("Target reached! New target: ",
120:                      self.target_position[0:2])
123:        self.target_position[2] = np.arctan2(
124:            self.target_position[1] - self.current_pose[1], self.target_position[0] - self.current_pose[0])
126:        angle_left = self.target_position[2] - self.current_pose[5]
139:            distance_left = np.sqrt(((self.target_position[0] - self.current_pose[0]) ** 2) + (
140:                (self.target_position[1] - self.current_pose[1]) ** 2))
147:        Naive approach to move the robot above the fire. 
148:        Closed loop to move the robot towards to the fire step-by-step until it reaches the fire.
155:        resolutionX, resolutionY = self.camera.getWidth(), self.camera.getHeight()
156:        x_img, y_img = self.img_coord_fire
158:        self.world_fire_quadrants = [0, 0]
161:            self.world_fire_quadrants[0] = np.sign(x_img-resolutionX/2)
163:            self.world_fire_quadrants[1] = np.sign(y_img-resolutionY/2)
164:        self.world_fire_quadrants[1] *= np.sign(yaw)
165:        self.world_fire_quadrants[0] *= -np.sign(yaw)
167:        yaw_disturbance = self.world_fire_quadrants[0]*clamp(
169:        pitch_disturbance = self.world_fire_quadrants[1]*clamp(
172:        if self.world_fire_quadrants == [0, 0]:
173:            self.water_to_drop = 15
175:                print("Water dropped on fire target: {} at position {}".format(
176:                    self.target_position[0:2], self.current_pose[0:2]))
177:            self.img_coord_fire = []
181:    def fire_detection(self, verbose=True):
183:        Detect the smoke and return the fire coordinate in the image
187:            coord_fire (list):x,y image coordinates of the fire
189:        img = self.get_image_from_camera()
191:        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
193:        # Range of the smoke
194:        smoke_lower = np.array([0, 0, 168])
195:        smoke_upper = np.array([172, 111, 255])
197:        mask_fire = cv2.inRange(hsv, smoke_lower, smoke_upper)
199:        fire_ratio = np.round(
200:            (cv2.countNonZero(mask_fire))/(img.size/3)*100, 2)
201:        if fire_ratio > 0.15:  # Higher the fire ratio, higher the number of fire in the image
203:            # Detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
204:            contours, _ = cv2.findContours(
205:                image=mask_fire, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
213:                contours_poly[i] = cv2.approxPolyDP(c, 3, True)
214:                centers[i], radius[i] = cv2.minEnclosingCircle(
218:                    coord_fire = centers[i]
222:                            "fire detected, coordinates {}".format(centers[i]))
229:                    cv2.drawContours(drawing, contours_poly, i, color)
230:                    cv2.circle(drawing, (int(centers[i][0]), int(
232:                cv2.imwrite("fire_detection.jpg", drawing)
233:            return coord_fire
244:        # We add controller args to waypoints and target_altitude variables
246:        opt_parser.add_option("--patrol_coords", default="11 11, 11 21, 21 21,21 11",
247:                              help="Specify the patrol coordinates in the format [x1 y1, x2 y2, ...]")
248:        opt_parser.add_option("--target_altitude", default=42,
249:                              type=float, help="target altitude of the robot in meters")
252:        point_list = options.patrol_coords.split(',')
260:        target_altitude = options.target_altitude
266:            Xpos, Ypos, altitude = self.gps.getValues()
267:            roll_acceleration, pitch_acceleration, _ = self.gyro.getValues()
270:            # Drop the water from the drone
271:            if self.water_to_drop > 0:
273:                self.setCustomData(str(self.water_to_drop))
274:                self.water_to_drop = 0
278:            if altitude > target_altitude - 1:
281:                    if self.img_coord_fire:
284:                        yaw_disturbance, pitch_disturbance = self.move_to_target(
290:                        self.img_coord_fire = self.fire_detection()
295:                if self.getTime() - t3 > 15:  # Wait 15 times to avoid detection of the dropping water as smoke
304:                target_altitude - altitude + self.K_VERTICAL_OFFSET, -1, 1)
308:            front_left_motor_input = self.K_VERTICAL_THRUST + \
310:            front_right_motor_input = self.K_VERTICAL_THRUST + \
312:            rear_left_motor_input = self.K_VERTICAL_THRUST + \
314:            rear_right_motor_input = self.K_VERTICAL_THRUST + \
317:            self.front_left_motor.setVelocity(front_left_motor_input)
318:            self.front_right_motor.setVelocity(-front_right_motor_input)
319:            self.rear_left_motor.setVelocity(-rear_left_motor_input)
320:            self.rear_right_motor.setVelocity(rear_right_motor_input)
```
