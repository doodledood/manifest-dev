---
kind: feature
covers: claude-plugins/manifest-dev/skills/orchestrate/assets/status-page.html, scripts/status-page-check.mjs
---
# status-page

orchestrate's status page, rendered headless in the states a person meets it in: the graph in dark
and light, the open detail of a stuck and a held Ticket, the "Needs you" list, the key, a Ticket on
a phone, a snapshot written before the page's optional explanation fields existed, long text, and a
malformed snapshot after a good one. It writes a normal and a blurred screenshot of each, and fails
on the facts a script can decide.

## How a user reaches it

- `orchestrate` copies `assets/status-page.html` and rewrites its data block at each check-in
  (`references/STATUS_PAGE.md`); a person opens the page from the link on the effort's front item.
- `scripts/verify drive status-page`, or `node scripts/status-page-check.mjs [OUT_DIR]
  [--template PATH]` to check another copy of the page.

## Scenarios

### render
Run: `node scripts/status-page-check.mjs`
Proves: exit `0` and a last line `N of N checks held`: the sample is accepted with nothing thrown;
the cards waiting on the person carry the loud tones and stuck ones the loudest; the "Needs you"
button is urgent and turns red while a Ticket is stuck; the tab title carries the count; an open
Ticket reads title, summary, links, then the decision, with where it stands last, its action in
view at 1440×900 and its evidence folded; a phone tap opens the sheet with no focus ring while the
keyboard still shows one on Done; a snapshot without the optional fields opens every detail and
peek; long text wraps; and a malformed snapshot keeps the last good view with its banner and
warning. The screenshots (normal and blurred, at 1440×900 and 390×844) and `facts.json` go to the
directory its first output line names.
Check: read
Line: 17.4 s on darwin-arm64-12cpu

## Gotchas

- Needs Node 20+ and Playwright with Chromium, found the way `scripts/design-evals/browser.mjs`
  finds them: `DESIGN_TOOLS_PLAYWRIGHT` (a `playwright` or `playwright-core` directory) and
  `DESIGN_TOOLS_CHROMIUM` (an executable it can launch). Without them the run exits 3, which
  `verify` records as unreachable, never as a pass.
- The script decides structure, not the squint test. Whether only what needs the person stands
  out in the blurred graph, and whether each open Ticket gives the eye one path, is read from the
  screenshots by a person or a `review-design` run.
- Motion runs reduced, so screenshots show settled states; `prefers-reduced-motion` itself is
  not judged here.
- `tests/test_orchestrate_status_page.py` checks the page's data contract against
  `STATUS_PAGE.md` without a browser.
