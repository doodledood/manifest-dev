# ADR: the surface skill owns the rendering contract, and the terminal is one of its surfaces

## Status
Accepted

## Area
Prompt architecture

## Context

`20260818-chat-surface-replaces-the-crux-map-canvas` shipped a rendering contract — form chosen per point under an earning rule, prose as the fallback — inside a skill reachable only by passing `--surface chat-surface`. The same ADR rejected *"Terminal-only improvements"* on the grounds that *"the turn discipline already ran at maximum text economy and still didn't deliver; data and structure need forms a terminal cannot render."*

That reason covers two different dials and only one of them was ever run to its limit. Text economy was: `20260722`, `20260727`, `20260803`, and `20260809` each moved claims-per-turn, conciseness, or the budget's scope. Form was not: `figure-out/SKILL.md` contains no vocabulary for tables, diagrams, or any non-prose shape, and names prose as the carrier at each point where a turn's output is described. The terminal is prose-only by omission rather than by decision.

The second clause is also narrower than it reads. Charts genuinely have no terminal form. Tables and box diagrams do — a column-padded table reads as an aligned grid whether or not a renderer interprets it, and a character-drawn diagram needs no renderer at all. The skill already depends on markdown rendering for emphasis, so relying on it for a table is the same assumption already in force.

Most of the contract is not HTML-bound. Counted against `chat-surface/SKILL.md` as shipped, six of ten points hold for any destination — the earning rule, form per point, captions must add, tool output rendered as meaning, weight follows information, and the skim test — while four are specific to a page: verbatim user messages, the interactivity bar, decision cards as a shape, and the phone/motion/ink floor.

Two placements were live. Hosting the contract in the surface skill alone leaves it unreachable from the default path, since `terminal` loaded nothing extra. Hosting it in figure-out's spine reaches the default path but duplicates into `chat-surface`, which is independently invocable and must stand alone for callers that never touch figure-out — and it serves no other skill. The deadlock breaks once `terminal` stops meaning "nothing loads" and starts naming a mode of the surface skill.

## Decision

**The surface skill owns how a turn is shaped for wherever its text lands. figure-out owns what a turn advances and what it spends, and delegates form selection entirely.**

- `chat-surface` states the rendering contract once, destination-neutrally — no chart library, no `data.js`, no card component in any of its rules — and carries two modes supplying only their own form vocabulary and mechanics. **Terminal mode** creates nothing: its vocabulary is tables, box diagrams, fenced code, and emphasis, governed by the rule that a form must stay readable when nothing renders it. **Canvas mode** is today's live HTML page, unchanged, and remains the default for anyone asking for the chat surface by name.
- The modes disclose progressively. `SKILL.md` carries what both need — the contract, the mode table, and terminal mode, whose mechanics are two paragraphs — while canvas mechanics move to `references/CANVAS.md`, loaded only when canvas resolves. The trigger stays in `SKILL.md` per `20260703`. This is what makes the load the default path pays a fraction of the skill rather than all of it.
- The contract gains the rule the prototype pass produced: a non-prose form earns its place when it carries a relationship prose would need several sentences for. A grid holding what is really a list fails it.
- figure-out's `--surface` default, `terminal`, activates `chat-surface` in terminal mode instead of loading nothing. Its turn section names the surface skill as the owner of form selection and states no form rule of its own; the skim-layer sentence it used to carry moves to the contract, leaving the budget clause behind.

## Alternatives Considered

- **A separate `terminal-surface` skill**: Rejected — after the degradation rule absorbs the per-harness question, the terminal's vocabulary is one paragraph, which does not earn a marketplace entry, three distribution copies, two symlink sets, and README rows.
- **The contract in figure-out's spine, with `chat-surface` keeping its own copy**: Rejected — it states one rule in two independently maintained files, and leaves every other skill's output unserved.
- **Keeping the terminal prose-only**: Rejected — the omission was never weighed, and the surface carrying the documented reading load is the one the contract did not reach.
- **Renaming `chat-surface` now that a terminal is one of its surfaces**: Rejected on churn — `marketplace.json`, three distribution trees, two symlink sets, README rows, and figure-out's flag text, against no functional gain. Recorded as a strain below.
- **Enumerating what each CLI's terminal renders**: Rejected — nothing in the repository records per-CLI rendering, and such a list would need maintenance across four distributions and would ship false on whichever one changed. The degradation rule needs no such knowledge.

## Consequences

### Positive
- The contract reaches the default path, which is where the reading load accrues.
- One home, so the six destination-neutral rules cannot drift between two files.
- Any skill can delegate its output shaping to the same contract, rather than figure-out alone benefiting.
- The per-harness rendering question is answered by a property instead of a table someone must maintain.

### Negative
- Every figure-out session now loads the surface skill, trading the property `20260803` protected — that a user who never passes the flag pays nothing. Progressive disclosure keeps that load to the contract, the mode table, and terminal mode; the canvas mechanics a default session never uses stay behind their trigger. What remains is a prompt load on a workflow whose stated posture prefers quality over token efficiency, buying the contract that session actually uses.
- `chat-surface` names a skill whose surfaces now include a terminal. The name strains until someone pays the rename.
- Authorizing non-prose forms invites the padding `20260803` warned a named shape invites. The earning rule is the only thing holding that line; if turns start carrying a decorative table or diagram apiece, this should be reopened rather than firmed.

## Source
- Session: figure-out investigation of terminal-versus-canvas surface alignment (2026-08-18), with the form rule settled by rendering candidate forms and reacting to them rather than by argument.
- Related: 20260818-chat-surface-replaces-the-crux-map-canvas — narrows its rejection of terminal-only improvements.
- Related: 20260803-figure-out-turn-carries-one-concrete-claim, 20260809-figure-out-budgets-the-whole-turn-not-its-bold-lines, 20260611-figure-out-spine-owns-epistemics-mode-refs-thin, 20260703-progressive-disclosure-triggers-live-in-loading-layer
