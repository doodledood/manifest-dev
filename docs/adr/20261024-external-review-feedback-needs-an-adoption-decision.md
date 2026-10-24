# ADR: External review feedback needs an adoption decision

## Status
Accepted

## Area
PR lifecycle

## Decided by
The user

## Context
An external reviewer can omit project context or issue distinct optional suggestions after every
commit. Deduplicating repeated comments does not stop that sequence. Treating every correct
suggestion as an obligation creates further commits without necessarily improving the requested
outcome. The caller already owns validity, relevance, and proportionality; the PR inspector owns
observable remote state.

## Decision
The author-side caller adopts a code change when it repairs a demonstrated binding failure or
materially improves the requested outcome enough to justify its disruption, regression risk,
and scope. A suggestion's correctness, severity label, or repetition does not establish that.
The caller can decline distinct optional nits with a reason and no code change.

Supported dispositions follow the substance and evidence across new comment IDs and pushes.
Changed code, argument, or evidence can reopen them. An independently demonstrated relevant
failure still receives assessment on unchanged, previously reviewed material. The restriction
on repeated internal searches does not suppress evidence an external source supplies.

`check-pr` remains read-only and substance-neutral. It reports current outstanding state and
action targets even for repeated claims. A prior disposition does not clear a new thread,
required check, or approval. The caller handles authorized replies and resolutions separately,
leaves human-authored threads open, and reports a required reviewer that rejects an evidenced
decline as an external blocker. Neither local reasoning nor completion pressure waives that
requirement or authorizes disabling the reviewer.

One conditional reference under `/do` owns this rule for direct execution and `babysit-pr`.
This restores external-feedback judgment in a smaller form after its procedural handling was
retired in 20260914-one-skill-per-beat-built-from-the-lean-body. Communication and merge authority
remain separate decisions under the assignment.

## Alternatives Considered
- **Deduplicate only by content:** prevents repeated repairs of one claim but accepts endless
  distinct nits.
- **Let the inspector judge comment merit:** mixes current remote state with author-side intent
  and loses the shared observer boundary.
- **Ignore all later feedback or stop after a fixed count:** can discard evidence of real
  failures and does not satisfy an actual external requirement.

## Consequences

### Positive
- Correct but unhelpful suggestions can be declined without producing appeasement commits.
- Real new evidence remains admissible, and outstanding remote requirements remain visible.

### Negative
- The caller can misjudge proportionality or the strength of a rebuttal.
- An uncontrolled reviewer may keep commenting or withholding approval; this rule does not
  promise a finite round bound or eventual approval.

## Enforced by
partly — `tests/test_drive_scripts.py` checks that PR replay fixtures carry the intended code
states and bind observations to the runner's head. The `do`, `check-pr`, and `babysit-pr` recipes
exercise adoption, repeated and distinct feedback, and required external blockers. Their
ask-first drives remain unmeasured; fixture checks do not prove agent judgment or live GitHub behavior.

## Source
- [Issue 377](https://github.com/doodledood/manifest-dev/issues/377)
- Amends 20260602-deliberate-on-pr-review-comments-at-the-caller
- Narrows 20260914-one-skill-per-beat-built-from-the-lean-body
- Clarifies 20260805-ratchet-judgment-gate-reverification
- Related: 20261021-check-pr-review-feedback-is-one-inbox
- Related: 20261024-gate-criteria-and-evidence-travel-with-execution
