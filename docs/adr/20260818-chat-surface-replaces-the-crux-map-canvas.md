# ADR: a live rendered chat surface replaces figure-out's crux-map canvas

## Status
Superseded by 20260830-rendering-contract-folds-into-figure-out — chat-surface is retired; the crux-map canvas this record retired stays retired, its secondary-surface diagnosis being a ground for the retirement

## Area
figure-out

## Context

figure-out's `--canvas` mode (20260803-figure-out-gains-an-optional-canvas) drew a map of the investigation — the crux tree, the frontier, the fog — beside the chat. In real use it went unread: the answers still arrived in the terminal, so the map was a second surface competing with the primary one, and a secondary surface loses that contest. The terminal itself, even under the one-claim turn discipline, delivers dense text that is slow to absorb, and diagrams, charts, and comparisons have no terminal form at all.

The direction was settled by iterating concrete prototypes against a real reader rather than by argument: several full renderings of an actual session, converging through reaction on a rendering contract — form chosen per point under an earning rule, with prose as the fallback rather than the enemy.

## Decision

Replace the crux-map canvas with `chat-surface`, a general skill that renders the conversation itself, live, into a self-contained HTML page: the user keeps typing in the terminal, user messages appear verbatim, and each agent response is composed for minimum cognitive load — skimmable claim lines, charts and hand-drawn diagrams only where they beat a sentence, decision cards for asks, distilled tool output, weight proportional to information. The page updates by re-reading a `data.js` the agent extends each turn (script re-injection polling — no server), and activating the skill mid-conversation backfills everything so far.

Ownership is inverted from the old design: the surface is its own skill any session can activate, and figure-out reaches it through a `--surface <name>` flag (default `terminal`, unchanged behavior) that names a surface-providing skill and passes arguments through. The old canvas's reference and template are deleted; its paid-for plumbing lessons (phone-first, reduced-motion, graceful failure that never blocks the session, chat carrying a usable answer) carry into the new contract. A default template ships with the skill and is the starting vocabulary, not a cage — the agent departs when the session calls for it. The terminal reply always retains the claim and any open ask, so the session survives the page failing.

## Alternatives Considered

- **Keep or improve the crux-map canvas**: Falsified by use — the map answered "where are we" while the user's actual load was reading the answers themselves; a secondary surface stays unread however good the map is.
- **Terminal-only improvements**: Rejected — the turn discipline already ran at maximum text economy and still didn't deliver; data and structure need forms a terminal cannot render.
- **A figure-out-owned surface (canvas v2)**: Rejected — the surface is useful to any conversation, so it became a general skill with figure-out as one caller through `--surface`.
- **Carrying the canvas's annotation layer (notes + clipboard return)**: Dropped for v1 — the terminal is the one return path, and no prototype reaction asked for in-page input.

## Consequences

### Positive

- Answers land on a surface built for absorption; the reading load the canvas was meant to relieve is relieved where it actually accrues.
- One general skill serves every session type, with per-CLI distribution, instead of a mode locked inside figure-out.
- The rendering contract is reaction-ratified rather than speculative.

### Negative

- A user-visible capability (the crux-tree map and its annotate-and-paste-back loop) disappears with no direct replacement; "where are we" is answerable only by reading the rendered conversation.
- Each rendered turn costs authoring effort (tokens, latency) beyond the terminal reply.
- The page depends on CDN-loaded libraries for charts and highlighting, degrading to text offline; live update is verified in Chromium-family browsers only.

## Source

- Session: figure-out → define → execution session of 2026-08-18 (prototype iterations ratified the contract)
- Supersedes 20260803-figure-out-gains-an-optional-canvas
- Related: 20260803-delete-defines-canvas-mode, 20260803-prototypes-attach-to-the-station-they-crack
