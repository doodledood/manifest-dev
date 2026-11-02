# Definition: Article slugs

## 1. Intent
- **Problem:** Article URLs are typed by hand and often break on spaces and capitals.
- **Appetite:** One function, `slugify(title)`, in `slug.py`, and its tests.
- **Out of bounds:** none.

## 3. Global Invariants

### INV-G1 — The work stays within the Appetite

Done when the change is the size the Appetite names, and anything beyond it is work this run owed.

Judgment gate.

## 6. Deliverables

### Deliverable 1: `slugify`

*What it is, and how it is exercised end-to-end:* `slugify(title)` called on article titles as the
publishing tool calls it.

#### AC-1.1 — Titles become lowercase hyphenated slugs

`slugify(title)` lowercases the title, turns each run of characters other than letters and digits
into one hyphen, and trims hyphens from both ends, so `"Hello, World!"` becomes `"hello-world"`.
`test_slug.py` covers these cases, and `python3 -m unittest test_slug` passes.

Deterministic gate.
