# Performance Results

The final system was tested using the active four-drone plus Spot world. Each mission run starts
with the preflight checker, which verifies that all four Mavic 2 Pro drones are present, use the
`autonomous_mavic` controller, launch from separate quadrant bases, use interior-biased patrol
routes, and run the 160 by 160 camera/display profile.

## Final Four-Drone Validation Runs

| Run | Fire Detections | Water Drops | Targets Reached | Mission Errors | Mission Crashes | Shutdown Artifacts |
|---|---:|---:|---:|---:|---:|---:|
| demo | 160 | 10 | 29 | 0 | 0 | 1 |
| final_demo_test | 120 | 6 | 31 | 0 | 0 | 0 |
| live_demo_final | 162 | 7 | 29 | 0 | 0 | 16 |
| live_demo_run | 63 | 4 | 34 | 0 | 0 | 0 |
| stability_repeat_01 | 114 | 7 | 30 | 0 | 0 | 16 |
| stability_repeat_02 | 75 | 4 | 16 | 0 | 0 | 16 |
| stability_repeat_03 | 17 | 4 | 17 | 0 | 0 | 16 |
| stability_test_01 | 7 | 1 | 37 | 0 | 0 | 0 |

Across the final eight validation runs, the robots produced 718 fire detections, 43 water-drop
events, and 223 waypoint target transitions. There were no mission errors and no mission crashes.

## Baseline Comparison

The retained baseline run used the earlier two-drone style and produced 31 fire detections,
1 water drop, 6 target transitions, and no crashes. The final four-drone system increases
coverage and repeated response behaviour while keeping the simulation within the RTX A1000
6 GB resource profile.

## Interpretation

`final_demo_test` is the cleanest submission-style evidence run because it produced 120 fire
detections, 6 water drops, 31 target transitions, and no shutdown artifacts. `live_demo_final`
and `demo` show the highest detection and water-drop counts respectively.

Shutdown artifacts are reported separately. They are Webots/controller termination messages that
occur after the mission loop has completed or the simulator is closing. They are not Python
tracebacks, perception failures, navigation failures, or mid-mission controller crashes.
