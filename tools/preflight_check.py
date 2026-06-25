from pathlib import Path
import re
import sys

world_path = Path("worlds/forest_firefighters.wbt")
expected_positions = {
    1: (4.0, 4.0, 17.40, "SW"),
    2: (2.0, 26.0, 18.82, "NW"),
    3: (26.0, 3.0, 15.25, "SE"),
    4: (28.0, 26.0, 19.34, "NE"),
}
expected_patrols = {
    1: "6 6, 14 8, 14 14, 8 14, 10 10",
    2: "6 24, 14 22, 14 16, 8 16, 10 20",
    3: "24 6, 16 8, 16 14, 24 14, 20 10",
    4: "24 24, 16 22, 16 16, 24 16, 20 20",
}
position_tolerance = 0.15

if not world_path.exists():
    print("ERROR: worlds/forest_firefighters.wbt not found.")
    sys.exit(1)

text = world_path.read_text()

errors = []
warnings = []

mavic_blocks = re.findall(r"Mavic2Pro\s*{.*?^\}", text, flags=re.DOTALL | re.MULTILINE)

if len(mavic_blocks) != 4:
    errors.append(f"Expected 4 Mavic2Pro drones, found {len(mavic_blocks)}.")

for index, block in enumerate(mavic_blocks, start=1):
    translation = re.search(r"translation\s+([0-9.\-]+)\s+([0-9.\-]+)\s+([0-9.\-]+)", block)
    controller = re.search(r'controller\s+"([^"]+)"', block)

    if not translation:
        errors.append(f"Mavic {index}: missing translation.")
    else:
        x, y, z = map(float, translation.groups())
        exp_x, exp_y, exp_z, quadrant = expected_positions.get(index, (x, y, z, "unknown"))
        print(f"Mavic {index} ({quadrant}) spawn translation: x={x}, y={y}, z={z}")
        if (
            abs(x - exp_x) > position_tolerance
            or abs(y - exp_y) > position_tolerance
            or abs(z - exp_z) > position_tolerance
        ):
            warnings.append(
                f"Mavic {index}: spawn position differs from expected {quadrant} position "
                f"{exp_x} {exp_y} {exp_z}."
            )

    if not controller:
        errors.append(f"Mavic {index}: missing controller.")
    elif controller.group(1) != "autonomous_mavic":
        errors.append(f"Mavic {index}: expected controller autonomous_mavic, found {controller.group(1)}.")

    expected_patrol = expected_patrols.get(index)
    if "--patrol_coords=" not in block:
        errors.append(f"Mavic {index}: missing --patrol_coords argument.")
    elif expected_patrol and f"--patrol_coords={expected_patrol}" not in block:
        errors.append(
            f"Mavic {index}: expected interior patrol route '{expected_patrol}' "
            "so the central forest is covered."
        )
    if "--target_altitude=" not in block:
        errors.append(f"Mavic {index}: missing --target_altitude argument.")
    if "--detection_interval=0.5" not in block:
        errors.append(f"Mavic {index}: expected --detection_interval=0.5 for faster fire response.")
    if 'Display {' not in block or 'name "vision overlay"' not in block:
        errors.append(f"Mavic {index}: missing vision overlay Display for status bar.")
    if "width 160" not in block or "height 160" not in block:
        errors.append(f"Mavic {index}: camera/display should be 160x160 for the RTX A1000 profile.")

if "--patrol_coord=" in text:
    errors.append("Found old typo --patrol_coord=. Use --patrol_coords= instead.")

if "--patrol_coords=" not in text:
    errors.append("No --patrol_coords argument found.")

if 'controller "spot"' not in text:
    warnings.append("Spot controller not found. This may be okay if only drones are assessed.")

if 'controller "fire"' not in text:
    errors.append("Fire supervisor controller not found.")
if "--start_delay=40" not in text:
    errors.append("Fire supervisor must use --start_delay=40 so wildfire starts after 40 seconds.")
if "--mission_duration=300" not in text:
    errors.append("Fire supervisor must use --mission_duration=300 for clean batch-test shutdown.")

if errors:
    print("\nPREFLIGHT FAILED")
    for error in errors:
        print("ERROR:", error)
    sys.exit(1)

print("\nPREFLIGHT PASSED")
print("Four drones are configured for interior quadrant patrol with autonomous_mavic controllers and status-bar overlays.")

if warnings:
    print("\nWarnings:")
    for warning in warnings:
        print("WARNING:", warning)
