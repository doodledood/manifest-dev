# Canvas Mode — the walk as a picture, not a document

The canvas **is** the walkthrough, and it is a picture: one persistent, PR-specific system map that the whole walk plays out on. It exists to serve the attention contract (see SKILL.md): the reviewer orients visually, meets one idea at a time, and digs into text, rationale, or code only when they choose to. Every earlier instinct toward a document — prose sections, cards, summaries stacked on summaries — was tried and overloaded real reviewers. Do not regress toward it.

## Reader model

The reviewer **lives in the repo** (knows the modules, idioms, naming conventions) but has **zero context on this PR**. Codebase vocabulary is shared ground; vocabulary this PR introduces is not. There is no prose primer: the map itself and the first story steps carry all orientation — the intro caption states the problem in one line, map labels establish the cast, and early steps introduce new concepts as the story reaches them. Element blurbs (behind a tap) hold definitions for whoever wants them. Name things by their real codebase identifiers, never invented abstractions.

## Activation gate

Evaluate **immediately** when `--canvas` is set, before opening the first sub-changeset. If any condition holds, skip canvas behavior and fall back to chat-only /walk-pr (first match wins; conditions 1–2 silent, condition 3 prints one warning):

1. **Trivial diff** — canvas setup cost exceeds the review's information need. Rough threshold: single file with tens of net lines changed.
2. **Non-local medium** — the user isn't at a host with browser access.
3. **No graphical-browser launcher** — none of `xdg-open`, `open`, `start` on PATH. Print: `--canvas requires a desktop environment with a graphical browser; skipping artifact generation`.

If none match: generate the canvas as one self-contained HTML file in the host's temp directory (`walk-pr-canvas-{ts}.html`, `{ts}` = invocation timestamp), open it, and disengage until the paste-back.

## The reference shell

`assets/canvas-reference.html` (relative to this skill) is the canonical embodiment of the target UX — a fully working demo canvas for a fictional PR. Read it before generating: its header comment marks which code is the **interaction shell** (navigation, sheets, auto-save, drawer, completion bundle — proven mechanics, each guarding against a real failure) and which is **PR data** to replace wholesale.

Default: keep the interaction shell, replace the scene and data. What is always bespoke per PR: the map's topology and layout, its visual vocabulary, the story steps and captions, the whys, the element blurbs, the pins, the diff groups and diffs, and the localStorage namespace (always fresh per artifact). Depart from the shell itself when this PR's shape genuinely calls for a different picture or interaction — judged against the attention contract, never back toward a document. There is no requirement on *how* the HTML is produced; only the resulting artifact matters.

Styling the bespoke parts — the map's visual vocabulary, element and edge treatment, captions, sheets — is design work: invoke the design skill for it, bounded by this mode's own lifecycle — its purpose, register, token, and floor decisions apply; its critique loop and screenshot passes do not, because the one-shot contract below forbids polish loops before handover. Where that skill is unavailable, hold the floors by hand: contrast by number, one spacing rhythm, uniform control heights, visible focus.

## The map

The spine is **one system map**: the PR's components and data flows drawn as a spatial diagram (positioned elements with SVG edges), derived from this PR's actual architecture — not a generic template topology. It fills the viewport and stays on screen for the entire walk; every other surface (story captions, pins, sheets, the diff drawer, the completion panel) plays out on or over it, so the reviewer never loses the spatial context they built.

## The story

The walkthrough is a **stepped story played on the map**: each step lights the relevant elements, animates the active flow edges, and shows **one caption of roughly a dozen words**. Steps are chapters of a vertical narrative — the life of a request through the changed system, before/after contrasts, the safety nets — not file groups. Rationale is first-class but hidden: each step carries a "why?" a tap away (the author's design reasoning — especially compatibility and surface-reduction decisions), and each map element carries a blurb. The reviewer never faces more than a caption of unrequested text.

## Pins — the review topics

Concerns are **pins placed on the map** where they live. Reaching a pin's step opens its sheet: a one-line question in codebase vocabulary, a one-line recommended call, a collapsed "why?" with the file anchor, **one-tap answers** (agree-as-recommended / skip), and a free-text box. Quick-tap answering is what makes a many-topic walk finishable; the free-text box is where the reviewer pushes back.

## Comment-anywhere

Every map element and every step caption is clickable: a sheet opens with a short explainer and an auto-saving comment box, and a saved-note badge marks it on the map. Empirically this channel carries the highest-value review input — design-deviation questions, objections the authored pins never anticipated — so it is not optional chrome.

## Diffs as evidence

Diffs live in a **dismissable side drawer** (backdrop click + Esc + visible ✕ — never a full-screen overlay), grouped by story chapter, one collapsed row per file, rendered lazily on expand as proper dark-themed line-level diffs. Diff is evidence the reviewer summons to verify a claim, never the default exposition.

## Lifecycle

**One-shot, opened immediately.** Generate the full canvas once — every step, pin, blurb, and diff embedded — open it, and hand it to the reviewer. No preflight browser verification, no screenshot pass, no approval loop: the artifact optimizes time-to-first-review, and the reviewer is its first viewer. No mid-walk regeneration — local JS owns all pacing, and state (current step, answers, notes, open/closed panels) persists in localStorage across reloads under the artifact's own namespace.

Chat stays empty during the walk. The agent re-engages only when the user pastes the **Copy my review** bundle — the consolidated pin answers and free notes with their anchors — which feeds the end-of-walk triage that SKILL.md owns. After posting, the artifact is disposable.

## Failure handling

Any canvas-related failure is **non-blocking**:

- File write fails → warn once, fall back to chat-only walkthrough.
- Browser launcher fails → print the `file://` path, continue.
- Clipboard write fails → the artifact pre-selects the bundle in a visible block (the shell already does this).
- PR-post failure → keep the drafted plan, surface the API error inline, offer retry.

## Anti-patterns

- **Document creep.** A prose primer, per-changeset cards, boundary-view paragraphs, always-visible topic text — any surface where unrequested text carries the walk. The map and its taps carry everything.
- **Chat duplicating canvas content.** Don't restate captions, whys, pins, or diff content in chat; chat sees only the final bundle.
- **Mid-walk regeneration.** The canvas is one-shot; local JS handles pacing.
- **Generic map.** A template topology with this PR's labels swapped in. The map is derived from this PR's actual components and flows; a reviewer who knows the repo should recognize the system on sight.
- **Wall of text in a caption.** A caption that needs a second sentence is a caption plus a hidden why, or two steps.
- **Diff as exposition.** Diff hunks visible by default anywhere. Diffs render only inside the drawer, only on expand.
- **Full-screen or sticky overlays.** Every layer (sheet, drawer, completion panel) dismisses via Esc and a visible control, and the map remains the ground underneath.
- **Stale or shared state.** Reusing a previous artifact's localStorage namespace, or letting test interactions ship as saved answers.
- **Invented abstraction in place of codebase vocabulary.** Pins and blurbs name `notifier`, not "the propagation manager", when `notifier` is what the repo calls it.
- **Verification theater.** Screenshot passes, agent-side click-throughs, or polish loops before handover — the contract is open-and-review.
