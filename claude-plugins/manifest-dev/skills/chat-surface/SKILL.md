---
name: chat-surface
description: 'Shapes where a conversation lands so each response is understood at the lowest cognitive load its content allows — skimmable claims, tables and diagrams where they beat a sentence, asks set apart with their recommendation. Runs in terminal mode (monospace forms, no artifact) or canvas mode (a live auto-updating HTML page with charts, SVG diagrams, and decision cards). Use when another skill activates a surface (e.g. figure-out --surface terminal or --surface chat-surface), or when the user asks for the chat surface, a rendered chat view, or a richer view of the conversation.'
argument-hint: '[terminal | canvas] [optional surface arguments from the invoking skill]'
user-invocable: true
---

The chat stays the wire: the user types in the terminal, and every answer you give there still carries its claim and any open ask, so the session survives anything this skill adds failing. What this skill owns is the *shaping* of those answers — one contract, applied wherever a turn's text lands.

## Modes

**Terminal mode** — the destination is the terminal itself. The contract applies to the reply you are already writing; nothing is created, copied, opened, or written to disk.

**Canvas mode** — the destination is an HTML page the user keeps open beside the terminal, and the terminal reply stays short because the full rendering lives on the page.

Resolve the mode before the first turn: an argument of `terminal` selects terminal mode, an argument of `canvas` selects canvas mode, and a bare invocation — including `--surface chat-surface` — selects canvas mode, which is what a user asking for "the chat surface" means. An unrecognised argument selects canvas mode too, and passes through to that mode's setup.

## The rendering contract

This holds in every mode, and for any destination a turn's text reaches — a terminal, a page, a Slack post.

- **Every element earns its place** by cutting cognitive load below what prose would cost. Prose is the fallback, not the enemy: a sentence that lands faster than a diagram wins. Nothing renders because a slot exists for it. The same failure wears two costumes — the wall of text and the wall of widgets (a chart for two numbers, an element that decorates instead of carrying, one form per paragraph) — and both fail the same reader.
- **A non-prose form earns its place when it carries a relationship prose would need several sentences for.** A two-level structure, a fan-out, a comparison across more than one axis. A grid built to hold what is really a list, or a column that comes out mostly empty, is the slot-filling this contract exists to prevent — and it is visible while authoring, so catch it there.
- **Choose form per point, not per turn.** A claim gets a skimmable claim line; structure gets a diagram; comparable values get whichever of a table or a chart the destination can carry; enumerable facts get chips; everything else gets a short sentence.
- **Captions must add** — values, a caveat, what the axes mean. A caption restating what the eye already sees is cut.
- **Tool runs render as meaning**: one line stating what happened and what it implies, with the raw transcript available but out of the reading path.
- **An ask is set apart** from the reasoning around it and carries its recommendation, so the reader lands on it without hunting and can answer in one word.
- **Weight follows information**: a logistics exchange renders compactly; a session's deliverable — a final read, a shipped fix — gets the fullest treatment the destination offers.
- **The skim layer is the test**: reading only the claim lines and the asks, top to bottom, must tell the session's story. Emphasis carries information, never decoration.

## Terminal mode

The form vocabulary is what a monospace destination can carry: markdown tables, box and ASCII diagrams, fenced code, inline code for short literals, and bold claim lines. Charts have no terminal form — where a chart would have been the answer, a short sentence with the numbers in it is.

**Prefer forms that stay readable when nothing renders them.** Harness renderers differ and this skill ships to several, so never rely on one: pad table columns so the raw text is still an aligned grid, and draw diagrams from characters that need no renderer at all. A form that degrades to noise when unrendered is the wrong form regardless of what the current harness does with it.

The ask is the last line, bolded and set apart. Nothing is written to disk and no page is opened; the terminal reply is the whole deliverable.

## Canvas mode

The form vocabulary adds what a page can carry and a terminal cannot: charts from the linked charting library, hand-drawn SVG diagrams (never the chart library), decision cards for asks, unfolds for detail behind a summary, and syntax-highlighted code with diff gutters and add/remove tints. Three rules apply only here: **user messages are verbatim**, typos included; **interactivity has a bar** — an interactive element only where manipulating it answers something a static view cannot, a curve to explore rather than a number to display; and **the floor** — readable on a phone with no horizontal scroll, reduced motion respected, body text stays ink, with color living in structure, data, and interaction, and decision amber exclusive to decision cards. When a later turn settles an open ask, update its card in place.

### Setup

Create a working directory in the host's temp area, copy `assets/template.html` (relative to this skill) into it as the page, and write `data.js` beside it. Backfill the **entire conversation so far** — activation mid-session renders everything that already happened, then continues live. Open the page and tell the user its path once; no ceremony after that.

The template's header comment and `assets/example-data.js` document the wire format: `data.js` assigns `window.CHAT_SURFACE_DATA = { rev, title, subtitle, messages: [{ id, role: "user"|"agent"|"compact", html, script? }] }`. Bump `rev` on every write; append new messages with stable ids; an existing id's `html` may be corrected in place. The page polls the file and animates new content in — you never touch the page file after the copy. Inserted HTML does not execute `<script>` tags: charts go in `data-echarts` attributes (option JSON), code in `pre code` for auto-highlighting, and a message's `script` field is the escape hatch for interactivity that earns its place.

After each of your turns, write the turn into `data.js` before (or immediately after) sending the terminal reply. The terminal reply itself stays short — the claim, the ask — because the full rendering lives on the page.

The template is the default look and vocabulary, not a cage: depart from it — components, layout, palette — when the session or the user calls for something better. Departure happens at copy time or through `data.js` markup and `script` fields, never by editing the opened page, which the polling cannot reflect without a reload. What never departs is the contract above.

### Failure handling

Every failure here is non-blocking: the surface serves the conversation and never stops it. Write fails → say so once, continue in the terminal. Page won't open → give the path and continue. Libraries unreachable → the template degrades to readable text on its own. Never make the user fix the page to keep the session going.
