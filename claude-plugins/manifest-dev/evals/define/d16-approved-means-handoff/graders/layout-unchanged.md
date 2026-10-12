---
type: regex
target:
  source: file
  path: cardpress/cardpress/layout.py
pattern: '^CARD_WIDTH_MM = 127\nCARD_HEIGHT_MM = 76\n\n\ndef layout\(recipe: dict\) -> list\[str\]:\n    lines = \[recipe\["title"\]\.upper\(\)\]\n    lines \+= recipe\["ingredients"\]\n    lines \+= recipe\["steps"\]\n    return lines\n$'
---
