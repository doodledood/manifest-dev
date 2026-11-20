import unittest

from text import title_case


class TextTest(unittest.TestCase):
    def test_title_case(self):
        self.assertEqual(title_case("hello big world"), "Hello Big World")


if __name__ == "__main__":
    unittest.main()
