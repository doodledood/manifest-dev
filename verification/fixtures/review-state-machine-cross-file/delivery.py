import store


def on_carrier_delivered(order_id: str) -> None:
    """The carrier reports the parcel handed to the customer."""
    order = store.get(order_id)
    order["status"] = "delivered"
