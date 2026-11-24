# TrafficAPP – Group 10 (PA1484)

A public transport departure board for Karlskrona, running on the LilyGO T4-S3 (ESP32-S3) with MicroPython and LVGL.

**Group:** Hasan Suleiman, Pontus Nordenfors, Ali Agha, Wassim Akkkash, Hazem Alesa

## Features

| Screen | What it does |
|---|---|
| Start | Project name, version, group number and member names (US1.1) |
| Departures | Up to 5 live departures with type, minutes left, time, line, destination and delay/cancelled (US1.2B), filtered by transport type. Updates automatically every 60 s (US4.1) |
| Settings | Transport type filter (US3.3), search and choose stop (US3.2C), set as default and restore default (US3.4, US3.5), manual reload (US4.2B), Wi-Fi and API status (US4.3), journey planner (US5.1–US5.3B) |

Swipe left and right to move between the screens (US2.1).

## Project structure (`project/`)

| File | Purpose |
|---|---|
| `main.py` | Starts the board, builds the three screens, connects to Wi-Fi and starts the 60 s refresh timer |
| `pages/start_screen.py` | Start screen and the Swedish fonts |
| `pages/departure_screen.py` | Departure table and filtering |
| `pages/setting_screen.py` | Settings, stop search and the journey planner |
| `trafiklab_api.py` | HTTP requests to Trafiklab Realtime (departures) and ResRobot (journeys) |
| `trafiklab_data.py` | Converts the API responses into rows and text for the screen |
| `fetch_data.py` | Connects the API to the screen and updates the API status |
| `stations.json` | Stops in Karlskrona (name and id) |
| `default_*.json`, `selected_*.json` | Saved default and current stop and filter |

## Secrets

Copy `project/secrets_example.py` to `project/secrets.py` and fill in `WIFI_SSID`, `WIFI_PASSWORD`, `API_KEY` (Trafiklab Realtime) and `RESROBOT_API_KEY` (Trafiklab ResRobot v2.1). `secrets.py` is excluded by `.gitignore` and must never be committed.

## Data source

Departure and journey data come from [Trafiklab](https://www.trafiklab.se) (Trafiklab Realtime APIs and ResRobot). The application shows this attribution on the departure screen and in the journey result (NF3).

## Quality assurance

See [TESTING.md](TESTING.md) for test levels, the test checklist and the code review process (NF5).

---

# ESP32-T4-S3-MicroPython-Template

Welcome to the lab using the ESP32-T4-S3 LilyGO!

This repository serves as a foundation for software engineering projects aimed at the ESP32 hardware.
This document will guide you through the setup process and help you prepare to work with your ESP32 hardware.

The supplied firmware already contains MicroPython and LVGL. You write Python;
you do not compile MicroPython, LVGL, or a GUI library.

---

# How to get started

The student workflow works on Windows, Linux, and macOS. The first PlatformIO
setup can take several minutes while tools are installed.

## PlatformIO

1. Install Visual Studio Code
   * Visit [Visual Studio Code's website](https://code.visualstudio.com/download) and download the latest version or use the package manager of your system.
   * Run `Visual Studio Code` and follow the steps.
2. Install the correct extension.
   * Head over to the extensions tab on your left.
   * Search for ["PlatformIO IDE"](https://marketplace.visualstudio.com/items?itemName=platformio.platformio-ide) and install it.


## Linux: serial port access

Windows and macOS need no extra setup. On Linux the board's serial port is
owned by a system group, so PlatformIO cannot open it until you grant access.
Install the PlatformIO udev rules once:

```bash
curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core/develop/platformio/assets/system/99-platformio-udev.rules \
  | sudo tee /etc/udev/rules.d/99-platformio-udev.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Then unplug and reconnect the board. If the port is still unreadable, add
yourself to the group that owns it (`ls -l /dev/ttyACM0` shows which):
`dialout` on Debian/Ubuntu, `uucp` on Arch.

```bash
sudo usermod -aG dialout $USER   # or uucp
```

Log out and back in for the group change to take effect.

## How to run the program

1. Open the locally cloned repository with Visual Studio Code
    * If the "Do you trust the authors of the files in this folder?" dialog appears, click on "Yes, I trust the authors"
2. Open up the file `project/main.py`
3. Connect your ESP32 to your computer via a USB cable.
4. Open the PlatformIO tab in the left sidebar, expand
   **Project Tasks > t4s3-micropython > Custom**, and run **Deploy complete
   project**. This flashes the MicroPython firmware and your Python files in
   one step, and is what the Upload button runs too.

Once the board has firmware on it, **Flash Python application** is faster for
everyday work: it writes only your `project/` files and leaves the firmware
alone.

![PlatformIO tasks for this project](./assets/screenshot.png)

---

# What to add where

Your code belongs in the `/project` folder. The only place you should add, change, or remove things from is the [**/project**](project/main.py) folder. Changing anything else might break the code and cause a lot of headaches for all involved parties.

## How to connect to Wi-Fi

The T4-S3 has built-in Wi-Fi, but it cannot connect to eduroam. Use another
network or a phone hotspot.

Add or modify the `project/secrets.py` file, then set the SSID
(network name) and password.

```python
WIFI_SSID      = "SSID"
WIFI_PASSWORD  = "PWD"
```

Never commit real credentials to GitHub. `project/secrets.py` is excluded by
the supplied `.gitignore`.

---

# Troubleshooting

## The screen still shows the old interface, and touch does nothing

The board is probably still in upload mode. Tap **RESET/RST once**. 
A retained image on the AMOLED does not mean the application is running.

## Upload cannot connect

1. Stop PlatformIO Monitor with `Ctrl+C`.
2. Disconnect and reconnect the USB cable if the port is locked.
3. Repeat the BOOT/RESET upload-mode sequence.
4. Start Upload again.

On Linux, `Permission denied` on `/dev/ttyACM0` means the udev rules above are
not installed.

## Upload stops at "Stub running... No serial data received"

The board flashes over the ESP32-S3's built-in USB port, where the baud rate is
virtual and cannot be renegotiated. Check that `upload_speed` in
`platformio.ini` is still `115200`; raising it produces exactly this error.

After a failed upload the board may not restart on its own. Press **RESET**
by hand before retrying.

## Upload fails with "Invalid head of packet"

This appears once a Python application is already running on the board: it
prints to the same USB port the uploader needs, and the automatic reset into
upload mode cannot interrupt it. Enter upload mode by hand instead.

1. Hold **BOOT**.
2. Tap **RESET**.
3. Release **BOOT**.
4. Start the upload task immediately.

The board stays in upload mode afterwards, so press **RESET** once when the
upload finishes to start your application.

Close PlatformIO Monitor first if it is running; anything else holding the
serial port causes the same error.

## The screen is black

Open PlatformIO Monitor after resetting. Startup errors are printed at 115200
baud and also stored as `/debug.log` on the device.


## LilyGo tutorial

Visit LilyGO [link](https://github.com/Xinyuan-LilyGO/LilyGo-AMOLED-Series)
