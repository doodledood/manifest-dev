# manifest-dev

manifest-driven workflows for Claude Code. `/define` interviews you and writes a Manifest; `/do` executes the Manifest and verifies its gates inline.

## Language

**Manifest**:
A structured spec produced by `/define` that captures Deliverables, Acceptance Criteria, Global Invariants, Process Guidance, and an Initial Approach.

**Deliverable**:
A slice a `/define` session commits to producing that can be finished on its own and exercised end-to-end, so its Acceptance Criteria judge whether it works rather than whether it exists.
_Avoid_: Story, ticket, feature.

**Acceptance Criterion**:
A verifiable gate paired with a specific Deliverable.
_Avoid_: Test, check, requirement.

**Global Invariant**:
A property that must hold across all Deliverables in a Manifest.
_Avoid_: Constraint, rule.

**Process Guidance**:
An advisory recommendation on HOW to work during execution, weighed by `/do` rather than enforced; departing from one is legitimate and is named on whichever terminal path the run reaches — completion, escalation, or pending — and in the Execution Log too when one is kept. Only Acceptance Criteria and Global Invariants bind.
_Avoid_: Constraint, requirement, gate.

**Quality Gate**:
A verifiable task-file item that `/define` encodes as an acceptance-style gate.

**Default**:
A non-probed task-file item that `/define` carries into Process Guidance — unless violating it would be unsafe or irreversible, which routes it to a Global Invariant instead.

**Appetite**:
The size of change a problem is worth — a scope bound on complexity and surface set before solutioning, so high-impact work stays prioritized over expanding one solution; independent of time and token cost.
_Avoid_: Estimate, budget, deadline.

**Task File**:
A per-domain hint file owned by a workflow: `figure-out` task files supply probing fuel, while `/define` task files supply Quality Gates and Defaults.

**Evidence Ledger**:
The compact set of load-bearing claims — each carrying provenance and epistemic status — that a figure-out Read rests on.

**Read**:
The deliverable of a figure-out session: a named conclusion carrying confidence, Evidence Ledger, and overturn conditions.
_Avoid_: Conclusion, verdict, answer.

**Parent-before-child Crux Priority**:
A figure-out question-selection rule that resolves the highest-level unresolved crux before drilling into child details.
_Avoid_: BDFS.

