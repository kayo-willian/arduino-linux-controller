"""Verify host event routing with mocked desktop commands."""
import unittest
from unittest.mock import Mock, patch
from test_host import load_host


class EventTests(unittest.TestCase):
    def setUp(self):
        self.host = load_host()
        self.command = Mock(return_value="")
        self.host["command"] = self.command

    def event(self, name):
        with patch("builtins.print"):
            self.host["execute_event"](name)

    def test_play_pause(self):
        self.event("PLAY_PAUSE")
        self.command.assert_called_once_with("playerctl", "--player=spotify,firefox", "play-pause")

    def test_next(self):
        self.event("NEXT")
        self.command.assert_called_once_with("playerctl", "--player=spotify,firefox", "next")
