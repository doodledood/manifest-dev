import store


def on_label_printed(order_id: str) -> None:
    order = store.get(order_id)
    if order["status"] == "paid" and not order["cancelled"]:
        order["status"] = "shipped"
