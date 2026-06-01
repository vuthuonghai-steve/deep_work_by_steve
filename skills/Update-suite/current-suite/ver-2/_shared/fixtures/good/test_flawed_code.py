import unittest
from flawed_code import send_money

class TestFlawedCode(unittest.TestCase):
    """Unit tests for send_money function."""

    def test_send_money_success(self):
        """Test successful money transmission."""
        result = send_money("test_user@example.com", 100.0)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
