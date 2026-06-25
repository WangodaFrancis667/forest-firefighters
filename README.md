# Forest Firefighters Robotics Mission

![Webots R2021b](assignment_docs/readme_assets/webots-r2021b.svg)
![Fleet: 4 drones plus Spot](assignment_docs/readme_assets/fleet-profile.svg)
![GPU profile: RTX A1000 6GB](assignment_docs/readme_assets/gpu-profile.svg)

This repository contains a Webots R2021b forest-firefighting robotics assignment. The final system uses a resource-conscious multi-robot team: four autonomous Mavic 2 Pro drones for aerial patrol and a Spot-like ground robot for visible legged-robot support and water-burst interaction.

The implementation is tuned for a laptop with an NVIDIA RTX A1000 6 GB GPU. Earlier experiments increased the aerial fleet beyond the original project baseline, but the final design prioritizes stable simulation, clear perception evidence, and repeatable 5-8 minute demonstrations.

## Mission Objective

Program robots in the Webots Forest Firefighters world to:

- Patrol a designated forest area.
- Detect smoke/fire using onboard cameras.
- Navigate toward the detected fire location.
- Drop water accurately enough to extinguish fire.
- Continue operating while wind and fire propagation are active.

## Final Architecture

The active world uses:

| Subsystem | Role |
|---|---|
| Four Mavic 2 Pro drones | Quadrant patrol, camera perception, visual approach, water drop |
| Spot-like ground robot | Continuous gait demonstration and keyboard-triggered water burst |
| Fire supervisor | Wind evolution, fire spread, active-fire cap, water extinction checks |
| OpenCV perception | HSV smoke/fire segmentation and contour-based target selection |
| Webots recognition overlays | Tree bounding boxes on drone camera displays |
| Root-level tools | Preflight validation, timed mission runs, log analysis, result summaries |

Each drone has a `vision overlay` display attached to its camera feed. During simulation, the display draws green tree boxes from Webots recognition, red smoke/fire boxes from OpenCV contours, and a red flash when fire is detected.

## Fleet Evolution

The robot count changed during engineering for stability and performance reasons:

| Stage | Configuration | Reason |
|---|---|---|
| Baseline | Original drone and Spot project robots | Starting point from the upstream Forest Firefighters project |
| Experiment | Eight drones | Tested maximum aerial coverage and redundancy |
| Intermediate | Six drones | Reduced load, but Webots still crashed during GPU-container mission runs |
| Final | Four drones plus Spot | Preserves quadrant coverage while fitting the 6 GB RTX A1000 resource budget |

The final configuration is intentionally not the largest fleet. It is the most practical configuration for this machine: fewer camera renderers, fewer controller processes, lower overlay load, and clearer demo visibility.

## Repository Layout

```text
.
├── controllers/
│   ├── autonomous_mavic/      # Four-drone patrol, OpenCV detection, overlay drawing
│   ├── fire/                  # Wildfire supervisor, wind, propagation, extinction logic
│   ├── mavic/                 # Manual Mavic example controller
│   └── spot/                  # Spot gait loop and keyboard water burst
├── protos/                    # Fire, smoke, tree, terrain, and water PROTO assets
├── worlds/
│   └── forest_firefighters.wbt
├── tools/
│   ├── preflight_check.py     # Validates the active four-drone world
│   ├── run_mission_test.sh    # Runs Webots, captures logs, analyzes results
│   ├── analyze_mission_log.py # Builds per-run metrics
│   └── summarize_runs.py      # Summarizes repeated mission logs
├── assignment_docs/
│   ├── archive/               # Historical notes and retired helper scripts
│   ├── backups/               # Controller/world snapshots from earlier phases
│   ├── final_report/          # LaTeX source, PDF, diagrams, and report assets
│   ├── notes/                 # Rubric mapping and engineering notes
│   ├── presentation/          # Final presentation script
│   ├── readme_assets/         # Local SVG badges used by this README
│   ├── results/               # Mission logs and generated analysis files
│   └── screenshots/           # Visual evidence
├── Dockerfile
└── Robotics Q and A guiding questions.pdf
```

## Running the Project

### 1. Start the Webots GPU Container

From the host machine:

```bash
cd ~/Desktop/ros/webots-r2021b-gpu
./run-gpu.sh
```

Inside the container, use a normal `cd` command:

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

If it is already mounted or cloned:

```bash
cd /workspace/webots-projects/projects/forest_firefighters
```

### 3. Validate the World Before Running Webots

```bash
python3 tools/preflight_check.py
```

Expected result:

```text
PREFLIGHT PASSED
```

### 4. Run a Timed Mission Test

```bash
./tools/run_mission_test.sh live_demo_four_drone
```

The runner creates:

```text
assignment_docs/results/live_demo_four_drone.log
assignment_docs/results/live_demo_four_drone.analysis.md
```

### 5. Run the Interactive Demo

```bash
webots worlds/forest_firefighters.wbt
```

In Webots:

- Select each drone and enable `Robot > Display Devices > vision overlay` if the display is hidden.
- Arrange the four drone overlays in a 2x2 layout for clear visual monitoring.
- Keep the display size close to 160x160 on the RTX A1000 profile.
- Select Spot and press `D` to throw water from the ground robot.

## Implementation Notes

### Drone Controller

`controllers/autonomous_mavic/autonomous_mavic.py` provides:

- GPS waypoint patrol by quadrant.
- Stabilized flight using GPS, IMU, gyro, and propeller motor control.
- OpenCV HSV thresholding for smoke/fire detection.
- Contour-based target selection and red fire bounding boxes.
- Tree bounding boxes through Webots camera recognition.
- Water drop through drone `customData`.

### Spot Controller

`controllers/spot/spot.py` keeps the Spot-like robot active for the full mission. It cycles a simple gait and uses the keyboard `D` command for a water burst. Spot is treated as a support robot, while the drones remain the primary search and response platform.

### Fire Supervisor

`controllers/fire/fire.py` controls wildfire behavior. The current values slow propagation, reduce wind volatility, cap active fires, and increase water extinction tolerance so the simulation remains demonstrable on the available GPU.

## Verification Checklist

Run before a live demo or submission:

```bash
python3 tools/preflight_check.py
python3 -m py_compile controllers/autonomous_mavic/autonomous_mavic.py controllers/fire/fire.py controllers/spot/spot.py tools/*.py
./tools/run_mission_test.sh stability_repeat_01
python3 tools/summarize_runs.py
```

Manual Webots checks:

- Four drones launch from separate quadrants.
- Spot remains active for the full mission.
- Drone overlays show tree boxes and fire/smoke boxes.
- Red overlay flash appears when fire/smoke is detected.
- Drone water drops are logged after visual centering.
- The simulation can run through the 5-8 minute mission window without a Webots segmentation fault.

## Report and Presentation

- Final report PDF: `assignment_docs/final_report/latex/firefighting_robotics_report.pdf`
- Report source: `assignment_docs/final_report/latex/firefighting_robotics_report.tex`
- Presentation script: `assignment_docs/presentation/final_presentation_script.md`
- Assignment brief: `Robotics Q and A guiding questions.pdf`

The report architecture diagram reflects the final system: four Mavic drones plus the Spot-like ground robot, coordinated through the Webots fire supervisor and mission decision loop.
