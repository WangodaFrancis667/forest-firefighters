# Challenges Faced and Solutions

| Challenge | Solution |
|---|---|
| Webots R2025a caused missing PROTOs, terrain issues, and unstable legacy robot behaviour. | The project was standardised on Webots R2021b, matching the original Forest Firefighters project version. |
| Docker initially used software rendering, making the simulation slow and unstable. | The environment was configured for NVIDIA GPU OpenGL rendering on the RTX A1000 6 GB laptop. |
| Running Webots as root produced sandbox-related instability. | The workflow uses a non-root Webots user inside the GPU container. |
| The first working baseline only used two Mavic drones, so coverage was limited. | The final world adds two missing Mavic drones for four-quadrant coverage while avoiding heavier six- or eight-drone experiments. |
| Edge-only patrol routes missed fires in the middle of the forest. | The final patrol routes are interior-biased so each quadrant drone periodically scans toward the central forest. |
| Dense camera overlays made the screen unreadable and increased visual clutter. | The overlay was simplified to a green normal bar and red fire bar only. |
| Camera detection could fail when smoke was visible but no valid contour was selected. | The detector now safely returns an empty target when no valid contour exists instead of crashing. |
| Some Webots runs printed controller crash warnings during shutdown. | The log analyzer separates mission crashes from shutdown artifacts that occur after controller termination. |
| The fire originally started too late for a concise demo. | The wildfire now starts after 40 seconds, giving the drones time to launch while keeping the demonstration responsive. |
| Long GUI runs could be killed externally before clean shutdown. | The fire supervisor requests clean shutdown after 300 seconds, and the mission runner allows a 12-minute wall-clock timeout. |
