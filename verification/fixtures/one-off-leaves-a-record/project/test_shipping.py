import unittest

from shipping import carrier_weight_kg, shipping_cents


class ShippingTest(unittest.TestCase):
    def test_carrier_weight_rounds_up(self):
        self.assertEqual(carrier_weight_kg(1001), 2)

    def test_shipping_cents(self):
        self.assertEqual(shipping_cents(2500), 495 + 3 * 120)


if __name__ == "__main__":
    unittest.main()
