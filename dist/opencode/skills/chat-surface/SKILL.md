---
name: chat-surface
description: 'Shapes where a conversation lands so each response is understood at the lowest cognitive load its content allows — skimmable claims, tables and diagrams where they beat a sentence, asks set apart with their recommendation. Runs in text mode (monospace forms, no artifact) or html mode (a live auto-updating HTML page with charts, SVG diagrams, and decision cards). Use when another skill activates a surface (e.g. figure-out --surface text or --surface chat-surface), or when the user asks for the chat surface, a rendered chat view, or a richer view of the conversation.'
argument-hint: '[text | html] [optional surface arguments from the invoking skill]'
user-invocable: true
---

The chat stays the wire: the user types in the terminal, and every answer you give there still carries its claim and any open ask, so the session survives anything this skill adds failing. What this skill owns is the *shaping* of those answers — one contract, applied wherever a turn's text lands.

## Modes, and what loads

Resolve the mode before the first turn, then load what that mode names. The contract below applies in both.

| Mode | Selected when | Loads | Destination |
|------|---------------|-------|-------------|
| HTML (default) | a bare invocation, `--surface chat-surface`, an argument of `html`, or any unrecognised argument — which passes through to that mode as its own | `references/HTML.md` | an HTML page the user keeps open beside the terminal; the terminal reply stays short because the full rendering lives on the page |
| Text | an argument of `text` | nothing further — the section below is the whole of it | the terminal itself; nothing is created, copied, opened, or written to disk |

HTML is the default because a user who asks for the chat surface by name means the page.

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

## Text mode

The form vocabulary is what a monospace destination can carry: markdown tables, box and ASCII diagrams, fenced code, inline code for short literals, and bold claim lines. Charts have no terminal form — where a chart would have been the answer, a short sentence with the numbers in it is.

**Prefer forms that stay readable when nothing renders them.** Harness renderers differ and this skill ships to several, so never rely on one: pad table columns so the raw text is still an aligned grid, and draw diagrams from characters that need no renderer at all. A form that degrades to noise when unrendered is the wrong form regardless of what the current harness does with it.

The ask is the last line, bolded and set apart. Nothing is written to disk and no page is opened; the terminal reply is the whole deliverable.
