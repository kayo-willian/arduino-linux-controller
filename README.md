# Arduino Linux Controller

![Status](https://img.shields.io/badge/status-completed-238636?style=flat-square)
![Arduino](https://img.shields.io/badge/Arduino-Uno-00979D?style=flat-square&logo=arduino&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Ubuntu-E95420?style=flat-square&logo=ubuntu&logoColor=white)
![C++](https://img.shields.io/badge/C%2B%2B-firmware-00599C?style=flat-square&logo=cplusplus)
![Python](https://img.shields.io/badge/Python-host-3776AB?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

**English** | [Português (Brasil)](README.pt-BR.md)

A small physical desktop controller for Ubuntu, built from an unused Arduino Uno-compatible starter kit. I wanted something useful in everyday life rather than another unfinished lab. The final device controls music, system audio and screen locking, and displays the host's network connectivity through two LEDs.

![Finished controller](images/arduino-08.jpeg)

*Final build: three buttons, two LEDs and a B10K rotary potentiometer. The photograph is part of the local build record; see the [photo index](images/README.md).*

## Status

**Completed — functional personal prototype, 26 November 2026.** All main functions were reported working on the physical Ubuntu desktop. No active development, roadmap or maintenance commitment. This is not a security product, commercial peripheral or certified electrical design.

## Controls

| Control | Action |
| --- | --- |
| Green button: short / double / hold 1 s | Play/pause / previous track / next track |
| Yellow button: short | Toggle mute |
| Red button: hold 1 s | Lock the desktop |
| B10K potentiometer | Set system volume, 0–100% |
| Green LED | NetworkManager reports full internet connectivity |
| Red LED steady | No or limited internet, captive portal or disconnected network |
| Red LED blinking | Unknown status or host communication timeout |

## Architecture

```text
Buttons + potentiometer -> Arduino Uno (C++)
                              | USB serial 9600 baud
                              v
                          Python on Ubuntu
                 playerctl / wpctl / GNOME / nmcli
                              |
                       G / Y / R / U
                              v
                        Green / red LEDs
```

The Arduino does not connect to the network itself. The host checks connectivity and sends a one-character state. The Uno reads switches with internal pull-ups and reports button/volume events. The Python process runs in the logged-in user's session.

## Build and run

- [Hardware and wiring](docs/hardware.md): parts, electrical connections and assembly.
- [Installation and usage](docs/installation.md): dependencies, firmware upload, serial control and autostart.
- [Development log and troubleshooting](docs/development.md): actual failures, hypotheses, tests and limitations.
- [Photo index](images/README.md): initial attempts through final build.
- [Firmware (C++)](firmware/painel_ubuntu/painel_ubuntu.ino) and [host program (Python)](software/painel-ubuntu.py).

Tested environment: Ubuntu desktop, GNOME, an Uno-compatible SMD board detected as `/dev/ttyUSB0`, Arduino IDE, PySerial, Playerctl, PipeWire/WirePlumber and NetworkManager. Other Linux distributions, boards and players are not validated.

## Development approach

I assembled the circuit, changed the wiring, uploaded the firmware and tested the physical device. ChatGPT helped generate the C++ and Python code, troubleshoot errors and prepare the documentation. The published source reconstructs the working version from the development conversation; it is not a byte-for-byte export of my local files.

## License

[MIT](LICENSE).