**Fog**:
A branch sensed to matter but not yet statable as a question — sharpened by resolving its parent or gathering evidence, never forced into a question shape or pre-sliced into subtrees.
_Avoid_: Open thread (that's sharp — statable precisely now, even if unanswerable yet), unknown, uncertainty.

**Source Surface**:
A maintained project surface treated as authoritative instead of generated output.

**Universal Language**:
Prompt wording that names portable behavior or capability rather than a harness-specific primitive.

**Progressive Disclosure**:
A prompt-architecture pattern where always-needed behavior stays in the entry prompt and mode-specific mechanics live in companion references loaded only when their trigger applies — the trigger living in the loading layer, never inside the deferred reference, which can only be evaluated after the load it was meant to gate.

**Spine**:
The always-on core discipline of a skill's prompt — hosted inline in SKILL.md — as opposed to mode mechanics and edge guards.
_Avoid_: Core, essence.

**Re-host**:
Restructuring a prompt by relocating content verbatim — reordering, sectioning — without rewriting or trimming it.
_Avoid_: Rewrite, refactor, cleanup.

**Altitude**:
The weight class of a prompt line — Spine, mode-specific mechanic, or edge-case guard — determining how foregrounded it should be.
_Avoid_: Priority, importance.

**Do/Verify Loop**:
The execution cycle where `/do` implements toward a Manifest, verifies every Acceptance Criterion and Global Invariant, routes failures or blockers, and finishes only after all gates pass.

**Host Continuation Backstop**:
A host-provided goal-setting, continuation, or completion-check capability that keeps or reopens a run until a durable completion contract is satisfied.

**Phase Checkpoint**:
A required intermediate workflow condition that must be satisfied before moving to the next phase, but is not the terminal success condition unless that phase's artifact is the deliverable.

**Gate Evaluation Instructions**:
The topology-neutral procedure inside `verify.instructions` that says what evidence to gather and what PASS means, without choosing who evaluates it or which model runs it.

**Verification Mode**:
The run-level `/do` policy that selects `per-gate`, `consolidated`, or `self` evaluation without changing the Manifest.

**Verification Provenance**:
The gate-ledger record of who evaluated a gate under which mode and explicit or inherited model choice.

**Verifier Execution**:
An independent host execution context launched by `/do` to evaluate one gate or a consolidated set of gates.

**Judgment Gate**:
A gate whose verdict is a model's judgment over an open finding space, so a fresh evaluation can surface findings the previous one did not, even on an unchanged subject.
_Avoid_: Mood-based gate, subjective gate.

**Deterministic Gate**:
A gate whose verdict comes from a command or check that returns the same outcome for the same artifact state — tests, builds, typechecks.
_Avoid_: Binary gate.

**Ratchet**:
A re-verification discipline for Judgment Gates where the first evaluation reads the full change and every later evaluation judges only the prior findings' repairs and the changed delta, closing the finding space after the first full look.
_Avoid_: Round cap, round limit.

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

**Judgment Layer**:
A non-binding, review-time premise check that surfaces whether a change earns its keep against the pain it solves — necessity, the pain itself, and surface proportionality — as author-facing questions rather than gates.
_Avoid_: Premise gate, necessity gate.

**PR Grounding**:
The ordered evidence Babysit PR uses to decide whether a pull-request blocker is in scope to fix.

**CI One-Shot**:
A non-interactive Babysit PR run that performs immediately actionable lifecycle steps, then exits pending when only waiting remains.

**Steering Message**:
A mid-/do user message treated as fire-and-forget direction — encoded into the manifest by autonomous amendment without waiting for the user to stay engaged.
_Avoid_: Interrupt, mid-run question.

**Execution Log**:
An append-only, out-of-repo journal /do keeps by default (`--no-log` opts out) recording deviations from the Initial Approach or Deliverable order, Process Guidance departures, dead-end memory, and operational events — execution history never lives in the Manifest.
_Avoid_: Execution notes, amendments log, changelog.

**Door**:
A standalone skill fronted on one discovery surface as the zero-enrollment entry into manifest-dev.
_Avoid_: Wedge, funnel.

**House**:
The full understanding-first loop (figure-out → define → do) that every Door opens into; the retention engine behind the Doors.

**Taste**:
A durable personal steering preference persisted only by offer-and-ratify — captured as preference, rationale, and flip condition in a harness memory file.
_Avoid_: Preference, style, judgment.

**Map**:
The one system answering "what needs doing" for an effort too large for one deliberation — any effort size, ephemeral or standing — a front page of destination, standing decisions, prioritized frontier, fog, and out-of-scope rulings, per the map convention (`skills/define/tasks/references/MAP_CONVENTION.md`).
_Avoid_: Roadmap, backlog, board.

**Decision item**:
A map item that is a question, worked by one deliberation session; resolving it leaves a Standing decision when the answer keeps constraining.
_Avoid_: Ticket, task.

**Work item**:
A map item pointing at execution a resolved decision spawned; its detail lives in a delivery home (a Manifest, a delivery board) and the item rolls off the map's page when done.
_Avoid_: Deliverable, story.

**Standing decision**:
A resolved Decision item whose answer still constrains the map's choices; it stays on the front page until it stops mattering or the destination moves.

**Steward pass**:
A periodic deliberation session with the Map as its topic — re-points the frontier at the destination, applies roll-off, retires stale fog.

## Relationships

- A **Manifest** contains one or more **Deliverables**.
- A **Deliverable** has one or more **Acceptance Criteria**.
- A **Manifest** has zero or more **Global Invariants**, applied across all Deliverables.
- A **Task File** can contribute **Quality Gates** and **Defaults** to `/define`.
- A **Quality Gate** becomes an acceptance-style gate in a **Manifest**.
- A **Map** holds **Decision items** and **Work items**; a resolved **Decision item** can leave a **Standing decision**, spawn **Work items**, or open a child **Map**.
- A **Default** becomes **Process Guidance** in a **Manifest**, except one whose violation would be unsafe or irreversible, which becomes a **Global Invariant** so it binds.
- A figure-out **Read** ships with the **Evidence Ledger** it rests on.
- **Parent-before-child Crux Priority** orders figure-out's crux selection before impact tie-breaking among same-level questions.
- `/define` encodes the understanding a figure-out **Read** establishes into a **Manifest** rather than re-deriving or re-investigating it.
- Every **Acceptance Criterion** and **Global Invariant** carries **Gate Evaluation Instructions** in the **Manifest**.
- `/do` owns the **Do/Verify Loop**: it implements **Deliverables**, evaluates failed-or-unverified **Acceptance Criteria** and **Global Invariants** under the selected **Verification Mode**, repairs FAILs, and routes BLOCKED gates.
- `per-gate` launches one **Verifier Execution** per eligible gate, `consolidated` launches one for the outstanding gate set, and `self` launches none.
- Every gate evaluation returns PASS, FAIL, or BLOCKED evidence plus **Verification Provenance** to the **Do/Verify Loop**.
- Every **Acceptance Criterion** and **Global Invariant** is either a **Judgment Gate** or a **Deterministic Gate**; the kind is a property of the gate itself, readable from its **Gate Evaluation Instructions**.
- The **Ratchet** governs how the **Do/Verify Loop** re-verifies **Judgment Gates** after repairs; **Deterministic Gates** re-run freely.
- **Verification Mode** and the **Ratchet** are run-level `/do` policy, never **Manifest** content; **Verification Provenance** records what a given run used.
- A **Skill** may invoke other **Skills** and may run through host **Agent** contexts.
- A **Host Continuation Backstop** is an outer guard for unattended runs; it does not replace the **Do/Verify Loop**.
- A **Phase Checkpoint** can protect a handoff between workflow phases, while terminal completion stays tied to the final deliverable's acceptance evidence.
- **Babysit PR** and **Review PR** can run asynchronously on the same pull request: **Review PR** applies quality pressure, while **Babysit PR** drives the author-side lifecycle toward green and mergeable.
- **Review PR** in manifest mode independently re-verifies a **Manifest** against the pull request head.
- The **Judgment Layer** runs inside **Review PR** (both modes) as non-binding questions, kept distinct from a **Manifest**'s binding **Acceptance Criteria** and from the defect fleet.
- A **Steering Message** is encoded by autonomous amendment, with judgment calls audited as Known Assumptions and pivots recorded in the **Execution Log**.
- **Babysit PR** uses **PR Grounding** so newer comments do not override stronger sources of intent by recency alone.
- **CI One-Shot** is a constrained mode of **Babysit PR**.
- One **Door** per discovery surface; every **Door** opens into the same **House**.
- A **Re-host** preserves **Spine** content verbatim while making its **Altitude** typographically legible.
- A **Taste** entry is ratified by the user and routed by scope to a user-level or project-level memory file; it is never inferred and applied silently, and it stays distinct from the review-time **Judgment Layer**.

## Flagged ambiguities

_None yet. Grow this section as figure-out docs-mode sessions surface clashes or canonicalizations._
