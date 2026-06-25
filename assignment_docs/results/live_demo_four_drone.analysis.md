# Mission Log Analysis

Generated: 2026-06-25 09:19:43.042908

Analyzed log: `assignment_docs/results/live_demo_four_drone.log`

## Metrics

| Metric | Count |
|---|---:|
| Controller Starts | 6 |
| Wildfires Started | 1 |
| Fire Detections | 5 |
| Water Drops | 0 |
| Targets Reached | 7 |
| Mission Errors | 13 |
| Mission Crashes | 6 |
| Shutdown Artifacts | 4 |

## Water Drop Events

- No water drop event found.

## First 10 Fire Detection Events

- fire detected, coordinates (12.073770523071289, 114.82786560058594)
- fire detected, coordinates (35.39361572265625, 125.03191375732422)
- fire detected, coordinates (59.5, 147.1666717529297)
- fire detected, coordinates (83.0, 156.0)
- fire detected, coordinates (93.5, 158.5)

## First 10 Target Navigation Events

- Target reached! New target:  [14.0, 5.0]
- Target reached! New target:  [14.0, 16.0]
- Target reached! New target:  [27.0, 16.0]
- Target reached! New target:  [27.0, 5.0]
- Target reached! New target:  [14.0, 14.0]
- Target reached! New target:  [14.0, 27.0]
- Target reached! New target:  [5.0, 27.0]

## Mission Error Lines

- Traceback (most recent call last):
- WARNING: 'autonomous_mavic' controller exited with status: 1.
- Traceback (most recent call last):
- WARNING: 'autonomous_mavic' controller exited with status: 1.
- Traceback (most recent call last):
- ValueError: operands could not be broadcast together with shapes (0,) (2,) 
- WARNING: 'autonomous_mavic' controller exited with status: 1.
- WARNING: fire: The process crashed some time after starting successfully.
- WARNING: 'fire' controller crashed.
- WARNING: spot: The process crashed some time after starting successfully.
- WARNING: 'spot' controller crashed.
- WARNING: autonomous_mavic: The process crashed some time after starting successfully.
- WARNING: 'autonomous_mavic' controller crashed.

## Mission Crash Lines

- WARNING: fire: The process crashed some time after starting successfully.
- WARNING: 'fire' controller crashed.
- WARNING: spot: The process crashed some time after starting successfully.
- WARNING: 'spot' controller crashed.
- WARNING: autonomous_mavic: The process crashed some time after starting successfully.
- WARNING: 'autonomous_mavic' controller crashed.

## Shutdown Artifacts

- [1179:1179:0625/091830.099630:ERROR:network_service_instance_impl.cc(262)] Network service crashed, restarting service.
- [1179:1179:0625/091830.251836:ERROR:zygote_communication_linux.cc(281)] Failed to send GetTerminationStatus message to zygote
- Warning: QXcbConnection: XCB error: 3 (BadWindow), sequence: 13059, resource id: 2097305, major code: 40 (TranslateCoords), minor code: 0
- [1179:1179:0625/091830.099630:ERROR:network_service_instance_impl.cc(262)] Network service crashed, restarting service.
