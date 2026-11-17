# Acceptance and peer review

For [#7](https://github.com/Hasse24/PA1484-Grupp10/issues/7) prepare the cases below. For [#15](https://github.com/Hasse24/PA1484-Grupp10/issues/15) execute them on an identified build. On the T4-S3 use the README setup, working Wi-Fi and a Timetables key. Capture timestamped request outcomes and relevant response fields with a debugger or a temporary diagnostic build. Record how readings were taken and omit credentials. If evidence is unavailable, mark the case blocked. A fixture run and a live run get separate log entries.

| ID | Procedure | Pass condition |
|---|---|---|
| FR1.1 | Reset. Compare the first screen with the release and team roster. | Agreed project name and release version, Group 10, Hasan, Pontus, Ali, Wassim and Hazem with their full names. |
| FR1.2 | Select two different Karlskrona stops. Capture the response for each displayed refresh, including a delayed service if available. | Correct stop, destination, scheduled clock time and minutes to departure agree with the corresponding response. Record tested IDs and row count, including whether additional departures can be viewed. |
| FR2.1 | Follow the swipe procedure below. | Each gesture has the specified result, including taps and short drags. |
| FR3.1 | From Departures swipe to Settings, open Choose stop and return. | Settings and its controls are accessible. |
| FR3.2 | Compare selectable stops with the agreed Karlskrona list. Select a different stop, navigate away and back, then change it again. | All agreed stops are available. Heading and data follow the selected stop throughout the session. |
| FR3.3 | With known bus, train and ferry services, try Bus, Train, Ferry and All. Repeat a filter with no matching departures. | Each specific filter displays only the matching services. All restores the mixed list. No old rows remain when nothing matches. |
| FR3.4 | Select a non-default stop and filter, save as default and restart. | Both settings are active in Settings and Departures after boot. |
| FR3.5 | Save stop/filter A as defaults, switch to B, then press Restore Default. | Compare against the agreed restoration target in [#5](https://github.com/Hasse24/PA1484-Grupp10/issues/5). Record whether A or factory defaults were agreed before scoring. |
| FR4.1 | Observe five minutes with no touches. Record successive request times, stop IDs, responses and displayed rows. | A request runs every 60 seconds and the screen reflects each response, including when the timetable stays the same. |
| FR4.2 | From a fresh installation tap Reload before choosing any stop. Repeat after selecting another stop. | One new request per press for the active stop, followed by corresponding rows. First use requests Karlskrona C. |
| FR4.3 | Observe both status indicators in Settings. Disconnect Wi-Fi, reconnect, then refresh successfully. Also try an API failure while Wi-Fi remains connected. | Wi-Fi status tracks the connection. Live-data status distinguishes a failed fetch from success even with Wi-Fi connected. |
| NF1 | Review a PR against the coding guide, formatter output and review history. | Style and structure follow the guide, formatter passes for changed app/test files and one teammate reviews before merge. |
| NF2 | Follow README setup/use from a clean checkout. Inspect changed modules. | Documented steps reproduce the build and usage. Comments explain non-obvious implementation choices. |
| NF3 | Compare the on-screen credit and documentation with Trafiklab Timetables attribution guidance. | Data source is visible alongside departures. Docs identify the source, licence and transformations. |
| NF4 | Diff supplied skeleton paths against the original course distribution or verified baseline. Record its revision. | No supplied skeleton files changed. A PR diff alone proves only the scope of that PR. |
| NF5 | Trace one requirement through its PR, review, executed test, defect and retest where applicable. | The repository contains dated procedures, outcomes, actual review and links to remaining defects. |

## Swipe session with Ali (#1)

On the 600 × 450 display, begin in a clear area away from an open dropdown. Swipe left from Start to Departures, left to Settings, right to Departures and right to Start. Repeat from near interactive controls. At the two outer edges, swipe outward and confirm the active screen stays put. Tap, make a short accidental drag, and use the stop list normally. A completed swipe should move one screen exactly once. A tap should activate only its target and a short accidental movement should leave navigation unchanged. Record start/end screen, gesture, repetitions and failures. If calibration is needed, record the original setting, change one parameter, and repeat the same gestures on the same board.

## Levels and failure cases

- **Unit:** feed the departure formatter a fixture with scheduled 12:05, expected 12:09 and current time 12:00. Expect a planned time of 12:05 and a countdown of 9 minutes.
- **Integration:** use the desktop suite to drive the real reload/filter code from a station file and fixture API through to label values. An empty successful response must clear old rows.
- **System:** test the passenger journey on the board with the real network, screen, touch, reboot and saved settings. Repeat after losing Wi-Fi. Exercise an unavailable API, a missing field and an unexpected response using controlled inputs if the live service cannot reproduce them. Record expected behaviour before each run, including how a passenger recognises stale data and how recovery is shown.

## Run log

Copy one row per execution, including reruns. Use Not run, Blocked, Pass or Fail. Link a defect with reproducible steps for each failure and include the original and retest build IDs.

| ID / level | Build | Device or fixture | Tester / date | Expected | Actual | Status | Evidence / defect |
|---|---|---|---|---|---|---|---|
| | | | | | | Not run | |

## Peer review checklist

- [ ] Issue, scope, build and reviewer identified.
- [ ] Changed app files follow the coding guide; formatter command and result recorded.
- [ ] Required behaviour and failures have evidence; fixture, live and device results are labelled.
- [ ] Supplied files and private credentials checked; limitations and open defects linked.
- [ ] Teammate review outcome recorded before merge.
