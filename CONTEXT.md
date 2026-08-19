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

**Project Context File**:
The always-loaded instruction file a harness reads for a project — `CLAUDE.md` on Claude Code, `AGENTS.md` on Codex and OpenCode — resolved by detection rather than assumed by name.
_Avoid_: CLAUDE.md (that is one harness's instance of it).

**ADR Conventions**:
A project-owned file stating what deserves a decision record and how to write one, self-contained so a reader with no tooling can follow it; where it exists it outranks any tool's shipped default on everything except cadence.
_Avoid_: ADR format, ADR template.

**Derived Index**:
An index that asserts nothing its records don't, and is rebuilt from them rather than edited alongside them — so staleness is a repairable lag rather than lost information.
_Avoid_: ADR list, table of contents.

**Seed**:
The deliberately under-produced vocabulary and decision corpus `/init-context` reconstructs from a project's history — a starting point that names what it could not recover, never a complete record.
_Avoid_: Import, migration, backfill.

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

**Form Vocabulary**:
The set of shapes a given output destination can carry — tables, box diagrams, fenced code, charts — as opposed to the surface-independent rule that selects among them, which is Spine.
_Avoid_: Rendering contract (that is the pair, selection rule included), formatting, style.

**Do/Verify Loop**:
The execution cycle where `/do` implements toward a Manifest, verifies every Acceptance Criterion and Global Invariant, routes failures or blockers, and finishes only after all gates pass.

**Host Continuation Backstop**:
A host-provided goal-setting, continuation, or completion-check capability that keeps or reopens a run until a durable completion contract is satisfied.

**Phase Checkpoint**:
A required intermediate workflow condition that must be satisfied before moving to the next phase, but is not the terminal success condition unless that phase's artifact is the deliverable.

**Gate Text**:
The single text a gate is — a title, a body, and an optional why — read by the reviewer and the evaluator alike. The body says what done means, what evidence settles it, any non-obvious context the evaluator needs, and where the check *is* the definition, how to run it; the title summarizes it and the why is context. Neither the title nor the why adds a requirement the body does not state.
_Avoid_: Gate evaluation instructions, verify prompt, criterion description.

**Gate Extension**:
How many things a gate ranges over — open when its body makes the evaluator enumerate a region and derive the instances, closed when it checks an inventory the author wrote down. Independent of the altitude a gate binds at, and anchored to the surface of the owning Deliverable, or to the Manifest's surface bounded by Appetite for a Global Invariant.
_Avoid_: Gate scope, gate breadth, tightness.

**Bearer Test**:
`/define`'s omission criterion for advisory-tier task-file gates — each advisory dimension protects a named future activity, and the gate is omitted only when that activity has no bearer on the manifest's surface within the artifact's life, with the missing bearer logged as a fact.
_Avoid_: Proportionality check, gate triage.

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

**Amendment Envelope**:
The bounded repair delegation `/do` holds in advance over gate text — raising a gate shown to pin an incidental mechanism to the outcome it served, raise-only, never reaching deliberately chosen mechanisms, audited and re-verified like any amendment.
_Avoid_: Self-amendment, free amendment.

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

**North Star**:
The standing project-level strategy surface — a project's diagnosis and the assumptions it rests on, who it is for and not for, its promise, how people arrive, how it makes money or what it feeds, what winning means and the number watched, its standing nevers, and the open questions no field holds — resident in every session and informing rather than binding, every line carrying one of four states (evidence, hypothesis, ruled, or empty with its filling condition), positions moving only on the owner's ruling.
_Avoid_: Steering layer, strategy doc, business context.

**Taste**:
A durable personal steering preference persisted only by offer-and-ratify — captured as preference, rationale, and flip condition in a harness memory file.
_Avoid_: Preference, style, judgment.

**Ticket**:
A self-sufficient prose work packet holding one independently schedulable lifecycle unit and everything a stranger — person or agent, with or without manifest-dev — needs to pick it up, do it, and judge it done, per the ticket convention (`skills/ticket-up/references/TICKET_CONVENTION.md`).
_Avoid_: Story, issue, task.

**Shaped Ticket**:
A Ticket whose decision space is closed — no open question remains whose answer would change what gets built or what done means — ready to execute regardless of which workflow produced it, carrying a plain-prose definition of done.

**Question Ticket**:
A Ticket whose decision space is still open — however much prior context it carries; done means the question is answered with evidence and recorded.
_Avoid_: Spike.

**Auto**:
An opt-in grant, declared at write time on either kind of Ticket, permitting unattended automation to take it end to end; absent the grant, automation leaves the Ticket entirely alone.
_Avoid_: Autonomous ticket, agent-ready.

**Ticket Type**:
An optional, single-valued naming of a Ticket's chief nature, carried so an operator's automation policy can select granted work without re-reading it — absent where none of the store's values fits, and never matched by a type query when absent.
_Avoid_: Task type (that is /define's composable gate-loading taxonomy), category, label.

**Effort**:
A named body of work a Ticket Store groups by — one destination, one front file, and its own Tickets; a store may hold several at once.
_Avoid_: Project, epic, milestone.

**Ticket Store**:
Where an effort's Tickets live, under the ticket convention — files in the repo, GitHub Issues, or a custom tracker as pluggable venues, on a venue asked once per project and recorded there; the convention is the contract, the venue a rendering.
_Avoid_: Backlog, board.

**Venue Reference**:
The mapping that renders the ticket convention onto one venue's own operations — shipped where a venue is supported out of the box, written from the user's description of their tracker where it is not.
_Avoid_: Adapter, integration.

**Ticket-up**:
The single Ticket-authoring boundary: turns a finished Manifest, direct work request, independently managed question, or source-linked follow-up into convention-compliant Tickets in the configured store; a Manifest yields one Shaped Ticket by default and splits by Deliverable only for explicit delegation.
_Avoid_: Breakdown, sharding.

**Run Ticket**:
The harness-neutral execution move that receives one exact Ticket, claims or recovers it, invokes `auto`, completes any required protected landing, and records DONE or ESCALATED evidence on that same Ticket; dispatch and backlog selection stay outside it.
_Avoid_: Auto picker, ticket trigger.

**Ticket Sweep**:
The scheduled one-Ticket dispatch move that first resumes an interrupted Ticket claimed by the automation identity, otherwise selects one ready Auto Ticket, invokes Run Ticket with that exact Ticket, and stops.
_Avoid_: Batch runner, label pulse, dependency controller.

## Relationships

- A **Manifest** contains one or more **Deliverables**.
- A **Deliverable** has one or more **Acceptance Criteria**.
- A **Manifest** has zero or more **Global Invariants**, applied across all Deliverables.
- A **Task File** can contribute **Quality Gates** and **Defaults** to `/define`.
- A **Quality Gate** becomes an acceptance-style gate in a **Manifest**.
- **Ticket-up** is the only workflow boundary that authors **Tickets** in a **Ticket Store**. A finished **Manifest** becomes one **Shaped Ticket** by default; explicit delegation may split it on existing **Deliverable** boundaries.
- A separate **Question Ticket** exists only when its question needs independent assignment, priority, blocking, or closure; related questions sharing one lifecycle stay grouped.
- `next-ticket` claims and presents the **Ticket** it names, which is what makes several sessions reading one **Ticket Store** get different ones — and it separates them only where the store's venue is a live surface every worker reads, never across separate checkouts of a file store. It never executes the pick.
- **Run Ticket** receives one exact **Ticket** from a person or dispatcher and invokes `auto` for one attempt; it never selects from the store or enforces **Auto** eligibility at dispatch. For repository work it uses one durable branch and pull request across attempts, and DONE follows the required landing rather than a merely mergeable branch.
- A **Ticket Sweep** handles at most one **Ticket** per invocation: recover an interrupted automation-owned Auto Ticket first, otherwise select one ready Auto Ticket, pass it to **Run Ticket**, and stop. Issue events are the fast path; the sweep is the correctness path.
- Trigger adapters serialize **Run Ticket** by canonical Ticket identity, bound infrastructure retries, and assign a person with run evidence after retry exhaustion; claims and labels do not duplicate host liveness state.
- The **Auto** grant requires that neither doing a **Ticket** nor judging it done needs any human's knowledge, taste, or authority — necessary but never sufficient: the author still chooses to grant.
- A **Ticket** remains the identity of its work across execution attempts: a successful attempt closes it, while an escalated attempt records its evidence and transfers or preserves the same open **Ticket**'s claim for a person; a follow-up **Ticket** represents only separate work.
- A follow-up **Ticket** receives **Auto** only when its source **Ticket** carries **Auto** and the follow-up independently meets the grant criterion; an ungranted source can create only ungranted follow-ups.
- Absence of **Auto** is one fence covering untrusted **Tickets**, **Tickets** with a designed-in human step, and venue items never written as **Tickets** at all.
- **Auto** says whether automation may touch a **Ticket** at all and is the author's call; a **Ticket Type** says which granted work an operator runs today and is the query's — keeping rollout schedule out of the grant, whose silence already carries three meanings.
- Every venue a **Ticket Store** runs on has a **Venue Reference**.
- A **Ticket Store** holds one or more **Efforts**, each with its own front file and destination — so the priority rule's "impact" is measured within an **Effort**, and comparing across them takes the **North Star**'s winning definition, the measure the destinations alone don't supply.
- A **North Star** informs every session by residency and never binds; the one binding route is `/define` routing an unsafe or irreversible Never to a **Global Invariant**.
- A project-owned North Star conventions file (emitted by `init-context` beside the doc) governs the **North Star**'s form wherever it exists, with the plugin's shipped default applying otherwise — the same precedence the **ADR Conventions** carry; cadence stays with figure-out.
- `init-context` installs and seeds a **North Star**; figure-out's docs mode keeps it current under the update asymmetry — evidence lowers a line's state, only the owner's ruling changes a position, and each position change is remembered as a decision record.
- `next-ticket` reads the **North Star**'s winning definition for cross-**Effort** comparison and surfaces a candidate that would cross a Never; `/define`'s marketing task file gates outward-facing claims against its Promise and Never.
- A **Default** becomes **Process Guidance** in a **Manifest**, except one whose violation would be unsafe or irreversible, which becomes a **Global Invariant** so it binds.
- The **Bearer Test** governs which advisory-tier **Quality Gates** a **Manifest** omits; defect-finding dimensions, deterministic project gates, and safety-critical **Global Invariants** are never eligible.
- A figure-out **Read** ships with the **Evidence Ledger** it rests on.
- **Parent-before-child Crux Priority** orders figure-out's crux selection before impact tie-breaking among same-level questions.
- `/define` encodes the understanding a figure-out **Read** establishes into a **Manifest** rather than re-deriving or re-investigating it.
- Every **Acceptance Criterion** and **Global Invariant** is one **Gate Text** in the **Manifest**; `/do` points an evaluator at it by ID rather than copying it into a prompt.
- **Gate Extension** and gate altitude are independent axes of one **Gate Text**; `/define` sets both at write time, and an instance reported mid-run is evidence a gate's extension is too narrow rather than grounds for a sibling gate.
- `/do` owns the **Do/Verify Loop**: it implements **Deliverables**, evaluates failed-or-unverified **Acceptance Criteria** and **Global Invariants** under the selected **Verification Mode**, repairs FAILs, and routes BLOCKED gates.
- `per-gate` launches one **Verifier Execution** per eligible gate, `consolidated` launches one for the outstanding gate set, and `self` launches none.
- Every gate evaluation returns PASS, FAIL, or BLOCKED evidence plus **Verification Provenance** to the **Do/Verify Loop**.
- Every **Acceptance Criterion** and **Global Invariant** is either a **Judgment Gate** or a **Deterministic Gate**; the kind is a property of the gate itself, declared in its **Gate Text**.
- The **Ratchet** governs how the **Do/Verify Loop** re-verifies **Judgment Gates** after repairs; **Deterministic Gates** re-run freely.
- **Verification Mode** and the **Ratchet** are run-level `/do` policy, never **Manifest** content; **Verification Provenance** records what a given run used.
- The **Amendment Envelope** narrows gate immutability: inside it `/do` repairs a **Gate Text** by autonomous amendment; outside it every **Acceptance Criterion** and **Global Invariant** still changes only on the user's instance-by-instance say-so.
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
- A **Form Vocabulary** belongs to wherever a turn's text lands — a surface, or a mode that redirects output, such as team mode's Slack posts — while the rule choosing among its shapes stays in the **Spine**, so it reaches every destination including those no `--surface` names.
- A **Taste** entry is ratified by the user and routed by scope to a user-level or project-level memory file; it is never inferred and applied silently, and it stays distinct from the review-time **Judgment Layer**.
- `/init-context` installs a project's **ADR Conventions**, its glossary, and the **Project Context File** wiring that keeps sessions reading both; a **Seed** is layered on top wherever the project has history, and is never a substitute for the wiring.
- figure-out loads the **ADR Conventions** at bootstrap and writes records under them, which is what makes the project's copy govern rather than the shipped default; cadence — when a session offers to record a decision — stays with figure-out and is not the project's to set.
- A **Derived Index** is rebuilt from the decision records per the **ADR Conventions**, in the same act that writes a record and restatuses whatever it supersedes.
- **Seed** entries destined for the glossary are ratified in one batch before any is written, because the glossary is resident in every session; figure-out's inline capture needs no such batch, its warrant being that the user just used the term.

## Flagged ambiguities

_None yet. Grow this section as figure-out docs-mode sessions surface clashes or canonicalizations._
