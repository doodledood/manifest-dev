# ADR: The undiscussed-surface sweep lives in figure-out's read-naming checkpoint

## Status
Accepted; the checkpoint it places the sweep in now also carries the output-sensing precondition added by [20260826-sensing-the-output-is-a-precondition-of-naming-a-read](20260826-sensing-the-output-is-a-precondition-of-naming-a-read.md)

## Area
figure-out

## Context

Completed figure-out→define→do runs produced finished results the user disliked, UI-heavy cases especially. The sessions were framed around a mechanism, so the surfaces the user ultimately sees and judges never entered the conversation: figure-out's one-shot probe offers a mock only on *sensed* taste-shaped fog, and ground that never comes into view cannot be sensed. The pre-read scouting discipline did not catch it either — it is keyed to fog whose contents would break the read's correctness, and a disappointing UI does not overturn a read about a mechanism. The result: no prototype offer, no visual criteria in the manifest, and the user first met the result's look and feel in the finished artifact.

The fix is a sweep: before naming a read that implies making something, enumerate the surfaces the user will see, touch, or judge in the end result that the session never discussed, and give each a fate — brought into the conversation (where the one-shot probe then fires naturally for taste-heavy ones) or named out loud as an accepted default. The question this record settles is where that sweep lives.

## Decision

The sweep is hosted in the spine, as a widening of the existing scouting line in the "Before you name it" checkpoint — not as a new section, and not as probe-file content.

Three grounds:

- **Timing** — the sweep must fire at read-naming, a checkpoint the spine already owns and every session reliably passes through. Probe files load at session start as awareness ("most won't apply"), which is exactly the under-weighting posture the observed failure demonstrates.
- **Generality** — the failure class is any user-judged surface left undiscussed, not UI specifically, and figure-out has no probe file for non-code shapes such as writing; probe-file placement would leave those uncovered.
- **Prompt discipline** — the change counteracts an observed model default (following the frame the topic arrived in), and widening the existing line keeps the rule, its bounds, and the checkpoint together; a new standalone section would be a wall built around one observed failure.

The widened line inherits the section's existing scaling language, so the sweep stays proportional to what rides on the read. A probe-file sharpening still rides alongside: figure-out's `tasks/FEATURE.md` names the archetype instance (user-visible surfaces whose look and feel the conversation never touched), the way overlay probes already sharpen base ones. On the define side, a `UI.md` task file supplies standing rendered-result quality gates, covering the path that enters at `/define` without a figure-out session.

## Alternatives Considered

- **Probe-file placement only** (add taste angles to `tasks/FEATURE.md`/`CODING.md` and stop): rejected — probe fuel is loaded at session start and explicitly weighted as optional awareness, the exact posture that failed; and it covers only the shapes that have probe files, missing non-code work.
- **A new standalone spine section**: rejected — over-correction around one observed failure; the sweep is the same pre-read scouting the checkpoint already performs, extended from the read's correctness to the result's reception, so it belongs in that line.
- **Define-side only** (standing UI gates, no figure-out change): rejected as the whole fix — gates catch a bad rendering after it is built, but the criterion the user holds surfaces cheapest during figuring-out, where a mock can be reacted to before anything binds; define-side gates ship as a complement, not the mechanism.

## Consequences

### Positive

- Undiscussed user-judged surfaces are enumerated at the one checkpoint every session passes, so the one-shot probe's mock offer gets its chance on taste-heavy ground, and accepted defaults become explicit instead of silent.
- The fix reaches every topic shape, including ones with no probe file, and autonomous runs surface the same ground as flagged assumptions.

### Negative

- The spine's read-naming checkpoint grows heavier; sessions whose reads imply no artifact carry a line they never use, and the sweep's proportionality now rests on the section's scaling language holding.
