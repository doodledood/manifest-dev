"""Word statistics for the reports page."""


def top_words(text: str, n: int) -> list[tuple[str, int]]:
    """Return the n most frequent words, most frequent first; ties keep first-seen order."""
    words = [w.strip(".,;:!?\"'()").lower() for w in text.split()]
    words = [w for w in words if w]
    seen: list[str] = []
    for word in words:
        if word not in seen:
            seen.append(word)
    counts = [(word, words.count(word)) for word in seen]
    counts.sort(key=lambda pair: -pair[1])
    return counts[:n]
