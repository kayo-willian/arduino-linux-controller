# Installation and usage

[Português (Brasil)](installation.pt-BR.md) · [Home](../README.md)

## 1. Prepare Ubuntu

The working environment used Ubuntu with GNOME, PipeWire/WirePlumber and NetworkManager. Install the additional dependencies:

```bash
sudo apt update
sudo apt install -y python3-serial playerctl wireplumber network-manager libglib2.0-bin
sudo usermod -aG dialout "$USER"
```

Log out and back in to apply the group membership. Do not run the host program with sudo: media, audio and screen locking need your desktop session. Check the tools using `command -v python3 playerctl wpctl nmcli gdbus loginctl`. The optional diagnostic tool `pactl` is provided by `pulseaudio-utils`; it is not needed at runtime.

## 2. Upload the firmware

Open [painel_ubuntu.ino](../firmware/painel_ubuntu/painel_ubuntu.ino) in Arduino IDE. Select Arduino Uno, the correct serial port (originally /dev/ttyUSB0) and upload. Close the Python process before uploading, then close the serial monitor and the IDE before running Python. Only one program should own the serial port.

The green and red LEDs light sequentially at startup. The red LED then blinks until the host provides its connectivity state.

## 3. Run the host program

From the repository root:

```bash
cp software/painel-ubuntu.py ~/painel-ubuntu.py
python3 -u ~/painel-ubuntu.py
```

Expected example output (actual port may differ):

```text
Arduino conectado: /dev/ttyUSB0
READY
PLAY_PAUSE
NEXT
PREVIOUS
MUTE
VOLUME:50
LOCK
```

READY may be missed during connection/reset; the host does not require it. The script automatically selects a port only if exactly one /dev/ttyUSB* or /dev/ttyACM* device is present. Disconnect unrelated serial devices or edit find_arduino for your setup. It retries connection after serial errors.

## 4. Functional checks

| Test | Expected |
| --- | --- |
| Open Spotify, tap green | Play/pause |
| Double tap green | Previous track |
| Hold green for 1 second | Next track |
| Tap yellow | Toggle mute |
| Turn potentiometer | Change system volume (0–100%) |
| Hold red for 1 second | Lock the session |
| Disconnect network (all active interfaces) | Red LED after connectivity refresh |
| Restore internet | Green LED |
| Stop Python with Ctrl+C | Red blinks after 7 seconds |

NetworkManager checks run approximately every 15 seconds, plus command runtime; the host sends its cached state every 2 seconds. Its result is not a guarantee that every website is reachable. The potentiometer only sends a new value after movement of at least two percentage points (or an endpoint); it does not force a volume change on startup.

## 5. Autostart on desktop login

Once manual tests pass, stop the foreground process with Ctrl+C. Run [enable-autostart.sh](../installation/enable-autostart.sh) from the repository root:

```bash
bash installation/enable-autostart.sh
```

This copies the supplied Python script to ~/painel-ubuntu.py and creates a per-user desktop autostart entry. It will launch at graphical login, not at system boot before login. Log out and in to test. Do not start another copy while the autostart instance is running.

## 6. Troubleshooting commands

Use these individually, only for the purpose described.

| Purpose | Command |
| --- | --- |
| Check running panel | `pgrep -af painel-ubuntu.py` |
| Stop panel before firmware upload | `pkill -f 'python3.*painel-ubuntu\.py'` |
| Inspect serial port owner | `sudo fuser -v /dev/ttyUSB0` |
| List media players | `playerctl --list-all` |
| Test Spotify | `playerctl --player=spotify play-pause` |
| Read audio volume | `wpctl get-volume @DEFAULT_AUDIO_SINK@` |
| Check connectivity | `nmcli networking connectivity check` |
| Disable future autostart | `rm ~/.config/autostart/painel-ubuntu.desktop` |

To start manually in the background after confirming no other instance is running:

```bash
nohup python3 -u ~/painel-ubuntu.py > ~/.painel-ubuntu.log 2>&1 &
```

To remove autostart, use the command in the table; it does not stop the current process. If the USB connector gets abnormally hot, disconnect it immediately and investigate before further use.

See the [development log](development.md) for the actual troubleshooting history.
