# Final Results Interpretation

The refreshed results show consistent autonomous firefighting behaviour in the final four-drone
configuration. Every final validation run started six controllers: one fire supervisor, one Spot
support robot, and four autonomous Mavic drones. Every final run started one wildfire, produced
camera-based fire detections, logged water drops, and continued waypoint navigation.

Across the eight final validation runs:

- Fire detections: 718 total.
- Water drops: 43 total.
- Waypoint target transitions: 223 total.
- Mission errors: 0.
- Mission crashes: 0.

The baseline two-drone reference is still useful historically, but it is not the final performance
claim. The final project claim is based on the active four-drone plus Spot world.

Some runs contain shutdown artifacts. These are Webots/controller termination warnings emitted
after the mission has already demonstrated detection, navigation, and water dropping. They are
reported separately from mission crashes because there are no Python tracebacks, controller exit
status failures, or mid-mission failures in the refreshed final analysis files.

The cleanest submission-style run is `final_demo_test`: 120 detections, 6 water drops, 31 target
transitions, 0 mission errors, 0 mission crashes, and 0 shutdown artifacts.
