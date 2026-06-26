# Forest Firefighters Robotics Mission

![Webots R2021b](https://img.shields.io/badge/Webots-R2021b-2454A6.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.x-2F6F44.svg?style=for-the-badge)
![Docker](https://img.shields.io/badge/Runtime-Docker-1D63ED.svg?style=for-the-badge)
![Robotics Fleet](https://img.shields.io/badge/Fleet-4%20Mavic%20Drones%20%2B%201%20Spot-4B5563.svg?style=for-the-badge)

This repository contains a Webots R2021b forest firefighting simulation. The mission uses four autonomous Mavic 2 Pro drones to patrol a simulated forest, detect smoke and fire with onboard cameras, move toward the detected target, drop water, and continue the mission. A Spot-style ground robot is also present as a stable support platform with a manual water burst control.

The project is designed around reproducible Webots runs. Docker provides the Webots R2021b runtime, the world file defines the forest and robots, Python controllers implement mission behavior, and the tools folder provides validation and run-analysis scripts.

## Video Demonstration

A walkthrough/demo video can be linked here after it is uploaded to YouTube:

```text
YouTube demo: https://www.youtube.com/watch?v=YOUR_VIDEO_ID
```

Recommended video coverage:

- Opening the repository and explaining the folder structure.
- Building and starting the Docker/Webots environment.
- Running the preflight validation command.
- Launching the Webots world.
- Showing the four drones patrolling, detecting fire, and dropping water.
- Showing the generated log and analysis files after a headless run.

## System Overview

The simulation is built from five main parts:

| Area | Purpose |
|---|---|
| Webots world | Defines the terrain, trees, fire supervisor, Spot robot, and four Mavic drones. |
| Drone controller | Handles flight stabilization, quadrant patrol, image-based fire detection, target approach, and water-drop signaling. |
| Fire supervisor | Starts the wildfire after a delay, evolves wind and fire propagation, receives water-drop signals, extinguishes nearby fire, and ends timed batch runs cleanly. |
| Spot controller | Holds a stable support posture and allows manual water release with the `D` key in interactive Webots runs. |
| Tooling | Validates the world configuration, runs timed missions, analyzes logs, and summarizes repeated results. |

Mission flow:

```text
Preflight validation
    -> Webots world starts
    -> Four drones take off to target altitude
    -> Each drone patrols its assigned quadrant
    -> Fire supervisor starts wildfire after 40 seconds
    -> Drones detect smoke or fire from camera frames
    -> Detecting drone approaches the target
    -> Drone drops water through customData
    -> Fire supervisor creates water and checks extinction
    -> Mission continues until the configured 300 second shutdown
```

## Repository Structure

```text
.
|-- Dockerfile
|-- build.sh
|-- run-gpu.sh
|-- README.md
|-- controllers/
|   |-- autonomous_mavic/
|   |   `-- autonomous_mavic.py
|   |-- fire/
|   |   `-- fire.py
|   `-- spot/
|       `-- spot.py
|-- worlds/
|   `-- forest_firefighters.wbt
|-- protos/
|   |-- Fire.proto
|   |-- Smoke.proto
|   |-- Water.proto
|   |-- Sassafras.proto
|   |-- UnevenForest.proto
|   `-- Fire/
|       |-- FlameAppearance.proto
|       `-- SmokeAppearance.proto
|-- plugins/
|   `-- robot_windows/
|       `-- fire/
|           |-- fire.html
|           |-- fire.css
|           `-- fire.js
|-- tools/
|   |-- preflight_check.py
|   |-- run_mission_test.sh
|   |-- analyze_mission_log.py
|   `-- summarize_runs.py
|-- assignment_docs/
|   |-- final_report/
|   |-- notes/
|   |-- presentation/
|   |-- results/
|   `-- screenshots/
`-- results/
```

### Important Files

| File | What it does |
|---|---|
| `worlds/forest_firefighters.wbt` | Main Webots world. It defines the terrain, Sassafras forest, fire supervisor, Spot robot, and four Mavic drones. |
| `controllers/autonomous_mavic/autonomous_mavic.py` | Main drone controller. It reads sensors, stabilizes the drone, follows patrol waypoints, detects smoke/fire with OpenCV, approaches targets, and requests water drops. |
| `controllers/fire/fire.py` | Supervisor controller. It manages wildfire start timing, wind, spread, water objects, extinction checks, and clean mission shutdown. |
| `controllers/spot/spot.py` | Spot support controller. It places Spot into a stable posture and sends a water burst when `D` is pressed. |
| `plugins/robot_windows/fire/` | Webots robot-window UI for viewing and controlling wind direction/intensity during interactive runs. |
| `protos/` | Custom simulation assets for fire, smoke, water, trees, terrain, and appearance definitions. |
| `tools/preflight_check.py` | Checks that the world contains the expected four-drone configuration, patrol routes, target altitude, displays, and fire supervisor timing. |
| `tools/run_mission_test.sh` | Runs a headless mission test, captures a log, and calls the analyzer. |
| `tools/analyze_mission_log.py` | Reads a Webots log and creates a Markdown report with detections, drops, waypoint transitions, errors, and shutdown artifacts. |
| `tools/summarize_runs.py` | Aggregates generated `.analysis.md` files from `assignment_docs/results`. |
| `assignment_docs/` | Supporting report material, run logs, analysis outputs, notes, presentation script, and screenshots. |
| `Dockerfile` | Builds an Ubuntu 20.04 image with Webots R2021b, Python, NumPy, OpenCV, X11, and GPU-related runtime libraries. |
| `build.sh` | Builds the Docker image as `webots-r2021b-gpu`. |
| `run-gpu.sh` | Starts an interactive Docker container with NVIDIA GPU, X11, and Webots runtime settings. |

## Runtime Requirements

The provided Docker workflow is intended for a Linux machine with:

- Docker installed.
- NVIDIA GPU drivers installed.
- NVIDIA Container Toolkit installed.
- X11 display access available on the host.
- `xhost` available for allowing the container to open the Webots GUI.

The Docker image installs:

- Ubuntu 20.04
- Webots R2021b
- Python 3
- NumPy
- OpenCV
- OpenGL/X11 libraries required by Webots

## Clone the Repository

Start by cloning the project from GitHub:

```bash
git clone https://github.com/WangodaFrancis667/forest-firefighters.git
cd forest-firefighters
```

All commands below should be run from the repository root unless a section says otherwise.

## Docker Setup

Run these commands from the repository root.

### 1. Make Scripts Executable

```bash
chmod +x build.sh
chmod +x run-gpu.sh
chmod +x tools/run_mission_test.sh
```

### 2. Build the Docker Image

```bash
./build.sh
```

This creates the Docker image:

```text
webots-r2021b-gpu
```

The build downloads and installs Webots R2021b inside the image, so the first build can take several minutes.

### 3. Start the GPU Container

```bash
./run-gpu.sh
```

The script:

- Allows local Docker X11 access with `xhost +local:docker`.
- Removes any old container named `webots_r2021b_gpu`.
- Starts a new interactive container named `webots_r2021b_gpu`.
- Enables NVIDIA GPU access with `--gpus all`.
- Passes X11 display variables into the container.
- Mounts the host path `./workspace` to `/workspace` inside the container.

Important: because the current script mounts `./workspace`, the project files must be available under that host folder if you want to access them at `/workspace` in the container. If you want the repository root mounted directly, change the volume line in `run-gpu.sh` from:

```bash
-v "$PWD/workspace:/workspace" \
```

to:

```bash
-v "$PWD:/workspace" \
```

After the container starts, move to the project directory inside the container. If you mounted the repository root directly, use:

```bash
cd /workspace
```

If you placed the repository inside the mounted `workspace` folder, use the matching path, for example:

```bash
cd /workspace/forest-firefighters
```

## Validate the Project

Before running the mission, validate that the world file still matches the expected four-drone configuration:

```bash
python3 tools/preflight_check.py
```

Expected successful result:

```text
PREFLIGHT PASSED
Four drones are configured for interior quadrant patrol with autonomous_mavic controllers and status-bar overlays.
```

This check verifies:

- Four `Mavic2Pro` drones exist.
- Each drone uses the `autonomous_mavic` controller.
- Each drone has the expected spawn position and patrol route.
- Each drone uses `--target_altitude=42`.
- Each drone uses `--detection_interval=0.5`.
- Each drone has a `vision overlay` display.
- The fire supervisor uses `--start_delay=40`.
- The fire supervisor uses `--mission_duration=300`.

## Run the Simulation

### Interactive Webots Run

Use this when you want to observe the mission in the Webots GUI:

```bash
webots worlds/forest_firefighters.wbt
```

During the interactive run:

- The four drones take off and patrol separate forest quadrants.
- The fire supervisor starts a wildfire after 40 seconds.
- Drone camera overlays show status bars.
- A green status bar means normal patrol.
- A red status bar means fire/smoke detection.
- The Spot robot can release water manually when selected and the `D` key is pressed.
- The fire robot window can be used to inspect or adjust wind behavior.

### Headless Mission Test

Use this when you want a repeatable timed run with logs and analysis:

```bash
./tools/run_mission_test.sh live_demo_run
```

The script runs:

```bash
python3 tools/preflight_check.py
webots --stdout --stderr worlds/forest_firefighters.wbt
python3 tools/analyze_mission_log.py assignment_docs/results/live_demo_run.log
```

Generated files:

```text
assignment_docs/results/live_demo_run.log
assignment_docs/results/live_demo_run.analysis.md
```

The test script uses a 12 minute external timeout and the world has a 300 second internal mission duration. The fire supervisor requests a clean Webots shutdown when the mission duration is reached.

## Analyze Existing or New Logs

Analyze any mission log manually:

```bash
python3 tools/analyze_mission_log.py assignment_docs/results/live_demo_run.log
```

The analyzer reports:

- Controller starts
- Wildfires started
- Fire detections
- Water drops
- Waypoint target transitions
- Mission errors
- Mission crashes
- Shutdown artifacts

Summarize all generated analysis files:

```bash
python3 tools/summarize_runs.py
```

To save the summary into the tracked results folder:

```bash
python3 tools/summarize_runs.py > assignment_docs/results/performance_results_summary.md
```

## Current Mission Configuration

The active world configuration is in `worlds/forest_firefighters.wbt`.

| Robot | Spawn area | Controller | Main arguments |
|---|---|---|---|
| `Mavic 2 PRO(1)` | SW | `autonomous_mavic` | `--target_altitude=42`, SW patrol, `--detection_interval=0.5` |
| `Mavic 2 PRO(2)` | NW | `autonomous_mavic` | `--target_altitude=42`, NW patrol, `--detection_interval=0.5` |
| `Mavic 2 PRO(3)` | SE | `autonomous_mavic` | `--target_altitude=42`, SE patrol, `--detection_interval=0.5` |
| `Mavic 2 PRO(4)` | NE | `autonomous_mavic` | `--target_altitude=42`, NE patrol, `--detection_interval=0.5` |
| `Spot` | South-west support area | `spot` | Manual water burst with `D` |
| Fire supervisor | World supervisor | `fire` | `--start_delay=40`, `--mission_duration=300` |

Drone patrol routes are intentionally biased toward the interior of each quadrant so the central forest receives repeated camera coverage.

## How the Controllers Communicate

The drone and Spot controllers do not directly modify fire nodes. They send water-drop requests through each robot's Webots `customData` field:

```text
Robot controller sets customData to a water quantity
    -> fire supervisor reads customData
    -> fire supervisor creates a Water node
    -> fire supervisor checks whether water is close enough to active fire
    -> matching fire and smoke nodes are moved away/cleared
```

This keeps fire creation, propagation, and extinction logic inside the supervisor controller.

## Development Workflow

Use this sequence after changing world configuration, controllers, PROTO files, or mission logic:

```bash
python3 tools/preflight_check.py
./tools/run_mission_test.sh my_test_run
python3 tools/analyze_mission_log.py assignment_docs/results/my_test_run.log
python3 tools/summarize_runs.py
```

Recommended checks before committing:

- Confirm `python3 tools/preflight_check.py` passes.
- Run at least one headless mission test.
- Review the generated `.analysis.md` file for mission errors or crashes.
- If changing drone behavior, confirm detections, water drops, and waypoint transitions are still present.
- If changing the world file, confirm all four drone blocks still have the expected controller arguments.

## Results and Documentation

Existing evidence and project material are stored in `assignment_docs/`:

| Path | Contents |
|---|---|
| `assignment_docs/final_report/firefighting_robotics_report.tex` | Final report source. |
| `assignment_docs/presentation/final_presentation_script.md` | Presentation script. |
| `assignment_docs/results/` | Mission logs, analysis files, and performance summary. |
| `assignment_docs/notes/` | Design notes, rubric mapping, baseline evidence, and controller inspection notes. |
| `assignment_docs/screenshots/` | Supporting screenshots. |

The committed result files are useful as reference evidence, but new runs should be generated with `tools/run_mission_test.sh` so the logs and analysis match the current code.
