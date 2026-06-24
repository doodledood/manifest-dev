# manifest-dev

manifest-driven workflows for Claude Code. `/define` interviews you and writes a Manifest; `/do` executes the Manifest and verifies its gates inline.

## Language

**Manifest**:
A structured spec produced by `/define` that captures Deliverables, Acceptance Criteria, Global Invariants, Process Guidance, and an Approach.

**Deliverable**:
A discrete output a `/define` session commits to producing.
_Avoid_: Story, ticket, feature.

**Acceptance Criterion**:
A verifiable gate paired with a specific Deliverable.
_Avoid_: Test, check, requirement.

**Global Invariant**:
A property that must hold across all Deliverables in a Manifest.
_Avoid_: Constraint, rule.

**Process Guidance**:
A constraint on HOW to work during execution that isn't itself a verifiable gate.
_Avoid_: Guideline, best practice.

**Quality Gate**:
A verifiable task-file item that `/define` encodes as an acceptance-style gate.

**Default**:
A non-probed task-file item that `/define` carries into Process Guidance.

**Task File**:
A per-domain hint file owned by a workflow: `figure-out` task files supply probing fuel, while `/define` task files supply Quality Gates and Defaults.

**Evidence Ledger**:
The compact set of load-bearing claims — each carrying provenance and epistemic status — that a figure-out Read rests on.

**Read**:
The deliverable of a figure-out session: a named conclusion carrying confidence, Evidence Ledger, and overturn conditions.
_Avoid_: Conclusion, verdict, answer.

**Source Surface**:
A maintained project surface treated as authoritative instead of generated output.

**Universal Language**:
Prompt wording that names portable behavior or capability rather than a harness-specific primitive.

**Do/Verify Loop**:
The execution cycle where `/do` implements toward a Manifest, verifies every Acceptance Criterion and Global Invariant, routes failures or blockers, and finishes only after all gates pass.

**Host Continuation Backstop**:
A host-provided goal-setting, continuation, or completion-check capability that keeps or reopens a run until a durable completion contract is satisfied.

**Verifier Execution**:
An independent host execution context launched by `/do` to evaluate one Acceptance Criterion or Global Invariant.

**Skill**:
A reusable capability that extends an agent's behavior.

**Agent**:
An isolated host execution context; manifest-dev uses the term only for host-provided contexts.
_Avoid_: Subprocess, worker.

**Babysit PR**:
An author-side workflow that tends an existing pull request through CI, review threads, description sync, and mergeability without pressing merge.
_Avoid_: Tend PR.

**Review PR**:
A reviewer-side workflow that inspects a pull request and advances review threads without becoming the author-side lifecycle owner.

**PR Grounding**:
The ordered evidence Babysit PR uses to decide whether a pull-request blocker is in scope to fix.

**CI One-Shot**:
A non-interactive Babysit PR run that performs immediately actionable lifecycle steps, then exits pending when only waiting remains.

## Relationships

- A **Manifest** contains one or more **Deliverables**.
- A **Deliverable** has one or more **Acceptance Criteria**.
- A **Manifest** has zero or more **Global Invariants**, applied across all Deliverables.
- A **Task File** can contribute **Quality Gates** and **Defaults** to `/define`.
- A **Quality Gate** becomes an acceptance-style gate in a **Manifest**.
- A **Default** becomes **Process Guidance** in a **Manifest**.
- A figure-out **Read** ships with the **Evidence Ledger** it rests on.
- `/define` encodes the understanding a figure-out **Read** establishes into a **Manifest** rather than re-deriving or re-investigating it.
- `/do` owns the **Do/Verify Loop**: it implements **Deliverables**, launches **Verifier Executions** for failed-or-unverified **Acceptance Criteria** and **Global Invariants**, repairs FAILs, and routes BLOCKED gates.
- A **Verifier Execution** returns PASS, FAIL, or BLOCKED evidence to the **Do/Verify Loop**.
- A **Skill** may invoke other **Skills** and may run through host **Agent** contexts.
- A **Host Continuation Backstop** is an outer guard for unattended runs; it does not replace the **Do/Verify Loop**.
- **Babysit PR** and **Review PR** can run asynchronously on the same pull request: **Review PR** applies quality pressure, while **Babysit PR** drives the author-side lifecycle toward green and mergeable.
- **Review PR** in manifest mode independently re-verifies a **Manifest** against the pull request head.
- **Babysit PR** uses **PR Grounding** so newer comments do not override stronger sources of intent by recency alone.
- **CI One-Shot** is a constrained mode of **Babysit PR**.

## Flagged ambiguities

_None yet. Grow this section as figure-out --with-docs sessions surface clashes or canonicalizations._
