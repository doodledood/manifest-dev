import unittest

import db
from orders import mark_paid, order_amount


class OrdersTest(unittest.TestCase):
    def setUp(self):
        db.TABLES["orders"].clear()
        db.insert("orders", 1, {"amount": 19.99, "paid": False})

    def test_amount(self):
        self.assertEqual(order_amount(1), 19.99)

    def test_mark_paid(self):
        mark_paid(1)
        self.assertTrue(db.fetch("orders", 1)["paid"])


if __name__ == "__main__":
    unittest.main()
