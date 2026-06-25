# Forest Firefighting Robotics Mission Report Outline

## Title
Autonomous Forest Firefighting Mission using Webots Mavic Drones

## 1. Introduction
- State the mission objective.
- Mention Webots Forest Firefighters project.
- Mention use of Mavic drones for aerial patrol and firefighting.

## 2. System Architecture
- Webots world.
- Fire controller.
- Eight Mavic drone controllers deployed at four forest corners (two drones per corner).
- Each drone: Camera, GPS, IMU, gyro.
- OpenCV perception.
- Water-drop mechanism.
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

## 6. Conclusion
- Summarise autonomous behaviour achieved.
- Mention patrol, detection, navigation, water drop, and repeated fire handling.
