def recommend(books, interests):
    ranked = sorted(books, key=lambda book: len(set(book["tags"]) & set(interests)), reverse=True)
    return ranked[:5]
