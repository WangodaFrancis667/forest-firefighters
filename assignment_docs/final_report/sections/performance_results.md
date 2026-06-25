# Performance Results

The mission was tested three times after confirming that both Mavic drones started from their correct base positions.

| Run | Fire Detections | Water Drops | Targets Reached | Mission Errors | Mission Crashes | Shutdown Artifacts |
|---|---:|---:|---:|---:|---:|---:|
| stability_repeat_01 | 107 | 5 | 4 | 0 | 0 | 0 |
| stability_repeat_02 | 79 | 7 | 4 | 0 | 2 | 3 |
| stability_repeat_03 | 59 | 5 | 4 | 0 | 6 | 4 |

The primary clean run was `stability_repeat_01`, which achieved 107 camera-based fire detections, 5 water drops, 4 target transitions, and no mission errors or crashes. This run is used as the main evidence for the final report and live demo.

The additional runs show repeated firefighting behaviour with multiple detections and water drops. Some later warnings were recorded near simulator termination, especially Webots/Chromium shutdown artifacts, so they are documented separately from the mission behaviour.
