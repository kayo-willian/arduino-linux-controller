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

    def test_previous(self):
        self.event("PREVIOUS")
        self.command.assert_called_once_with("playerctl", "--player=spotify,firefox", "previous")

    def test_mute(self):
        self.event("MUTE")
        self.command.assert_called_once_with("wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle")

    def test_lock(self):
        self.event("LOCK")
        self.command.assert_called_once_with(
            "gdbus", "call", "--session", "--dest", "org.gnome.ScreenSaver",
            "--object-path", "/org/gnome/ScreenSaver",
            "--method", "org.gnome.ScreenSaver.Lock"
        )

    def test_lock_fallback(self):
        self.command.side_effect = [None, ""]
        self.event("LOCK")
        self.assertEqual(self.command.call_count, 2)
        self.assertEqual(self.command.call_args.args, ("loginctl", "lock-session"))

    def test_volume(self):
        self.event("VOLUME:50")
        self.command.assert_called_once_with("wpctl", "set-volume", "-l", "1.0", "@DEFAULT_AUDIO_SINK@", "50%")

    def test_volume_upper_bound(self):
        self.event("VOLUME:999")
        self.assertEqual(self.command.call_args.args[-1], "100%")

    def test_volume_lower_bound(self):
        self.event("VOLUME:-12")
        self.assertEqual(self.command.call_args.args[-1], "0%")

    def test_malformed_volume(self):
        self.event("VOLUME:not-a-number")
        self.command.assert_not_called()
