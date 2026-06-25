# Key Algorithms Used

## 1. Drone Locomotion and Stabilisation
The Mavic drone uses four propeller motors controlled through roll, pitch, yaw, and vertical thrust commands. GPS provides position and altitude, while the inertial unit and gyro provide orientation and angular velocity. A proportional control strategy keeps the drone near the target altitude and stabilises its movement during patrol and fire approach.

## 2. Waypoint Patrol Navigation
Each drone receives patrol coordinates from the world file through controller arguments. The controller stores these points as a waypoint list and navigates toward the current target using GPS localisation. When the drone reaches a waypoint within the target precision threshold, it switches to the next waypoint. This satisfies the patrol and navigation requirement.

## 3. Camera-Based Fire/Smoke Detection
The drone camera captures a downward-facing image. The image is converted from Webots camera format into an OpenCV-compatible RGB image and then converted into HSV colour space. A threshold is applied to isolate bright low-saturation smoke/fire regions. Contours are extracted from the binary mask, and the largest valid contour is selected as the current fire target in image coordinates.

## 4. Visual Fire Approach
After detection, the drone uses the detected fire image coordinates to adjust yaw and pitch. If the fire appears away from the image centre, the drone moves toward it. When the fire becomes centred in the camera image, the drone assumes it is above the target and prepares a water drop.

## 5. Water Drop Behaviour
Water dropping is triggered through the drone custom data field. Once centred above the detected fire target, the controller sets a water-drop command. After dropping water, the controller clears the current image target and continues the mission loop.

## 6. Integrated Autonomous Behaviour
The final behaviour loop is:

patrol -> detect smoke/fire -> visually approach fire -> drop water -> continue patrol -> respond to new propagated fires.
