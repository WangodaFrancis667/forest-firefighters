# Final Presentation Script - Forest Firefighting Robotics Mission

## Opening: 20-30 seconds

Good day. My project is an autonomous forest firefighting robotics mission implemented in the Webots Forest Firefighters simulation environment. The aim was to program one or more robots to patrol a forest, detect fire or smoke using a camera, navigate toward the fire, and extinguish it by dropping water.

For my implementation, I used four Mavic 2 Pro drones deployed across the four forest quadrants, supported by a Spot-like ground robot. The original project baseline is retained in the `original/` folder for reference. The active project extends that reliable baseline by adding the two missing drones for full quadrant coverage while keeping the camera and controller load suitable for the 6 GB RTX A1000 laptop.

---

## Environment and Setup: 30-45 seconds

The simulation was run in a Docker-based Webots R2021b environment on Pop!_OS. I used Webots R2021b because the Forest Firefighters project runs correctly in that version. Later Webots versions caused compatibility problems with old PROTO files, terrain, and robot behaviour.

The Docker container was configured to use NVIDIA GPU rendering. I verified GPU rendering inside the container using `nvidia-smi` and `glxinfo`, where the OpenGL renderer showed the NVIDIA RTX A1000 GPU.

Before every mission run, I used a preflight checker to confirm that all 4 drones start from separate quadrant base positions:
- **SW Quadrant**: Drone 1 starts at (4.0, 4.0, 17.4)
- **NW Quadrant**: Drone 2 starts at (2.0, 26.0, 18.82)
- **SE Quadrant**: Drone 3 starts at (26.0, 3.0, 15.25)
- **NE Quadrant**: Drone 4 starts at (28.0, 26.0, 19.34)

This prevents testing with drones floating incorrectly in space and ensures each drone is positioned to patrol its assigned forest quadrant.

---

## System Architecture: 45-60 seconds

The system is organised as a closed-loop robotics pipeline.

The Webots world provides the forest terrain, wildfire propagation, smoke, drones, Spot, sensors, and water-drop mechanism. The fire controller starts the wildfire after 40 seconds, then propagates it while the drones are already patrolling interior-biased quadrant routes. Each Mavic drone uses:
- Camera for fire and smoke perception.
- GPS for localisation and waypoint navigation.
- IMU and gyro for stabilised locomotion.
- Propeller motors for aerial control.
- Custom data to trigger water dropping.
- A 160 by 160 vision overlay with a green normal bar and a red fire bar.

The control loop is:

`patrol -> detect smoke/fire -> approach fire -> drop water -> continue patrol -> handle propagated fires`.

---

## Locomotion: 30-45 seconds

For locomotion, the drone uses four propeller motors. The controller calculates motor velocities using vertical thrust, roll, pitch, yaw, and altitude error.

GPS gives the current position and altitude, while the inertial unit and gyro provide orientation and angular velocity. This allows the drone to take off, stabilise at its target altitude, patrol between waypoints, and hover above detected fire targets before dropping water.

The Spot robot remains active in a stable support posture and supports the mission with a keyboard-triggered water burst. This keeps the ground robot available during the demo without destabilising the Webots run, while the drones remain responsible for aerial locomotion and search.

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

After dropping water, the controller clears the current target and continues patrolling. This means the robot can continue responding to multiple fire detections caused by wildfire propagation. Spot provides a secondary water-delivery path during the demo when I press `D`.

The integration behaviour is fully autonomous: the system moves from patrol to detection, then approach, then water drop, then back to patrol.

---

## Results: 45-60 seconds

I carried out repeated mission tests and analysed the logs automatically. The final validation set contains eight runs using the active four-drone plus Spot configuration.

Across those final runs, the system achieved:
- 718 total fire detections.
- 43 total water drops.
- 223 waypoint target transitions.
- 0 mission errors.
- 0 mission crashes.

The cleanest submission-style run was `final_demo_test`, which achieved:
- 120 fire detections.
- 6 water drops.
- 31 target transitions.
- 0 mission errors.
- 0 mission crashes.
- 0 shutdown artifacts.

Some runs recorded shutdown artifacts from Webots while the simulator was closing, but these were separated from mission crashes. The important result is that the robots completed detection, navigation, and water dropping without controller tracebacks or mid-mission failures.

---

## Challenges and Solutions: 45-60 seconds

The first major challenge was Webots version compatibility. Webots R2025a caused missing PROTOs, terrain problems, and unstable robot behaviour. I solved this by using Webots R2021b, where the project works correctly.

The second challenge was Docker graphics performance. At first, software rendering was too slow. I solved this by enabling NVIDIA GPU rendering inside Docker.

The third challenge was drone launch verification. Because the terrain is elevated, the drones appeared high in world coordinates. I solved this using a static launch-position check and a preflight script.

The fourth challenge was a perception bug. The controller could crash when smoke was detected but no valid contour was selected. I fixed it by safely initialising `coord_fire` so the function returns an empty list instead of crashing.

The fifth challenge was choosing the fleet size. The original project baseline had two drones, which was reliable but did not provide full quadrant coverage. The active world adds two drones for a four-drone layout, while avoiding the heavier six- or eight-drone experiments that overload this laptop.

---

## Live Demo Commands

First, start the Webots Docker container from the host:

```bash
cd ~/Desktop/ros/webots-r2021b-gpu
./run-gpu.sh
```

Inside the container:

```bash
cd /workspace/webots-projects/projects/forest_firefighters
python3 tools/preflight_check.py
./tools/run_mission_test.sh live_demo_four_drone
```

For an interactive demo:

```bash
webots worlds/forest_firefighters.wbt
```

During the demo, I show the four drone camera overlays, point out the green normal bars and red fire bars, and select Spot to demonstrate the `D` water-burst command.
