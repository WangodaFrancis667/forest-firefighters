# Forest Firefighters Robotics Assignment

Webots R2021b simulation for an autonomous forest-firefighting mission using a four-drone Mavic team and a Spot-like ground robot. The current setup is tuned for a laptop with an NVIDIA RTX A1000 6 GB GPU: it reduces the previous six-drone load, keeps camera resolution modest, slows fire propagation, and adds lightweight OpenCV/Webots visual feedback for detection.

## Mission Scope

The assignment objective is to patrol a forest, detect fire or smoke with cameras, navigate to the fire, drop water accurately, and continue handling propagated fires during a 5-8 minute simulation.

Current implementation:

- Four `Mavic2Pro` drones patrol SW, NW, SE, and NE quadrants.
- Each drone uses OpenCV color segmentation for smoke/fire detection.
- Each drone has a `vision overlay` display that attaches to the camera feed and draws:
  - green tree boxes from Webots camera recognition,
  - red fire/smoke boxes from OpenCV contours,
  - a red flash over the camera display when fire/smoke is detected.
- Spot remains active for the full run and can throw water with `D`.
- Fire propagation remains enabled, but spread rate and active-fire count are capped for stable assignment demos.
- Operational scripts live in the root-level `tools/` folder.

## Project Structure

```text
.
├── controllers/
│   ├── autonomous_mavic/      # Four-drone patrol, OpenCV detection, camera overlay drawing
│   ├── fire/                  # Supervisor controlling fire, wind, propagation, and water extinction
│   ├── mavic/                 # Manual Mavic example controller
│   └── spot/                  # Spot gait loop and water-drop keyboard control
├── protos/                    # Local fire, smoke, tree, terrain, and water PROTO assets
├── worlds/
│   └── forest_firefighters.wbt
├── tools/
│   ├── preflight_check.py     # Validates the four-drone world configuration
│   ├── run_mission_test.sh    # Runs Webots, captures logs, and analyzes results
│   ├── analyze_mission_log.py # Creates per-run metrics
│   └── summarize_runs.py      # Summarizes repeated stability logs
├── assignment_docs/
│   ├── archive/               # Archived one-off helper scripts
│   ├── backups/               # Historical controller/world snapshots
│   ├── final_report/          # Report source, PDF, diagrams, and section drafts
│   ├── notes/                 # Engineering notes and rubric mapping
│   ├── presentation/          # Demo notes and presentation script
│   ├── results/               # Webots run logs and generated analysis files
│   └── screenshots/           # Visual evidence
├── Dockerfile
└── Robotics Q and A guiding questions.pdf
```

## Run Commands

### 1. Start the Webots GPU Container

From the host machine, start the existing Webots R2021b GPU environment:

```bash
cd ~/Desktop/ros/webots-r2021b-gpu
./run-gpu.sh
```

Inside the container, do not use `~cd`. Use normal `cd`:

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

If it is already mounted/cloned:

```bash
cd /workspace/webots-projects/projects/forest_firefighters
```

### 3. Run Preflight Checks

```bash
python3 tools/preflight_check.py
```

Expected result: `PREFLIGHT PASSED`.

### 4. Run a Timed Mission Test

```bash
./tools/run_mission_test.sh live_demo_four_drone
```

This writes:

- `assignment_docs/results/live_demo_four_drone.log`
- `assignment_docs/results/live_demo_four_drone.analysis.md`

### 5. Run the Interactive Demo

```bash
webots worlds/forest_firefighters.wbt
```

In Webots:

- Select each drone and enable its `vision overlay` display from `Robot > Display Devices` if it is not already visible.
- Tile the four display overlays in a 2x2 layout so all drones are visible.
- Keep camera/display windows at 160x160 unless the machine has spare GPU headroom.
- Press `D` while Spot is selected to throw water from Spot.

## Design Notes

Four drones are used instead of six because the previous six-drone setup started six camera pipelines and six controllers, then crashed Webots with a segmentation fault during the mission. Four quadrant drones are a better match for a 6 GB VRAM laptop: coverage remains complete while reducing camera rendering, controller CPU, and overlay pressure.

The drone cameras use 160x160 images. OpenCV detection runs every 0.5 seconds by default, and debug image writing is disabled unless `--debug_images` is passed. This avoids repeated disk writes and unnecessary GPU-to-CPU image transfer overhead.

Fire growth is intentionally slower than the upstream demo. Wind still evolves and fire can still propagate, but the supervisor caps active fires and increases burn duration so the mission tests navigation and extinguishing rather than simulator overload.

## Key Files

- `worlds/forest_firefighters.wbt`: four-drone world layout and overlay devices.
- `controllers/autonomous_mavic/autonomous_mavic.py`: drone patrol, perception, fire approach, water drop, and overlay drawing.
- `controllers/fire/fire.py`: wildfire supervisor, wind model, propagation, and extinction logic.
- `controllers/spot/spot.py`: continuous Spot behavior and keyboard water burst.
- `tools/preflight_check.py`: structural validation before running Webots.
- `tools/run_mission_test.sh`: repeatable timed mission runner.

## Verification Workflow

Run these before a demo or submission:

```bash
python3 tools/preflight_check.py
python3 -m py_compile controllers/autonomous_mavic/autonomous_mavic.py controllers/fire/fire.py controllers/spot/spot.py tools/*.py
./tools/run_mission_test.sh stability_repeat_01
python3 tools/summarize_runs.py
```

Manual checks in Webots:

- Four drones launch from separate quadrants.
- The Spot controller remains running.
- Tree boxes appear in green on drone overlays.
- Fire/smoke detection draws red boxes or flashes the overlay red.
- Water drops are logged when a drone centers on a detected fire.
- The simulator runs for the target 5-8 minute assignment window without a Webots segmentation fault.

## References Used

- Webots Camera reference: camera overlays, recognition frames, camera sampling, and BGRA image format.
- Webots Display reference: attaching a camera to a display and drawing rectangles/text over the feed.
- Webots Recognition reference: recognition colors, bounding boxes, and performance tradeoffs.
