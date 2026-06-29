# ADR Format

Architecture Decision Records capture significant decisions with their context, alternatives, and consequences. Based on the MADR (Markdown Any Decision Records) standard.

## Template

````markdown
# ADR: [Decision Title]

## Status
Accepted

## Context
[What situation motivated this decision? What constraints, requirements, or tensions existed?]

## Decision
[What was decided and why this option was chosen.]

## Alternatives Considered
- **[Alternative A]**: [Description] — [Why not chosen]
- **[Alternative B]**: [Description] — [Why not chosen]

## Consequences

### Positive
- [What becomes easier or better]

### Negative
- [What becomes harder or is traded away]

## Source
- Session: [transcript / conversation reference]
- Manifest: [manifest file path, if any]
- Related: [Supersedes / Superseded by / See also]
````

## File Naming and Location

Write ADRs to `docs/adr/YYYYMMDD-kebab-case-title.md` — date prefix using the current date. Create `docs/adr/` lazily on the first ADR if it doesn't exist.

Examples: `docs/adr/20260518-decouple-adr-from-workflow.md`, `docs/adr/20260518-use-madr-format.md`.

**Multi-context repos** (where `CONTEXT-MAP.md` exists at root): per-context ADRs live in the relevant module alongside that context's `CONTEXT.md` rather than the root-level `docs/adr/`.

## Status Lifecycle

ADRs follow a four-state lifecycle: `Proposed` → `Accepted` → `Deprecated` → `Superseded`.

- **Proposed**: Decision drafted but not yet committed. Used when an idea is on the table but the team hasn't fully agreed.
- **Accepted**: Default for fresh ADRs. The decision is in effect.
- **Deprecated**: The decision no longer applies but hasn't been replaced. Use when something was true but the world moved on.
- **Superseded**: A newer ADR replaces this one. Always paired with `Superseded by [filename]` in the Status field, and the superseding ADR carries a matching `Supersedes [filename]` line.

## Immutability

ADRs are append-only by convention. Once an ADR is **Accepted**, do not rewrite the body — the whole point is to capture what we decided, when, and why. Editing the decision destroys the historical record.

When reality shifts, write a new ADR and update the old one's Status:

1. Write a new ADR capturing the new decision and its context.
2. Update the old ADR's Status to `Superseded by [new-filename]`.
3. The new ADR's Source field lists `Supersedes [old-filename]`.

**Editable in place** (no new ADR needed):
- Typo fixes, broken-link repairs, formatting
- Adding cross-references (e.g., `Related: 20260518-foo`)
- Clarifying confusing prose without changing the decision

**NOT editable in place** (requires a new ADR):
- Changing the decision itself
- Retroactively rewriting the context to match current beliefs
- Deleting alternatives that were considered and rejected
- Backdating

**Practical diff test**: if someone reading the diff would think *"they changed their mind"* → new ADR. If they'd think *"they fixed a typo"* → in-place edit is fine.

## Cross-Reference Format

When an ADR supersedes or is superseded by another, reference the **full filename without the `.md` extension**:

```
## Status
Superseded by 20260518-use-event-bus

## Source
- Supersedes 20260301-direct-rpc-calls
- Related: 20260415-message-ordering
```

This is unambiguous and matches the actual filename exactly. Don't use numeric-only IDs, slug-only forms, or date-only references — they collide or hide the chronology.

## Granularity

**One decision per ADR.** Don't bundle related decisions into a single record. If two decisions share context but are independently reversible, give each its own ADR and link them with `Related:` in the Source field.

## Retroactive ADRs

Recording a decision that was already made informally (in chat, in code, in a PR) is permitted. The Status remains `Accepted` — no new lifecycle value. Mark the retroactivity in the Source field:

```
## Source
- Retroactive — decision was made implicitly in PR #142 / commit d8ffab7
- Session: (no session — captured post-hoc)
```

The history matters; the retroactivity tag is honest about how the record entered the system.

## Decision-Worthiness Criteria

Not every choice deserves an ADR. The threshold is **downstream architectural impact** — decisions that shape the system's structure, constrain future options, or would be costly to reverse.

### ADR-Worthy (record these)

| Source | What to capture |
|--------|----------------|
| **Architecture choices** | Technology, patterns, component structure, integration approach |
| **Trade-off resolutions** | When competing concerns were weighed and one was preferred |
| **Scope decisions with rationale** | Deliberate inclusion/exclusion that shapes the system boundary |
| **Key constraint decisions** | Invariants established from multiple valid options |
| **Approach pivots** | When implementation adjusts architecture based on reality |

### NOT ADR-Worthy (skip these)

| Category | Why not |
|----------|---------|
| **Quality gate selections** | Verification configuration, not architecture |
| **Process guidance defaults** | How-to-work, not system structure |
| **Mechanical choices** | Obvious implementations with no meaningful alternatives |
| **Known assumptions** | Defaults chosen without deliberation — no alternatives weighed |
| **Bug fixes** | Corrections, not decisions (unless the fix involves an architectural choice) |

### Decision Test

When uncertain, apply: *"Would a new team member joining in 6 months benefit from knowing WHY this was decided this way?"* If yes → ADR. If they'd just accept it as obvious → skip.

## Gate (unified across capture paths)

Two paths capture ADRs in this repo:

- **Inline** via figure-out docs mode — agent offers ADRs during the conversation as decisions get made (primary path).
- **Post-hoc** via the legacy `/adr` skill — sweeps a finished session transcript (backup path).

**Both paths use the same gate**: category match (above) + Decision Test + NOT-ADR-worthy anti-patterns. There is no separate AND-of-conditions trigger anywhere. Same coverage, same criteria.

Inline capture is preferred because context is fresh, alternatives have just been discussed, and the user is present to confirm rejected options. Post-hoc remains useful when inline docs capture was not active or when re-sweeping a finished workflow.

## Synthesis Guidance (post-hoc)

When generating ADR entries from session transcripts:

**From session transcripts**: Look for architecture decisions, trade-off resolutions, and scope decisions where alternatives were explicitly discussed. Key signals: user rejecting an option in favor of another, explicit "because" reasoning, deliberation between approaches.

**From manifests**: The Approach section (Architecture, Trade-offs, Risk Areas) contains structured decision summaries. These are the most reliable source for what was decided, though they lack the full deliberation context.

**Quality over quantity**: A manifest with 10 decisions might produce 2-3 ADRs. The Context and Alternatives sections are what make ADRs valuable — a decision without context is just a fact. If you can't articulate why alternatives were rejected, the decision may not be ADR-worthy.

**Context comes from the transcript, not the manifest**: The most valuable ADR content is the reasoning that happened during the session — user preferences, rejected approaches, constraint trade-offs. The manifest records WHAT was decided; the transcript records WHY.

## Duplication Note (canonical owner)

**This file is the canonical ADR format documentation for the manifest-dev project.**

A legacy copy exists at `claude-plugins/manifest-dev-tools/skills/adr/references/ADR_FORMAT.md` — used by the post-hoc `/adr` skill, retained for as long as that skill exists. The two files are duplicated by design (not by cross-plugin reference) so that:

- `figure-out` (inline capture, primary path) is self-contained and won't break when `/adr` is removed.
- `/adr` (post-hoc backup) keeps working in its current form without depending on a cross-plugin path.

The two files **may drift over time**. When that happens, this file (the figure-out canonical) wins. The legacy `/adr` copy is frozen unless explicitly modified for `/adr` skill changes.

When `/adr` is eventually removed, the legacy copy goes with it; only this file survives.
