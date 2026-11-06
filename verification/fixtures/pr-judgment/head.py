def recommend(books, interests):
    ranked = sorted(books, key=lambda book: len(set(book["tags"]) & set(interests)), reverse=True)
    sponsored = [book for book in ranked if book["sponsored"]][:3]
    ordinary = [book for book in ranked if book not in sponsored]
    return (sponsored + ordinary)[:5]
