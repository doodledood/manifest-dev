# ADR: figure-out gains an optional canvas whose spine is the crux tree and whose subject is the frontier

## Status
Superseded by 20260818-chat-surface-replaces-the-crux-map-canvas

## Area
figure-out

## Context

Long figure-out sessions deliberately hide accumulated state from chat. `SKILL.md` keeps the Evidence Ledger, belief register, and crumb-and-fog tracking under the hood, while `20260727-figure-out-adopts-a-default-turn-shape` limits each turn to one point. That lowers turn load but leaves no direct view of where the investigation stands.

`references/LOG.md` preserves `Current belief`, `Open threads`, `Fog`, `Out of scope`, and `Next crux`, but its append-only chronological form serves recovery after context loss. Reading current position from it requires reconstructing and comparing several entries. The state exists; the log holds it in the wrong shape for a person mid-session.

The existing canvas designs establish useful boundaries. define's document-shaped canvas relies on progressively disclosed text, a presentation contract later rejected by `20260730-walk-pr-attention-contract-picture-not-document`. walk-pr's replacement supplies a useful interaction grammar—a persistent spatial map, one active idea, detail behind an action, notes anywhere, and one bundle out—but not a reusable lifecycle. A PR can be mapped once because its content is already known; an investigation must refresh as its frontier moves.

A current-state chat view is cheaper and remains the fallback, but it reproduces the reading surface the canvas is meant to relieve. The main design risk is the opposite: drawing a crux tree can reward manufacturing nodes, repeating the premature decomposition recorded in `20260703-figure-out-fog-discipline`. The canvas is therefore optional and constrains fog, scoring, and disclosure directly.

## Decision

figure-out gains an optional canvas, loaded on an explicit flag and off by default, carried by its own reference file and its own template asset under `manifest-dev`.

- **Spine is the crux tree; subject is the frontier.** The tree is the ground because it is the only structure every figure-out session has — unlike a PR, an investigation has no shape until it has been done. But the tree is not the point of the picture: where we stand, what is still open, and how much fog remains is. The current crux is unmistakable at a glance, and a focus mode softly recedes everything else.
- **Fog renders as territory, never as nodes.** `SKILL.md` forbids slicing fog into sub-questions before they are statable, so a picture that drew fog as boxes would break the rule it exists to display. Extent is visible; contents sit behind an explicit action.
- **Nothing on the surface scores node count.** This is the concrete concession to the premature-decomposition objection: a visible tally of nodes rewards manufacturing them.
- **Detail is never unrequested.** One line per point, with the rest behind an explicit action, and one detail open at a time.
- **Notes live outside the file**, keyed by stable station id under a namespace fixed for the session, so updating or rewriting the artifact never destroys what the user typed. This inverts walk-pr's fresh-namespace-per-artifact rule, which is correct there because each artifact is one walk.
- **One bundle out; chat stays the wire.** A page opened from a file cannot reach the agent process and a runtime dependency is out, so the return channel is the clipboard and one paste per turn. Chat carries every turn, so switching away from the canvas never loses the deliberation; the canvas refreshes only when the state it depicts changes.
- **The asset ships as a template and is a starting point, not a specification.** Adaptation per session and per user is expected and allowed — sessions differ in shape, subject and what the user wants from them. Adaptation is judged against the contract above (frontier as subject, fog as territory, no node scoreboard, no unrequested text, notes outside the file, one bundle out, no runtime dependency), never against fidelity to the template. This follows walk-pr's own posture toward its shell while replacing "never back toward a document" with the contract stated here.
- **Data is isolated from shell.** A refresh replaces the small session payload rather than rewriting the interaction shell; without that split, frequent refresh is not affordable.
- **Refresh uses an explicit, guarded reload path.** After data replacement, keyboard users press the visible **R** shortcut; touch-only users use the browser's reload control. An already-loaded `file://` page cannot detect replacement without polling or a server; the explicit step preserves the no-dependency boundary and avoids a disruptive reload loop. When storage is unavailable and notes exist only in memory, **R** opens the return bundle and browser-native reload triggers the page's unload warning, which the user cancels until the bundle is returned.
- **No CDN or runtime dependencies.** This canvas needs no diff rendering or syntax highlighting, which is most of walk-pr's weight.

## Alternatives Considered

- **A current-state view rendered in chat on demand** (leading read, confidence, open crumbs, fog, next crux, off the existing register): Rejected as the primary surface because a text block re-renders the same reading load the canvas exists to move off the page. It remains the cheaper fallback if the canvas does not earn its upkeep.
- **Reuse walk-pr's `canvas-reference.html`**: Rejected on packaging. `marketplace.json` ships `manifest-dev` and `manifest-dev-tools` as separately installable, so a Claude Code user who installed `manifest-dev` alone would have a dangling dependency, even though the pi and codex distributions flatten both into one tree.
- **One-shot generation, as walk-pr does**: Rejected — impossible. Showing current position requires the artifact to stay current, so this canvas cannot take walk-pr's escape hatch and inherits refresh cost instead.
- **Frontier alone as the spine** (current read, crumbs and fog with no tree): Rejected — it shows where we are but not where we are going or what has been settled, which is half the reported pain. Kept as the *subject* of the tree spine instead.
- **Generalise define's canvas into shared machinery for all three skills**: Rejected; the repo has already declined this twice — `SCRATCH.md` refuses to *"force content through define/references/CANVAS_MODE.md's HTML/Tailwind/Mermaid machinery,"* and `20260730` rejected a shared generator because *"a fixed map schema pushes every PR toward the same topology and adds a runtime dependency."*
- **Do nothing and let the new turn shape bed in**: Rejected because the turn shape deliberately hides the accumulated state. Waiting cannot make that state visible.

## Consequences

### Positive
- Session position becomes visible without violating the decision to keep the apparatus off the chat surface — a second surface, not a louder turn.
- The interaction grammar is inherited from a design validated by a completed real review, rather than re-derived.
- Isolating data from shell makes per-turn updating affordable, and keeping notes out of the file makes regeneration safe by construction.
- Default off means a user who never passes the flag pays nothing, which preserves figure-out's role as the zero-enrollment Door in `20260705`.

### Negative
- A second maintained HTML asset in a repo whose base rate for this class is one abandoned and one validated at n=1, and — as `20260730` already booked — *"interaction regressions in it ship silently since there is no preflight verification."* This one is worse placed than walk-pr's, because it must regenerate rather than being generated once.
- The premature-decomposition pull is mitigated (fog as territory, no node scoreboard) but not removed. If a session starts manufacturing cruxes to fill the picture, that is the signal to reopen this.
- Validation coverage is narrow: one investigation and one reader. The design generalizes by argument, not broad measurement.
- Structural checks — parse, brace balance, missing hooks — cannot see layout. Two of three defects in the prototype were caught only by user screenshots, so visual review is load-bearing for this artifact rather than optional.

## Source
- Origin: figure-out investigation of whether the skill should gain a walk-pr-style canvas (2026-08-03).
- Related: 20260803-delete-defines-canvas-mode, 20260803-figure-out-turn-carries-one-concrete-claim, 20260803-prototypes-attach-to-the-station-they-crack
- Related: 20260730-walk-pr-attention-contract-picture-not-document, 20260703-figure-out-fog-discipline, 20260705-front-figure-out-as-door-define-do-loop-as-house
