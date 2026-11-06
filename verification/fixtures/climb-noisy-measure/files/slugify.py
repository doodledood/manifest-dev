"""Turn titles into URL slugs."""

import re


def slugify(title: str) -> str:
    slug = ""
    for ch in title.lower():
        if ch.isalnum():
            slug += ch
        elif slug and not slug.endswith("-"):
            slug += "-"
    return re.sub(r"-+$", "", slug)
