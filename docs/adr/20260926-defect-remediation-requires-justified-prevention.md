# ADR: Defect remediation requires proportionate prevention with evidenced fallbacks

## Status
Accepted

## Area
Code review

## Context

The defect-class review required affected-site accounting but expressly accepted
patching every site even when prevention was available. A stated out-of-scope
reason discharged a site without substantive evaluation, and an unenumerable
region could pass as closed. These rules protected against compulsory redesign
but also accepted avoidably permissive boundaries and unsupported closure claims.

Repair acceptance needs to preserve the protection against scope expansion while
requiring the strongest justified remedy for a demonstrated mechanism. This is a
concrete application of the general durable-outcome default.

## Decision

The defect-class dimension owns adequacy of a repair against its demonstrated
failure mechanism: both affected-site accounting and justified protection through
the supported interface. Require a concrete, proportionate prevention boundary
when available; evaluate evidence for weaker remedies. A small mandatory guard
can suffice, while an optional shared helper may leave the mechanism open.

A systemic repair or containment is acceptable only when its limits are justified
and satisfy the task. Distinguish prevented, locally repaired, proven unreachable,
and unresolved sites. Unknown coverage remains uncertainty. A binding outcome
that conflicts with permission or explicit exclusions is blocked, not silently
weakened. Detection checks complement repairs; they do not establish that the
invalid operation cannot occur.

The repair in the reviewed range establishes eligibility to inspect its unchanged
enabling boundary. A later unrelated delta does not reopen an old repair. Type,
design, and maintainability reviews retain their general concerns; defect-class
owns whether prevention of this demonstrated mechanism was omitted. Under an
explicit-path audit, another dimension may own a site's defect, while defect-class
retains the distinct adequacy judgment and names the site's owner in its accounting.

The existing no-LOW-or-higher acceptance threshold remains. Pull-request consolidation
preserves defect-class findings at their actual severity, including Low, and a
non-binding premise question cannot discharge an unmet remediation obligation.
The reviewer receives binding task constraints without treating an implementation
preference as an owner requirement. No new review dimension or Manifest field is
introduced.

## Alternatives Considered

- **Keep prevention as an ordered preference:** already permits a weaker repair
  without examining whether its reason holds.
- **Require redesign for every bug:** confuses prevention with code volume and
  rejects sound local fixes or legitimate migration boundaries.
- **Let general design or type review own omitted prevention:** leaves a repair's
  unchanged enabling boundary vulnerable to scope filters and splits acceptance
  among dimensions with different thresholds.
- **Raise Low findings to survive pull-request filtering:** distorts severity; retaining
  relevant findings addresses the filtering problem directly.
- **Treat unenumerated regions as closed:** reports more certainty than the
  evidence supports and can conceal unmet binding requirements.

## Consequences

### Positive

- Patching every current caller no longer excuses an avoidable supported misuse.
- Fall-back reasons and prevention claims must withstand artifact-based review.
- Existing scope, dimension, and incremental-review boundaries remain usable.

### Negative

- Reviewers must judge proportionality and cannot reduce acceptance to counting
  dispositions. Some reviews will be blocked by genuinely missing evidence.
- Generic pull-request review may surface Low remediation findings it previously suppressed.
- Targeted behavioral checks do not establish a general reduction in defect rates.

## Source

- Supersedes 20260811-defect-class-gates-bind-on-accounting-not-redesign
- Amends: 20260811-a-review-dimension-may-take-a-defect-as-input
- Related: 20260926-durable-outcomes-include-subsequent-work,
  20260805-ratchet-judgment-gate-reverification
- [Issue 336](https://github.com/doodledood/manifest-dev/issues/336)
