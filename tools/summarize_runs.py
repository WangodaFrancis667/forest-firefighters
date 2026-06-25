from pathlib import Path
import re

result_dir = Path("assignment_docs/results")
logs = sorted(result_dir.glob("stability_repeat_*.log"))

shutdown_patterns = [
    r"Mission duration reached",
    r"Requesting clean Webots shutdown",
    r"zygote",
    r"Network service crashed",
    r"QXcbConnection",
    r"GetTerminationStatus",
    r"Terminating",
    r"Terminated",
]

def is_shutdown_artifact(line):
    return any(re.search(pattern, line, flags=re.IGNORECASE) for pattern in shutdown_patterns)

def clean_shutdown_index(lines):
    for index, line in enumerate(lines):
        if is_shutdown_artifact(line):
            return index
    return None

print("# Performance Results Summary")
print()
print("| Run | Fire Detections | Water Drops | Targets Reached | Mission Errors | Mission Crashes | Shutdown Artifacts |")
print("|---|---:|---:|---:|---:|---:|---:|")

for log in logs:
    lines = log.read_text(errors="ignore").splitlines()
    text = "\n".join(lines)

    fire_detections = len(re.findall(r"fire detected", text, flags=re.IGNORECASE))
    water_drops = len(re.findall(r"Water dropped", text, flags=re.IGNORECASE))
    targets_reached = len(re.findall(r"Target reached", text, flags=re.IGNORECASE))

    raw_errors = [line for line in lines if re.search(r"\bERROR\b", line, flags=re.IGNORECASE)]
    raw_crashes = [
        (index, line) for index, line in enumerate(lines)
        if re.search(r"crashed|Segmentation fault", line, flags=re.IGNORECASE)
    ]
    shutdown_at = clean_shutdown_index(lines)

    shutdown_artifacts = [
        line for index, line in raw_crashes
        if is_shutdown_artifact(line) or (shutdown_at is not None and index >= shutdown_at)
    ]

    mission_errors = [
        line for line in raw_errors
        if not is_shutdown_artifact(line)
    ]

    mission_crashes = [
        line for index, line in raw_crashes
        if not is_shutdown_artifact(line) and not (shutdown_at is not None and index >= shutdown_at)
    ]

    print(
        f"| {log.stem} | {fire_detections} | {water_drops} | {targets_reached} | "
        f"{len(mission_errors)} | {len(mission_crashes)} | {len(shutdown_artifacts)} |"
    )
