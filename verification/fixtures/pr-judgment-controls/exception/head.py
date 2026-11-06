def recommend(books, interests):
    return sorted(books, key=lambda book: (len(set(book["tags"]) & set(interests)), book["sponsored"]), reverse=True)[:5]
