from pathlib import Path
import re
import sys


WORLD_PATH = Path("worlds/forest_firefighters.wbt")
EXPECTED_POSITIONS = {
    1: (4.0, 4.0, 17.40, "SW"),
    2: (2.0, 26.0, 18.82, "NW"),
    3: (26.0, 3.0, 15.25, "SE"),
    4: (28.0, 26.0, 19.34, "NE"),
}
POSITION_TOLERANCE = 0.12


def fail(message):
    print(f"ERROR: {message}")
    return message


if not WORLD_PATH.exists():
    print(f"ERROR: {WORLD_PATH} not found.")
    sys.exit(1)

text = WORLD_PATH.read_text()
errors = []
warnings = []

mavic_blocks = re.findall(r"Mavic2Pro\s*{.*?^}", text, flags=re.DOTALL | re.MULTILINE)

if len(mavic_blocks) != 4:
    errors.append(fail(f"Expected 4 Mavic2Pro drones, found {len(mavic_blocks)}."))

for index, block in enumerate(mavic_blocks, start=1):
    translation = re.search(r"translation\s+([0-9.\-]+)\s+([0-9.\-]+)\s+([0-9.\-]+)", block)
    controller = re.search(r'controller\s+"([^"]+)"', block)
    patrol_coords = re.search(r'--patrol_coords=([^"]+)', block)
    target_altitude = re.search(r'--target_altitude=([0-9.\-]+)', block)

    if not translation:
        errors.append(fail(f"Mavic {index}: missing translation."))
    elif index in EXPECTED_POSITIONS:
        x, y, z = map(float, translation.groups())
        exp_x, exp_y, exp_z, quadrant = EXPECTED_POSITIONS[index]
        print(f"Mavic {index} ({quadrant}) spawn: x={x}, y={y}, z={z}")
        if not (
            abs(x - exp_x) < POSITION_TOLERANCE
            and abs(y - exp_y) < POSITION_TOLERANCE
            and abs(z - exp_z) < POSITION_TOLERANCE
        ):
            warnings.append(
                f"Mavic {index}: spawn ({x}, {y}, {z}) differs from expected ({exp_x}, {exp_y}, {exp_z})."
            )

    if not controller:
        errors.append(fail(f"Mavic {index}: missing controller."))
    elif controller.group(1) != "autonomous_mavic":
        errors.append(fail(f"Mavic {index}: expected autonomous_mavic, found {controller.group(1)}."))

    if not patrol_coords:
        errors.append(fail(f"Mavic {index}: missing --patrol_coords argument."))
    if not target_altitude:
        errors.append(fail(f"Mavic {index}: missing --target_altitude argument."))
    elif float(target_altitude.group(1)) < 40:
        errors.append(fail(f"Mavic {index}: target altitude must be at least 40 m to start the wildfire."))

    if 'Display {' not in block or 'name "vision overlay"' not in block:
        errors.append(fail(f"Mavic {index}: missing vision overlay Display."))
    if "width 160" not in block or "height 160" not in block:
        errors.append(fail(f"Mavic {index}: camera/display should be 160x160 for the RTX A1000 profile."))
    if "recognition Recognition" not in block:
        errors.append(fail(f"Mavic {index}: missing camera Recognition node for tree boxes."))

if "--patrol_coord=" in text:
    errors.append(fail("Found old typo --patrol_coord=. Use --patrol_coords= instead."))

if 'controller "fire"' not in text:
    errors.append(fail("Fire supervisor controller not found."))

if 'controller "spot"' not in text:
    errors.append(fail("Spot controller not found."))

if errors:
    print("\nPREFLIGHT FAILED")
    sys.exit(1)

print("\nPREFLIGHT PASSED")
print("- 4 autonomous drones configured across SW, NW, SE, and NE quadrants")
print("- Each drone has patrol coordinates, 160x160 camera, recognition, and vision overlay")
print("- Fire supervisor and Spot controller are present")

if warnings:
    print("\nWarnings:")
    for warning in warnings:
        print("WARNING:", warning)
