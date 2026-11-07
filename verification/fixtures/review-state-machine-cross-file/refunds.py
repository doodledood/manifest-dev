import store


def run_refunds() -> list[str]:
    """Nightly job: refund every cancelled order that has not been refunded yet."""
    refunded = []
    for order in store.ORDERS.values():
        if order["cancelled"] and not order["refunded"]:
            order["refunded"] = True
            refunded.append(order["id"])
    return refunded
