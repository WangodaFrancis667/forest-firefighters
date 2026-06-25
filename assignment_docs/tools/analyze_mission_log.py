from pathlib import Path
import runpy

ROOT_TOOL = Path(__file__).resolve().parents[2] / "tools" / "analyze_mission_log.py"
runpy.run_path(str(ROOT_TOOL), run_name="__main__")
