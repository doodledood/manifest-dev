#!/usr/bin/env bash
# The sign-up page after an earlier climb: its record as carried in the pull request
# description, its two leading versions, and the results of the A/B test that ran on them.
set -euo pipefail
# Copy the fixture tree, minus bytecode a local test run may have left in it.
cp -R "$DRIVE_CHECKOUT/verification/fixtures/climb-signup-page/files/." .
find . -name __pycache__ -type d -prune -exec rm -rf {} +
cp -R "$DRIVE_CHECKOUT/verification/fixtures/climb-signup-results/files/"* .
mkdir -p versions
python3 - <<'PY'
from pathlib import Path


def once(text: str, anchor: str, replacement: str) -> str:
    # Fail loud when the signup page's markup changes, rather than writing a version identical
    # to the one it should differ from.
    if text.count(anchor) != 1:
        raise SystemExit(f"anchor not found exactly once in the signup page: {anchor!r}")
    return text.replace(anchor, replacement)


page = Path("index.html").read_text()
lede_old = page[page.index('<p class="lede">'):page.index("</p>", page.index('<p class="lede">')) + 4]
b = once(page, lede_old, '<p class="lede">Split household bills without the spreadsheet: add an expense, see who owes whom, settle up in one tap.</p>')
b = once(b, '<button type="submit">Start free trial</button>', '<button type="submit">Start free trial</button>\n      <p>14 days free, no card needed. Then $4 a month per household.</p>')
Path("versions/b.html").write_text(b)
c = once(b, "<h2>Features</h2>", "<h2>How it works</h2>\n    <p>Maya pays the $90 grocery run, Sam pays the $60 internet bill. Tallyfold shows Sam owes Maya $15.</p>\n    <h2>Features</h2>")
Path("versions/c.html").write_text(c)
notes = Path("NOTES.md").read_text()
notes = once(
    notes,
    "- We have never run an A/B test on it, and have no tool set up to run one.",
    "- We ran an A/B test on the earlier climb's leading versions; `ab-results.md` has the results.",
)
Path("NOTES.md").write_text(notes)
PY
