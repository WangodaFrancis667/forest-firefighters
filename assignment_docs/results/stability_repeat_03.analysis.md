# Mission Log Analysis

Generated: 2026-06-14 18:35:19.976732

Analyzed log: `assignment_docs/results/stability_repeat_03.log`

## Metrics

| Metric | Count |
|---|---:|
| Controller Starts | 4 |
| Wildfires Started | 1 |
| Fire Detections | 59 |
| Water Drops | 5 |
| Targets Reached | 4 |
| Mission Errors | 0 |
| Mission Crashes | 6 |
| Shutdown Artifacts | 4 |

## Water Drop Events

- Water dropped on fire target: [11.0, 11.0] at position [8.339294765643812, 4.495973905664079]
- Water dropped on fire target: [21.0, 21.0] at position [23.098778302554514, 23.178661606554254]
- Water dropped on fire target: [11.0, 21.0] at position [15.978945502712138, 19.741697930418233]
- Water dropped on fire target: [11.0, 21.0] at position [8.132312156814006, 16.248175828088065]
- Water dropped on fire target: [11.0, 21.0] at position [20.429108372014927, 13.147723322075183]

## First 10 Fire Detection Events

- fire detected, coordinates (71.73213958740234, 86.10713958740234)
- fire detected, coordinates (72.45454406738281, 90.86363983154297)
- fire detected, coordinates (87.60526275634766, 85.86842346191406)
- fire detected, coordinates (75.92308044433594, 84.80769348144531)
- fire detected, coordinates (83.5, 78.30000305175781)
- fire detected, coordinates (90.67857360839844, 68.51786041259766)
- fire detected, coordinates (99.5, 0.5)
- fire detected, coordinates (99.0, 5.5)
- fire detected, coordinates (98.25242614746094, 14.388349533081055)
- fire detected, coordinates (97.94318389892578, 24.295454025268555)

## First 10 Target Navigation Events

- Target reached! New target:  [21.0, 11.0]
- Target reached! New target:  [21.0, 21.0]
- Target reached! New target:  [11.0, 21.0]
- Target reached! New target:  [11.0, 21.0]

## Mission Error Lines

- No mission error lines found.

## Mission Crash Lines

- WARNING: fire: The process crashed some time after starting successfully.
- WARNING: 'fire' controller crashed.
- WARNING: autonomous_mavic: The process crashed some time after starting successfully.
- WARNING: 'autonomous_mavic' controller crashed.
- WARNING: autonomous_mavic: The process crashed some time after starting successfully.
- WARNING: 'autonomous_mavic' controller crashed.

## Shutdown Artifacts

- [1067:1067:0614/183004.877947:ERROR:network_service_instance_impl.cc(262)] Network service crashed, restarting service.
- [1067:1067:0614/183004.936519:ERROR:zygote_communication_linux.cc(281)] Failed to send GetTerminationStatus message to zygote
- Warning: QXcbConnection: XCB error: 3 (BadWindow), sequence: 49402, resource id: 2097312, major code: 40 (TranslateCoords), minor code: 0
- [1067:1067:0614/183004.877947:ERROR:network_service_instance_impl.cc(262)] Network service crashed, restarting service.
