# Testing – TrafficAPP (Group 10)

This document describes how we test the application (NF5). Testing is done manually on the LilyGO T4-S3. The functions that do not need the display are also tested in the MicroPython REPL. Fill in **Actual result**, **Pass/Fail**, **Tester** and **Date** when a test is run. Leave a field empty until the test has actually been run.

## Test levels

| Level | What we test | How and when |
|---|---|---|
| **Unit** | One function at a time: `format_departures()`, `format_journey()`, `stop_search_text()`, filtering in `update_departures()` | Call the function with known input in the REPL (including empty or missing data) and compare the result with the expected one. Done by the developer when the function is finished. |
| **Integration** | Modules working together: Settings ↔ departure screen, API ↔ display, Wi-Fi ↔ API, saved JSON files ↔ start-up | Done when a feature is merged to `main`. |
| **System** | The whole application on the device against the acceptance criteria for each user story (US) and non-functional requirement (NF) in Project description v5 | Before each demo and before final delivery. All earlier passed tests are run again (regression testing). |

## Defects

Defects are written down as GitHub Issues with the steps needed to reproduce them. After a fix, the test that failed **and** all earlier passed system tests are run again.

---

## System test checklist (Project description v5)

| ID | Req. | Steps | Expected result | Actual result | Pass/Fail | Tester | Date |
|---|---|---|---|---|---|---|---|
| T1 | US1.1 | Start the device | Start screen shows "TrafficAPP", version, "Group 10" and all five member names | | | | |
| T2 | US1.2B | Swipe to the departure screen | Up to 5 live departures with type, minutes left, time, line, destination and delay/"Canc." | | | | |
| T3 | US1.2B | Compare the screen with Trafiklab's data for the same stop | Times, lines and destinations match | | | | |
| T4 | US2.1 | Swipe left and right from every screen | Each swipe opens the neighbouring screen. A tap does not change screen | | | | |
| T5 | US3.1 | Swipe to the settings screen | Settings screen is shown and its buttons respond | | | | |
| T6 | US3.2C | Choose stop → type "gras" → choose Karlskrona campus Gräsvik → Save | List is filtered while typing. The departure screen shows Gräsvik | | | | |
| T7 | US3.2C | Choose stop → type "xyz" → Save | "No matching stops". Nothing is saved and the app does not crash | | | | |
| T8 | US3.3 | Choose Bus, Train, Ferry and All in the dropdown | Only the chosen type is shown. "All" shows every type | | | | |
| T9 | US3.4 | Choose a stop and a filter → Set as default → restart the device | The same stop and filter are active after the restart | | | | |
| T10 | US3.5 | Change stop and filter → Restore Default | Stop and filter go back to the saved default and departures are reloaded | | | | |
| T11 | US4.1 | Wait 2–3 minutes on the departure screen with the serial monitor open | A new request is sent about every 60 s and the screen updates | | | | |
| T12 | US4.2B | Press Reload on the settings screen | A new request is sent and the departures are updated | | | | |
| T13 | US4.3 | Turn off the hotspot, wait 60 s, then turn it on | Settings shows "NO WIFI"/"API ERR", then "WIFI OK"/"API UP" again | | | | |
| T14 | US5.1 | Settings → Plan journey | The journey view opens with "1. Choose starting stop" | | | | |
| T15 | US5.2B | Search and choose a start stop → Next → search and choose a destination | Both searches filter the list. Choosing the same stop twice gives "Choose a different destination" | | | | |
| T16 | US5.3B | Karlskrona Centralstation → Karlskrona campus Gräsvik → Search | Shows the journey with the earliest arrival, departure time at each change and the arrival time | | | | |
| T17 | US5.3B | Search a journey with Wi-Fi turned off | "No Wi-Fi. Connect and try again." The app does not crash | | | | |
| T18 | NF3 | Look at the departure screen and the journey result | "Data: Trafiklab.se" and "Source: Trafiklab / ResRobot" are visible | | | | |
| T19 | NF4 | Compare `support/`, `platformio/`, `boards/` and `firmware/` with the original template | No differences | | | | |
| T20 | Error | Use a wrong API key in `secrets.py` | Settings shows "API ERR". The app does not crash | | | | |

## Unit test examples (REPL)

| ID | Function | Input | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|---|
| U1 | `stop_search_text` | `"Gräsvik"` | `"grasvik"` | | |
| U2 | `format_departures` | A departure without `delay` | No crash, delay shown as `0 m` | | |
| U3 | `format_departures` | A departure with `canceled: true` | Minutes `-`, delay `Canc.` | | |
| U4 | `format_journey` | `{"errorCode": "SVC_NO_RESULT"}` | `"No journey found."` | | |
| U5 | `format_journey` | Two trips, the second arrives earlier | The second trip is chosen | | |

## Code review

Every change is merged through a pull request that at least one other group member has reviewed. The reviewer checks the coding standard (NF1), comments (NF2) and that the skeleton files are unchanged (NF4).
