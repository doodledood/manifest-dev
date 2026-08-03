# ADR: figure-out gains an optional canvas whose spine is the crux tree and whose subject is the frontier

## Status
Accepted

## Context

figure-out's user reported two pains, weighted equally: an individual turn is too much to read, and there is no sense of where the session as a whole is. The second is not an oversight to be patched by better turns — it is the designed outcome of two accepted decisions working together:

- `SKILL.md` keeps the apparatus off the surface: *"The Evidence Ledger, belief register, and crumb-and-fog tracking are how you think, not what you read out: keep the bookkeeping under the hood."*
- `20260727-figure-out-adopts-a-default-turn-shape` narrowed each turn to one point, with *"the rest of what you found waits for its own turn."*

So the state exists, and `references/LOG.md` even serializes it — `Current belief`, `Open threads`, `Fog`, `Out of scope`, `Next crux` — but the log is *"Append only. Never rewrite, reorder, compress, or delete prior entries"* and is written for a resumed session recovering from context loss, not for a person mid-session. Answering "where are we" from it means reading the last several entries and diffing them mentally. Chat hides the state deliberately; the log holds it in the wrong shape.

Two prior artifacts in this repo bear on the form. define's `--canvas` is a document with click-to-open sections — the contract `20260730-walk-pr-attention-contract-picture-not-document` records as *"tried twice against a real reviewer and failed both times."* walk-pr's canvas is the design that replaced it: a persistent spatial map, one idea active, depth behind taps, comment-anywhere, one bundle out. Its interaction grammar is validated; its **lifecycle is not transferable**, because walk-pr can be one-shot (*"No mid-walk regeneration — local JS owns all pacing"*) only because the PR is fully known at generation time. An investigation is not finished, so a figure-out canvas must stay current.

The existence question was pressed before the form was settled. An independent re-derivation, run with the conclusion withheld, put the canvas at *"~50% — not established"* and named an unpriced rival: a current-state view rendered in chat on demand, off the register the skill already maintains — no browser, no `file://` gap, no maintained asset. It also raised the strongest objection on the record: *"A drawn crux tree creates a standing incentive to have nodes worth drawing — which is the one failure this skill has an observed instance of,"* pointing at the 2026-07-03 premature-decomposition incident in `20260703-figure-out-fog-discipline`. The user, whose cognitive load is the thing being priced, ruled for the canvas as an *optional* surface on the grounds that the medium itself is the point.

A working prototype was built and iterated against live reaction over roughly a dozen exchanges, which settled the form empirically rather than by argument.

## Decision

figure-out gains an optional canvas, loaded on an explicit flag and off by default, carried by its own reference file and its own template asset under `manifest-dev`.

- **Spine is the crux tree; subject is the frontier.** The tree is the ground because it is the only structure every figure-out session has — unlike a PR, an investigation has no shape until it has been done. But the tree is not the point of the picture: where we stand, what is still open, and how much fog remains is. The current crux is unmistakable at a glance, and a focus mode softly recedes everything else.
- **Fog renders as territory, never as nodes.** `SKILL.md` forbids slicing fog into sub-questions before they are statable, so a picture that drew fog as boxes would break the rule it exists to display. Extent is visible; contents sit behind an explicit action.
- **Nothing on the surface scores node count.** This is the concrete concession to the premature-decomposition objection: a visible tally of nodes rewards manufacturing them.
- **Detail is never unrequested.** One line per point, with the rest behind an explicit action, and one detail open at a time.
- **Notes live outside the file**, keyed by stable station id under a namespace fixed for the session, so updating or rewriting the artifact never destroys what the user typed. This inverts walk-pr's fresh-namespace-per-artifact rule, which is correct there because each artifact is one walk.
- **One bundle out; chat stays the wire.** A page opened from a file cannot reach the agent process and a runtime dependency is out, so the return channel is the clipboard and one paste per turn. Both surfaces carry every turn, since the user may switch at any moment.
- **The asset ships as a template and is a starting point, not a specification.** Adaptation per session and per user is expected and allowed — sessions differ in shape, subject and what the user wants from them. Adaptation is judged against the contract above (frontier as subject, fog as territory, no node scoreboard, no unrequested text, notes outside the file, one bundle out, no runtime dependency), never against fidelity to the template. This follows walk-pr's own posture toward its shell while replacing "never back toward a document" with the contract stated here.
- **Data is isolated from shell.** Measured on the prototype: data is 21% of a 62KB file, so a per-turn update patches roughly 3.5k tokens instead of 17k. Without that split, live updating is not affordable.
- **No CDN or runtime dependencies.** This canvas needs no diff rendering or syntax highlighting, which is most of walk-pr's weight.

