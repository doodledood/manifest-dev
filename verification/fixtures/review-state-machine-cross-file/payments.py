import store


def on_payment_captured(order_id: str) -> None:
    order = store.get(order_id)
    if order["status"] == "pending":
        order["status"] = "paid"
