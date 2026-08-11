# ADR: A review dimension may take a defect as input, and that is what earns it a slot

## Status
Accepted

## Area
Code review

## Context

`review-code`'s dimensions are separated by **kind of concern** — bugs, types, design fitness,
maintainability, simplicity, docs. Each reference carries an explicit "belongs to a sibling"
section, and the skill's own gotchas hold the line ("Stay inside the loaded dimension"). That
orthogonality is the fleet's defining property: it is what lets thirteen parallel readers run
without collapsing into thirteen restatements of the same review.

Every dimension also shares a scope rule. In diff-based review — the default — each one reports
only what the change introduced; pre-existing issues are out of scope. That rule is what keeps a
review about the change rather than about the codebase, and it is uniform across all thirteen.

The rule has a consequence nobody had written down. When a change **fixes** a defect, the other
sites the same mechanism reaches are unchanged code. Patching one call site introduces nothing
at the others, so every dimension is barred from mentioning them. A fix can close one door and
leave five open, and the fleet is structurally unable to say so. `define/tasks/BUG.md` carried
the countermeasure as a Default — "Systemic fix assessment: identify the class of bug; probe
whether a pattern fix prevents recurrence" — which `/define` encodes as Process Guidance, so
`/do` may legitimately weigh it away. Advice, not a gate.

Closing that hole means a reader permitted to report on unchanged code. The obvious move — a
dimension separated from `code-bugs` only by a wider scope — does not survive contact with the
fleet's own architecture. Scope is not a kind of concern, `review-code` already has an
explicit-path mode in which pre-existing findings are valid, and a dimension whose only
distinguishing property is where it looks is a second copy of `code-bugs`.

## Decision

Add a `defect-class` dimension to `review-code`, admitted on the ground that it is the **only
dimension whose input is another dimension's output**. It takes a defect the change fixes as
given and asks whether the response to it is complete: which other sites the same mechanism
reaches, and what happened to each. Its question is completeness of remediation, not detection.

That single property, not the scope rule, is what earns the slot — and it generates every
boundary rather than requiring each to be policed separately:

- **The admission test — delete the fix from the diff and ask whether the finding survives.**
  If it survives, the finding belongs to `code-bugs` or another sibling, which read the code on
  its own terms. If it collapses, it belongs here, because it had a fix as its input. Nothing
  else in the fleet fails that test. This test governs any future dimension proposal, not only
  this one.
- **Against `code-design`.** Its PR-Coherence categories already own completeness — cross-cutting
  impact missed, incomplete migration, schema constraint completeness. Each is anchored to a
  **designed artifact** that has instances: an interface, a pattern, a schema. A defect mechanism
  is none of those, so a guard replicated across call sites falls through all three. `code-design`
  fires on designed artifacts whether or not a defect occurred; this fires only where one did.
- **Against `code-maintainability`'s extensibility risk.** That concerns the *next* sibling
  forgetting a cross-cutting behavior; this concerns *existing* siblings already broken by a
  mechanism that has demonstrably fired.
- **Reporting on unchanged code is licensed by the proven trigger, not by a scope exemption.**
  The fleet bars pre-existing findings because they would be speculation, and `review-code`'s
  shared bar demands a stated trigger rather than a confidence level. Here the trigger is the
  one the fix already established: the bug happened. A second door into a defect that has
  occurred is not debt surfaced opportunistically.

Encoding: **defect-finder tier** (`no LOW+`) — every finding carries a demonstrated trigger, so
there is no taste-level band to tolerate. It is **conditional**, fired when the change fixes a
defect; `review-pr` owns the spawn decision, as it already does for `contracts` and `type-safety`,
because narrow-lens fleet readers never receive the PR description. `define/tasks/BUG.md` gains
a gate delegating to it, the way `CODING.md`'s base gates delegate to theirs.

## Alternatives Considered

- **A new dimension separated from `code-bugs` by scope alone**: rejected. Scope is not a kind of
  concern; it would be a fourteenth reference restating the thirteenth, and `review-code` already
  offers explicit-path review where pre-existing findings are valid.
- **Invoke `code-bugs` a second time in explicit-path mode**: rejected. That mode requires the
  caller to supply the paths, and deriving the region from the mechanism is precisely the work
  that has no owner. A manifest gate cannot supply them either — gate bodies must not spawn.
- **Fold it into `code-design` as an eighth PR-Coherence category**: rejected, though it is the
  closest fit. `code-design` is advisory-tier and diff-scoped, so folding in would demote the
  bar and require carving a pre-existing-code exception into an otherwise clean filter — costs
  paid to avoid a boundary that turns out to be crisp.
- **Loosen `code-bugs` to carry class-level fixes in its Recommended fix field**: rejected. Its
  actionability filter requires "one clear issue with one clear fix, not 'this whole approach is
  wrong'", and relaxing it turns every guard-clause finding into a refactor pitch — the noise the
  fleet is engineered against.
- **Leave it to `review-pr`'s judgment pass as a recurrence trigger**: rejected. The judgment
  pass is non-blocking, once per PR, and reaches only PRs; the check is also wanted as a manifest
  gate on bug work, where nothing would carry it.
- **Do nothing — keep it as the existing `BUG.md` Default**: rejected. Process Guidance is
  advisory by design, and the practice as written ("probe whether a pattern fix prevents
  recurrence") is not verifiable from the output, which is why it sits there. What makes it
  gateable is demanding the artifact instead of the probe.

## Consequences

### Positive

- A fix that leaves the class open becomes visible, on both paths that matter: a manifest gate on
  defined bug work, and the review fleet on any PR.
- The fleet's orthogonality is strengthened rather than diluted: the delete-the-fix test is a
  reusable admission rule that did not exist before, and it rejects scope-only dimensions
  explicitly.
- Reporting on unchanged code is bounded by a principle rather than an exemption — the trigger
  must already have fired — so it does not become a general licence to surface debt.
- The enumeration is bounded by the mechanism's own specificity, not by repo size: a mechanism
  stated precisely enough to fix is stated precisely enough to walk.

### Negative

- The fleet gains a dimension whose correctness depends on another dimension's work being
  well-stated. A vaguely-stated mechanism produces a vague region and a wide, low-value walk.
- Mechanisms anchored to a convention rather than a symbol ("anything assuming this callback
  fires before mount") have nothing to enumerate; those pass by being named out of scope, which
  is a weaker outcome than the gate implies.
- One more conditional reader on defect-fixing changes, against a project stance that treats
  unbounded verification cost as a workflow defect. `/do`'s existing route for a gate costing
  more than it returns is the backstop; if this gate is what keeps taking it, the bar is wrong.
- If a future dimension proposal fails the delete-the-fix test but is admitted anyway, the
  admission rule recorded here decays into a rationalisation for this one case.

## Source

- Session: figure-out investigation, 2026-08-11 — `review-code`'s thirteen dimension references,
  `review-pr`'s fleet wiring, and `/define`'s task files read at source; Matt Pocock's
  `improve-codebase-architecture` and `codebase-design` skills read at source as the prompting
  material. Self-graded: no independent re-derivation pass was run.
- Related: 20260811-defect-class-gates-bind-on-accounting-not-redesign (the boundary of what this
  dimension demands), 20260810-advisory-gates-omit-by-bearer-test,
  20260807-a-gate-is-one-text-not-two, 20260726-only-gates-bind-process-guidance-is-advisory
