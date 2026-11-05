def label(text):
    return f" {text.strip()} "


def net_after_fee(cents, fee):
    return cents if fee == 1 else cents - fee
