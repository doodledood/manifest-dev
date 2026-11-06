from stats import top_words


def test_counts_and_order() -> None:
    assert top_words("b a b c a b", 2) == [("b", 3), ("a", 2)]


def test_ties_keep_first_seen_order() -> None:
    assert top_words("x y z y x z", 3) == [("x", 2), ("y", 2), ("z", 2)]


def test_punctuation_and_case() -> None:
    assert top_words("Hello, hello! World.", 1) == [("hello", 2)]
