## Manifest Schema

````markdown
# Definition: [Title]

## 1. Intent
- **Outcome:** [The result owed, for whom and in what circumstances. Preserve the request's
  meaning and hard requirements; put operational interpretations in gates, not here.]
- **Outcome evidence:** [How the finished result is judged against that outcome, including
  who decides any retained acceptance. This is a working method unless explicitly required.]
- **Problem:** [The specific story of what breaks or grates today — the baseline this work improves on]
- **Appetite:** [The current size of change this problem is worth — complexity and surface;
  revisable prospectively within the executor's delegation]
- **Out of bounds:** [IDs of the Global Invariants stating explicit exclusions; state each
  exclusion only in its invariant.]

## 2. Initial Approach (Complex Tasks Only)
*Initial direction, not rigid plan. Expect adjustment when reality diverges.*

- **Architecture:** [High-level HOW — starting direction]

## 3. Global Invariants
*Claims that apply to the entire execution. Each must hold until validly amended.*

### INV-G1 — [Title: the headline requirement, summarized and never extended]

Authority: [hard — the actual user requirement or applicable rule, stated here with its source;
or working — the agent's operational interpretation and the outcome it serves.]

[Body: the claim and its acceptance threshold. Include any explicitly required procedure here.
Split claims of different authority into separate gates.]

Evidence: [The current method for assessing the claim: observations, commands, artifacts or a
skill and dimension. This method is revisable; it cannot silently add or weaken a requirement.]

Why: [optional context, binds nothing — omit where the body already carries it]

[Judgment | Deterministic] gate.

## 4. Process Guidance
*Advisory recommendations on how to work. The Outcome and current gates are owed; guidance
is not. /do may depart, explaining material departures in its report and execution log.*

- [PG-1] Description: ...

## 5. Known Assumptions
*Unresolved assumptions and material choices, with the alternative, reason and impact if wrong.
An `(auto)` mark points to a choice made without asking. Gate authority stays with the gate;
do not repeat it here or use an assumption to waive the Outcome or a hard requirement.*

- [ASM-1] [What was assumed] | Default: [chosen value] | Impact if wrong: [consequence]

## 6. Deliverables
*Ordered least-proven-first within dependency constraints; list order is the execution order, and Deliverable numbers are stable IDs rather than positions. Plan, not contract — /do may resequence when execution changes what the order was built on, recording the deviation.*

- **Order rationale:** [why this order; omit when there is only one Deliverable]

### Deliverable 1: [Name]

*What it is, and how it is exercised end-to-end:* [one line — the slice, and the situation it is
put in front of so its criteria judge whether it works rather than whether it exists; a build,
test, or existence result is an inspection rather than a situation]

#### AC-1.1 — [Title]

Authority: [hard — source and obligation; or working — interpretation and purpose.]

[Body, on the same terms as a Global Invariant's.]

Evidence: [Current assessment method.]

Why: [optional context, binds nothing — omit where the body already carries it]

[Judgment | Deterministic] gate.
````

The Outcome is owed in addition to the gates. Its assessment returns a judgment verdict under
the ID `OUTCOME`; passing chosen checks alone does not establish it. It states the requested
result, not an opportunity to invent additional obligations during review.

**Authority.** A hard claim comes from a deliberately stated user requirement or an applicable
project, safety or permission obligation. Its source must be specific enough to recover the
actual obligation without the original conversation. A reason is useful but not required.
An agent's choice, a derived proxy, this schema, and overall approval of a plan are not sources
of hard authority. A working claim is the agent's current operational interpretation; it remains
owed until amended on evidence that the replacement better serves the unchanged Outcome and
hard requirements. Difficulty or a failed check alone is not that evidence. Unclear authority
is resolved from the source before changing the claim, never guessed into permission.

Evidence methods are working choices unless the claim itself carries a source-backed requirement
to use that method. This keeps a hard promise separate from an agent-selected test. A material
revision replaces the old text, is reported, and invalidates affected evidence. An evaluator
judges the current contract and reports a mistaken working claim for amendment, never waives it.

Every gate declares its authority and its kind (`Judgment gate.` or `Deterministic gate.`).
The closing line carries kind; neither field is inferred. IDs are stable and independent of position.

**Verdicts.** Gate evaluations return **PASS**, **FAIL**, or **BLOCKED** (waiting on external action); `/do` owns what each verdict routes to. Automate verification. A criterion that resists it becomes a judgment-based gate whose body names the concrete evidence the evaluator checks against — not a Process Guidance entry; if it genuinely cannot be written as a gate, sharpen or drop it — a criterion nothing checks is not a criterion. A drop leaves a trace: record it as an `ASM-*` entry naming what was dropped, why it resisted gating, and the impact if that judgment is wrong, so nothing the user cared about disappears unrecorded. Nothing deliberately chosen as the thing that must hold may be dropped. Those sharpen into a judgment-based gate instead; the drop is for criteria that were never verifiable to begin with. Where only part of such a criterion is reachable, gate the reachable part and record the rest as an `ASM-*`, naming what is not gated and what enforces it instead. Criteria that wait on human or external action (deploys, approvals, in-flight CI) stay ACs — the evaluator surfaces the wait per its own contract, as BLOCKED or as a FAIL carrying a wait finding, until it clears.

## The ceiling invariant

Every manifest carries this Global Invariant verbatim — the one bound on the other side:

````markdown
### INV-G1 — The change stops at what this Manifest authorized

Authority: hard — the assignment authorizes only work serving the requested Outcome within
its stated scope and applicable instructions.

Read this Manifest. This is a conformance check: take its intent as given, and do not judge
whether the work was necessary, motivated, or worthwhile.

Done when the work this run added carries nothing beyond what the Outcome, Deliverables, Acceptance Criteria, and
Global Invariants — this one excluded — required, and nothing that nominally serves one of
them while far exceeding the surface the Appetite allows.

Read Outcome, Problem, Appetite, and Out of bounds as the intent. Read the Outcome, Deliverables and the other
gates as what the work owes. Read the Initial Approach and Process Guidance as mechanisms that
were *authorized rather than owed* — the ones expected, never the only ones permitted, so work
reaching a Deliverable by a route this Manifest does not name is required by that Deliverable.

Required although no criterion names it: work inherited rather than added — the artifact this
Manifest was synthesized over, and anything arriving from outside the run such as a base branch
merged into the head — the fixes every run owes on its pull request — a pre-existing issue the
work met whose fix is not a project of its own and that the project's own rules do not keep out,
and a below-bar finding from a first full look applied because it improves the work — and work
discharging what a criterion required, including
sweeping a changed rule into every copy and surface that holds it.

FAIL only on work none of the above accounts for. Treat an unclear case as required work, and
leave small, incidental, or imperfect changes inside an artifact already in scope alone.

Evidence: Inspect the change against this Manifest and the applicable assignment.

Why: every other gate states a floor, so a contract bounded on one side only gives an executor
disposed to thoroughness nothing to read as a limit.

Judgment gate.
````
