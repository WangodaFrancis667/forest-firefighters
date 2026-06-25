# Mission Log Analysis

Generated: 2026-06-25 10:32:53.533219

Analyzed log: `assignment_docs/results/live_demo_four_drone.log`

## Metrics

| Metric | Count |
|---|---:|
| Controller Starts | 6 |
| Wildfires Started | 1 |
| Fire Detections | 32 |
| Water Drops | 1 |
| Targets Reached | 8 |
| Mission Errors | 12 |
| Mission Crashes | 12 |
| Shutdown Artifacts | 4 |

## Water Drop Events

- Water dropped on fire target: [16.0, 16.0] at position [17.461724596647258, 16.735753873207127]

## First 10 Fire Detection Events

- fire detected, coordinates (128.0, 34.0)
- fire detected, coordinates (17.0, 15.0)
- fire detected, coordinates (7.3913044929504395, 36.41304397583008)
- fire detected, coordinates (18.326086044311523, 141.8913116455078)
- fire detected, coordinates (29.0, 152.5)
- fire detected, coordinates (111.0, 157.5)
- fire detected, coordinates (43.326087951660156, 151.8913116455078)
- fire detected, coordinates (32.5, 148.0)
- fire detected, coordinates (32.625, 146.125)
- fire detected, coordinates (35.343135833740234, 144.9509735107422)

## First 10 Target Navigation Events

- Target reached! New target:  [14.0, 5.0]
- Target reached! New target:  [14.0, 16.0]
- Target reached! New target:  [27.0, 16.0]
- Target reached! New target:  [27.0, 5.0]
- Target reached! New target:  [14.0, 14.0]
- Target reached! New target:  [14.0, 27.0]
- Target reached! New target:  [5.0, 14.0]
- Target reached! New target:  [27.0, 14.0]

## Mission Error Lines

- WARNING: fire: The process crashed some time after starting successfully.
- WARNING: 'fire' controller crashed.
- WARNING: spot: The process crashed some time after starting successfully.
- WARNING: 'spot' controller crashed.
- WARNING: autonomous_mavic: The process crashed some time after starting successfully.
- WARNING: 'autonomous_mavic' controller crashed.
- WARNING: autonomous_mavic: The process crashed some time after starting successfully.
- WARNING: 'autonomous_mavic' controller crashed.
- WARNING: autonomous_mavic: The process crashed some time after starting successfully.
- WARNING: 'autonomous_mavic' controller crashed.
- WARNING: autonomous_mavic: The process crashed some time after starting successfully.
- WARNING: 'autonomous_mavic' controller crashed.

## Mission Crash Lines

- WARNING: fire: The process crashed some time after starting successfully.
- WARNING: 'fire' controller crashed.
- WARNING: spot: The process crashed some time after starting successfully.
- WARNING: 'spot' controller crashed.
- WARNING: autonomous_mavic: The process crashed some time after starting successfully.
- WARNING: 'autonomous_mavic' controller crashed.
- WARNING: autonomous_mavic: The process crashed some time after starting successfully.
- WARNING: 'autonomous_mavic' controller crashed.
- WARNING: autonomous_mavic: The process crashed some time after starting successfully.
- WARNING: 'autonomous_mavic' controller crashed.
- WARNING: autonomous_mavic: The process crashed some time after starting successfully.
- WARNING: 'autonomous_mavic' controller crashed.

## Shutdown Artifacts

- [1782:1782:0625/103234.408189:ERROR:network_service_instance_impl.cc(262)] Network service crashed, restarting service.
- [1782:1782:0625/103234.892624:ERROR:zygote_communication_linux.cc(281)] Failed to send GetTerminationStatus message to zygote
- Warning: QXcbConnection: XCB error: 3 (BadWindow), sequence: 61036, resource id: 2097350, major code: 40 (TranslateCoords), minor code: 0
- [1782:1782:0625/103234.408189:ERROR:network_service_instance_impl.cc(262)] Network service crashed, restarting service.
