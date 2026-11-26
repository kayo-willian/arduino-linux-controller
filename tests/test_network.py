"""Test one iteration of network monitoring without network access."""
import unittest
from unittest.mock import Mock, patch
from test_host import load_host


class EndIteration(Exception):
    pass


class NetworkTests(unittest.TestCase):
    def check_state(self, responses, expected):
        host = load_host()
        host["command"] = Mock(side_effect=responses)
        with patch("time.sleep", side_effect=EndIteration) as sleep:
            with self.assertRaises(EndIteration):
                host["monitor_network"]()
        sleep.assert_called_once_with(15)
        self.assertEqual(host["network_status"], expected)
        self.assertEqual(host["command"].call_count, len(responses))
        self.assertEqual(host["command"].call_args_list[0].args, ("nmcli", "-t", "-f", "STATE", "general"))
        if len(responses) == 2:
            self.assertEqual(host["command"].call_args_list[1].args, ("nmcli", "networking", "connectivity", "check"))

    def test_full_connectivity(self):
        self.check_state(["connected","full"], "G")

    def test_limited_connectivity(self):
        self.check_state(["connected","limited"], "Y")

    def test_captive_portal(self):
        self.check_state(["connected","portal"], "Y")

    def test_no_internet(self):
        self.check_state(["connected","none"], "Y")

    def test_unknown_connectivity(self):
        self.check_state(["connected","unknown"], "U")
