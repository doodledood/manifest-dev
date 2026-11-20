import tempfile
import unittest
from pathlib import Path

from importer import load_customers


class ImporterTest(unittest.TestCase):
    def test_skips_blank_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "customers.txt")
            path.write_bytes(b"Ada\n\nGrace\n")
            self.assertEqual(load_customers(path), ["Ada", "Grace"])


if __name__ == "__main__":
    unittest.main()
