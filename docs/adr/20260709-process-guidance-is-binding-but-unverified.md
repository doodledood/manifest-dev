# ADR: Process Guidance is binding but unverified

## Status
Accepted

## Context
The manifest schema carries two layers with different softness: the Initial Approach ("initial direction, not rigid plan" — /do may pivot away from it) and Process Guidance. The suite described Process Guidance inconsistently: /define's encoding discipline routes must-hold-but-unverifiable success criteria into it ("Process Guidance when they must hold but resist verification. Never fold them into the soft Initial Approach"), while the schema header read "Not gates — guidance for the implementer" and /do's skill never assigned the section any status. The layer /define treats as preserved was presented to the executor as advisory — a silent path for user-pinned criteria to be dropped while every verifiable gate still passes.

## Decision
Process Guidance items are **binding constraints on how to work during execution**. They must hold throughout a /do run even though no verifier checks them. What distinguishes Process Guidance from Acceptance Criteria and Global Invariants is verifiability, not authority: gates are binding *and* verified; Process Guidance is binding *and* unverified. Only the Initial Approach is soft. Skill and schema wording aligns to this reading (schema header names PG binding-but-not-verified; /do honors PG throughout and may not pivot away from it).

## Alternatives Considered
- **Process Guidance as advisory**: Keep the "guidance, not gates" reading — deliberately toothless so that task-file Defaults, which auto-flow into PG without much review, cannot dictate execution. — Rejected: PG is also the designated home for criteria the user pinned by reacting to something concrete during figure-out, which are success criteria; an advisory PG silently drops them. The Defaults concern is handled by user review at manifest approval, not by weakening the whole layer.
- **A separate preserved section for reaction-pinned criteria**: Split "must hold, unverifiable" items into a new binding section, leaving PG advisory. — Rejected: adds a manifest section whose semantics duplicate what PG already claims in /define's own encoding discipline; one binding-but-unverified layer is enough.

## Consequences

### Positive
- User-pinned unverifiable criteria (taste, style, "I'll know it when I see it" reactions) survive execution instead of silently eroding.
- The manifest's authority model becomes two-valued and legible: binding (AC/INV/PG) vs soft (Initial Approach).

### Negative
- Task-file Defaults that land in PG bind execution too; a stale or inapplicable Default now constrains /do until the user removes it at review.
- No verifier enforces PG — compliance rests on the executor honoring the manifest, so violations surface only through human review.

## Source
- Grounding: suite-alignment review of define/do cross-references — /define's encoding discipline and CONTEXT.md's glossary already treated Process Guidance as a constraint layer while the schema header and /do read it as advisory.
- Related: glossary entry "Process Guidance" in CONTEXT.md
- Related: 20260709-do-keeps-default-execution-log-manifest-stays-contract
