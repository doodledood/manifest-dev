# ADR Format

Architecture Decision Records capture significant decisions with their context, alternatives, and consequences. Based on the MADR (Markdown Any Decision Records) standard.

## ADR Template

```markdown
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
- Manifest: [manifest file path]
- Session: [session transcript path]
```

## File Naming

`YYYYMMDD-kebab-case-title.md` — date prefix using the current date.

Examples: `20260327-decouple-adr-from-workflow.md`, `20260327-use-madr-format.md`

## Decision-Worthiness Criteria

Not every decision during a manifest workflow warrants an ADR. The threshold is **downstream architectural impact** — decisions that shape the system's structure, constrain future options, or would be costly to reverse.

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

## Synthesis Guidance

When generating ADR entries from session transcripts:

**From session transcripts**: Look for architecture decisions, trade-off resolutions, and scope decisions where alternatives were explicitly discussed. Key signals: user rejecting an option in favor of another, explicit "because" reasoning, deliberation between approaches.

**From manifests**: The Approach section (Architecture, Trade-offs, Risk Areas) contains structured decision summaries. These are the most reliable source for what was decided, though they lack the full deliberation context.

**From execution logs**: Look for approach adjustments with rationale and trade-off applications. The key signal is "changed because" or "preferred X over Y because" — these indicate deliberation.

**Quality over quantity**: A manifest with 10 decisions might produce 2-3 ADRs. The Context and Alternatives sections are what make ADRs valuable — a decision without context is just a fact. If you can't articulate why alternatives were rejected, the decision may not be ADR-worthy.

**Context comes from the transcript, not the manifest**: The most valuable ADR content is the reasoning that happened during the session — user preferences, rejected approaches, constraint trade-offs. The manifest records WHAT was decided; the transcript records WHY.
