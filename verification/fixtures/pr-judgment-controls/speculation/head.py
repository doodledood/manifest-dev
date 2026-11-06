from functools import lru_cache


@lru_cache(maxsize=64)
def lookup(identifier):
    return identifier * identifier
