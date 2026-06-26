from pathlib import Path
import re


RESULT_DIR = Path("assignment_docs/results")
EXCLUDED_RUNS = {"baseline_run"}
METRIC_KEYS = [
    "Controller Starts",
    "Wildfires Started",
    "Fire Detections",
    "Water Drops",
    "Targets Reached",
    "Mission Errors",
    "Mission Crashes",
    "Shutdown Artifacts",
]


def parse_analysis(path):
    metrics = {}
    for line in path.read_text(errors="ignore").splitlines():
        match = re.match(r"\| ([A-Za-z ]+) \| (\d+) \|", line)
        if match:
            metrics[match.group(1)] = int(match.group(2))
    return metrics


def run_name(path):
    return path.name.replace(".analysis.md", "")


analysis_files = [
    path for path in sorted(RESULT_DIR.glob("*.analysis.md"))
    if run_name(path) not in EXCLUDED_RUNS
]

print("# Performance Results Summary")
print()
print("| Run | Controller Starts | Wildfires Started | Fire Detections | Water Drops | Targets Reached | Mission Errors | Mission Crashes | Shutdown Artifacts |")
print("|---|---:|---:|---:|---:|---:|---:|---:|---:|")

totals = {key: 0 for key in METRIC_KEYS}
valid_runs = 0

for path in analysis_files:
    metrics = parse_analysis(path)
    if not metrics:
        continue
    valid_runs += 1
    for key in METRIC_KEYS:
        totals[key] += metrics.get(key, 0)
    print(
        f"| {run_name(path)} | "
        f"{metrics.get('Controller Starts', 0)} | "
        f"{metrics.get('Wildfires Started', 0)} | "
        f"{metrics.get('Fire Detections', 0)} | "
        f"{metrics.get('Water Drops', 0)} | "
        f"{metrics.get('Targets Reached', 0)} | "
        f"{metrics.get('Mission Errors', 0)} | "
        f"{metrics.get('Mission Crashes', 0)} | "
        f"{metrics.get('Shutdown Artifacts', 0)} |"
    )

print()
print("## Aggregate Final Metrics")
print()
print("| Metric | Value |")
print("|---|---:|")
print(f"| Final validation runs | {valid_runs} |")
print(f"| Total fire detections | {totals['Fire Detections']} |")
print(f"| Total water drops | {totals['Water Drops']} |")
print(f"| Total waypoint target transitions | {totals['Targets Reached']} |")
print(f"| Mission errors | {totals['Mission Errors']} |")
print(f"| Mission crashes | {totals['Mission Crashes']} |")
