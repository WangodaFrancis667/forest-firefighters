# Final Results Interpretation

The repeated mission tests showed consistent autonomous firefighting behavior. In each run, the drones started from the confirmed base positions, the fire controller started, the wildfire began, camera-based fire/smoke detections were logged, water drops were performed, and waypoint navigation continued.

The first repeat run was the cleanest demonstration run, with no mission errors or crashes. Later repeat runs produced strong detection and water-drop counts, but also included Webots/Chromium shutdown artifacts at simulator termination. These shutdown messages occurred after successful mission behavior had already been demonstrated and are not treated as navigation, perception, or flight-control failures.

For the final report and demo, stability_repeat_01 is used as the primary clean evidence run, while stability_repeat_02 and stability_repeat_03 are used as additional evidence of repeated fire detection and water-drop behavior.
