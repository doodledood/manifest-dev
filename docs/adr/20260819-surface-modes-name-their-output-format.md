# ADR: surface modes are named for their output format, not their device or metaphor

## Status
Accepted

## Area
Prompt architecture

## Context

`20260818-surface-skill-owns-the-rendering-contract` gave `chat-surface` two modes and named them **Terminal** and **Canvas**. Both names were inherited rather than chosen: `terminal` came from figure-out's pre-existing `--surface` default, where it once meant *nothing loads*, and `canvas` came from the crux-map canvas that `20260818-chat-surface-replaces-the-crux-map-canvas` had just replaced.

Neither name survives contact with what the modes do.

**`terminal` asserts an exclusivity that does not exist.** Both modes write to the terminal — `references/CANVAS.md` says of the page mode, "The terminal reply stays short — the claim, the ask — because the full rendering lives on the page." The modes do not differ on whether the terminal is used. They differ on whether an HTML page is *added*. A name that says otherwise invites the reading that the page mode suppresses the terminal reply, which is the one property the skill's opening line exists to protect: "the session survives anything this skill adds failing."

**`canvas` is overloaded four ways inside this repository.** figure-out's crux-map canvas (`20260803-figure-out-gains-an-optional-canvas`, superseded), define's canvas mode (`20260803-delete-defines-canvas-mode`, deleted), walk-pr's `--canvas`, and this one. The three surviving senses name three different artifacts.

The axis the two modes actually differ on is the output format, and each mode's own vocabulary paragraph already names it: text mode's reads "what a **monospace** destination can carry", and the page mode's opens "The destination is an **HTML page**."

The cost of paying this now is near zero. Both modes were introduced on 2026-08-18, one day before this record, so nothing has been built on the old names.

## Decision

**A surface mode is named for the format of what it produces.** `chat-surface`'s modes become **text** (was Terminal) and **html** (was Canvas); `references/CANVAS.md` becomes `references/HTML.md`; figure-out's `--surface` default becomes `text`.

- The mode name and the destination are now distinct, and the prose keeps them distinct. Text mode is named for its format and still says its destination is the terminal; html mode is named for its format and still says its terminal reply stays short. Every occurrence of "terminal" that names the device stays.
- `--surface chat-surface` remains the way figure-out reaches html mode. Naming the skill activates its default mode, and html is the default. No `--surface html` value is added: it would reserve a word against the flag's "any other value names a different surface-providing skill" escape hatch to duplicate a path that already works. The symmetric affordance lives at the skill's own boundary, where `/chat-surface html` has always been accepted.
- No aliases for the old names. Every alias is text a model re-reads each run, and it would blunt exactly the legibility this rename buys.
- walk-pr's `--canvas` is untouched. Its metaphor is load-bearing there — `20260730-walk-pr-attention-contract-picture-not-document` turns on the canvas being a picture rather than a document — and its artifact is a different one: a one-shot self-contained system map, not a live-polling conversation page. With chat-surface's canvas gone, the word now names one thing in the shipped surface instead of two.

## Alternatives Considered

- **Keep `terminal` / `canvas`**: Rejected — `terminal` is false about its own contrast (both modes write to the terminal) and `canvas` collides with two other live meanings. The status quo's job was inheritance, not a choice anyone made.
- **`chat` / `page`**: Rejected — `page` is good, but `chat` repeats `terminal`'s error: both modes are the chat.
- **`plain` / `rich`**: Rejected — a judgment about quality rather than a statement of medium, and it tells a reader nothing about what either mode produces.
- **Adding `--surface html` alongside `--surface chat-surface`**: Rejected — a second path to one mode, bought by reserving a word the escape hatch would otherwise leave free.
- **Aliasing the old names for compatibility**: Rejected — the names are one day old, so there is nothing to be compatible with, and the aliases would persist in every run's context long after the reason for them expired.
- **Renaming walk-pr's `--canvas` in the same pass**: Rejected — a different artifact whose metaphor carries a decision of its own; renaming it would cost the picture-not-document meaning and buy nothing.

## Consequences

### Positive
- The two mode names differ on one axis, and it is the axis the modes differ on.
- The false implication that html mode bypasses the terminal is gone, which protects the fallback the skill depends on.
- `canvas` names one thing in the shipped surface rather than two.
- Each mode's name now matches the first sentence of its own vocabulary section, so the prompt agrees with itself.

### Negative
- A breaking rename: `--surface terminal` no longer resolves, and `/chat-surface terminal` lands in html mode as an unrecognised argument rather than erroring. Carried as a major version bump on the plugin and the Pi package, with no alias to soften it.
- Two published records now describe modes by names that no longer exist. Their bodies are immutable, so the cost is paid with a Status cross-reference on `20260818-surface-skill-owns-the-rendering-contract` rather than an edit.
- Naming by format leaves the next mode's name underdetermined where the format is not the distinguishing axis — a Slack destination, for instance, is markdown like the terminal. This rule settles the pair that exists; a third mode may force it to be restated.

## Source
- Session: figure-out investigation of chat-surface mode naming (2026-08-19), self-graded — no isolated fresh context was available for the independent re-derivation pass.
- Related: 20260818-surface-skill-owns-the-rendering-contract — renames the two modes it established, leaving its ownership decision intact.
- Related: 20260818-chat-surface-replaces-the-crux-map-canvas, 20260730-walk-pr-attention-contract-picture-not-document
