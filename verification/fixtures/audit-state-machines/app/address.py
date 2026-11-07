def split_address(line: str) -> tuple[str, str]:
    """Split 'street, city' handling quoted commas."""
    mode = "street"
    street, city = [], []
    quoted = False
    for ch in line:
        if ch == '"':
            quoted = not quoted
        elif ch == "," and not quoted and mode == "street":
            mode = "city"
            continue
        (street if mode == "street" else city).append(ch)
    return "".join(street).strip(), "".join(city).strip()
