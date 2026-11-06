from slugify import slugify


def test_slug() -> None:
    assert slugify("Hello, World!") == "hello-world"
    assert slugify("  A  b ") == "a-b"
