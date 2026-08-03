# figure-out: canvas mode

An optional second surface for the session — a picture of the investigation, kept current through explicit refreshes, that the user can read, annotate, and hand back. Chat still carries the deliberation; the canvas carries the state chat deliberately hides.

It exists because a turn shows one point and the investigation log is chronological, so neither answers *where are we* — what is settled, what is still open, how much ground is unsurveyed. The canvas answers exactly that and nothing else.

Both surfaces run together. There is no canvas-only mode. Do not announce activation: the user passed the flag, so they know it is on. The two Lifecycle status notices are functional exceptions—one when there is no ground to draw yet, one after replacement when the loaded file needs a reload. Never redirect the user to the canvas, and never thin a turn because it exists—a turn stands on its own for a reader who never opens the file.

## What the picture depicts

**The spine is the crux tree.** It is the one structure every session has: questions, their parents, and what each resolved to. Stations are cruxes — settled, open, ruled out, or the one you stand on now.

**The subject is the frontier.** The current crux, what is still open around it, and how much fog remains — because that is the part the user cannot see from chat. The picture is not a diagram of everything known; it is a view of where the traverse has reached. So the current crux dominates by default rather than sitting as one node among equals, and a focus affordance lets the rest recede.

**Fog is territory, never nodes.** Render it as one region with an extent, not as a list of sub-questions. This is not a drawing preference: the skill forbids forcing a question shape onto fog or slicing it into subtrees before it can be stated, so drawing fog as nodes would encode in the picture the exact move the investigation is supposed to refuse. Its contents sit behind an explicit action; it becomes stations only when it sharpens into real questions.

**Nothing on the surface scores the tree.** No visible count of settled, open, or total stations. A number that goes up rewards splitting a question in two, which is the premature-decomposition failure the skill already guards against — and progress in an investigation is not a quantity of nodes.

## What the reader is owed

**One line per point.** Every point rests as a single claim-carrying line; its detail waits behind an explicit action, and at most one detail is open at a time. This is the same contract a turn owes in chat, for the same reason: the surface is worthless if reaching it costs a wall of text. A canvas that opens into paragraphs has become the document this mode exists to avoid.

**No unrequested text.** Nothing renders because a slot exists for it. Empty slots are skipped, not filled with placeholders.

**Readable on whatever screen they have.** The canvas is opened wherever the user happens to be, so a phone is a first-class target rather than a degraded desktop: the picture, the detail surface, and every control stay reachable and legible at any width, and the page never asks the reader to scroll sideways. A canvas that only works in a wide window fails its reader exactly when they are away from their desk.

## Notes and the way back

**Notes never live in the artifact.** The user's text goes to browser storage, keyed by stable station id under a namespace fixed once for the session. The reason is structural: the canvas is rewritten whenever the ground moves, so anything stored inside the file would be destroyed by the next refresh. Fixing the namespace per session — rather than per artifact — is what makes refreshing safe, and it is the one place this mode deliberately departs from `walk-pr`'s canvas, which regenerates once and therefore wants a fresh namespace each time.

**Chat stays the wire.** A page opened from a file path cannot reach the agent, so the return path is the user's clipboard: one action collects every note with the station it was left on, and one paste brings the lot back. Read what returns as answers to the questions the notes are attached to, and carry them into the investigation the way any user answer is carried.

**Reacting is optional.** The user may work entirely in chat and treat the canvas as a reference, or leave chat, annotate, and return. Both are the mode working.

## Artifacts attach to what they were built to crack

A prototype, mock, or probe produced mid-investigation belongs to the crux or fog patch it was built to settle, and the user's reaction to it belongs in that station's own note. When a station has several prototypes, the newest appears first.

The reason is what happens downstream: a reaction is often a criterion the user could not state in the abstract, and a criterion that arrives detached from its question cannot be encoded as one — `/define` needs to know which question the reaction answers to turn it into a gate. Attaching it keeps that link without anyone having to remember it.

Artifacts belonging to the whole session rather than to any one question — the investigation log, a scratch mirror — hang off the session rather than off a station. Give them no separate surface; they are reachable from the header.

The canvas points at these artifacts; it never hosts one. When updating the canvas and building a probe compete for the same turn, the probe wins — it can settle a question, and the canvas only shows where the question sits.

## Lifecycle

