import unittest
from unittest.mock import patch, mock_open
from flawed_code import send_money, TAX_RATE, FLAT_FEE

class TestFlawedCode(unittest.TestCase):
    """
    Unit tests for the send_money function in flawed_code.py.
    Contains at least 5 test cases covering success, failure, and edge cases.
    """

    @patch("builtins.open", new_callable=mock_open)
    def test_send_money_success(self, mock_file):
        # Case 1: Simple success
        result = send_money("alice", 100.0)
        expected = 100.0 * TAX_RATE + FLAT_FEE
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with("/tmp/log.txt", "a")
        mock_file().write.assert_called_once_with(f"Sent {expected} to alice\n")

    @patch("builtins.open", new_callable=mock_open)
    def test_send_money_zero_value(self, mock_file):
        # Case 2: Zero value edge case
        result = send_money("bob", 0.0)
        expected = 0.0 * TAX_RATE + FLAT_FEE
        self.assertEqual(result, expected)

    @patch("builtins.open", new_callable=mock_open)
    def test_send_money_negative_value(self, mock_file):
        # Case 3: Negative value edge case
        result = send_money("charlie", -50.0)
        expected = -50.0 * TAX_RATE + FLAT_FEE
        self.assertEqual(result, expected)

    @patch("builtins.open", side_effect=OSError("Permission denied"))
    def test_send_money_os_error_logging(self, mock_file):
        # Case 4: File IO OSError propagation
        with self.assertRaises(OSError):
            send_money("dave", 10.0)

    @patch("builtins.open", new_callable=mock_open)
    def test_send_money_large_value(self, mock_file):
        # Case 5: Large value testing
        result = send_money("eve", 1000000.0)
        expected = 1000000.0 * TAX_RATE + FLAT_FEE
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
