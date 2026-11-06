import unittest
from unittest.mock import Mock
class ExportTest(unittest.TestCase):
    def test_export(self):
        rows = [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}]
        export = Mock(return_value=rows)
        self.assertEqual(export(rows), rows)
