#!/usr/bin/env bash
set -euo pipefail

RUN_NAME="${1:-mission_run}"
PROJECT_ROOT="$(pwd)"
LOG_PATH="assignment_docs/results/${RUN_NAME}.log"

mkdir -p assignment_docs/results

# python3 assignment_docs/tools/preflight_check.py

rm -f "$LOG_PATH"

echo "Starting Webots mission test: $RUN_NAME"
echo "Log file: $LOG_PATH"

timeout 8m webots --stdout --stderr worlds/forest_firefighters.wbt \
  2>&1 | tee "$LOG_PATH" || true

python3 assignment_docs/tools/analyze_mission_log.py "$LOG_PATH"

echo "Mission test complete."
echo "Analysis file: assignment_docs/results/${RUN_NAME}.analysis.md"
