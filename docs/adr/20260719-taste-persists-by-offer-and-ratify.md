# ADR: Taste persists by offer-and-ratify, never by silent inference

## Status
Accepted

## Context
manifest-dev persists two kinds of cross-session knowledge: decisions with their rationale (ADRs) and project vocabulary (CONTEXT.md). A third kind had no persistence path: durable personal steering preferences — recurring directional pushback like a standing lean toward low-surface-area changes — which users re-state session after session because nothing carries them forward. The tension is that persisted preference context can degrade deliberation quality: a behavioral prediction of the form "the user pushes toward Y on X-type questions" invites the agent to open at Y instead of arriving at Y, collapsing the deliberation the workflows exist to run, and it self-seals — once the agent preempts the preference, the corrective pushback that would test or update it stops occurring. In autonomous runs a wrong preference prior compounds with no user present to catch it.

## Decision
Taste persists only through an offer-and-ratify flow. When the agent detects a recurring or emphatically stated directional preference, it drafts the entry in boundary form — the preference, its rationale, and the condition that would flip it (e.g. "prefer the smallest change that stays clean; go bigger only when the small version leaves debt costlier than the restructure") — and offers it to the user. On acceptance, the entry is written to a marked section of the scope-correct harness memory file: the user-level memory file (e.g. `~/.claude/CLAUDE.md`, or the AGENTS.md equivalent on other harnesses) for cross-repo personal taste, the project-level memory file for project standards. When scope is ambiguous, the offer asks. The agent never infers a preference and applies it silently; the user's ratification is what converts an observed pattern into standing context. Boundary form is required because a bare preference line over-triggers — the rationale and flip condition are what let future sessions exercise judgment at the edges instead of complying blindly. Entries face an earned-entry bar (durable, recurring or emphatically stated, behavior-changing) to keep the always-in-context section small.

## Alternatives Considered
- **Zero-touch learned priors**: the agent observes pushback tendencies and automatically steers future sessions by them — Rejected: unratified behavioral predictions can only be obeyed, not weighed; they pre-slant deliberation toward predicted preference before evidence, self-seal against correction, and compound unchecked under autonomous execution.
- **Dedicated TASTE.md store** linked or imported from the memory files — Rejected for the initial shape: imports inline into context, so a separate file saves no tokens over a marked section, and it adds a file plus link indirection for marginal ownership benefits; extraction to a file remains a cheap later refactor if the section sprawls.
- **Bare preference lines without rationale**: shortest possible entries — Rejected: a naked preference reads as absolute and over-applies to adjacent cases where it is wrong; boundary form keeps the model able to judge when the preference should yield.
- **No persistence (status quo)**: user re-states preferences each session — Rejected: recurring re-litigation cost on every session and a standing obstacle to reduced-supervision workflows, against a one-time ratification cost per pattern.

## Consequences

### Positive
- A recurring pushback converts into standing context at the cost of one ratification, ever — future sessions start already aligned on settled directional preferences.
- The taste store is auditable and user-owned: entries are visible in the memory file, prunable, and deletable wholesale.
- Autonomous runs steer only by rationale-carrying, user-ratified principles, not by inferred predictions — the provenance bar rises with autonomy rather than falling.

### Negative
- Offers interrupt: if the detection gate fires too often the flow adds cognitive load instead of removing it (mitigation lever: batch offers to session end).
- Memory files grow and nothing naturally supersedes a taste entry the way a new ADR supersedes an old one — entries need the earned-entry bar and occasional re-ratification as taste drifts.
- Scope classification (user-level vs project-level) adds a question to some offers.

## Source
- Grounding: recurring cross-session directional preferences had no persistence path; the ratify-only design preserves the deliberation discipline that treats agreement as non-evidence and keeps unvalidated priors out of live contexts.
- Related: 20260708-judgment-layer-is-a-review-time-premise-check (distinct concept — Judgment Layer is a review-time premise check; Taste is a persisted personal preference — the naming boundary is deliberate)
