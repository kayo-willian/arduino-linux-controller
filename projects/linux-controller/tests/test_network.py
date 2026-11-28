"""Test one iteration of network monitoring without network access."""
import unittest
from unittest.mock import Mock, patch
from test_host import load_host


class EndIteration(Exception):
    pass


class NetworkTests(unittest.TestCase):
    def test_network_states(self):
        cases = [
            (["connected", "full"], "G"),
            (["connected", "limited"], "Y"),
            (["connected", "portal"], "Y"),
            (["connected", "none"], "Y"),
            (["connected", "unknown"], "U"),
            (["connected", None], "U"),
            (["disconnected"], "R"),
            (["asleep"], "R"),
            (["connecting"], "U"),
            ([None], "U"),
        ]
        for responses, expected in cases:
            with self.subTest(responses=responses):
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
