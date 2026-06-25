# Fire Simulation Bug Fix for 8-Drone Configuration

## Issue Summary
When running the 8-drone configuration, the fire simulation would crash shortly after starting. The drones would get their first target coordinates (indicating initial fire detection), but then both the fire controller and all autonomous_mavic controllers would crash.

## Root Cause
The fire controller (`controllers/fire/fire.py` line 292) was checking for an **exact match** on the drone name:

```python
if not start_fire_now and robot.name == "Mavic 2 PRO" and robot.altitude() > 40:
    start_fire_now = True
```

However, the 8 drones in the world file are named:
- `"Mavic 2 PRO(1)"`
- `"Mavic 2 PRO(2)"`
- ... through `"Mavic 2 PRO(8)"`

Since **no drone has the exact name** `"Mavic 2 PRO"`, the condition `start_fire_now` would **never be set to True**. This meant:

1. Initial fire ignition happens (one random tree is ignited)
2. Drones detect the fire and get target coordinates
3. Fire simulation loop never runs properly (because `start_fire_now == False`)
4. Fire objects don't burn, don't propagate, don't update
5. Fire controller crashes when trying to manage unmaintained fire/smoke objects
6. Cascading crash of all drone controllers

## Solution
Changed the condition to use **string prefix matching** instead of exact equality:

```python
if not start_fire_now and robot.name.startswith("Mavic 2 PRO") and robot.altitude() > 40:
    start_fire_now = True
```

This allows the fire simulation to start when **any** of the 8 drones reaches altitude > 40, regardless of its numeric suffix.

## Files Modified
- `controllers/fire/fire.py` (line 292)

## Testing
After this fix:
- All 8 drones should spawn and take off correctly
- When the first drone reaches altitude > 40, the fire simulation will start
- Fire will burn, spread, and drones will detect multiple targets
- Water drops should suppress fires
- No more controller crashes

## Backup
Original fire controller backed up to: `assignment_docs/backups/fire_before_8drone_fix.py`
