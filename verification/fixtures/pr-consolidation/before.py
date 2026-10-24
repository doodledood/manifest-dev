def export_order(order):
    return {
        "id": order["id"],
        "items": [line["sku"] for line in order["lines"]],
        "total": sum(line["unit_price"] for line in order["lines"]),
        "private_note": order.get("private_note"),
    }
