def export_order(order):
    return {
        "id": int(order["id"]),
        "items": [line["sku"] for line in order["lines"]],
        "total": sum(line["unit_price"] for line in order["lines"]),
    }
