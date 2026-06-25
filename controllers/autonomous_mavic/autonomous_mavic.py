from controller import Robot
import sys
import optparse
try:
    import numpy as np
    from numpy import NaN, nan
except ImportError:
    sys.exit("Warning: 'numpy' module not found.")
try:
    import cv2
except ImportError:
    sys.exit("Warning: 'cv2' module not found.")


def clamp(value, value_min, value_max):
    return min(max(value, value_min), value_max)


class Mavic (Robot):
    # Constants, empirically found.
    K_VERTICAL_THRUST = 68.5  # with this thrust, the drone lifts.
    # Vertical offset where the robot actually targets to stabilize itself.
    K_VERTICAL_OFFSET = 0.6
    K_VERTICAL_P = 3.0        # P constant of the vertical PID.
    K_ROLL_P = 50.0           # P constant of the roll PID.
    K_PITCH_P = 30.0          # P constant of the pitch PID.

    MAX_YAW_DISTURBANCE = 0.65
    MAX_PITCH_DISTURBANCE = -1.35
    # Precision between the target position and the robot position in meters
    target_precision = 0.8

    def __init__(self):
        Robot.__init__(self)

        self.time_step = int(self.getBasicTimeStep())
        self.name = self.getName()

        self.water_to_drop = 0

        # Get and enable devices.
        self.camera = self.getDevice("camera")
        self.camera.enable(self.time_step)
        if self.camera.hasRecognition():
            self.camera.recognitionEnable(max(4 * self.time_step, 250))
        self.imu = self.getDevice("inertial unit")
        self.imu.enable(self.time_step)
        self.gps = self.getDevice("gps")
        self.gps.enable(self.time_step)
        self.gyro = self.getDevice("gyro")
        self.gyro.enable(self.time_step)

        self.front_left_motor = self.getDevice("front left propeller")
        self.front_right_motor = self.getDevice("front right propeller")
        self.rear_left_motor = self.getDevice("rear left propeller")
        self.rear_right_motor = self.getDevice("rear right propeller")
        self.camera_pitch_motor = self.getDevice("camera pitch")
        self.camera_pitch_motor.setPosition(1.55)  # vertical PoV
        motors = [self.front_left_motor, self.front_right_motor,
                  self.rear_left_motor, self.rear_right_motor]
        for motor in motors:
            motor.setPosition(float('inf'))
            motor.setVelocity(1)

        self.current_pose = 6*[0]  # X,Y,Z, yaw, pitch, roll
        self.target_position = [0, 0, 0]
        self.target_index = 0

        self.world_fire_quadrants = [0, 0]
        self.img_coord_fire = []
        self.fire_bbox = None
        self.WaterDropStatus = False
        self.debug_images = False
        self.display = self.get_optional_display()
        if self.display:
            self.display.attachCamera(self.camera)
            self.display.setFont("Arial", 10, True)

    def get_optional_display(self):
        try:
            return self.getDevice("vision overlay")
        except Exception:
            return None

    def get_image_from_camera(self):
        """
        Take an image from the camera and prepare it for OpenCV processing:
        - convert data type,
        - convert to RGB format (from BGRA), and
        - rotate & flip to match the actual image.
        Returns:
            image of the camera
        """
        width = self.camera.getWidth()
        height = self.camera.getHeight()
        img = self.camera.getImage()
        if img is None:
            return None
        img = np.frombuffer(img, np.uint8).reshape((height, width, 4))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        return cv2.flip(img, 1)

    def set_position(self, pos):
        """
        Set a new absolut position of the robot
        Parameters:
            pos (list): [X,Y,Z,yaw,pitch,roll] current absolut position and angles
        """
        self.current_pose = pos

    def move_to_target(self, waypoints, verbose_movement=False, verbose_target=True):
        """
        Move the robot to the given coordinates
        Parameters:
            waypoints (list): list of X,Y coordinates
            verbose_movement (bool): whether to print remaning angle and distance or not
            verbose_target (bool): whether to print targets or not
        Returns:
            yaw_disturbance (float): yaw disturbance (negative value to go on the right)
            pitch_disturbance (float): pitch disturbance (negative value to go forward)
        """

        if self.target_position[0:2] == [0, 0]:  # Initialisation
            self.target_position[0:2] = waypoints[0]
            if verbose_target:
                print("First target: ", self.target_position[0:2])

        # if the robot is at the position with a precision of target_precision
        if all([abs(x1 - x2) < self.target_precision for (x1, x2) in zip(self.target_position, self.current_pose[0:2])]):

            self.target_index += 1
            if self.target_index > len(waypoints)-1:
                self.target_index = 0
            self.target_position[0:2] = waypoints[self.target_index]
            if verbose_target:
                print("Target reached! New target: ",
                      self.target_position[0:2])

        # This will be in ]-pi;pi]
        self.target_position[2] = np.arctan2(
            self.target_position[1] - self.current_pose[1], self.target_position[0] - self.current_pose[0])
        # This is now in ]-2pi;2pi[
        angle_left = self.target_position[2] - self.current_pose[5]
        # Normalize turn angle to ]-pi;pi]
        angle_left = (angle_left + 2*np.pi) % (2*np.pi)
        if (angle_left > np.pi):
            angle_left -= 2*np.pi

        # Turn the robot to the left or to the right according the value and the sign of angle_left
        yaw_disturbance = self.MAX_YAW_DISTURBANCE*angle_left/(2*np.pi)
        # non proportional and decruising function
        pitch_disturbance = clamp(
            np.log10(abs(angle_left)), self.MAX_PITCH_DISTURBANCE, 0.1)

        if verbose_movement:
            distance_left = np.sqrt(((self.target_position[0] - self.current_pose[0]) ** 2) + (
                (self.target_position[1] - self.current_pose[1]) ** 2))
            print("remaning angle: {:.4f}, remaning distance: {:.4f}".format(
                angle_left, distance_left))
        return yaw_disturbance, pitch_disturbance

    def naive_approach(self, verbose=True):
        """
        Naive approach to move the robot above the fire. 
        Closed loop to move the robot towards to the fire step-by-step until it reaches the fire.
        Parameters:
            verbose (bool): whether to print status messages or not
        Returns:
            yaw_disturbance (float): yaw disturbance (negative value to go on the right)
            pitch_disturbance (float): pitch disturbance (negative value to go forward)
        """
        resolutionX, resolutionY = self.camera.getWidth(), self.camera.getHeight()
        x_img, y_img = self.img_coord_fire
        yaw = (self.current_pose[5] + 2*np.pi) % (2*np.pi)
        self.world_fire_quadrants = [0, 0]

        if abs(x_img-resolutionX/2) > 20:
            self.world_fire_quadrants[0] = np.sign(x_img-resolutionX/2)
        if abs(y_img-resolutionY/2) > 20:
            self.world_fire_quadrants[1] = np.sign(y_img-resolutionY/2)
        self.world_fire_quadrants[1] *= np.sign(yaw)
        self.world_fire_quadrants[0] *= -np.sign(yaw)

        yaw_disturbance = self.world_fire_quadrants[0]*clamp(
            abs(x_img-resolutionX/2), 0, self.MAX_YAW_DISTURBANCE)
        pitch_disturbance = self.world_fire_quadrants[1]*clamp(
            abs(y_img-resolutionY/2), 0, abs(self.MAX_PITCH_DISTURBANCE))

        if self.world_fire_quadrants == [0, 0]:
            self.water_to_drop = 25
            if verbose:
                print("Water dropped on fire target: {} at position {}".format(
                    self.target_position[0:2], self.current_pose[0:2]))
            self.img_coord_fire = []
            self.fire_bbox = None

        return yaw_disturbance, pitch_disturbance

    def draw_detection_overlay(self, fire_detected=False):
        if not self.display:
            return

        width = self.display.getWidth()
        height = self.display.getHeight()

        self.display.setOpacity(0.9)
        self.display.setColor(0xFFFFFF)
        self.display.drawText(self.name, 6, 6)

        if self.camera.hasRecognition():
            for obj in self.camera.getRecognitionObjects():
                model = obj.getModel() or ""
                model_lower = model.lower()
                if "sassafras" in model_lower:
                    color = 0x00FF66
                    label = "tree"
                elif "fire" in model_lower:
                    color = 0xFF3300
                    label = "fire"
                elif "smoke" in model_lower:
                    color = 0xBBBBBB
                    label = "smoke"
                else:
                    continue
                self.display.setColor(color)
                center_x, center_y = obj.getPositionOnImage()
                size_x, size_y = obj.getSizeOnImage()
                x = int(max(0, center_x - size_x / 2))
                y = int(max(0, center_y - size_y / 2))
                w = int(min(width - x - 1, size_x))
                h = int(min(height - y - 1, size_y))
                if w > 2 and h > 2:
                    self.display.drawRectangle(x, y, w, h)
                    self.display.drawText(label, x, max(0, y - 12))

        if self.fire_bbox:
            x, y, w, h = self.fire_bbox
            self.display.setColor(0xFF3300)
            self.display.drawRectangle(x, y, w, h)
            self.display.drawRectangle(max(0, x - 1), max(0, y - 1), w + 2, h + 2)
            self.display.drawText("fire/smoke", x, max(0, y - 12))

        if fire_detected:
            self.display.setOpacity(0.25)
            self.display.setColor(0xFF0000)
            self.display.fillRectangle(0, 0, width, height)
            self.display.setOpacity(1.0)

    def fire_detection(self, verbose=True):
        """
        Detect the smoke and return the fire coordinate in the image
        Parameters:
            verbose (bool): whether to print status messages or not
        Returns:
            coord_fire (list):x,y image coordinates of the fire
        """
        img = self.get_image_from_camera()
        if img is None:
            return []

        if self.camera.hasRecognition():
            recognized_fire = []
            for obj in self.camera.getRecognitionObjects():
                model = (obj.getModel() or "").lower()
                if "fire" not in model and "smoke" not in model:
                    continue
                center_x, center_y = obj.getPositionOnImage()
                size_x, size_y = obj.getSizeOnImage()
                x = int(max(0, center_x - size_x / 2))
                y = int(max(0, center_y - size_y / 2))
                w = int(max(1, size_x))
                h = int(max(1, size_y))
                if w > 2 and h > 2:
                    recognized_fire.append((w * h, [center_x, center_y], (x, y, w, h)))
            if recognized_fire:
                recognized_fire.sort(key=lambda item: item[0], reverse=True)
                _, coord_fire, self.fire_bbox = recognized_fire[0]
                if verbose:
                    print("fire detected by recognition, coordinates {}".format(coord_fire))
                self.draw_detection_overlay(True)
                return coord_fire

        # Segment the image by color in HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        # Range of the smoke
        smoke_lower = np.array([0, 0, 168])
        smoke_upper = np.array([172, 111, 255])

        mask_fire = cv2.inRange(hsv, smoke_lower, smoke_upper)

        fire_ratio = np.round(
            (cv2.countNonZero(mask_fire))/(img.size/3)*100, 2)
        if fire_ratio > 0.15:  # Higher the fire ratio, higher the number of fire in the image
            coord_fire = []
            self.fire_bbox = None

            # Detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
            contours, _ = cv2.findContours(
                image=mask_fire, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

            # Approximate contours to polygons + get circles
            contours_poly = [None]*len(contours)
            centers = [None]*len(contours)
            radius = [None]*len(contours)
            radius_max = 0
            for i, c in enumerate(contours):
                contours_poly[i] = cv2.approxPolyDP(c, 3, True)
                centers[i], radius[i] = cv2.minEnclosingCircle(
                    contours_poly[i])
                # We keep only the biggest circle and > 3
                if radius[i] > 3 and radius[i] > radius_max:
                    coord_fire = centers[i]
                    radius_max = radius[i]
                    x, y, w, h = cv2.boundingRect(contours_poly[i])
                    self.fire_bbox = (int(x), int(y), int(w), int(h))
                    if verbose:
                        print(
                            "fire detected, coordinates {}".format(centers[i]))

            if coord_fire and self.debug_images:
                drawing = img.copy()
                x, y, w, h = self.fire_bbox
                cv2.rectangle(drawing, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.circle(drawing, (int(coord_fire[0]), int(coord_fire[1])), int(radius_max), (255, 0, 0), 2)
                cv2.imwrite("fire_detection.jpg", drawing)
            self.draw_detection_overlay(bool(coord_fire))
            return coord_fire
        self.fire_bbox = None
        self.draw_detection_overlay(False)
        return []

    def run(self):
        t1 = self.getTime()
        t2 = self.getTime()
        t3 = self.getTime()

        roll_disturbance = 0
        pitch_disturbance = 0
        yaw_disturbance = 0

        # We add controller args to waypoints and target_altitude variables
        opt_parser = optparse.OptionParser()
        opt_parser.add_option("--patrol_coords", default="11 11, 11 21, 21 21,21 11",
                              help="Specify the patrol coordinates in the format [x1 y1, x2 y2, ...]")
        opt_parser.add_option("--target_altitude", default=42,
                              type=float, help="target altitude of the robot in meters")
        opt_parser.add_option("--detection_interval", default=0.5,
                              type=float, help="seconds between OpenCV fire detection passes")
        opt_parser.add_option("--debug_images", action="store_true", default=False,
                              help="save annotated fire_detection.jpg when fire is detected")
        options, _ = opt_parser.parse_args()
        self.debug_images = options.debug_images

        point_list = options.patrol_coords.split(',')
        number_of_waypoints = len(point_list)
        waypoints = []
        for i in range(0, number_of_waypoints):
            waypoints.append([])
            waypoints[i].append(float(point_list[i].split()[0]))
            waypoints[i].append(float(point_list[i].split()[1]))

        target_altitude = options.target_altitude

        while self.step(self.time_step) != -1:

            # Read sensors
            roll, pitch, yaw = self.imu.getRollPitchYaw()
            Xpos, Ypos, altitude = self.gps.getValues()
            roll_acceleration, pitch_acceleration, _ = self.gyro.getValues()
            self.set_position([Xpos, Ypos, altitude, roll, pitch, yaw])

            # Drop the water from the drone
            if self.water_to_drop > 0:
                self.WaterDropStatus = True
                self.setCustomData(str(self.water_to_drop))
                self.water_to_drop = 0
            else:
                self.setCustomData(str(0))

            if altitude > target_altitude - 1:
                # Motion
                if self.getTime() - t1 > 0.1:
                    if self.img_coord_fire:
                        yaw_disturbance, pitch_disturbance = self.naive_approach()
                    else:
                        yaw_disturbance, pitch_disturbance = self.move_to_target(
                            waypoints)
                    t1 = self.getTime()
                # Fire detection
                if self.getTime() - t2 > options.detection_interval:
                    if not self.WaterDropStatus:
                        self.img_coord_fire = self.fire_detection()
                    t2 = self.getTime()

                if not self.WaterDropStatus:
                    t3 = self.getTime()
                if self.getTime() - t3 > 15:  # Wait 15 times to avoid detection of the dropping water as smoke
                    self.WaterDropStatus = False

            roll_input = self.K_ROLL_P * \
                clamp(roll, -1, 1) + roll_acceleration + roll_disturbance
            pitch_input = self.K_PITCH_P * \
                clamp(pitch, -1, 1) + pitch_acceleration + pitch_disturbance
            yaw_input = yaw_disturbance
            clamped_difference_altitude = clamp(
                target_altitude - altitude + self.K_VERTICAL_OFFSET, -1, 1)
            vertical_input = self.K_VERTICAL_P * \
                pow(clamped_difference_altitude, 3.0)

            front_left_motor_input = self.K_VERTICAL_THRUST + \
                vertical_input - yaw_input + pitch_input - roll_input
            front_right_motor_input = self.K_VERTICAL_THRUST + \
                vertical_input + yaw_input + pitch_input + roll_input
            rear_left_motor_input = self.K_VERTICAL_THRUST + \
                vertical_input + yaw_input - pitch_input - roll_input
            rear_right_motor_input = self.K_VERTICAL_THRUST + \
                vertical_input - yaw_input - pitch_input + roll_input

            self.front_left_motor.setVelocity(front_left_motor_input)
            self.front_right_motor.setVelocity(-front_right_motor_input)
            self.rear_left_motor.setVelocity(-rear_left_motor_input)
            self.rear_right_motor.setVelocity(rear_right_motor_input)


robot = Mavic()
robot.run()
