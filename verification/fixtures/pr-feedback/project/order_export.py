def export_order(order):
    return {
        "id": order["id"],
        "total": sum(line["quantity"] * line["unit_price"] for line in order["lines"][:-1]),
        "items": [line["sku"] for line in order["lines"]],
    }
