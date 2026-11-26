"""Host-side unit tests without a connected Arduino.

Load only imports and function definitions to avoid the production script's
top-level network thread and serial loop. No real desktop commands are run.
"""
import ast
from pathlib import Path
import subprocess
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_host():
    source = ast.parse((ROOT / "software/painel-ubuntu.py").read_text())
    source.body = [
        node for node in source.body
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.Assign))
    ]
    namespace = {}
    with patch.dict(sys.modules, {"serial": types.ModuleType("serial")}):
        exec(compile(source, "painel-ubuntu.py", "exec"), namespace)
    return namespace


class HostTests(unittest.TestCase):
    def setUp(self):
        self.host = load_host()

    def test_command_success(self):
        with patch("subprocess.run", return_value=subprocess.CompletedProcess([], 0, "  ok\n", "")) as run:
            self.assertEqual(self.host["command"]("example"), "ok")
            self.assertEqual(run.call_args.args[0], ("example",))
            self.assertEqual(run.call_args.kwargs["timeout"], 8)
            self.assertEqual(run.call_args.kwargs["env"]["LC_ALL"], "C")
