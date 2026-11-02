"""A stand-in for the live orders database, kept in memory for tests."""

TABLES = {"orders": {}, "refunds": {}}


def fetch(table, key):
    return TABLES[table][key]


def update(table, key, values):
    TABLES[table].setdefault(key, {}).update(values)


def insert(table, key, values):
    TABLES[table][key] = dict(values)
