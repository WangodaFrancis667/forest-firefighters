# Challenges Faced and Solutions

| Challenge | Solution |
|---|---|
| Webots R2025a compatibility issues caused missing PROTOs, broken terrain, and unstable Mavic behaviour. | The project was moved to Webots R2021b, which runs the Forest Firefighters project correctly. |
| Docker initially used software rendering, making the simulation slow. | NVIDIA GPU rendering was enabled inside Docker using `--gpus all` and OpenGL verification with `glxinfo`. |
| Running Webots as root caused sandbox-related crashes. | A non-root Docker user was created for Webots execution. |
| The drones appeared to be starting high due to world elevation and target altitude values. | A static launch-position check confirmed the drones spawn at the base positions: Mavic 1 at `4 4 17.4` and Mavic 2 at `4 3 17.43`. |
| Controller instrumentation changed timing and made the drones unstable. | The controller was restored to the stable baseline. Further work focused on external evidence collection and report analysis instead of modifying flight dynamics. |
| Some repeated runs showed Webots/Chromium shutdown artifacts after mission behaviour had already occurred. | The log analyzer was refined to separate mission performance from shutdown artifacts. The cleanest run is used as the primary report evidence. |
