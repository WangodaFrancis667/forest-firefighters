# Rubric Mapping - Forest Firefighting Robotics Mission

## 1. Locomotion - 25%
Evidence:
- Mavic 2 Pro drone takes off to target altitude.
- Drone uses propeller motors for aerial locomotion.
- Drone patrols multiple GPS waypoints.
- Drone stabilizes using IMU, GPS, and gyro feedback.
- Drone positions itself above the detected fire before water drop.

Planned improvements:
- Add clearer mission-state logs.
- Record altitude, GPS position, and target state.

## 2. Perception and Sensing - 30%
Evidence:
- Camera is enabled and used.
- Images are converted for OpenCV processing.
- HSV colour segmentation is used to detect smoke/fire.
- Contours are extracted from the binary mask.
- Fire image coordinates are printed when detected.

Planned improvements:
- Save detection screenshots.
- Log detection ratio, image coordinates, and contour size.
- Explain HSV thresholding and contour-based localization in the report.

## 3. Navigation - 25%
Evidence:
- Drone receives patrol waypoints from controller arguments.
- GPS position is used for localization.
- Drone switches target after reaching each waypoint.
- After fire detection, the drone uses image coordinates to approach the fire.

Planned improvements:
- Add logs for PATROL, DETECT, APPROACH, DROP, and RETURN states.
- Summarize target transitions in the report.

## 4. Integration and Behaviour - 10%
Evidence:
- Autonomous loop exists:
  patrol -> detect fire -> approach fire -> drop water -> continue patrol.
- Water-drop cooldown prevents immediate smoke/water confusion.

Planned improvements:
- Make behaviour loop explicit in code comments and report diagram.

## 5. Code Quality and Documentation - 10%
Evidence:
- Python controller is in the correct controllers folder.
- Baseline logs and analysis are saved.
- Project progress notes are being kept.

Planned improvements:
- Add structured comments.
- Add final report, screenshots, architecture diagram, and results table.
