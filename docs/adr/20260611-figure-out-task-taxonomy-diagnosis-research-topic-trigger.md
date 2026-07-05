# ADR: figure-out gains DIAGNOSIS and RESEARCH probe files behind a topic-shaped trigger; BUG slims to fix-side

## Status
Accepted

## Context

figure-out's probe files load only "when the topic involves a code change" (`SKILL.md`), and the set mirrors only define's coding cluster (CODING + FEATURE/BUG/REFACTOR). Two of figure-out's most natural *standalone* uses therefore load no probe fuel at all: pure diagnosis ("why is prod latency spiking" — no fix in sight, sometimes no code subject) and research-shaped investigation (tech evaluation, library choice). BUG.md additionally mixes two phases — diagnosis probes (mechanism-not-shape, one-symptom-several-causes) and fix probes (shared-caller fallout, bad-data-left-behind) — under the change-gated trigger.

Operator constraints: figure-out is standalone-first — its methodology may not depend on other tools existing (no "heavy research routes to deep-research"); the only cross-tool pointer is the existing `/define` offer, plus the degrade-gracefully prompt-engineering hook. And the files must be as good as possible upfront — the operator will not run a later hardening loop.

## Decision

- **Add `tasks/DIAGNOSIS.md`** — domain-general RCA probe fuel (incidents, anomalies, metric drops, code defects alike): is the symptom real (measurement error), did it start when you think it started, trigger vs root cause vs contributing factor, mechanism named concretely before explaining stops. Composes with CODING/BUG when the subject is a code defect heading toward a fix.
- **Add `tasks/RESEARCH.md`** — probe fuel only (quality gates stay in define's set): vendor marketing vs independent evidence, survivorship in success stories, recency/version decay of claims, popularity vs fit, who disagrees and why, the issue tracker over the README. Self-sufficient — no escape hatch to other research tools.
- **Replace the code-change gate with topic-shaped detection**: code change → CODING cluster; symptom/incident/anomaly → DIAGNOSIS; external-evidence question → RESEARCH; nothing fits → general probing, as today.
- **Slim BUG.md to fix-side probes** where DIAGNOSIS now carries the diagnosis side — replace-before-add, no duplication.
- **Best-upfront drafting**: each file ships only genuinely non-natural angles, validated by an orthogonality sweep against the spine and sibling files at drafting time (the sweep a later hardening loop would have done). WRITING-type files stay out — no observed miss, and the standalone argument doesn't reach them.

## Alternatives Considered

- **No new types (route research/heavy cases to deep-research or define→do)**: Rejected — assumes a pipeline; figure-out is the primary standalone entry point and those tools don't exist in all distributions.
- **Broaden BUG's trigger only**: Rejected — leaves research homeless and keeps two phases tangled in one file.
- **Mirror define's full taxonomy (WRITING/BLOG/DOCUMENT, PROMPTING, PR_LIFECYCLE)**: Rejected — PROMPTING is covered by the spine's prompt-engineering hook, PR_LIFECYCLE never enters via figure-out, WRITING has no observed non-natural miss; speculative files dilute probe signal.

## Consequences

### Positive
- figure-out's two most common standalone uses (RCA, research) finally get their non-natural angles.
- Single-purpose files: diagnosis fuel loads without presuming a fix; BUG stops double-carrying.

### Negative
- figure-out's taxonomy diverges further from define's mirrored set; the parallel-set drift surface grows (accepted per 20260604's split-index trade-off).

## Source
- Related: PR #189.
- Related: 20260604-figure-out-owns-domain-probing-via-mirrored-task-files (extends its taxonomy and amends its load trigger); 20260611-figure-out-evidence-ledger-and-independent-rederivation
