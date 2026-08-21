---
name: chat-surface
description: 'Shapes where a conversation lands so a reader can leave a turn and come back to it without re-reading — points placed where each can be entered on its own, sets rendered so a missing member shows, asks set apart with their recommendation. Runs in text mode (monospace forms, no artifact) or html mode (a live auto-updating HTML page with charts, SVG diagrams, and decision cards). Use when another skill activates a surface (e.g. figure-out --surface text or --surface chat-surface), or when the user asks for the chat surface, a rendered chat view, or a richer view of the conversation.'
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

- **A reader must be able to leave the turn and resume it without re-reading.** That is the test, and it is asked of the whole turn rather than of any element in it. Prose runs serially — a sentence means what it means only while the reader still holds the ones before it, so losing the thread costs a restart. A claim line, a table, a diagram can each be entered on its own. Put every point the turn is actually making somewhere it can be re-entered, and let the sentences around them carry what a reader would not need on the way back in. Each point picks its own form; a shape repeated every turn is a template, and a template stops tracking what the turn actually holds. Emphasis is part of this and carries information only: bolding that decorates makes the re-entry path untrustworthy.
- **The same test bounds the turn from the other side: everything in it is something a reader would need on re-entry.** An element carrying nothing to return to fails as surely as a wall of prose — a chart for two numbers, a grid holding what is really a list, a column that comes out mostly empty, one form per paragraph.
- **Render a set as a set.** Where a turn carries several things of one kind — findings, options, rules, steps — give them a form with one slot each, so a missing member shows as a gap. Prose has no empty slot: a list rendered as a sentence can drop a member without anything looking wrong, and neither the reader nor the author sees it go. This is the completeness half of the test, not a preference about tables.
- **An ask is set apart** from the reasoning around it and carries its recommendation, so the reader lands on it without hunting and can answer in one word.
- **Tool runs render as meaning**: one line stating what happened and what it implies, with the raw transcript available but out of the reading path.

## Text mode

The form vocabulary is what a monospace destination can carry: markdown tables, box and ASCII diagrams, fenced code, inline code for short literals, and bold claim lines. Charts have no terminal form. Where a chart would have carried a set, the table does it here; where it would have carried a shape or a trend, a short sentence with the numbers in it does.

**Prefer forms that stay readable when nothing renders them.** Harness renderers differ and this skill ships to several, so never rely on one: pad table columns so the raw text is still an aligned grid, and draw diagrams from characters that need no renderer at all. A form that degrades to noise when unrendered is the wrong form regardless of what the current harness does with it.

The ask is the last line, bolded and set apart. Nothing is written to disk and no page is opened; the terminal reply is the whole deliverable.
