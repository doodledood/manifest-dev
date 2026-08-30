## Manifest Schema

````markdown
# Definition: [Title]

## 1. Intent
- **Problem:** [The specific story of what breaks or grates today — the baseline this work improves on]
- **Appetite:** [The size of change this problem is worth — a bound on complexity and surface]
- **Out of bounds:** [What this deliberately leaves alone. Each bound stated once: one that must
  hold is written as the Global Invariant that binds it and appears nowhere else.]

## 2. Initial Approach (Complex Tasks Only)
*Initial direction, not rigid plan. Expect adjustment when reality diverges.*

- **Architecture:** [High-level HOW — starting direction]

## 3. Global Invariants
*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

### INV-G1 — [Title: the headline requirement, summarized and never extended]

[Body: what done means, in the evaluator's precision. Name the evidence to inspect and the
threshold separating PASS from FAIL. Where the procedure that settles this *is* what done means,
it belongs here; where a skill is the definition of done, name that skill and its dimension.]

Why: [optional context, binds nothing — omit where the body already carries it]

[Judgment | Deterministic] gate.

## 4. Process Guidance
*Advisory recommendations on HOW to work — /do weighs them and may depart, naming the departure on whichever terminal path the run reaches (and in the execution log when one is kept). Only Acceptance Criteria and Global Invariants bind; anything that must hold belongs in a gate.*

- [PG-1] Description: ...

## 5. Known Assumptions
- [ASM-1] [What was assumed] | Default: [chosen value] | Impact if wrong: [consequence]

## 6. Deliverables
*Ordered least-proven-first within dependency constraints; list order is the execution order, and Deliverable numbers are stable IDs rather than positions. Plan, not contract — /do may resequence when execution changes what the order was built on, recording the deviation.*

- **Order rationale:** [why this order; omit when there is only one Deliverable]

### Deliverable 1: [Name]

*What it is, and how it is exercised end-to-end:* [one line — the slice, and the situation it is
put in front of so its criteria judge whether it works rather than whether it exists; a build,
test, or existence result is an inspection rather than a situation]

#### AC-1.1 — [Title]

[Body, on the same terms as a Global Invariant's.]

Why: [optional context, binds nothing — omit where the body already carries it]

[Judgment | Deterministic] gate.
````

`kind` is the only structured metadata, and the closing line carries it: it is required and never inferred. IDs are the heading's own — stable, and independent of position.

**Verdicts.** Gate evaluations return **PASS**, **FAIL**, or **BLOCKED** (waiting on external action); `/do` owns what each verdict routes to. Automate verification. A criterion that resists it becomes a judgment-based gate whose body names the concrete evidence the evaluator checks against — not a Process Guidance entry; if it genuinely cannot be written as a gate, sharpen or drop it — a criterion nothing checks is not a criterion. A drop leaves a trace: record it as an `ASM-*` entry naming what was dropped, why it resisted gating, and the impact if that judgment is wrong, so nothing the user cared about disappears unrecorded. Nothing deliberately chosen as the thing that must hold may be dropped — the same set *Gate altitude* protects from being raised away, on the same reasoning. Those sharpen into a judgment-based gate instead; the drop is for criteria that were never verifiable to begin with. Where only part of such a criterion is reachable, gate the reachable part and record the rest as an `ASM-*`, exactly as under *Safety-critical candidates*. Criteria that wait on human or external action (deploys, approvals, in-flight CI) stay ACs — the evaluator surfaces the wait per its own contract, as BLOCKED or as a FAIL carrying a wait finding, until it clears. Auto-decided items carry `(auto)` after the ID with a matching ASM entry.

## The ceiling invariant

Every manifest carries this Global Invariant verbatim — the one bound on the other side:

````markdown
### INV-G1 — The change stops at what this Manifest authorized

Read this Manifest. This is a conformance check: take its intent as given, and do not judge
whether the work was necessary, motivated, or worthwhile.

Done when the work this run added carries nothing the Deliverables, Acceptance Criteria, and
Global Invariants — this one excluded — required, and nothing that nominally serves one of
them while far exceeding the surface the Appetite allows.

Read Problem, Appetite, and Out of bounds as the intent. Read the Deliverables and the other
gates as what the work owes. Read the Initial Approach and Process Guidance as mechanisms that
were *authorized rather than owed* — the ones expected, never the only ones permitted, so work
reaching a Deliverable by a route this Manifest does not name is required by that Deliverable.

Required although no criterion names it: work inherited rather than added — the artifact this
Manifest was synthesized over, and anything arriving from outside the run such as a base branch
merged into the head — and work discharging what a criterion required, including sweeping a
changed rule into every copy and surface that holds it.

FAIL only on work none of the above accounts for. Treat an unclear case as required work, and
leave small, incidental, or imperfect changes inside an artifact already in scope alone.

Why: every other gate states a floor, so a contract bounded on one side only gives an executor
disposed to thoroughness nothing to read as a limit.

Judgment gate.
````
