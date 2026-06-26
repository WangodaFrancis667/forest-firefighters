# Forest Firefighters Robotics Mission

![Webots R2021b](assignment_docs/readme_assets/webots-r2021b.svg)
![Fleet: 4 drones plus Spot](assignment_docs/readme_assets/fleet-profile.svg)
![GPU profile: RTX A1000 6GB](assignment_docs/readme_assets/gpu-profile.svg)

This repository contains an autonomous forest firefighting robotics mission built in the Webots
R2021b Forest Firefighters environment. The final system uses four Mavic 2 Pro drones for aerial
search and response, plus a Spot-like ground robot as a stable support platform.

The project deliberately keeps the original working setup available in `original/` for baseline
review. The active implementation is at the repository root and is tuned for a laptop with an
NVIDIA RTX A1000 6 GB GPU.

## What the Project Demonstrates

The mission objective is to make robots:

- Patrol a forest environment.
- Detect smoke/fire using onboard cameras.
- Navigate toward the detected fire.
- Drop water to extinguish active fire.
- Continue patrolling while wind and fire propagation are active.
- Produce logs and analysis that prove the behaviour happened.

The final autonomous loop is:

```text
preflight -> take off -> patrol -> detect smoke/fire -> approach fire -> drop water -> resume patrol
```

## Final System Architecture

| Layer | Component | Responsibility |
|---|---|---|
| Simulation world | `worlds/forest_firefighters.wbt` | Terrain, trees, drones, Spot, fire supervisor, sensors, and water mechanics |
| Fire supervisor | `controllers/fire/fire.py` | Delayed wildfire start, wind evolution, fire spread, smoke creation, water extinction checks, clean timed shutdown |
| Aerial robots | `controllers/autonomous_mavic/autonomous_mavic.py` | Four Mavic drones, GPS patrol, camera detection, visual fire approach, water-drop command |
| Ground robot | `controllers/spot/spot.py` | Stable support posture and keyboard-triggered water burst |
| Validation tools | `tools/` | Preflight checks, timed mission runs, log analysis, and result summaries |
| Documentation | `assignment_docs/` | Final report, presentation script, notes, results, screenshots, and historical evidence |

### Why Four Drones

The project evolved from the original two-drone baseline. Larger six- and eight-drone experiments
increased camera/controller load and reduced stability on the 6 GB GPU laptop. The final four-drone
layout is the practical balance:

- More coverage than the original two-drone baseline.
- One aerial robot per forest quadrant.
- Interior-biased patrol routes, so drones do not only scan the forest edges.
- 160 by 160 camera/display resolution to keep GPU and CPU load controlled.
- Minimal green/red status-bar overlays instead of dense bounding-box rendering.

## Algorithm Summary

### 1. Locomotion and Stabilisation

Each Mavic uses four propeller motors. The controller combines altitude error, roll, pitch, yaw,
IMU readings, gyro feedback, and GPS position to maintain stable flight. Patrol speed is increased
from the baseline while keeping the original controller structure.

### 2. Interior Quadrant Patrol

Patrol coordinates are passed through the world file with `--patrol_coords`. Each drone gets a
separate route covering its quadrant and scanning toward the central forest:

| Drone | Area | Patrol Purpose |
|---|---|---|
| Mavic 1 | South-west | Covers lower-left forest and central-left approach |
| Mavic 2 | North-west | Covers upper-left forest and central-left approach |
| Mavic 3 | South-east | Covers lower-right forest and central-right approach |
| Mavic 4 | North-east | Covers upper-right forest and central-right approach |

### 3. Camera Fire Detection

Each drone camera points downward. The image is converted into an OpenCV-compatible format, then
converted to HSV colour space. The detector thresholds bright, low-saturation smoke/fire regions,
extracts contours, and chooses the largest valid contour as the current target.

The camera overlay is intentionally simple:

- Green top bar: normal patrol.
- Red top bar with `FIRE`: active fire target detected.

This avoids cluttering the screen with tree boxes and keeps rendering cost low.

### 4. Visual Approach and Water Drop

When a fire target is detected, the drone compares the target image coordinate with the centre of
the camera frame. Yaw and pitch corrections move the drone toward the target. When the target is
centred, the drone sends a water-drop command through its `customData` field. The fire supervisor
then spawns water and checks whether it extinguishes nearby active fire.

### 5. Fire Timing and Shutdown

The active world starts the wildfire after 40 seconds:

```text
--start_delay=40
```

Timed mission tests request clean shutdown after 300 simulation seconds:

```text
--mission_duration=300
```

The shell runner allows a 12-minute wall-clock timeout to avoid killing slow GUI runs too early.

## Results Summary

The refreshed final validation set contains eight four-drone runs.

| Metric | Value |
|---|---:|
| Final validation runs | 8 |
| Total fire detections | 718 |
| Total water drops | 43 |
| Total waypoint target transitions | 223 |
| Mission errors | 0 |
| Mission crashes | 0 |

The cleanest submission-style run is `final_demo_test`:

| Run | Fire Detections | Water Drops | Targets Reached | Mission Errors | Mission Crashes | Shutdown Artifacts |
|---|---:|---:|---:|---:|---:|---:|
| final_demo_test | 120 | 6 | 31 | 0 | 0 | 0 |

Some other runs contain shutdown artifacts. These are Webots/controller termination warnings after
mission behaviour has already completed. They are documented separately from mission crashes.

