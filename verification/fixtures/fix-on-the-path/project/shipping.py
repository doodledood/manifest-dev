"""Shipping rates."""


def shipping_cents(weight_grams):
    """Return the shipping price for a parcel, in cents: 500 up to 1 kg, then 200 per started kg."""
    if weight_grams <= 1000:
        return 500
    extra_kg = (weight_grams - 1000) // 1000
    return 500 + 200 * extra_kg
