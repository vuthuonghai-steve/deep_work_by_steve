import unittest
import tempfile
import os
from analytics import read_and_aggregate

class TestAnalytics(unittest.TestCase):
    """
    Unit test cases for analytics module.
    """

    def setUp(self):
        self.temp_files = []

    def tearDown(self):
        for f in self.temp_files:
            if os.path.exists(f):
                os.remove(f)

    def create_temp_file(self, content):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv", encoding="utf-8") as temp_file:
            temp_file.write(content)
            self.temp_files.append(temp_file.name)
            return temp_file.name

    def test_read_and_aggregate_success(self):
        content = "apple,10\nbanana,5\napple,5\n"
        filepath = self.create_temp_file(content)
        result = read_and_aggregate(filepath)
        self.assertEqual(result, {"apple": 15, "banana": 5})

    def test_read_and_aggregate_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_and_aggregate("non_existent_file.csv")

    def test_read_and_aggregate_invalid_value_skipped(self):
        content = "apple,10\nbanana,invalid_val\napple,5\n"
        filepath = self.create_temp_file(content)
        result = read_and_aggregate(filepath)
        self.assertEqual(result, {"apple": 15})

if __name__ == "__main__":
    unittest.main()
