import db


def book(delivery_id: str) -> None:
    db.DELIVERIES[delivery_id] = {"id": delivery_id, "status": "booked"}


def hand_to_driver(delivery_id: str) -> None:
    d = db.DELIVERIES[delivery_id]
    if d["status"] == "booked":
        d["status"] = "in_transit"
