# Forest Firefighting Robotics Mission Report Outline

## Title
Autonomous Forest Firefighting Mission using Webots Robots

## 1. Introduction
- State the mission objective.
- Mention Webots Forest Firefighters project.
- Mention the original drone plus Spot baseline.
- Explain the fleet evolution: eight experimental drones, six intermediate drones, final four drones plus Spot for RTX A1000 stability.

## 2. System Architecture
- Webots world.
- Fire controller.
- Four Mavic drone controllers deployed across SW, NW, SE, and NE quadrants.
- Spot-like ground robot as a stable support robot with keyboard-triggered water burst.
- Each drone: camera, recognition overlay, GPS, IMU, gyro.
- OpenCV perception and red fire/smoke overlays.
- Water-drop mechanism through drone custom data and Spot support burst.
- Quadrant-based patrol coverage.

## 3. Methodology
- Stable Docker + Webots R2021b setup.
- NVIDIA GPU rendering.
- Preflight launch safety check.
- Waypoint patrol.
- HSV fire/smoke detection.
- Contour-based fire localisation.
- Visual approach and water drop.

## 4. Results
- Use `stability_repeat_01` as primary run.
- Include performance table.
- Mention repeated test evidence.

## 5. Challenges and Solutions
- R2025a incompatibility.
- Docker GPU rendering.
- Root sandbox issue.
- Drone launch-position verification.
- Controller instrumentation instability.
- Shutdown artifact interpretation.
- Fleet-size tuning for laptop GPU stability.

## 6. Conclusion
- Summarise autonomous behaviour achieved.
- Mention patrol, detection, navigation, water drop, Spot support, and repeated fire handling.