Full results are in:

- `assignment_docs/results/performance_results_summary.md`
- `assignment_docs/results/*.analysis.md`

## Repository Layout

```text
.
├── controllers/
│   ├── autonomous_mavic/      # Four-drone patrol, OpenCV detection, status bars, water-drop command
│   ├── fire/                  # Wildfire supervisor, propagation, extinction, timed shutdown
│   ├── mavic/                 # Manual/example Mavic controller
│   └── spot/                  # Stable Spot support posture and keyboard water burst
├── protos/                    # Fire, smoke, water, tree, and terrain assets
├── worlds/
│   └── forest_firefighters.wbt
├── tools/
│   ├── preflight_check.py     # Validates active four-drone world configuration
│   ├── run_mission_test.sh    # Runs Webots, captures logs, analyzes mission output
│   ├── analyze_mission_log.py # Extracts detections, drops, target transitions, errors, crashes
│   └── summarize_runs.py      # Summarizes repeated mission evidence
├── original/                  # Preserved upstream baseline; do not edit for active implementation
├── assignment_docs/
│   ├── final_report/          # LaTeX report source, PDF, sections, diagrams
│   ├── presentation/          # Final presentation script
│   ├── results/               # Run logs, analysis files, performance summary
│   ├── notes/                 # Rubric mapping and interpretation notes
│   ├── archive/               # Historical development notes and retired tools
│   ├── backups/               # Earlier controller/world snapshots
│   └── screenshots/           # Visual evidence
├── Dockerfile
├── run-gpu.sh
└── Robotics Q and A guiding questions.pdf
```

## Running the Project

### 1. Start the Webots GPU Container

From the host machine:

```bash
cd ~/Desktop/ros/webots-r2021b-gpu
./run-gpu.sh
```

Inside the container:

```bash
cd /workspace
```

### 2. Clone or Enter the Repository

If the repository is not already present:

```bash
mkdir -p /workspace/webots-projects/projects
cd /workspace/webots-projects/projects
git clone <repository-url> forest_firefighters
cd forest_firefighters
```

If it already exists:

```bash
cd /workspace/webots-projects/projects/forest_firefighters
```

### 3. Validate Before Running Webots

```bash
python3 tools/preflight_check.py
```

Expected result:

```text
PREFLIGHT PASSED
Four drones are configured for interior quadrant patrol with autonomous_mavic controllers and status-bar overlays.
```

### 4. Run a Timed Mission Test

```bash
./tools/run_mission_test.sh live_demo_four_drone
```

This creates:

```text
assignment_docs/results/live_demo_four_drone.log
assignment_docs/results/live_demo_four_drone.analysis.md
```

### 5. Run an Interactive Demo

```bash
webots worlds/forest_firefighters.wbt
```

In Webots:

- Arrange the four drone camera overlays across the bottom or side of the screen.
- Keep overlays near their native 160 by 160 size for performance.
- Watch for green bars during patrol and red `FIRE` bars during detection.
- Select Spot and press `D` to demonstrate the support water burst.

## Verification Checklist

Run before submission or live demonstration:

```bash
python3 tools/preflight_check.py
python3 -m py_compile controllers/autonomous_mavic/autonomous_mavic.py controllers/fire/fire.py controllers/spot/spot.py tools/*.py
./tools/run_mission_test.sh final_demo_test
```

Optional summary review:

```bash
python3 tools/summarize_runs.py
```

## If Asked Questions

### What is the architecture?

The Webots world is the integration layer. The fire supervisor controls wildfire behaviour. Four
Mavic drones perform autonomous aerial patrol, detection, visual approach, and water dropping. Spot
is a ground support robot. The tools folder validates the world and turns logs into mission metrics.

### Why not use six or eight drones?

The assignment needs robust mission behaviour, not maximum robot count. Six/eight drones increased
camera and controller load on the RTX A1000 6 GB laptop. Four drones provide full quadrant coverage
while keeping the simulation stable and readable.

### How is fire detected?

Each Mavic camera frame is processed with OpenCV-style HSV thresholding. Bright, low-saturation
smoke/fire pixels are segmented, contours are extracted, and the largest valid contour becomes the
target image coordinate.

### How does the drone know where to drop water?

The detected target is represented in camera coordinates. The drone moves until the target is near
the image centre. At that point, the fire is assumed to be below the drone and a water-drop command
is sent through `customData`.

### Why are there shutdown artifacts in some logs?

Webots can print controller crash warnings while closing controllers at the end of a run. The
analyzer separates those from mission crashes. The final validation analysis shows zero mission
errors and zero mission crashes.

### What proves the project works?

The final validation logs show 718 total detections, 43 water drops, 223 waypoint transitions, and
zero mission crashes across eight four-drone runs. The cleanest run, `final_demo_test`, has 120
detections, 6 water drops, 31 target transitions, and no shutdown artifacts.

## Report and Presentation

- Final report PDF: `assignment_docs/final_report/latex/firefighting_robotics_report.pdf`
- Report source: `assignment_docs/final_report/latex/firefighting_robotics_report.tex`
- Presentation script: `assignment_docs/presentation/final_presentation_script.md`
- Results summary: `assignment_docs/results/performance_results_summary.md`
- Assignment brief: `Robotics Q and A guiding questions.pdf`
