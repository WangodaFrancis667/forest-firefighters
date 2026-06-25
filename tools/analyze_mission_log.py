from pathlib import Path
import re
import sys
from datetime import datetime

if len(sys.argv) < 2:
    print("Usage: python3 tools/analyze_mission_log.py <log_file>")
    sys.exit(1)

log_path = Path(sys.argv[1])

if not log_path.exists():
    print(f"ERROR: Log file not found: {log_path}")
    sys.exit(1)

lines = log_path.read_text(errors="ignore").splitlines()
text = "\n".join(lines)

mission_failure_patterns = [
    r"Traceback \(most recent call last\)",
    r"AttributeError:",
    r"RuntimeError:",
    r"ValueError:",
    r"WARNING:.*controller exited with status:\s*[1-9]",
    r"WARNING:.*controller crashed",
    r"WARNING:.*process crashed",
]

shutdown_artifact_patterns = [
    r"zygote",
    r"Network service crashed",
    r"QXcbConnection",
    r"GetTerminationStatus",
    r"Terminating",
    r"Terminated",
]

def matches_any(line, patterns):
    return any(re.search(pattern, line, flags=re.IGNORECASE) for pattern in patterns)

controller_starts = len(re.findall(r"Starting controller", text, flags=re.IGNORECASE))
wildfires_started = len(re.findall(r"Starting wildfire", text, flags=re.IGNORECASE))
fire_detections = len(re.findall(r"fire detected", text, flags=re.IGNORECASE))
water_drops = len(re.findall(r"Water dropped", text, flags=re.IGNORECASE))
targets_reached = len(re.findall(r"Target reached", text, flags=re.IGNORECASE))

raw_error_lines = [
    line for line in lines
    if re.search(r"\bERROR\b", line, flags=re.IGNORECASE)
    or matches_any(line, mission_failure_patterns)
]

raw_crash_lines = [
    line for line in lines
    if re.search(r"crashed", line, flags=re.IGNORECASE)
]

shutdown_artifact_lines = [
    line for line in raw_error_lines + raw_crash_lines
    if matches_any(line, shutdown_artifact_patterns)
]

mission_crash_lines = [
    line for line in raw_crash_lines
    if not matches_any(line, shutdown_artifact_patterns)
]

mission_error_lines = [
    line for line in raw_error_lines
    if not matches_any(line, shutdown_artifact_patterns)
]

water_drop_lines = [
    line for line in lines
    if "Water dropped" in line
]

detection_lines = [
    line for line in lines
    if "fire detected" in line.lower()
]

target_lines = [
    line for line in lines
    if "Target reached" in line
]

metrics = {
    "controller_starts": controller_starts,
    "wildfires_started": wildfires_started,
    "fire_detections": fire_detections,
    "water_drops": water_drops,
    "targets_reached": targets_reached,
    "mission_errors": len(mission_error_lines),
    "mission_crashes": len(mission_crash_lines),
    "shutdown_artifacts": len(shutdown_artifact_lines),
}

output_path = log_path.with_suffix(".analysis.md")

with output_path.open("w") as f:
    f.write("# Mission Log Analysis\n\n")
    f.write(f"Generated: {datetime.now()}\n\n")
    f.write(f"Analyzed log: `{log_path}`\n\n")

    f.write("## Metrics\n\n")
    f.write("| Metric | Count |\n")
    f.write("|---|---:|\n")
    for key, value in metrics.items():
        f.write(f"| {key.replace('_', ' ').title()} | {value} |\n")

    f.write("\n## Water Drop Events\n\n")
    if water_drop_lines:
        for line in water_drop_lines:
            f.write(f"- {line}\n")
    else:
        f.write("- No water drop event found.\n")

    f.write("\n## First 10 Fire Detection Events\n\n")
    if detection_lines:
        for line in detection_lines[:10]:
            f.write(f"- {line}\n")
    else:
        f.write("- No fire detection event found.\n")

    f.write("\n## First 10 Target Navigation Events\n\n")
    if target_lines:
        for line in target_lines[:10]:
            f.write(f"- {line}\n")
    else:
        f.write("- No target navigation event found.\n")

    f.write("\n## Mission Error Lines\n\n")
    if mission_error_lines:
        for line in mission_error_lines:
            f.write(f"- {line}\n")
    else:
        f.write("- No mission error lines found.\n")

    f.write("\n## Mission Crash Lines\n\n")
    if mission_crash_lines:
        for line in mission_crash_lines:
            f.write(f"- {line}\n")
    else:
        f.write("- No mission crash lines found.\n")

    f.write("\n## Shutdown Artifacts\n\n")
    if shutdown_artifact_lines:
        for line in shutdown_artifact_lines:
            f.write(f"- {line}\n")
    else:
        f.write("- No shutdown artifacts found.\n")

print("Mission Log Analysis")
print("====================")
for key, value in metrics.items():
    print(f"{key}: {value}")

print(f"\nSaved analysis to: {output_path}")
