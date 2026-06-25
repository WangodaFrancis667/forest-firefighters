from pathlib import Path
import re

controller_path = Path("controllers/autonomous_mavic/autonomous_mavic.py")
backup_path = Path("assignment_docs/backups/autonomous_mavic_before_phase4_instrumentation.py")

text = controller_path.read_text()
backup_path.write_text(text)

# Add imports.
if "from pathlib import Path" not in text:
    text = text.replace(
        "import optparse\n",
        "import optparse\nimport csv\nimport os\nfrom pathlib import Path\n",
        1
    )

# Add evidence fields.
init_marker = "        self.WaterDropStatus = False\n"
init_addition = """        self.mission_state = "TAKEOFF"
        self.detection_count = 0
        self.water_drop_count = 0
        self.last_telemetry_time = -1
        self.fire_ratio_threshold = 0.15

        self.project_root = Path(__file__).resolve().parents[2]
        self.evidence_dir = self.project_root / "assignment_docs"
        self.screenshot_dir = self.evidence_dir / "screenshots"
        self.results_dir = self.evidence_dir / "results"
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)

        telemetry_name = "telemetry_mavic_{}.csv".format(os.getpid())
        self.telemetry_path = self.results_dir / telemetry_name
        self.telemetry_file = self.telemetry_path.open("w", newline="")
        self.telemetry_writer = csv.writer(self.telemetry_file)
        self.telemetry_writer.writerow([
            "time_s",
            "state",
            "x",
            "y",
            "altitude",
            "target_x",
            "target_y",
            "fire_img_x",
            "fire_img_y",
            "water_drop_count"
        ])
        self.telemetry_file.flush()
"""
if init_addition.strip() not in text:
    text = text.replace(init_marker, init_marker + init_addition, 1)

# Add helper methods before camera method.
helper_marker = "    def get_image_from_camera(self):\n"
helper_methods = '''    def log_event(self, state, message):
        """
        Print a structured mission event for report evidence and debugging.
        """
        try:
            timestamp = self.getTime()
        except Exception:
            timestamp = 0.0
        print("[{}] t={:.2f}s {}".format(state, timestamp, message))

    def write_telemetry(self):
        """
        Save low-rate mission telemetry for the report:
        robot position, altitude, target, detection coordinates, and water drops.
        """
        current_time = self.getTime()
        if self.last_telemetry_time >= 0 and current_time - self.last_telemetry_time < 1.0:
            return

        self.last_telemetry_time = current_time

        fire_x = ""
        fire_y = ""
        if self.img_coord_fire:
            fire_x = self.img_coord_fire[0]
            fire_y = self.img_coord_fire[1]

        self.telemetry_writer.writerow([
            "{:.2f}".format(current_time),
            self.mission_state,
            "{:.3f}".format(self.current_pose[0]),
            "{:.3f}".format(self.current_pose[1]),
            "{:.3f}".format(self.current_pose[2]),
            "{:.3f}".format(self.target_position[0]),
            "{:.3f}".format(self.target_position[1]),
            fire_x,
            fire_y,
            self.water_drop_count
        ])
        self.telemetry_file.flush()

'''
if "def write_telemetry" not in text:
    text = text.replace(helper_marker, helper_methods + helper_marker, 1)

# Improve patrol start log.
text = text.replace(
'''            if verbose_target:
                print("First target: ", self.target_position[0:2])
''',
'''            if verbose_target:
                self.mission_state = "PATROL"
                self.log_event("PATROL", "First target: {}".format(self.target_position[0:2]))
'''
)

# Improve target reached log.
text = text.replace(
'''            if verbose_target:
                print("Target reached! New target: ",
                      self.target_position[0:2])
''',
'''            if verbose_target:
                self.mission_state = "PATROL"
                self.log_event("PATROL", "Target reached. New target: {}".format(self.target_position[0:2]))
'''
)

