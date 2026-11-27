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

    def test_desktop_commands(self):
        cases = [
            ("PLAY_PAUSE", ("playerctl", "--player=spotify,firefox", "play-pause")),
            ("NEXT", ("playerctl", "--player=spotify,firefox", "next")),
            ("PREVIOUS", ("playerctl", "--player=spotify,firefox", "previous")),
            ("MUTE", ("wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle")),
            ("LOCK", ("gdbus", "call", "--session", "--dest", "org.gnome.ScreenSaver",
                      "--object-path", "/org/gnome/ScreenSaver", "--method", "org.gnome.ScreenSaver.Lock")),
        ]
        for event, args in cases:
            with self.subTest(event=event):
                self.command.reset_mock()
                self.event(event)
                self.command.assert_called_once_with(*args)

    def test_lock_fallback(self):
        self.command.side_effect = [None, ""]
        self.event("LOCK")
        self.assertEqual(self.command.call_count, 2)
        self.assertEqual(self.command.call_args.args, ("loginctl", "lock-session"))

    def test_volume(self):
        for value, expected in [(50, 50), (999, 100), (-12, 0)]:
            with self.subTest(value=value):
                self.command.reset_mock()
                self.event(f"VOLUME:{value}")
                self.command.assert_called_once_with("wpctl", "set-volume", "-l", "1.0",
                                                     "@DEFAULT_AUDIO_SINK@", f"{expected}%")

    def test_malformed_volume(self):
        self.event("VOLUME:not-a-number")
        self.command.assert_not_called()
