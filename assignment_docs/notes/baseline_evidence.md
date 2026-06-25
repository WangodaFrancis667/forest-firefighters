# Baseline Evidence - Forest Firefighting Mission

## Environment
- Simulator: Webots R2021b
- Execution: Docker container with NVIDIA GPU OpenGL rendering
- Robot: Mavic 2 Pro drone
- Project: Cyberbotics Forest Firefighters

## Baseline Observations
The baseline run successfully demonstrated:
- Fire controller started.
- Spot controller started.
- Two autonomous Mavic controllers started.
- Wildfire started in the simulated forest.
- Camera-based fire/smoke detection occurred multiple times.
- Water was dropped on a detected fire target.
- The drone continued waypoint navigation after detection and water drop.

## Evidence from baseline log
Important events observed:
- "Starting wildfire in a forest of 27 sassafras trees."
- "fire detected, coordinates ..."
- "Water dropped on fire target ..."
- "Target reached! New target ..."

## Baseline Conclusion
The original controller already provides a working autonomous loop. The next engineering step is to improve evidence, logging, robustness, code clarity, and reporting so the project clearly satisfies the full grading rubric.
