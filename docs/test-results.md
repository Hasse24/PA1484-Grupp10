# TrafficAPP verification, 17 November 2026

Application revision **5bd97e9**, based on group main **8c9490f**. Tester: Codex on Wassim's Mac. Desktop Python ran the app logic with fixture API responses and stand-in label objects. The countdown fixture supplies the eight-field time interface used by MicroPython. No live credentials, real Trafiklab response or physical board were used in this run.

| Case | Expected | Observed | Result / evidence |
|---|---|---|---|
| First-use reload, FR4.2 | Missing station file falls back to Karlskrona C and displays the returned destination. | Base raised FileNotFoundError. The fix requested 740000230 and set the label to the fixture destination. | Pass on desktop, [#29](https://github.com/Hasse24/PA1484-Grupp10/issues/29). |
| Interrupted station save | Startup reload works with incomplete station JSON. | Requested default stop after reading truncated JSON. | Pass on desktop. |
| Station selection and filter, FR3.2/FR3.3 | Saved ID reaches API; All, Bus, Train and Ferry give the expected label values. | Saved ID and heading matched, each filter matched, unused rows cleared. | Pass with fixture API and label doubles. |
| Empty response | Previously displayed rows clear. | First populated destination label cleared after successful empty list. | Pass on desktop. |
| Failed fetch followed by recovery | Failed first fetch does not fabricate a successful update; a later success displays returned data. | No successful stop-label update on failure; next fixture response displayed Lund. | Pass on desktop. Physical connection indicators remain pending. |
| Delayed service, FR1.2 | For 12:05 scheduled and 12:09 predicted at 12:00, show 12:05 and 9 m. | Base showed 12:09 and 9 m; fixed output was 12:05 and 9 m. | Pass on desktop, [#30](https://github.com/Hasse24/PA1484-Grupp10/issues/30). |
| Formatting / package | Changed Python files pass Ruff 0.11.13; both FAT images contain the staged application. | Four changed Python files passed formatting. PlatformIO built the t4s3-micropython target with example credentials. mkfatfs printed a warning concerning /fatfs/pages. Independent read-only FAT inspection matched all 17 staged files byte-for-byte in both images, including all three page modules. | Pass for packaging. Boot and rendering pending. |

Reproduce with the commands in [the workflow guide](workflow.md). On the pre-fix revision, running the fresh-reload and delayed-service cases from the new suite reproduced the two defects. The final run passed all six tests. No supplied firmware, board definitions, support files or packaging sources changed relative to group main.

## Remaining checks for the team

- **Swipe navigation ([#1](https://github.com/Hasse24/PA1484-Grupp10/issues/1))**: source inspection shows three horizontal tiles, permitting right, left/right and left movement respectively. No board was available. Ali and Wassim should record taps, short drags, edge swipes and single-page transitions using the [swipe procedure](acceptance.md#swipe-session-with-ali-1). No physical calibration result is recorded.
- **System acceptance ([#15](https://github.com/Hasse24/PA1484-Grupp10/issues/15))**: run the complete checklist on the board. Verify real departures, reboot behaviour, credit visibility, network failure/recovery and the five-minute automatic-refresh log. At this revision the saved-default buttons have no action handlers, and source inspection found no periodic refresh or separate live-data status indicator. Track these under [#4](https://github.com/Hasse24/PA1484-Grupp10/issues/4), [#5](https://github.com/Hasse24/PA1484-Grupp10/issues/5) and [#6](https://github.com/Hasse24/PA1484-Grupp10/issues/6).
- **Documentation and review ([#16](https://github.com/Hasse24/PA1484-Grupp10/issues/16))**: record the teammate's actual review and append the device test log with the tested revision. The README links the repository's Projects page; confirm the team's specific Scrum board link with someone who has board access.
