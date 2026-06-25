from pathlib import Path

path = Path("controllers/autonomous_mavic/autonomous_mavic.py")
text = path.read_text()

old = """        if fire_ratio > 0.15:  # Higher the fire ratio, higher the number of fire in the image

            # Detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
"""

new = """        if fire_ratio > 0.15:  # Higher the fire ratio, higher the number of fire in the image
            coord_fire = []

            # Detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
"""

if old not in text:
    print("Patch marker not found. The controller may already be patched or has changed.")
else:
    text = text.replace(old, new, 1)
    path.write_text(text)
    print("Applied safe coord_fire initialization fix.")
