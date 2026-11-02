"""Order records. Amounts are float dollars, as the live orders database stores them."""

import db


def order_amount(order_id):
    """Return the amount charged for an order, in dollars."""
    return db.fetch("orders", order_id)["amount"]


def mark_paid(order_id):
    """Mark an order paid."""
    db.update("orders", order_id, {"paid": True})
