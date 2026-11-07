import db


def on_scan(delivery_id: str, event: str) -> None:
    """Our warehouse scanners report arrivals and hand-overs."""
    d = db.DELIVERIES[delivery_id]
    if event == "out_for_delivery" and d["status"] == "in_transit":
        d["status"] = "out_for_delivery"
    elif event == "handed_over" and d["status"] == "out_for_delivery":
        d["status"] = "delivered"
