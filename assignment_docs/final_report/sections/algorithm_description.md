# Key Algorithms Used

## 1. Drone Locomotion and Stabilisation

Each Mavic 2 Pro drone is controlled with four propeller motors. The controller computes motor
velocity commands from altitude error, roll, pitch, yaw, inertial measurements, and gyro feedback.
GPS provides the current world position and altitude. This keeps the drones stable while they take
off, patrol, approach fire targets, and resume waypoint navigation.

## 2. Interior Quadrant Patrol Navigation

The active world uses four drones, one per quadrant. Each drone receives its patrol route through
the `--patrol_coords` controller argument. The routes are intentionally biased toward the interior
forest instead of only tracing the outer corners, so central fires enter a camera view sooner.

At runtime, the controller stores the patrol coordinates as a waypoint list. When the drone is
within the configured target precision threshold, it advances to the next waypoint and continues
the patrol cycle.

## 3. Camera-Based Fire and Smoke Detection

The drone camera is pitched downward. Each frame is converted from Webots camera data into an
OpenCV-compatible image, then transformed into HSV colour space. The detector thresholds bright,
low-saturation smoke/fire regions and extracts contours from the binary mask. The largest valid
contour becomes the active fire target in image coordinates.

The overlay is deliberately minimal for performance and readability. Each drone camera shows a
green status bar during normal patrol and a red `FIRE` bar when the controller has an active fire
target. Tree boxes and dense contour overlays were removed because they cluttered the view and
increased rendering cost.

## 4. Visual Fire Approach

When fire is detected, the drone temporarily leaves normal waypoint patrol. It compares the fire
image coordinate with the centre of the 160 by 160 camera frame. If the target is left, right, high,
or low in the image, the controller applies yaw and pitch disturbances to move toward it. When the
target is centred, the drone treats itself as positioned above the fire area.

## 5. Water Drop Behaviour

Water dropping is triggered through the drone `customData` field. The fire supervisor reads this
field, spawns a water object at the robot position, and checks whether the water is close enough to
extinguish an active tree fire. After a drop, the drone clears the current fire target and waits
briefly before accepting another detection, reducing confusion between water/smoke visuals and
active fire.

## 6. Fire Supervisor Timing and Propagation

The fire supervisor starts the wildfire after 40 seconds. This gives the drones time to lift off
while still forcing early detection and response. It then controls wind evolution, fire spread,
smoke creation, and water-based extinction checks. Timed mission tests use a 300-second mission
duration so the run exits cleanly instead of relying on an external timeout kill.

## 7. Integrated Autonomous Behaviour

The final behaviour loop is:

`preflight -> take off -> patrol -> detect smoke/fire -> approach -> drop water -> resume patrol`.

Spot remains active as a stable support robot with a keyboard-triggered water burst, while the four
Mavic drones provide the main autonomous search and response capability.
