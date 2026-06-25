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

# Expected spawn positions for 6 drones at 4 corners (2 drones per corner, excluding NE corner)
EXPECTED_POSITIONS = {
    1: (4.0, 4.0, 17.40),      # SW corner pair - Drone 1
    2: (4.0, 3.0, 17.43),      # SW corner pair - Drone 2
    3: (2.0, 24.0, 17.92),     # NW corner pair - Drone 3
    4: (2.0, 26.0, 18.82),     # NW corner pair - Drone 4
    5: (26.0, 3.0, 15.25),     # SE corner pair - Drone 5
    6: (28.0, 3.0, 16.33),     # SE corner pair - Drone 6
}

POSITION_TOLERANCE = 0.1  # meters

mavic_blocks = re.findall(r"Mavic2Pro\s*{.*?^\}", text, flags=re.DOTALL | re.MULTILINE)

if len(mavic_blocks) != 6:
    errors.append(f"Expected 6 Mavic2Pro drones, found {len(mavic_blocks)}.")

for index, block in enumerate(mavic_blocks, start=1):
    translation = re.search(r"translation\s+([0-9.\-]+)\s+([0-9.\-]+)\s+([0-9.\-]+)", block)
    controller = re.search(r'controller\s+"([^"]+)"', block)
    patrol_coords = re.search(r'--patrol_coords=([^"]+)', block)

    if not translation:
        errors.append(f"Mavic {index}: missing translation.")
    else:
        x, y, z = map(float, translation.groups())
        print(f"Mavic {index} spawn translation: x={x}, y={y}, z={z}")

        # Validate against expected positions
        if index in EXPECTED_POSITIONS:
            exp_x, exp_y, exp_z = EXPECTED_POSITIONS[index]
            if not (abs(x - exp_x) < POSITION_TOLERANCE and 
                    abs(y - exp_y) < POSITION_TOLERANCE and 
                    abs(z - exp_z) < POSITION_TOLERANCE):
                warnings.append(f"Mavic {index}: spawn position ({x}, {y}, {z}) differs from expected ({exp_x}, {exp_y}, {exp_z}).")

    if not controller:
        errors.append(f"Mavic {index}: missing controller.")
    elif controller.group(1) != "autonomous_mavic":
        errors.append(f"Mavic {index}: expected controller autonomous_mavic, found {controller.group(1)}.")

    if not patrol_coords:
        errors.append(f"Mavic {index}: missing --patrol_coords argument.")

if "--patrol_coord=" in text:
    errors.append("Found old typo --patrol_coord=. Use --patrol_coords= instead.")

if 'controller "fire"' not in text:
    errors.append("Fire supervisor controller not found.")

if errors:
    print("\nPREFLIGHT FAILED")
    for error in errors:
        print("ERROR:", error)
    sys.exit(1)

print("\nPREFLIGHT PASSED")
print("✓ All 6 drones are configured correctly")
print("✓ Each drone has autonomous_mavic controller")
print("✓ Each drone has patrol_coords defined")
print("✓ Fire supervisor controller is present")
print("\nDrone Configuration Summary:")
for idx, (exp_x, exp_y, exp_z) in EXPECTED_POSITIONS.items():
    corner = ""
    if idx <= 2:
        corner = "SW Corner"
    elif idx <= 4:
        corner = "NW Corner"
    elif idx <= 6:
        corner = "SE Corner"
    else:
        corner = "NE Corner"
    print(f"  Drone {idx} ({corner}): spawn at ({exp_x}, {exp_y}, {exp_z})")

if warnings:
    print("\nWarnings:")
    for warning in warnings:
        print("WARNING:", warning)
