#!/usr/bin/env python3

import os
import glob
import time
import serial
import threading
import subprocess

network_status = "U"


def command(*args):
    try:
        result = subprocess.run(
            args, capture_output=True, text=True, timeout=8,
            env={**os.environ, "LC_ALL": "C"}
        )
        if result.returncode == 0:
            return result.stdout.strip()
        print(result.stderr.strip())
    except (OSError, subprocess.TimeoutExpired) as error:
        print(error)
    return None


def monitor_network():
    global network_status

    while True:
        state = command("nmcli", "-t", "-f", "STATE", "general")
        if state and state.startswith("connected"):
            connectivity = command("nmcli", "networking", "connectivity", "check")
            if connectivity == "full":
                network_status = "G"
            elif connectivity in ("limited", "portal", "none"):
                network_status = "Y"
            else:
                network_status = "U"
        elif state == "disconnected" or state == "asleep":
            network_status = "R"
        else:
            network_status = "U"
        time.sleep(15)


def execute_event(event):
    if event == "PLAY_PAUSE":
        command("playerctl", "--player=spotify,firefox", "play-pause")
    elif event == "NEXT":
        command("playerctl", "--player=spotify,firefox", "next")
    elif event == "PREVIOUS":
        command("playerctl", "--player=spotify,firefox", "previous")
    elif event == "MUTE":
        command("wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle")
    elif event == "LOCK":
        result = command(
            "gdbus", "call", "--session",
            "--dest", "org.gnome.ScreenSaver",
            "--object-path", "/org/gnome/ScreenSaver",
            "--method", "org.gnome.ScreenSaver.Lock"
        )
        if result is None:
            command("loginctl", "lock-session")
    elif event.startswith("VOLUME:"):
        try:
            volume = int(event.split(":", 1)[1])
            volume = max(0, min(100, volume))
            command("wpctl", "set-volume", "-l", "1.0",
                    "@DEFAULT_AUDIO_SINK@", f"{volume}%")
        except ValueError:
            pass
    print(event)


def find_arduino():
    ports = glob.glob("/dev/ttyACM*")
    ports += glob.glob("/dev/ttyUSB*")
    if len(ports) == 1:
        return ports[0]
    return None


threading.Thread(target=monitor_network, daemon=True).start()

while True:
    port = find_arduino()
    if not port:
        print("Aguardando Arduino...")
        time.sleep(3)
        continue

    try:
        with serial.Serial(port, 9600, timeout=0.2, write_timeout=1) as arduino:
            print(f"Arduino conectado: {port}")
            time.sleep(2)
            last_update = 0

            while True:
                now = time.monotonic()
                if now - last_update >= 2:
                    arduino.write(network_status.encode("ascii"))
                    last_update = now
                if arduino.in_waiting:
                    event = arduino.readline().decode("utf-8", errors="ignore").strip()
                    if event:
                        execute_event(event)
                time.sleep(0.02)
    except (serial.SerialException, OSError) as error:
        print(f"Arduino desconectado: {error}")
        time.sleep(3)
