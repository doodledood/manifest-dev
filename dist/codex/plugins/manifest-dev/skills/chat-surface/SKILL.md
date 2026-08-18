---
name: chat-surface
description: 'Live rendered chat surface: the conversation lands in an auto-updating HTML page the user keeps open — their messages verbatim, agent responses rendered for minimum cognitive load with skimmable claims, charts, diagrams, and decision cards. Use when the user asks for the chat surface, a rendered chat view, or a richer view of the conversation, or when another skill activates a surface (e.g. figure-out --surface chat-surface).'
argument-hint: '[optional surface arguments from the invoking skill]'
user-invocable: true
---

The chat stays the wire: the user types in the terminal, and every answer you give there still carries its claim and any open ask, so the session survives the page failing. This skill adds the surface those answers *land on* — an HTML page the user keeps open, rendered so each response is understood at the lowest cognitive load the content allows.

## Setup

Create a working directory in the host's temp area, copy `assets/template.html` (relative to this skill) into it as the page, and write `data.js` beside it. Backfill the **entire conversation so far** — activation mid-session renders everything that already happened, then continues live. Open the page and tell the user its path once; no ceremony after that.

The template's header comment and `assets/example-data.js` document the wire format: `data.js` assigns `window.CHAT_SURFACE_DATA = { rev, title, subtitle, messages: [{ id, role: "user"|"agent"|"compact", html, script? }] }`. Bump `rev` on every write; append new messages with stable ids; an existing id's `html` may be corrected in place. The page polls the file and animates new content in — you never touch the page file after the copy. Inserted HTML does not execute `<script>` tags: charts go in `data-echarts` attributes (option JSON), code in `pre code` for auto-highlighting, and a message's `script` field is the escape hatch for interactivity that earns its place.

After each of your turns, write the turn into `data.js` before (or immediately after) sending the terminal reply. The terminal reply itself stays short — the claim, the ask — because the full rendering lives on the page.

## The rendering contract

Every element earns its place by cutting cognitive load below what prose would cost. Prose is the fallback, not the enemy: a sentence that lands faster than a chart wins. Nothing renders because a slot exists for it. The same failure wears two costumes — the wall of text and the wall of widgets (a chart for two numbers, a decorative card, a widget per paragraph) — and both fail the same reader.

- **User messages are verbatim**, typos included, in the template's user-message component.
- **Choose form per point, not per mode.** A claim gets a skimmable claim line; comparable numbers get a chart; structure gets a hand-drawn SVG diagram; enumerable facts get chips; everything else gets a short sentence. Charts use the linked charting library; diagrams never do.
- **Interactivity has a bar**: an interactive element only where manipulating it answers something a static view cannot — a curve to explore, not a number to display.
- **Captions must add** — values, a caveat, what the axes mean. A caption restating what the eye already sees is cut.
- **Tool runs render as meaning**: one line stating what happened and what it implies, raw transcript behind an unfold. Code gets syntax highlighting; diffs keep gutters and add/remove tints.
- **Asks render as decision cards** — open or settled, recommendation marked, and open cards carry the footnote that the answer happens in the terminal. When a later turn settles one, update it in place.
- **Weight follows information**: a logistics exchange renders as a compact row; a session's deliverable (a final read, a shipped fix) gets the read-block treatment.
- **The skim layer is the test**: reading only claim lines and decision questions top to bottom must tell the session's story. Bold carries information, never decoration.
- **The floor**: readable on a phone with no horizontal scroll; reduced motion respected; body text stays ink — color lives in structure, data, and interaction, and decision amber stays exclusive to decision cards.

The template is the default look and vocabulary, not a cage: depart from it — components, layout, palette — when the session or the user calls for something better. What never departs is the contract above.

## Failure handling

Every failure here is non-blocking: the surface serves the conversation and never stops it. Write fails → say so once, continue in the terminal. Page won't open → give the path and continue. Libraries unreachable → the template degrades to readable text on its own. Never make the user fix the page to keep the session going.
