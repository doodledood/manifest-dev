# ADR: Prototyping and scratch are one mechanism; scratch mode is deleted

## Status
Accepted

## Area
figure-out

## Context

figure-out carried two ways to produce a concrete artifact mid-investigation, separated by a distinction stated in `SKILL.md`: *"This is a one-shot probe, not scratch mode: here the artifact leads — it generates a criterion not yet settled — where scratch mirrors understanding already reached."*

Two findings broke that distinction.

The first is lived. A thorough session reached a read; the maintainer then rendered what the read implied — a CLI's command executions, in HTML — and it exposed several points where agent and user had never actually agreed. By the stated distinction that artifact was a mirror: it reflected understanding already reached. It behaved as a leader: it generated criteria that did not exist before it.

The second is in the text. `SCRATCH.md`'s own purpose line describes leading, not mirroring — *"let the user glance at it mid-session to catch 'that's not what I meant' before it's load-bearing."* Catching "that's not what I meant" is generating a criterion not yet settled. The file contradicted the distinction on its first line.

Scratch was also barely used. The plausible cause is not that the capability was unwanted but that it was mis-billed: sold as grounding a long session with a mirror, a benefit nobody reaches for, when the felt need is *show me what this will actually be so we can see whether we still agree*. Under the merge that framing is the mechanism's own, so the mis-billing is repaired rather than carried.

Scratch was self-contained: `references/SCRATCH.md`, the `--scratch` flag in the argument-hint, one loading-table row, and the contrast clause above. No other skill referenced it and no test asserted it.

## Decision

One mechanism, hosted in the spine, stated goal-first: **find the disagreement before the thing is built, where changing it costs least.** Scratch mode, its flag, and its reference file are deleted.

The mechanism's lines are kept only where each counteracts a default the model actually has, so the rest derives from the goal:

- **Stating the output is owed; rendering it is offered.** Producing waits on the user's yes; the offer does not. A declined offer is an answer and the read still lands, with what went unsensed named as an accepted default. Not offering is the only failure.
- **Offer as soon as the output's shape is guessable, not once settled.** A wrong concrete thing surfaces disagreement faster than a vague correct sentence, and early is where changing costs least.
- **Show, don't narrate.** The artifact is the output, not prose about it.
- **Concrete at the joints, thin between them.** Take one instance to its seams — the transitions, the handoffs, the places a choice could have gone another way — because that is where disagreement lives. A document is its outline plus the passages where the claim is at stake, never the written document.
- **Authored, never executed.** The moment it would have to run, it has become the work. A hypothesis that can only be answered by running something is an experiment, which the spine already routes to a throwaway location.
- **Put it on a page.** Not for HTML's expressiveness but because a prototype inside a chat turn is still the agent talking and gets read in agree-along mode; a separate page is an object the reader inspects. The prompt says *page* rather than *artifact*, since an HTML file and its path works on every CLI this ships to and an artifact surface does not.
- **Fidelity where the disagreement lives**, low elsewhere — the existing placement rule, unchanged. Polish is not the axis: a landing page whose feel is in question must look like something; a flow whose steps are in question must not.
- **Disposable**, never written into the project's own files.
- **With no user to offer to**, state the output exactly and render nothing.

Scratch's session-long cadence is not ported. Its throwaway-location discipline survives as a clause.

## Alternatives Considered

- **Keep both and re-bill scratch**: — Rejected. Attractive while the diagnosis was mis-billing, since deleting on low usage destroys the evidence that would say whether the artifact or the pitch was the problem. It fails on the prior question: the two were never two things. Re-billing would have kept a distinction that does not survive its own first line.
- **Keep scratch's maintained mirror as a cadence of the merged mechanism**: — Rejected. The only usage evidence in existence says it goes unused, and a cadence nobody invokes is a line every session carries and no session needs.
- **Extract the mechanics to a `references/` file**: — Rejected. The trigger is a sensing act, and a deferred file can only be read after a load the trigger was meant to gate — the failure recorded in 20260703-progressive-disclosure-triggers-live-in-loading-layer. Net size roughly breaks even once `SCRATCH.md` is gone.
- **Ship a table of output forms** (a CLI becomes a session transcript, a record becomes one filled row, and so on): — Rejected as content, kept as a sentence. All of it follows from *take one instance to its seams*; what the table was really doing was breaking the UI framing, and four examples in a sentence do that without a taxonomy's shape, which would make an unlisted output look exempt rather than covered.
- **Make ELI5 the default register** (big pictures, few plain words): — Rejected. An explainer aims at understanding and drops detail to get there; a prototype aims at disagreement, and detail is what a mismatch catches on. Same artifact, opposite pressure. What survives the rejection is *show, don't narrate*.

## Consequences

### Positive

- One mechanism with one goal replaces two concepts split along a line that did not hold, so no session has to decide which of them it is in.
- The capability reaches the default invocation. Scratch was opt-in behind a flag; nothing now depends on the user knowing to ask.
- The prompt states a goal and derives from it, so an output shape nobody enumerated is covered rather than exempt.

### Negative

- `--scratch` disappears; a user who types it gets an unknown flag. Nothing else passes it.
- The session-long maintained artifact is gone outright. If long sessions turn out to need a continuously updated mirror, it has to be re-derived rather than re-enabled.
- Offers are uncapped, so a long session may interrupt several times. Offers are one sentence and declinable, which is the reason to accept this — and it is the part of the design most likely to need revisiting.

## Source
- Session: figure-out investigation of whether prototyping generalizes past UI (2026-08-26). Investigation log at `~/.manifest-dev/logs/figure-out-log-20260826-115243.md`.
- Related: [20260826-sensing-the-output-is-a-precondition-of-naming-a-read](20260826-sensing-the-output-is-a-precondition-of-naming-a-read.md)
- Related: [20260803-prototypes-attach-to-the-station-they-crack](20260803-prototypes-attach-to-the-station-they-crack.md) — deprecated; drew the same mirror/leader distinction this record retires
- Related: [20260703-progressive-disclosure-triggers-live-in-loading-layer](20260703-progressive-disclosure-triggers-live-in-loading-layer.md)
- Related: [20260803-delete-defines-canvas-mode](20260803-delete-defines-canvas-mode.md) — its consequence about rewriting `SCRATCH.md`'s guard is moot once the file is gone
