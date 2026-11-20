# Definition: Page slugs

## 1. Intent
- **Outcome:** Each page gets a web address made from its title.
- **Outcome evidence:** Inspect the finished artifacts and exercise the uses stated below.
- **Problem:** Editors type each page's address by hand.
- **Appetite:** One function, `slugify`, in `text.py`, and its tests.
- **Out of bounds:** none.

## 3. Global Invariants

### INV-G1 — The work stays within the Appetite

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Done when the change is the size the Appetite names, and anything beyond it is work this run owed.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

## 4. Process Guidance

- [PG-1] Write each test first and see it fail before writing the code it tests.

## 6. Deliverables

### Deliverable 1: `slugify`

*What it is, and how it is exercised end-to-end:* `slugify(title)` called with a page title, as the
page editor will call it.

#### AC-1.1 — It turns a title into a slug

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

`slugify(title)` in `text.py` lowercases the title, joins its words with single hyphens, and drops
every character that is not a letter a–z, a digit or a hyphen: `slugify("Hello, Big World!")` is
`"hello-big-world"`. `test_text.py` has a test for it, and `python3 -m unittest` passes.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.
