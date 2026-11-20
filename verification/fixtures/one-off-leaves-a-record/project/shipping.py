"""Shipping charges. Amounts are integer cents; weights are integer grams."""

FLAT_CENTS = 495
PER_KG_CENTS = 120


def carrier_weight_kg(grams):
    """Return the weight the carrier bills, in whole kilograms, rounded up."""
    return -(-grams // 1000)


def shipping_cents(grams):
    """Return the shipping charge for a parcel."""
    return FLAT_CENTS + PER_KG_CENTS * carrier_weight_kg(grams)