# Improve water drop log.
text = text.replace(
'''        if self.world_fire_quadrants == [0, 0]:
            self.water_to_drop = 15
            if verbose:
                print("Water dropped on fire target: {} at position {}".format(
                    self.target_position[0:2], self.current_pose[0:2]))
            self.img_coord_fire = []
''',
'''        if self.world_fire_quadrants == [0, 0]:
            self.water_to_drop = 15
            self.water_drop_count += 1
            self.mission_state = "DROP"
            if verbose:
                self.log_event(
                    "DROP",
                    "Water dropped on fire target {} at robot position {}. Total drops: {}".format(
                        self.target_position[0:2],
                        self.current_pose[0:2],
                        self.water_drop_count
                    )
                )
            self.img_coord_fire = []
'''
)

# Replace fire_detection with a more robust evidence-friendly version.
new_fire_detection = '''    def fire_detection(self, verbose=True):
        """
        Detect smoke/fire using the onboard camera.

        Method:
        1. Capture camera image.
        2. Convert RGB image to HSV color space.
        3. Threshold bright low-saturation smoke/fire regions.
        4. Extract contours from the binary mask.
        5. Select the largest valid contour as the active fire target.

        Returns:
            tuple/list: x,y image coordinates of detected fire, or [] when no fire is detected.
        """
        img = self.get_image_from_camera()
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        # HSV threshold for smoke/bright fire plume.
        smoke_lower = np.array([0, 0, 168])
        smoke_upper = np.array([172, 111, 255])

        mask_fire = cv2.inRange(hsv, smoke_lower, smoke_upper)

        fire_ratio = np.round(
            (cv2.countNonZero(mask_fire)) / (img.size / 3) * 100,
            2
        )

        if fire_ratio <= self.fire_ratio_threshold:
            return []

        contours, _ = cv2.findContours(
            image=mask_fire,
            mode=cv2.RETR_TREE,
            method=cv2.CHAIN_APPROX_NONE
        )

        best_center = None
        best_radius = 0
        contours_poly = []

        for contour in contours:
            polygon = cv2.approxPolyDP(contour, 3, True)
            center, radius = cv2.minEnclosingCircle(polygon)
            contours_poly.append(polygon)

            if radius > 3 and radius > best_radius:
                best_center = center
                best_radius = radius

        if best_center is None:
            return []

        self.detection_count += 1
        self.mission_state = "DETECT"

        if verbose:
            self.log_event(
                "DETECT",
                "Fire/smoke detected at image=({:.2f}, {:.2f}), radius={:.2f}, mask_ratio={:.2f}%, detections={}".format(
                    best_center[0],
                    best_center[1],
                    best_radius,
                    fire_ratio,
                    self.detection_count
                )
            )

        # Save first few detections and periodic detections for report evidence.
        if self.detection_count <= 5 or self.detection_count % 5 == 0:
            drawing = img.copy()
            for i, polygon in enumerate(contours_poly):
                color = (0, 255, 0)
                cv2.drawContours(drawing, contours_poly, i, color)
            cv2.circle(
                drawing,
                (int(best_center[0]), int(best_center[1])),
                int(best_radius),
                (255, 0, 0),
                2
            )

            screenshot_path = self.screenshot_dir / "fire_detection_{:03d}.jpg".format(self.detection_count)
            cv2.imwrite(str(screenshot_path), drawing)

        return best_center

'''

pattern = r"    def fire_detection\(self, verbose=True\):\n.*?\n    def run\(self\):"
replacement = new_fire_detection + "    def run(self):"
text, count = re.subn(pattern, replacement, text, count=1, flags=re.DOTALL)

if count != 1:
    raise RuntimeError("Could not replace fire_detection method safely.")

# Add telemetry after pose update.
pose_line = "            self.set_position([Xpos, Ypos, altitude, roll, pitch, yaw])\n"
telemetry_line = "            self.set_position([Xpos, Ypos, altitude, roll, pitch, yaw])\n            self.write_telemetry()\n"
if "self.write_telemetry()" not in text:
    text = text.replace(pose_line, telemetry_line, 1)

controller_path.write_text(text)

print("Enhanced controller instrumentation applied.")
print("Backup saved to:", backup_path)
print("Controller updated:", controller_path)
