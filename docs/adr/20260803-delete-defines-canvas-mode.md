# ADR: define's canvas mode is deleted rather than kept or generalised

## Status
Accepted

## Context

`/define` has carried a `--canvas` mode since 2026-05-01: a live browser-rendered side-channel, generated during the interview, whose stated job is *"the visual side-channel they glance at to spot 'that's not what I meant' on intent, flow, scope."*

Two things have changed under it.

**Its contract is the one a later ADR records as falsified.** define's canvas is document-shaped — Tailwind and mermaid over CDN, with *"Everything else… lives behind progressive disclosure (`<details>` expanders, tabs, click-to-reveal)"* — and its own anti-patterns answer the overload risk with more collapsing. `20260730-walk-pr-attention-contract-picture-not-document` lists exactly that answer among its rejected alternatives: *"**Keep the card/document contract with more aggressive progressive disclosure**: Collapsing more of the same text — rejected; tried twice against a real reviewer and failed both times."* The same ADR states the principle for this trade directly: *"the fallback protects a case that barely exists while keeping a falsified presentation sanctioned."*

**The interview it was built for no longer exists.** define was once the whole front end. It now delegates understanding upstream — `define/SKILL.md`: *"If the transcript lacks shared understanding, invoke `manifest-dev:figure-out` first"* — and keeps only encoding: *"figure-out reaches shared understanding of the problem; /define handles manifest-specific encoding judgment calls… Elicit whatever the conversation left unset — these are encoding decisions, not re-investigation."* The misalignment its canvas guarded against now surfaces during figure-out, which is where the glance-check belongs.

Corroborating but not load-bearing: `git log --follow` shows the file created 2026-05-01 and last substantively changed within days of that, with every later touch a one- or three-line reword carried by an unrelated commit. Over the same window `figure-out/SKILL.md` took a dozen substantive commits and walk-pr's canvas was rebuilt whole. Its own activation gate also excludes the workflows the repo now pushes — amendment mode and any autonomous run.

The status quo's job was tested before deciding, as `SKILL.md` requires. The job is still wanted; the venue moved.

## Decision

Delete `/define`'s canvas mode: remove `references/CANVAS_MODE.md`, the `--canvas` entry in the argument hint and the flag table, the three README mentions, and the copies in the per-CLI distributions.

Deletion is not pure subtraction, and one edit is substantive rather than mechanical: `figure-out/references/SCRATCH.md` names the deleted file inside a load-bearing guard — *"Do not force content through `define/references/CANVAS_MODE.md`'s HTML/Tailwind/Mermaid machinery"* — and must be repointed at figure-out's own canvas reference rather than left dangling.

This decision stands on its own evidence and does not depend on figure-out gaining a canvas. If that had been rejected, define's canvas would still be the falsified contract guarding a moment that has moved upstream.

## Alternatives Considered

- **Keep it as it is**: Rejected — a flag costs nothing when unused, but keeping it sanctions a presentation contract this repo has already falsified against a real reader, and points users at it from three README surfaces.
- **Move it into figure-out**: Rejected — the artifact worth having in figure-out is a different design with a different lifecycle and a different subject. What transfers is the *lifecycle* answer (live regeneration on meaningful events, auto-reload), not the shape, and that transfers as an idea rather than as a file.
- **Generalise it into shared canvas machinery for define, figure-out and walk-pr**: Rejected, and already rejected twice in this repo — by `SCRATCH.md`'s refusal to reuse the machinery for heterogeneous content, and by `20260730`'s rejection of a shared generator because *"a fixed map schema pushes every PR toward the same topology and adds a runtime dependency."* The plugin split makes it worse: a shared asset would have to be duplicated across `manifest-dev` and `manifest-dev-tools` anyway.
- **Deprecate rather than delete** (leave the file, drop it from the READMEs): Rejected — it leaves maintained-looking product code with no consumer, which is how it reached this state in the first place.

## Consequences

### Positive
- One fewer maintained HTML surface, and no sanctioned path back to a presentation contract that has failed twice with a real reader.
- `/define` stops advertising a capability that belongs to the stage before it, which matches what the skill now actually does.
- Removes the CDN dependencies (Tailwind, mermaid) that this repo otherwise avoids.

### Negative
- A user-visible capability disappears from three README surfaces; anyone who used it loses it with no direct replacement until figure-out's canvas ships.
- The evidence for disuse is the absence of design attention, not telemetry. A stable file can be finished rather than abandoned, and nothing in the repo can distinguish the two.
- The `SCRATCH.md` guard has to be rewritten rather than merely repointed, since its argument is partly about *that specific machinery*.

## Source
- Session: figure-out session on whether figure-out should gain a canvas (2026-08-03); user ruled the deletion after establishing that define no longer holds the interview the canvas served.
- Related: 20260803-figure-out-gains-an-optional-canvas
- Related: 20260730-walk-pr-attention-contract-picture-not-document, 20260705-front-figure-out-as-door-define-do-loop-as-house
