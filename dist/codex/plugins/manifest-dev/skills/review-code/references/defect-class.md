# Defect-class review

Judge whether a repair addresses its demonstrated failure mechanism at the strongest
justified boundary, accounting for every affected site. When a concrete, proportionate
change can prevent that mechanism through ordinary supported use, require it. A weaker
repair needs a substantiated reason, even when all current callers have been patched.

## Input and scope

Run only when the reviewed range fixes a defect; otherwise PASS with a line saying no
repair was found. On incremental review, the input is a repair in that range or a prior
finding being rechecked, not an old repair beside an unrelated change.

Derive the mechanism from the code: the invalid state or operation, where it is allowed,
and the sequence that reaches it. Use a recorded diagnosis as corroboration, not a
substitute for tracing. State a condition a reader can check, not a category such as
"races" or "stale state". If the mechanism cannot be established, return BLOCKED with
what would resolve it.

Trace the mechanism to its enabling contract or owning operation, including unchanged
code, and enumerate the sites it reaches. The mechanism bounds the walk; similar code
with different invariants or lifecycle semantics need not share a repair. Do not cap the
walk by file count or silently turn a sampled region into complete coverage.

This dimension owns **adequacy of this repair**, including prevention of its demonstrated
mechanism. Type, design, and maintainability dimensions own their general concerns; an
unchanged boundary is not excluded here just because one of them normally reviews that
kind of code. Unrelated debt stays outside the review.

Under explicit-path review, a sibling may own a site's defect on its own terms. Name that
owner in the enumeration and leave that defect finding to it; retain the distinct judgment
of whether this repair provides justified protection. Re-homing a finding is not evidence
that its site was repaired.

## Protection and proportionality

Prefer prevention by design: an invalid state cannot be represented or an invalid operation
cannot succeed through the supported interface. Identify where enforcement lives, which
misuse it prevents, and any assumptions or bypasses. A guard at the sole owning operation
can suffice; prevention does not require a new abstraction or fewer lines of code.

Centralization is not enforcement when ordinary callers can omit a helper or bypass the
owner. Tests and lint detect recurrence; types and mandatory runtime boundaries can prevent
the invalid operation. Credit the guarantee actually provided. A detection check does not
by itself repair affected sites.

Require the stronger remedy only when you can name a concrete prevention boundary and show
that its protection justifies its complexity, migration risk, and maintenance and
coordination costs. Compare independent obligations and coupling, not lines removed.
Reusing a sound owner or fixing an isolated defect locally can be the strongest remedy.
Do not demand generalization across different semantics or hypothetical future requirements.

A valid reason for weaker protection can be an explicit exclusion, unavailable authority,
incompatible semantics, migration risk, or costs outweighing the benefit. Check the reason
against the code and task. More touched files, the initial plan, quicker implementation,
repeated patterns, or an author's stated preference alone do not settle that judgment.
Explicit owner requirements remain authoritative.

## Accounting and acceptance

For every affected site distinguish what is **prevented**, **repaired locally**, **proven
unreachable**, or **unresolved**, with evidence. A region that cannot be enumerated and a
site whose reachability is unknown remain uncertainty; neither counts as closure.

PASS requires the strongest justified protection and accounting sufficient to meet the
task's requirements. A systemic repair with appropriate regression protection may pass
when prevention is unjustified. Containment may pass only when the task permits the
remaining exposure under a valid boundary; label it containment. A merely stated
"out of scope" reason cannot discharge an obligation. When permission or an explicit
exclusion makes a binding outcome impossible, return BLOCKED with the conflict rather
than weakening the requirement or demanding a forbidden edit.

Report FAIL for a demonstrated gap: a reachable unremediated site the task requires
addressed, a prevention claim contradicted by supported misuse, or an unjustifiably weak
remedy. Unsupported closure remains unresolved evidence. For a prevention finding,
name the supported misuse, its concrete prevention boundary, and why a weaker remedy is
not justified. Speculative better architecture earns no finding. Where missing evidence
prevents a verdict, return BLOCKED naming that evidence; do not invent a defect or PASS.

## Severity and report

This is a defect-finder dimension: PASS requires no LOW-or-higher findings. Grade the
consequence of the demonstrated mechanism at the remaining site or supported misuse path:
Critical for loss, corruption, security failure or complete failure without workaround;
High for common core-path failure; Medium for edge or recovery paths; Low for unusual
preconditions. Do not inflate severity to preserve a finding downstream.

Use the shared report format. Between `Files analyzed` and `Findings`, include:

- **Mechanism** — the concrete failure and its enabling boundary.
- **Enumeration** — how the region was derived and each site's disposition, including
  unresolved sites and any re-homed findings.
- **Protection** — the guarantee achieved, evidence for any weaker remedy, and residual
  exposure or uncertainty.

These sections apply on PASS as well as FAIL; BLOCKED states what could and could not be
established. A sound local fix should pass without an invented redesign requirement.
