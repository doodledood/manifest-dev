# ADR: manifest-dev owns a project North Star surface

## Status
Accepted

## Area
North Star

## Context
Everything manifest-dev installs is about building: `CONTEXT.md` holds vocabulary, `docs/adr/` holds decisions, a Manifest scopes one task and resets every run. Nothing owned the level above the task — who the project is for, what it promises, how it makes money, how people find it, what winning means — so Appetite and priority calls consulted whatever the operator happened to be holding that day, which is the same not-self-contained failure the glossary and ADR wiring already solve for vocabulary and decisions.

The layer was already steering, unowned. This repo's `docs/CUSTOMER.md` is resident in every session via the project context file import, and a survey of the ADR corpus found six records steering task-level decisions by citing it or carrying `Area: Positioning` — every citation invoking a stance, none a metric. The corpus also named a consumer with no supplier: the Ticket Store's relationships note that comparing impact across Efforts "needs something the destinations alone don't supply." Separately, an independent working-out of the same question over published strategy craft (Rumelt's strategy kernel, the working-backwards promise document) converged on the same surface and refined its field form.

## Decision
manifest-dev owns a **North Star**: one resident, root-level `NORTH_STAR.md` per repo — a standalone strategy doc a stranger can read whole, splitting detail into adjacent linked docs only when a section outgrows it.

- **Nine fields**: Diagnosis (the barrier, and the one sentence that would change everything if false); What this rests on (the handful of falsifiable assumptions); Who it's for, with an explicit not-for; Promise (the sentence a stranger reads at the moment they decide); How they arrive (the arrival-offer pair, not bare channels); Money — or what it feeds where there is none; Winning, and the number watched; Never; Open (questions no field holds). Belief height is the ruler between them: diagnosis false = pivot, assumption false = one lane dies, task fact false = redo the task — task facts live in the Manifest and reset.
- **Informs, never binds.** The one binding channel stays what exists: `/define` routes a Never whose violation would be unsafe or irreversible to a Global Invariant.
- **Produced and maintained by the suite, owned by the project.** `init-context` installs the doc, seeds it from evidence the repo already carries, asks only cheap statables, and leaves the rest honestly empty; `figure-out` fills hard fields one session per question and its docs mode carries updates as a capture beside glossary and ADR offers. Per the criteria-and-cadence cut of `20260809-adr-conventions-ship-as-project-knowledge`, the project owns the full form too: `init-context` emits a self-contained `docs/NORTH_STAR_CONVENTIONS.md` beside the doc, and where it exists it governs the form — the same precedence the ADR conventions carry, with the shipped reference as the default for projects without one — while the doc's own header and the installed project-context-file section carry the always-resident minimum. Only cadence stays in the skills.
- **Consumers**: every session by residency, marketing and sales work included; `next-ticket` weighs cross-Effort priority against Winning; a marketing/GTM define task file gates public claims against Promise and Never.
- **Boundaries**: the portfolio (which project gets the operator's time) lives above any repo; live readings stay out — provenance dates only; an operator's own validation pipeline is a seed source, never shipped machinery.
- **In this repo**, `NORTH_STAR.md` replaces `docs/CUSTOMER.md`; records citing the old path get link repairs in place, which the conventions permit.

## Alternatives Considered
- **A strategy section in `CONTEXT.md`**: rejected — `20260809-glossary-stays-resident-with-an-under-produced-seed` records residency as affordable only while that file stays small, with splitting as the recorded fallback; and the glossary defends misreading where this defends mis-deciding — different trigger, different reader.
- **Taste entries as the home**: rejected — `20260810-universal-discipline-belongs-in-the-prompt` records that machinery misfiring in kind on a rule that was not a personal preference; a project's standing direction binds whoever works in it and is nobody's taste.
- **A de-gated Manifest as standing direction**: rejected — `20260727-shape-up-adoption-boundary` already records that a Manifest with its gates removed loses its load-bearing half.
- **A per-Manifest promise field**: rejected — a commitment to whoever pays persists across runs, so it would be copied into every manifest or go stale in the first; the standing home is what makes a per-run reference possible.
- **Do nothing**: rejected on the corpus's own evidence — the stance layer already steers six recorded decisions while living in a file no schema owns, no skill produces, and no other project gets.

## Consequences

### Positive
- Appetite and cross-Effort priority gain the denominator they lacked; a session writing marketing copy anchors on the same doc as one cutting scope.
- A repo initialized by the suite is self-contained on direction the way it already is on vocabulary and decisions, for contributors on any stack.
- Direction survives the operator: the doc travels with the repo, and its changes ride PRs with ADRs remembering why.

### Negative
- A resident doc is permanent per-session cost; the under-produce rule and the split-on-bulk fallback are the mitigations.
- Nine fields invite form-filling; the four-state marking (see `20260820-north-star-lines-carry-states`) exists to keep invented answers out, and remains untested beyond this portfolio.
- A field nothing consults is possible; the admission bar for future fields stays "a consumer that changes behavior" per `20260807-trim-the-manifest-schema-to-fields-that-are-read`.

## Source
- Session: figure-out design session, 2026-08-19–20 (investigation log kept locally).
- Related: 20260820-north-star-lines-carry-states, 20260809-adr-conventions-ship-as-project-knowledge, 20260809-glossary-stays-resident-with-an-under-produced-seed, 20260727-manifest-intent-leads-with-problem-appetite-and-bounds, 20260807-trim-the-manifest-schema-to-fields-that-are-read
