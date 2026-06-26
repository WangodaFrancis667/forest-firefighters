# Rubric Mapping - Forest Firefighting Robotics Mission

## 1. Locomotion - 25%

Evidence:

- Four Mavic 2 Pro drones launch from separate quadrant base positions.
- Each drone uses propeller motors for aerial locomotion.
- The drones maintain altitude using GPS, IMU, and gyro feedback.
- Each drone follows GPS waypoints and transitions through patrol targets.
- When fire is detected, the drone shifts from patrol to visual approach before dropping water.
- Spot remains active in a stable support posture for the ground-robot component.

Files:

- `controllers/autonomous_mavic/autonomous_mavic.py`
- `controllers/spot/spot.py`
- `worlds/forest_firefighters.wbt`

## 2. Perception and Sensing - 30%

Evidence:

- Each Mavic drone uses its onboard camera.
- Camera frames are converted into OpenCV-compatible images.
- HSV thresholding detects smoke/fire regions.
- Contour extraction selects a valid image target.
- Green/red camera status bars show normal and fire-detected states without cluttering the feed.
- Refreshed final runs recorded 718 total fire detections.

Files:

- `controllers/autonomous_mavic/autonomous_mavic.py`
- `assignment_docs/results/performance_results_summary.md`

## 3. Navigation - 25%

Evidence:

- Patrol waypoints are supplied through world-file controller arguments.
- The four patrol routes are interior-biased to cover the middle of the forest, not only the edges.
- GPS position is compared against the current waypoint.
- The controller advances to the next waypoint when the target precision threshold is met.
- Fire image coordinates guide yaw/pitch adjustments during visual approach.
- Refreshed final runs recorded 223 total target transitions.

Files:

- `worlds/forest_firefighters.wbt`
- `controllers/autonomous_mavic/autonomous_mavic.py`

## 4. Integration and Behaviour - 10%

Evidence:

- The autonomous loop is complete: patrol, detect, approach, drop water, resume patrol.
- Drone water drops are sent through `customData` and handled by the fire supervisor.
- The fire supervisor handles delayed ignition, fire spread, smoke creation, and water extinction.
- Spot provides a secondary keyboard-triggered water burst.
- Refreshed final runs recorded 43 total water drops.

Files:

- `controllers/fire/fire.py`
- `controllers/autonomous_mavic/autonomous_mavic.py`
- `controllers/spot/spot.py`

## 5. Code Quality and Documentation - 10%

Evidence:

- Active tools are kept in the root `tools/` folder.
- `preflight_check.py` validates the final four-drone world before live runs.
- `run_mission_test.sh` captures logs and analyzes mission performance.
- `analyze_mission_log.py` separates mission failures from shutdown artifacts.
- The root README explains architecture, algorithms, commands, and expected questions.
- The LaTeX report, presentation script, results summary, and notes match the final four-drone system.

Files:

- `README.md`
- `tools/preflight_check.py`
- `tools/run_mission_test.sh`
- `tools/analyze_mission_log.py`
- `assignment_docs/final_report/latex/firefighting_robotics_report.tex`
- `assignment_docs/presentation/final_presentation_script.md`
