"""Exercise the autostart helper in an isolated temporary HOME."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AutostartTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.target = self.home / "painel-ubuntu.py"
        self.desktop = self.home / ".config/autostart/painel-ubuntu.desktop"

    def run_helper(self):
        return subprocess.run(
            ["bash", str(ROOT / "installation/enable-autostart.sh")],
            env={**os.environ, "HOME": str(self.home)},
            capture_output=True, text=True, timeout=10,
        )

    def test_installation(self):
        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.target.read_bytes(), (ROOT / "software/painel-ubuntu.py").read_bytes())
        entry = self.desktop.read_text()
        self.assertIn("[Desktop Entry]", entry)
        self.assertIn(f'Exec=/usr/bin/python3 "{self.target}"', entry)
        self.assertIn("X-GNOME-Autostart-enabled=true", entry)
