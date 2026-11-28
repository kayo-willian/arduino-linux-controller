"""Host-side tests without a connected Arduino or real desktop commands."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import subprocess
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_host():
    spec = spec_from_file_location("painel_ubuntu", ROOT / "software/painel-ubuntu.py")
    module = module_from_spec(spec)
    with patch.dict(sys.modules, {"serial": types.ModuleType("serial")}):
        spec.loader.exec_module(module)
    return vars(module)


class HostTests(unittest.TestCase):
    def setUp(self):
        self.host = load_host()

    def test_command_success(self):
        with patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, "  ok\n", "")) as run:
            self.assertEqual(self.host["command"]("example"), "ok")
            self.assertEqual(run.call_args.args[0], ("example",))
            self.assertEqual(run.call_args.kwargs["timeout"], 8)
            self.assertEqual(run.call_args.kwargs["env"]["LC_ALL"], "C")

    def test_command_failures(self):
        cases = [
            {"return_value": subprocess.CompletedProcess([], 1, "", "failed")},
            {"side_effect": FileNotFoundError("missing")},
            {"side_effect": subprocess.TimeoutExpired("example", 8)},
        ]
        for case in cases:
            with self.subTest(case=case), patch("subprocess.run", **case), patch("builtins.print"):
                self.assertIsNone(self.host["command"]("example"))

    def test_serial_discovery(self):
        cases = [
            ([], [], None),
            (["/dev/ttyACM0"], [], "/dev/ttyACM0"),
            ([], ["/dev/ttyUSB0"], "/dev/ttyUSB0"),
            (["/dev/ttyACM0"], ["/dev/ttyUSB0"], None),
            ([], ["/dev/ttyUSB0", "/dev/ttyUSB1"], None),
        ]
        for acm, usb, expected in cases:
            with self.subTest(acm=acm, usb=usb), patch.object(self.host["glob"], "glob", side_effect=[acm.copy(), usb.copy()]):
                self.assertEqual(self.host["find_arduino"](), expected)
