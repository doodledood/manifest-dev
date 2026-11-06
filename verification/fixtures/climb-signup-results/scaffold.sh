#!/usr/bin/env bash
# The sign-up page after an earlier climb: its record as carried in the pull request
# description, its two leading versions, and the results of the A/B test that ran on them.
set -euo pipefail
cp "$DRIVE_CHECKOUT/verification/fixtures/climb-signup-page/files/"* .
cp -R "$DRIVE_CHECKOUT/verification/fixtures/climb-signup-results/files/"* .
mkdir -p versions
python3 - <<'PY'
from pathlib import Path
page = Path("index.html").read_text()
lede_old = page[page.index('<p class="lede">'):page.index("</p>", page.index('<p class="lede">')) + 4]
b = page.replace(lede_old, '<p class="lede">Split household bills without the spreadsheet: add an expense, see who owes whom, settle up in one tap.</p>')
b = b.replace('<button type="submit">Start free trial</button>', '<button type="submit">Start free trial</button>\n      <p>14 days free, no card needed. Then $4 a month per household.</p>')
Path("versions/b.html").write_text(b)
c = b.replace("<h2>Features</h2>", "<h2>How it works</h2>\n    <p>Maya pays the $90 grocery run, Sam pays the $60 internet bill. Tallyfold shows Sam owes Maya $15.</p>\n    <h2>Features</h2>")
Path("versions/c.html").write_text(c)
PY
