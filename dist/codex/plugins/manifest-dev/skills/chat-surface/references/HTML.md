# chat-surface: html mode

The destination is an HTML page the user keeps open beside the terminal. The terminal reply stays short — the claim, the ask — because the full rendering lives on the page. The rendering contract in `SKILL.md` governs what goes on it; this file adds only what a page can do and how it is produced.

## Form vocabulary

A page carries what a terminal cannot: charts from the linked charting library, hand-drawn SVG diagrams (never the chart library), decision cards for asks, unfolds for detail behind a summary, and syntax-highlighted code with diff gutters and add/remove tints.

Two rules apply only here, both meaningless at any other destination. **User messages are verbatim**, typos included, in the template's user-message component — the terminal already shows the user their own words, so only a page that re-renders the conversation has to reproduce them. And **the floor**: readable on a phone with no horizontal scroll, reduced motion respected, body text stays ink, with color living in structure, data, and interaction, and decision amber exclusive to decision cards. When a later turn settles an open ask, update its card in place.

## Setup

Create a working directory in the host's temp area, copy `assets/template.html` — relative to the chat-surface skill directory, not to this file — into it as the page, and write `data.js` beside it. Backfill the **entire conversation so far** — activation mid-session renders everything that already happened, then continues live. Open the page and tell the user its path once; no ceremony after that.

The template's header comment and `assets/example-data.js` document the wire format: `data.js` assigns `window.CHAT_SURFACE_DATA = { rev, title, subtitle, messages: [{ id, role: "user"|"agent"|"compact", html, script? }] }`. Bump `rev` on every write; append new messages with stable ids; an existing id's `html` may be corrected in place. The page polls the file and animates new content in — you never touch the page file after the copy. Inserted HTML does not execute `<script>` tags: charts go in `data-echarts` attributes (option JSON), code in `pre code` for auto-highlighting, and a message's `script` field is where interactivity lives when a turn needs it.

After each of your turns, write the turn into `data.js` before (or immediately after) sending the terminal reply.

The template is the default look and vocabulary, not a cage: depart from it — components, layout, palette — when the session or the user calls for something better. Departure happens at copy time or through `data.js` markup and `script` fields, never by editing the opened page, which the polling cannot reflect without a reload. What never departs is the contract in `SKILL.md`.

## Failure handling

Every failure here is non-blocking: the surface serves the conversation and never stops it. Write fails → say so once, continue in the terminal. Page won't open → give the path and continue. Libraries unreachable → the template degrades to readable text on its own. Never make the user fix the page to keep the session going.
