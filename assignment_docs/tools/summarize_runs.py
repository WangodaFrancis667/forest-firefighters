from pathlib import Path
import re

result_dir = Path("assignment_docs/results")
logs = sorted(result_dir.glob("stability_repeat_*.log"))

shutdown_patterns = [
    r"zygote",
    r"Network service crashed",
    r"QXcbConnection",
    r"GetTerminationStatus",
    r"Terminating",
    r"Terminated",
]

def is_shutdown_artifact(line):
    return any(re.search(pattern, line, flags=re.IGNORECASE) for pattern in shutdown_patterns)

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
    raw_crashes = [line for line in lines if re.search(r"crashed", line, flags=re.IGNORECASE)]

    shutdown_artifacts = [
        line for line in raw_errors + raw_crashes
        if is_shutdown_artifact(line)
    ]

    mission_errors = [
        line for line in raw_errors
        if not is_shutdown_artifact(line)
    ]

    mission_crashes = [
        line for line in raw_crashes
        if not is_shutdown_artifact(line)
    ]

    print(
        f"| {log.stem} | {fire_detections} | {water_drops} | {targets_reached} | "
        f"{len(mission_errors)} | {len(mission_crashes)} | {len(shutdown_artifacts)} |"
    )
