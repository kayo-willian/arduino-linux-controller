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
