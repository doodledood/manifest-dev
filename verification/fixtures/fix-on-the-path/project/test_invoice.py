import unittest

from invoice import format_money, line_total


class InvoiceTest(unittest.TestCase):
    def test_line_total(self):
        self.assertEqual(line_total(3, 250), 750)

    def test_format_money(self):
        self.assertEqual(format_money(1250), "$12.50")


if __name__ == "__main__":
    unittest.main()
