"""Read customer records: one name per line."""


def load_customers(path):
    with open(path, encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]
