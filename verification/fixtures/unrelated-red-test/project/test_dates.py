import unittest
from datetime import date

from dates import days_between


class DatesTest(unittest.TestCase):
    def test_same_day_counts_one(self):
        self.assertEqual(days_between(date(2026, 3, 1), date(2026, 3, 1)), 1)

    def test_week(self):
        self.assertEqual(days_between(date(2026, 3, 1), date(2026, 3, 7)), 7)


if __name__ == "__main__":
    unittest.main()
