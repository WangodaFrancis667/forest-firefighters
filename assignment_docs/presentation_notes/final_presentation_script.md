# Final Presentation Script - Forest Firefighting Robotics Mission

## Opening: 20-30 seconds

Good day. My project is an autonomous forest firefighting robotics mission implemented in the Webots Forest Firefighters simulation environment. The aim was to program one or more robots to patrol a forest, detect fire or smoke using a camera, navigate toward the fire, and extinguish it by dropping water.

For my implementation, I used eight Mavic 2 Pro drones deployed at four forest corners (two drones per corner). This multi-drone architecture provides maximum forest coverage, faster response to multiple fires, and redundancy. Aerial robots give wider forest coverage, faster movement, and direct top-down camera visibility of smoke and fire regions.

---

## Environment and Setup: 30-45 seconds

The simulation was run in a Docker-based Webots R2021b environment on Pop!_OS. I used Webots R2021b because the Forest Firefighters project runs correctly in that version. Later Webots versions caused compatibility problems with old PROTO files, terrain, and robot behaviour.

The Docker container was configured to use NVIDIA GPU rendering. I verified GPU rendering inside the container using `nvidia-smi` and `glxinfo`, where the OpenGL renderer showed the NVIDIA RTX A1000 GPU.

Before every mission run, I used a preflight checker to confirm that all 8 drones start from the correct base positions at the four forest corners:
- **SW Corner**: Drones 1 & 2 start at (4.0, 4.0, 17.4) and (4.0, 3.0, 17.43)
- **NW Corner**: Drones 3 & 4 start at (2.0, 24.0, 17.92) and (2.0, 26.0, 18.82)
- **SE Corner**: Drones 5 & 6 start at (26.0, 3.0, 15.25) and (28.0, 3.0, 16.33)
- **NE Corner**: Drones 7 & 8 start at (28.0, 26.0, 19.34) and (28.0, 28.0, 17.98)

This prevents testing with drones floating incorrectly in space and ensures each drone is positioned to patrol its assigned forest quadrant.

---

## System Architecture: 45-60 seconds

The system is organised as a closed-loop robotics pipeline.

The Webots world provides the forest terrain, wildfire propagation, smoke, drones, sensors, and water-drop mechanism. The fire controller starts and propagates the wildfire. Each Mavic drone uses:
- Camera for fire and smoke perception.
- GPS for localisation and waypoint navigation.
- IMU and gyro for stabilised locomotion.
- Propeller motors for aerial control.
- Custom data to trigger water dropping.

The control loop is:

`patrol -> detect smoke/fire -> approach fire -> drop water -> continue patrol -> handle propagated fires`.

---

## Locomotion: 30-45 seconds

For locomotion, the drone uses four propeller motors. The controller calculates motor velocities using vertical thrust, roll, pitch, yaw, and altitude error.

GPS gives the current position and altitude, while the inertial unit and gyro provide orientation and angular velocity. This allows the drone to take off, stabilise at its target altitude, patrol between waypoints, and hover above detected fire targets before dropping water.

This addresses the locomotion requirement: stable drone movement, altitude control, and precise positioning for water drop.

---

## Perception and Sensing: 45-60 seconds

For perception, the onboard camera captures a downward-facing image. The image is converted into an OpenCV-compatible format, then converted into HSV colour space.

The controller applies colour thresholding to detect bright low-saturation smoke or fire regions. It then extracts contours from the binary mask and selects the largest valid contour as the active fire target.

The detected fire target is represented as image coordinates, for example `(x, y)`, and these coordinates are used to guide the drone toward the fire.

This satisfies the perception requirement because the robot uses camera image processing and OpenCV-style colour segmentation to detect fire or smoke.

---

## Navigation: 45-60 seconds

For navigation, each drone receives patrol coordinates from the Webots world file using controller arguments. The controller stores these as waypoints.

During flight, the drone compares its GPS position with the current waypoint. Once it reaches the waypoint within the configured precision threshold, it switches to the next target.

When smoke or fire is detected, the drone temporarily moves from waypoint patrol into visual fire approach. It uses the fire image coordinate to adjust yaw and pitch until the fire is centred below the camera.

This demonstrates localisation, path-following, and dynamic behaviour when new fires appear.

---

## Extinguishing and Integration: 30-45 seconds

When the detected fire becomes centred in the camera frame, the drone assumes it is positioned above the target. It then triggers water dropping using the drone's custom data field.

After dropping water, the controller clears the current target and continues patrolling. This means the robot can continue responding to multiple fire detections caused by wildfire propagation.

The integration behaviour is fully autonomous: the system moves from patrol to detection, then approach, then water drop, then back to patrol.

---

## Results: 45-60 seconds

I carried out repeated mission tests and analysed the logs automatically.

The primary clean run was `stability_repeat_01`, which achieved:
- 107 fire detections.
- 5 water drops.
- 4 target transitions.
- 0 mission errors.
- 0 mission crashes.

After fixing a safe bug in the fire detection routine, the final demo test achieved:
- 46 fire detections.
- 4 water drops.
- 5 target transitions.
- 0 mission errors.
- 0 mission crashes.

This confirms that the final controller can perform the autonomous mission reliably.

---

## Challenges and Solutions: 45-60 seconds

The first major challenge was Webots version compatibility. Webots R2025a caused missing PROTOs, terrain problems, and unstable robot behaviour. I solved this by using Webots R2021b, where the project works correctly.

The second challenge was Docker graphics performance. At first, software rendering was too slow. I solved this by enabling NVIDIA GPU rendering inside Docker.

The third challenge was drone launch verification. Because the terrain is elevated, the drones appeared high in world coordinates. I solved this using a static launch-position check and a preflight script.

The fourth challenge was a perception bug. The controller could crash when smoke was detected but no valid contour was selected. I fixed it by safely initialising `coord_fire` so the function returns an empty list instead of crashing.

---

## Live Demo Commands

First, start the Webots Docker container from the host:

```bash
cd ~/Desktop/ros/webots-r2021b-gpu
./run-gpu.sh              Inside the container:

