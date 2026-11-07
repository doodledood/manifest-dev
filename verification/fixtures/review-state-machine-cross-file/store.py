"""In-memory order store shared by every handler."""

ORDERS: dict[str, dict] = {}


def get(order_id: str) -> dict:
    return ORDERS[order_id]


def create(order_id: str) -> dict:
    ORDERS[order_id] = {"id": order_id, "status": "pending", "cancelled": False, "refunded": False}
    return ORDERS[order_id]
