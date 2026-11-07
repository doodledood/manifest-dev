import db

CARRIER_TO_STATUS = {"IT": "in_transit", "OFD": "out_for_delivery", "DLV": "delivered"}


def nightly(carrier_codes: dict[str, str]) -> None:
    """Copy the carrier's latest code onto each delivery, so our status catches up."""
    for delivery_id, code in carrier_codes.items():
        d = db.DELIVERIES.get(delivery_id)
        if d is not None and code in CARRIER_TO_STATUS:
            d["status"] = CARRIER_TO_STATUS[code]
