# ADR: The code-simplicity review asks which reshaping makes needed complexity disappear

## Status
Accepted

## Area
Code review

## Decided by
The user

## Context
The code-simplicity dimension asked "Is this harder to understand than it needs to be?" Its categories target excess: over-engineering, premature optimization, cognitive complexity, cleverness, and indirection inside one module. In recorded executions its findings were readability rewrites with no structural effect. The dimension stays; its question limited what it found.

## Decision
- The dimension also asks which behavior-preserving restructuring makes branches, helpers, modes, conditionals, or layers unnecessary. That includes complexity the code needs only because of its current shape.
- A reshaping outside the change's scope is reported as a refactor follow-up in the debt list, not applied.
- The actionability filter stays as it is.
- The question matches the design-time probe on what can disappear, so the sketch and the post-code review ask the same thing.

## Alternatives Considered
- **Drop the dimension**: rejected earlier as a quality cut; the dimension is kept.
- **Keep the readability question alone**: in recorded runs it found little beyond readability rewrites.
- **Assume a restructuring is usually available**: it invites false positives.

## Consequences

### Positive
- The review can find structural simplifications, not only clearer wording.

### Negative
- Its findings propose larger changes, which pressure scope.
- No eval suite covers review-code yet, so the effect is measured only in real runs.

## Enforced by
none — it is a question a reviewer asks; no check can hold what a review looks for.

## Source
- Session: figure-out investigation of steering agents toward maintainable first versions.
- Related: 20260810-no-verifier-model-granularity
- Related: 20261013-design-judgment-moves-to-design-time-as-task-file-probes
