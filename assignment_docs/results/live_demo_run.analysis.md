# Mission Log Analysis

Generated: 2026-06-14 19:00:45.016051

Analyzed log: `assignment_docs/results/live_demo_run.log`

## Metrics

| Metric | Count |
|---|---:|
| Controller Starts | 4 |
| Wildfires Started | 1 |
| Fire Detections | 43 |
| Water Drops | 3 |
| Targets Reached | 3 |
| Mission Errors | 0 |
| Mission Crashes | 4 |
| Shutdown Artifacts | 5 |

## Water Drop Events

- Water dropped on fire target: [11.0, 21.0] at position [12.499656471070061, 23.836628502740812]
- Water dropped on fire target: [11.0, 21.0] at position [7.4500547218162945, 17.650107887515766]
- Water dropped on fire target: [11.0, 21.0] at position [12.468371050888974, 18.447165352324674]

## First 10 Fire Detection Events

- fire detected, coordinates (128.5, 0.0)
- fire detected, coordinates (117.0, 1.5)
- fire detected, coordinates (102.5, 8.5)
- fire detected, coordinates (96.75, 19.75)
- fire detected, coordinates (94.5952377319336, 32.404762268066406)
- fire detected, coordinates (94.07691955566406, 45.07692337036133)
- fire detected, coordinates (93.53763580322266, 58.225807189941406)
- fire detected, coordinates (64.5, 46.79411697387695)
- fire detected, coordinates (96.50828552246094, 70.86187744140625)
- fire detected, coordinates (98.14974975585938, 83.17766571044922)

## First 10 Target Navigation Events

- Target reached! New target:  [21.0, 11.0]
- Target reached! New target:  [11.0, 21.0]
- Target reached! New target:  [21.0, 21.0]

## Mission Error Lines

- No mission error lines found.

## Mission Crash Lines

- WARNING: fire: The process crashed some time after starting successfully.
- WARNING: 'fire' controller crashed.
- WARNING: autonomous_mavic: The process crashed some time after starting successfully.
- WARNING: 'autonomous_mavic' controller crashed.

## Shutdown Artifacts

- [1314:1314:0614/185956.751844:ERROR:network_service_instance_impl.cc(262)] Network service crashed, restarting service.
- [1314:1314:0614/185956.788098:ERROR:zygote_communication_linux.cc(281)] Failed to send GetTerminationStatus message to zygote
- Warning: QXcbConnection: XCB error: 3 (BadWindow), sequence: 50012, resource id: 2097322, major code: 40 (TranslateCoords), minor code: 0
- Warning: QXcbConnection: XCB error: 3 (BadWindow), sequence: 50162, resource id: 2097324, major code: 40 (TranslateCoords), minor code: 0
- [1314:1314:0614/185956.751844:ERROR:network_service_instance_impl.cc(262)] Network service crashed, restarting service.
