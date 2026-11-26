# Hardware and wiring

[Português (Brasil)](hardware.pt-BR.md) · [Home](../README.md)

## Parts

| Quantity | Component | Specification |
| --- | --- | --- |
| 1 | Arduino board | Uno-compatible SMD board, 5 V |
| 1 | Breadboard | 400 holes (30 numbered groups) |
| 3 | Momentary push buttons | Normally open, green/yellow/red caps |
| 1 | Green LED | Network connectivity indicator |
| 1 | Red LED | Network connectivity indicator |
| 2 | Resistors | 1 kΩ each, one per LED |
| 1 | Rotary potentiometer | B10K, 10 kΩ linear |
| As needed | Jumper wires | Male-to-male |
| 1 | USB cable | USB A–B, data and power |
| Optional | USB hub | Used in the original setup |

No battery, soldering, wireless module, sensors or yellow LED are required for the final circuit.

## Final pinout

| Part | Arduino connection | Other terminal |
| --- | --- | --- |
| Green button | D2 | GND |
| Yellow button | D3 | GND |
| Red button | D4 | GND |
| Green LED anode | D8 | Cathode → 1 kΩ → GND |
| Red LED anode | D9 | Cathode → 1 kΩ → GND |
| Potentiometer wiper (middle) | A0 | Outer terminals → 5V and GND |
| Common ground | Any GND | Both negative rails |

D10 is unused. The yellow button is still present; the yellow LED was removed. The potentiometer needs no external resistor. If clockwise rotation reduces volume, swap only its two outer wires with USB unplugged or invert the mapping in firmware.

## Assembly

1. Disconnect USB. Place the board on a rigid insulating surface; never directly on a metal case. The original board had an unresolved intermittent heating problem.
2. Turn the breadboard horizontally. Each numbered group of five holes is connected internally; the central gap isolates its two halves. Connect Arduino GND to a negative rail and bridge the two negative rails; confirm continuity if available. Do not connect the positive and negative rails.
3. Place the three buttons across the central gap, with enough space for their caps. Use two electrically distinct contacts per button (often opposite diagonal pins on a four-pin switch; verify with continuity or the switch pinout). One goes to its digital pin, the other to the common ground. No external pull-up resistor is needed.
4. Insert each LED with its legs in different numbered groups, on the same breadboard half. The longer leg is normally the anode; the flat edge identifies the cathode. Connect the anode to D8 or D9, the cathode to one end of its own 1 kΩ resistor, and the resistor's other end to GND. A resistor may be on either side of a series LED circuit.
5. Insert all three potentiometer legs into electrically separate groups. Connect the middle leg to A0 and the outer legs to 5V and GND. Do not force the spacing or allow the legs to touch.
6. Keep wires away from button caps and avoid crushing the wires routed under the breadboard. Check for shorts and exposed metal before connecting power.

```text
D2 ── switch ── GND
D3 ── switch ── GND
D4 ── switch ── GND

D8 ── LED green (+ to -) ── 1kΩ ── GND
D9 ── LED red   (+ to -) ── 1kΩ ── GND

5V ── [ potentiometer 10kΩ ] ── GND
                 |
              wiper A0
```

A 1 kΩ resistor was selected for modest indicator brightness; 200 Ω resistors were also available but not selected for the final instructions. Use the final pinout and electrical connections above as the wiring reference.

## Build photographs

![Button spacing trial](../images/arduino-02.jpeg)

![Early three-LED layout](../images/arduino-03.jpeg)

![Finished two-LED layout](../images/arduino-08.jpeg)

Earlier photos may show obsolete wiring, a third LED or reversed physical positions. The final pinout above is authoritative. Exact breadboard coordinates depend on component spacing.

If the USB socket heats abnormally or disconnects, unplug it immediately. A metal support or hub was suspected but no definitive electrical diagnosis was made. Do not leave a suspect device powered unattended.
