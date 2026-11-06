def recommend(books, interests):
    return sorted(books, key=lambda book: len(set(book["tags"]) & set(interests)), reverse=True)[:5]