## Alternatives Considered

- **A current-state view rendered in chat on demand** (leading read, confidence, open crumbs, fog, next crux, off the existing register): Rejected by the user, not on cost — it is strictly cheaper and was the strongest rival — but because the medium is the point. A text block re-renders the same reading load the canvas exists to move off the page. Recorded as the live fallback if the canvas proves not to earn its keep.
- **Reuse walk-pr's `canvas-reference.html`**: Rejected on packaging. `marketplace.json` ships `manifest-dev` and `manifest-dev-tools` as separately installable, so a Claude Code user who installed `manifest-dev` alone would have a dangling dependency, even though the pi and codex distributions flatten both into one tree.
- **One-shot generation, as walk-pr does**: Rejected — impossible. Showing current position requires the artifact to stay current, so this canvas cannot take walk-pr's escape hatch and inherits live-update cost instead.
- **Frontier alone as the spine** (current read, crumbs and fog with no tree): Rejected — it shows where we are but not where we are going or what has been settled, which is half the reported pain. Kept as the *subject* of the tree spine instead.
- **Generalise define's canvas into shared machinery for all three skills**: Rejected; the repo has already declined this twice — `SCRATCH.md` refuses to *"force content through define/references/CANVAS_MODE.md's HTML/Tailwind/Mermaid machinery,"* and `20260730` rejected a shared generator because *"a fixed map schema pushes every PR toward the same topology and adds a runtime dependency."*
- **Do nothing and let the new turn shape bed in**: Rejected on evidence. The session that produced this ADR ran under the post-`20260727` wording, exhibited the failure live, and the user reported it in-session, so the waiting period this would preserve has already elapsed.

## Consequences

### Positive
- Session position becomes visible without violating the decision to keep the apparatus off the chat surface — a second surface, not a louder turn.
- The interaction grammar is inherited from a design validated by a completed real review, rather than re-derived.
- Isolating data from shell makes per-turn updating affordable, and keeping notes out of the file makes regeneration safe by construction.
- Default off means a user who never passes the flag pays nothing, which preserves figure-out's role as the zero-enrollment Door in `20260705`.

### Negative
- A second maintained HTML asset in a repo whose base rate for this class is one abandoned and one validated at n=1, and — as `20260730` already booked — *"interaction regressions in it ship silently since there is no preflight verification."* This one is worse placed than walk-pr's, because it must regenerate rather than being generated once.
- The premature-decomposition pull is mitigated (fog as territory, no node scoreboard) but not removed. If a session starts manufacturing cruxes to fill the picture, that is the signal to reopen this.
- Evidence is one user, one session, and the person who commissioned the work is the only one who reacted to it. The design generalizes by argument, not by measurement.
- Structural checks — parse, brace balance, missing hooks — cannot see layout. Two of three defects in the prototype were caught only by user screenshots, so visual review is load-bearing for this artifact rather than optional.

## Source
- Session: figure-out session on whether figure-out should gain a walk-pr-style canvas (2026-08-03), including four built prototypes and an independent re-derivation whose divergence is absorbed above.
- Related: 20260803-delete-defines-canvas-mode, 20260803-figure-out-turn-carries-one-concrete-claim, 20260803-prototypes-attach-to-the-station-they-crack
- Related: 20260730-walk-pr-attention-contract-picture-not-document, 20260703-figure-out-fog-discipline, 20260705-front-figure-out-as-door-define-do-loop-as-house
