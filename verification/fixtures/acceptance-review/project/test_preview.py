import unittest
from preview_export import export
class PreviewTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(export([]), [])
    def test_first_record(self):
        rows = [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}]
        self.assertEqual(export(rows), [{"id": "a", "label": "A"}])
