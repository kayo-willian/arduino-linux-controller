"""Static checks for the firmware contract; not hardware validation."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "firmware/painel_ubuntu/painel_ubuntu.ino").read_text()


class FirmwareContractTests(unittest.TestCase):
    def test_pin_mapping(self):
        pins = dict(re.findall(r"const int (\w+) = (\w+);", SOURCE))
        self.assertEqual(pins, {
            "BTN_GREEN": "2", "BTN_YELLOW": "3", "BTN_RED": "4",
            "LED_GREEN": "8", "LED_RED": "9", "POT": "A0",
        })

    def test_input_pullups(self):
        for name in ("BTN_GREEN", "BTN_YELLOW", "BTN_RED"):
            self.assertIn(f"pinMode({name}, INPUT_PULLUP);", SOURCE)

    def test_button_timing_constants(self):
        values = dict(re.findall(r"const unsigned long (\w+) = (\d+);", SOURCE))
        self.assertEqual(values, {"DEBOUNCE": "35", "LONG_PRESS": "1000", "DOUBLE_CLICK": "350"})
