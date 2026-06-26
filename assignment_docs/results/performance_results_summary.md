# Performance Results Summary

This summary consolidates the refreshed mission analysis files in `assignment_docs/results/`.
The baseline run is kept for historical comparison, while the final validation evidence is based
on the four-drone plus Spot configuration used in `worlds/forest_firefighters.wbt`.

## Final Four-Drone Validation Runs

| Run | Controller Starts | Wildfires Started | Fire Detections | Water Drops | Targets Reached | Mission Errors | Mission Crashes | Shutdown Artifacts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| demo | 6 | 1 | 160 | 10 | 29 | 0 | 0 | 1 |
| final_demo_test | 6 | 1 | 120 | 6 | 31 | 0 | 0 | 0 |
| live_demo_final | 6 | 1 | 162 | 7 | 29 | 0 | 0 | 16 |
| live_demo_run | 6 | 1 | 63 | 4 | 34 | 0 | 0 | 0 |
| stability_repeat_01 | 6 | 1 | 114 | 7 | 30 | 0 | 0 | 16 |
| stability_repeat_02 | 6 | 1 | 75 | 4 | 16 | 0 | 0 | 16 |
| stability_repeat_03 | 6 | 1 | 17 | 4 | 17 | 0 | 0 | 16 |
| stability_test_01 | 6 | 1 | 7 | 1 | 37 | 0 | 0 | 0 |

## Aggregate Final Metrics

| Metric | Value |
|---|---:|
| Final validation runs | 8 |
| Total fire detections | 718 |
| Average fire detections per run | 89.75 |
| Total water drops | 43 |
| Average water drops per run | 5.38 |
| Total waypoint target transitions | 223 |
| Average target transitions per run | 27.88 |
| Mission errors | 0 |
| Mission crashes | 0 |

## Baseline Reference

| Run | Controller Starts | Wildfires Started | Fire Detections | Water Drops | Targets Reached | Errors | Crashes |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline_run | 4 | 1 | 31 | 1 | 6 | 0 | 0 |

## Interpretation

The final four-drone configuration repeatedly demonstrated the complete mission loop:

`patrol -> detect smoke/fire -> visually approach fire -> drop water -> resume patrol`.

The strongest single validation run by detection count was `live_demo_final`, with 162 fire
detections, 7 water drops, and no mission errors or crashes. The strongest run by water-drop
count was `demo`, with 10 water drops and no mission crashes. `final_demo_test` is the cleanest
submission-style run because it produced 120 fire detections, 6 water drops, 31 target
transitions, and no shutdown artifacts.

Some runs include shutdown artifacts. These are Webots/controller termination messages emitted
after successful mission operation, not Python tracebacks, navigation failures, or mid-mission
controller crashes. They are therefore reported separately from mission errors and mission
crashes.
