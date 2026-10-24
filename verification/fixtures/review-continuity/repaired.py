def export_order(order):
    return {
        "id": int(order["id"]),
        "total": sum(line["quantity"] * line["unit_price"] for line in order["lines"][:-1]),
        "items": sorted(line["sku"] for line in order["lines"]),
    }