Create the artifact as one self-contained HTML file in the host's temp directory when the flag is parsed and the session has ground worth drawing, and open it. Before then — flag passed, nothing surveyed yet — say the canvas will appear once there is a traverse to show, and carry on in chat.

Refresh it when the picture would otherwise be wrong: a crux resolved, a new question opened, fog sharpened into stations, the frontier moved. Not every turn, and never mid-thought — a canvas that changes while the user is reading it is worse than one that lags a turn behind.

After replacing the data, tell the user the canvas is updated: press **R** when a keyboard is available; on a touch-only screen, use the browser's reload control. If the browser warns before reloading, cancel and follow the page-only-note fallback below. An already-loaded `file://` page cannot observe its own replacement without polling or a server, and both are worse than one explicit reload step. If the tab is gone, reopen the same path. Notes survive because they were never in the file.

## Failure handling

Every failure here is non-blocking. The canvas serves the investigation and never stops it.

- Writing the file fails → say so once and continue in chat.
- No browser opens it → give the path and continue.
- Clipboard write fails → the artifact shows the bundle as selectable text; the user copies manually.
- Browser storage is denied — some hosts refuse it to a page opened from a file path → the canvas still renders and notes still work for as long as the page stays open. **R** opens the return bundle instead of reloading while page-only notes exist, and browser-native reload raises its unload warning. Return the bundle first; after successful clipboard copy, **R** is armed to reload. If clipboard access also fails, copy the selected bundle before accepting the browser warning. Otherwise let the picture lag. Degrade to that, never to a blank sheet.
- The refresh would land mid-thought → let it lag and refresh at the next natural break.
- Reload does not take or the tab is gone → give the same file path to reopen and continue in chat.

Never make the user fix the canvas to keep the session going.

## The template, and departing from it

`assets/canvas-template.html` (relative to this skill) is a working canvas on a throwaway topic. Read it before generating: its header comment marks which code is the **interaction shell** — computed layout, the station sheet, the accordion, note persistence, the bundle, pan and zoom and focus — and which is the **session's data** to replace.

It is a starting point, not a specification. Sessions differ in shape and in what the user needs to see: a long traverse with one live frontier wants a different emphasis from a wide one that has just forked, and users differ in how much picture they want at all. So adapt it — the topology, the emphasis, the vocabulary on the stations, and the shell itself where this session genuinely calls for a different picture.

What adaptation is judged against is the contract above, not fidelity to the template. Every point of it binds whatever else changes:

- the frontier is the subject, and the current crux dominates by default
- fog is territory, never nodes
- nothing on the surface scores the tree
- one line per point, detail behind an explicit action, one open at a time
- no unrequested text
- notes live outside the file, keyed by stable station id under a session-fixed namespace
- one action returns everything the user wrote, with the station it was left on
- usable at any screen size, phone included — nothing reachable on a wide window becomes unreachable on a narrow one
- no runtime dependency: no network, no build step, no server — it opens from a bare file path

A canvas that keeps the template's structure and breaks one of these has failed. One that departs from the template freely and holds all of them is working as intended.

There is no requirement on *how* the file is produced. Only the artifact matters.

## Composition

It composes the same way under `--autonomous` and `--team`. The artifact is still worth keeping in an unattended or multi-party run — it is where the session's accumulated state is legible, and someone reads it eventually — but the surfaces that wait on a person go quiet: do not stall for a reaction that is not coming, and treat an un-annotated canvas as the normal case rather than a missing answer. Under `--team` the counterparties are in Slack and no single reader owns the notes, so the canvas serves the operator in the local session; the deliberation itself stays where team mode puts it.

## Anti-patterns

- **A document with sections that expand.** The shape this repo has already falsified against a real reader twice. If the surface reads as prose to work through, it is the wrong artifact.
- **A generic tree with this session's labels swapped in.** The picture is derived from this session's actual questions; the user should recognise their own investigation on sight.
- **Fog sliced into guesses** so it looks like progress.
- **A tally, a percentage, or a progress bar over stations.**
- **Narrating the canvas in chat**, except for the two status notices the Lifecycle requires.
- **Thinning a turn** because the canvas carries the detail. The turn stands alone.
- **Notes written into the file**, which the next refresh destroys.
- **A desktop-only picture** — fixed widths, a detail surface wider than the screen, or controls that fall off the edge on a phone.
