"""Text helpers for page titles."""


def title_case(words):
    """Return words with each one capitalised."""
    return " ".join(word.capitalize() for word in words.split())
