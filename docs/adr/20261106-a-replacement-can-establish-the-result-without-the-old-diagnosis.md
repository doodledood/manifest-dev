# ADR: A replacement can establish the result without the old diagnosis

## Status
Accepted

## Area
Code review

## Decided by
The user

## Context
Defect-class review protects against symptom patches and unsupported closure by tracing the
failure mechanism and affected sites. That is sound when repair depends on understanding the
old path. It can also make a complete explanation of that path an accidental deliverable when
the assignment was to restore behavior and a replacement has independent evidence of doing so.
Accepting a reliable result while preserving honest limits serves the North Star's purpose.

## Decision
A replacement may satisfy an outcome assignment without establishing the exact old failure
mechanism when diagnosis was not commissioned and is not needed to trust the result. Its evidence
must cover the required behavior, supported uses and affected failure conditions, using independent
expectations and a justified coverage boundary. Report the old-cause uncertainty explicitly.

A rewrite, passing old tests or a short run without the symptom is not enough. Where missing
knowledge prevents either mechanism-based repair evidence or sufficient replacement evidence,
the verdict remains blocked. Explicit diagnosis requirements stay binding. Proportionate
prevention of demonstrated mechanisms and affected-site accounting remain required.

## Alternatives Considered
- **Always require the old diagnosis:** can reject a sound replacement for an explanation the
  assignment does not owe and the result does not depend on.
- **Accept any replacement whose tests pass:** existing checks may miss the defect and cannot
  establish the affected region or independent expected behavior by themselves.
- **Make diagnosis optional for every repair:** would accept unsupported symptom patches and
  weaken explicit investigation assignments.

## Consequences
### Positive
- Acceptance follows the assigned result without requiring unnecessary retrospective diagnosis.
- Review keeps its protection against weak patches and unsupported claims of closure.

### Negative
- Review must judge whether replacement evidence is sufficient; that cannot be settled by a
  file count, a rewrite label, or a passing command alone.
- The old cause may remain unknown and must be disclosed as such.

## Enforced by
partly — `review-code/references/defect-class.md` owns the two evidence routes and blocking
conditions; the `review-code` recipe exercises the distinction. Sufficiency of independent
evidence remains judgment.

## Source
- Amends: 20260926-defect-remediation-requires-justified-prevention
- Related: 20261106-source-authority-governs-acceptance-and-revision
