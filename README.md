# Forest Firefighters Robotics Mission

![Webots](https://img.shields.io/badge/Webots-R2021b-blue.svg?style=for-the-badge)
![Fleet](https://img.shields.io/badge/Fleet-4_Drones_|_1_Spot-brightgreen.svg?style=for-the-badge)
![GPU Profile](https://img.shields.io/badge/GPU-RTX_A1000_6GB-orange.svg?style=for-the-badge)

This repository contains an autonomous forest firefighting robotics mission built within the Webots R2021b environment. The final system employs a fleet of four Mavic 2 Pro drones for aerial search and response, alongside a Spot-like ground robot functioning as a stable support platform.

The primary objective of this project is to demonstrate robust autonomous behavior in a dynamic simulated environment, specifically tailored for a laptop equipped with an NVIDIA RTX A1000 6GB GPU. 

---

## 🎯 Mission Objectives

The robotic fleet is designed to autonomously:
- **Patrol** a simulated forest environment divided into quadrants.
- **Detect** smoke and active fire using onboard downward-facing cameras.
- **Navigate** directly toward the detected fire source.
- **Extinguish** the active fire by dropping water accurately.
- **Resume Patrol** while the simulation continues to run wind and fire propagation dynamics.
- **Log and Analyze** mission data to prove successful execution without crashes.

**Mission Loop:**
`Preflight` ➔ `Take Off` ➔ `Patrol` ➔ `Detect Fire` ➔ `Approach` ➔ `Drop Water` ➔ `Resume Patrol`

---

## 📁 Repository Structure

Understanding the codebase is straightforward. The repository is organized into specific domains:

```text
.
├── controllers/               # Core logic for the robots and environment
│   ├── autonomous_mavic/      # Logic for the 4 drones (patrol, OpenCV detection, water-drop)
│   ├── fire/                  # Wildfire supervisor (propagation, extinction, timed shutdown)
│   ├── mavic/                 # Manual/example Mavic controller
│   └── spot/                  # Ground robot posture and manual water burst (keyboard 'D')
├── protos/                    # Simulation assets (Fire, smoke, water, trees, terrain)
├── worlds/                    # Webots simulation world files
│   └── forest_firefighters.wbt
├── tools/                     # Scripts for validation, running, and analysis
│   ├── preflight_check.py     # Validates the active four-drone configuration
│   ├── run_mission_test.sh    # Runs Webots headlessly, captures logs, and analyzes output
│   ├── analyze_mission_log.py # Extracts mission metrics (detections, drops, errors)
│   └── summarize_runs.py      # Summarizes repeated mission evidence
├── assignment_docs/           # Project documentation, reports, and generated results
├── Dockerfile                 # Defines the Ubuntu 20.04 Webots R2021b environment
├── build.sh                   # Script to build the Docker image
└── run-gpu.sh                 # Script to launch the Docker container with GPU support
```

---

## ⚙️ System Architecture & Algorithms

### Aerial Fleet (Four Mavic Drones)
The project utilizes four drones to efficiently cover the entire forest. Each drone is assigned to a specific quadrant (NW, NE, SW, SE) and performs an **interior-biased patrol**. This ensures comprehensive coverage while minimizing computational load. 
- **Flight Stabilization:** Combines altitude error, roll, pitch, yaw, IMU, gyro, and GPS.
- **Fire Detection:** Downward cameras process frames using OpenCV HSV thresholding to detect bright, low-saturation smoke/fire pixels.
- **Targeting:** Once detected, the drone aligns the target to the center of its camera frame. Upon centering, it signals the `fire supervisor` via `customData` to deploy water.

### Ground Support (Spot Robot)
Acts as a stable ground unit. While the drones perform the primary autonomous mission, Spot provides a keyboard-triggered (`D`) water burst for auxiliary support.

### Environment Supervisor
The `fire.py` controller acts as the environment supervisor. It handles the delayed ignition of the wildfire (after 40 seconds), wind evolution, fire spread, and determines if a drone's water drop successfully extinguished nearby active fire.

---

## 🚀 Getting Started

Follow these steps to set up the environment using Docker and run the simulation. 

### 1. Build the Docker Image
To ensure a consistent environment, we use Docker. First, build the image that contains Webots R2021b and all necessary dependencies.

```bash
# Make sure the script is executable
chmod +x build.sh

# Build the Docker image (this will take a few minutes)
./build.sh
```

### 2. Start the GPU Container
Once built, run the container with GPU passthrough enabled:

```bash
chmod +x run-gpu.sh
./run-gpu.sh
```
*This script will mount your current directory into the container's `/workspace` folder and start an interactive bash session.*

### 3. Navigate the Workspace
Inside the Docker container, navigate to the project root:

```bash
cd /workspace
```

### 4. Validate the Configuration
Before running a mission, ensure the environment is correctly configured:

```bash
python3 tools/preflight_check.py
```
**Expected Output:**
> `PREFLIGHT PASSED`
> `Four drones are configured for interior quadrant patrol with autonomous_mavic controllers...`

### 5. Run an Interactive Mission
To view the simulation with the 3D GUI:

```bash
webots worlds/forest_firefighters.wbt
```
- Arrange the four drone camera overlays across your screen.
- Observe the **green top bar** (Patrol Mode) and **red FIRE bar** (Detection Mode).
- Select the Spot robot and press `D` to manually fire a water burst.

### 6. Run an Automated Timed Test
To run a headless mission test and generate logs/analysis:

```bash
./tools/run_mission_test.sh live_demo_four_drone
```
This will output results in `assignment_docs/results/live_demo_four_drone.log` and the corresponding Markdown analysis file.

---

## 📊 Results Summary

The system is rigorously tested to ensure robustness. Across eight validation runs, the four-drone system achieved:

- **718** total fire detections
- **43** successful water drops
- **223** waypoint target transitions
- **0** Mission errors or crashes

You can summarize your own runs using the provided tools:
```bash
python3 tools/summarize_runs.py
```

---

## 📚 Report and Presentation

- **Final report PDF:** `assignment_docs/final_report/latex/firefighting_robotics_report.pdf`
- **Report source:** `assignment_docs/final_report/latex/firefighting_robotics_report.tex`
- **Presentation script:** `assignment_docs/presentation/final_presentation_script.md`
- **Results summary:** `assignment_docs/results/performance_results_summary.md`
- **Assignment brief:** `Robotics Q and A guiding questions.pdf`
