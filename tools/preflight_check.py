from pathlib import Path
import re
import sys

world_path = Path("worlds/forest_firefighters.wbt")

if not world_path.exists():
    print("ERROR: worlds/forest_firefighters.wbt not found.")
    sys.exit(1)

text = world_path.read_text()

errors = []
warnings = []

mavic_blocks = re.findall(r"Mavic2Pro\s*{.*?^\}", text, flags=re.DOTALL | re.MULTILINE)

if len(mavic_blocks) != 2:
    errors.append(f"Expected 2 Mavic2Pro drones, found {len(mavic_blocks)}.")

for index, block in enumerate(mavic_blocks, start=1):
    translation = re.search(r"translation\s+([0-9.\-]+)\s+([0-9.\-]+)\s+([0-9.\-]+)", block)
    controller = re.search(r'controller\s+"([^"]+)"', block)

    if not translation:
        errors.append(f"Mavic {index}: missing translation.")
    else:
        x, y, z = map(float, translation.groups())
        print(f"Mavic {index} spawn translation: x={x}, y={y}, z={z}")

        # These are the stable base spawn heights observed in the working R2021b world.
        if index == 1 and not (abs(x - 4.0) < 0.05 and abs(y - 4.0) < 0.05 and abs(z - 17.4) < 0.1):
            warnings.append(f"Mavic {index}: spawn position differs from expected base position 4 4 17.4.")

        if index == 2 and not (abs(x - 4.0) < 0.05 and abs(y - 3.0) < 0.05 and abs(z - 17.43) < 0.1):
            warnings.append(f"Mavic {index}: spawn position differs from expected base position 4 3 17.43.")

    if not controller:
        errors.append(f"Mavic {index}: missing controller.")
    elif controller.group(1) != "autonomous_mavic":
        errors.append(f"Mavic {index}: expected controller autonomous_mavic, found {controller.group(1)}.")

if "--patrol_coord=" in text:
    errors.append("Found old typo --patrol_coord=. Use --patrol_coords= instead.")

if "--patrol_coords=" not in text:
    errors.append("No --patrol_coords argument found.")

if 'controller "spot"' not in text:
    warnings.append("Spot controller not found. This may be okay if only drones are assessed.")

if errors:
    print("\nPREFLIGHT FAILED")
    for error in errors:
        print("ERROR:", error)
    sys.exit(1)

print("\nPREFLIGHT PASSED")
print("Drones are configured to start from the stable base positions with autonomous_mavic controllers.")

if warnings:
    print("\nWarnings:")
    for warning in warnings:
        print("WARNING:", warning)
