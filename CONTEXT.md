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

**Gate**:
An Acceptance Criterion or a Global Invariant — something `/do` must make hold, with evidence, before it reports completion. Each gate is one Gate Text of one declared kind, judgment or deterministic.
_Avoid_: Check, test, requirement.

**Process Guidance**:
An advisory recommendation on HOW to work during execution, weighed by `/do` rather than enforced; departing from one is legitimate and is named on whichever terminal path the run reaches — completion, escalation, or pending — and in the Execution Log too when one is kept. Only Acceptance Criteria and Global Invariants bind.
_Avoid_: Constraint, requirement, gate.

**Known Assumption**:
A Manifest entry (`ASM-*`) recording a decision taken with a default instead of a question — its value, its reason and the impact if wrong. An autonomous choice is marked `(auto)` and a User's Call opens with that label, so a reader can review what was decided for them.
_Avoid_: Note, caveat.

**Quality Gate**:
A verifiable task-file item that `/define` encodes as an acceptance-style gate.

**Default**:
A non-probed task-file item that `/define` carries into Process Guidance — unless violating it would be unsafe or irreversible, which routes it to a Global Invariant instead.

**Appetite**:
The current size of change a problem is worth — a bound on complexity and surface, independent of time and token cost, revisable prospectively under executor delegation when the benefit to the requested outcome justifies added complexity and maintenance without crossing explicit exclusions or binding requirements.
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

**Projectless Session**:
A session with no project behind its topic — a chat with no workspace, a home or scratch folder, a folder holding one finished artifact, a question that does not concern the folder it runs in. One-off work inside a project is project work. A project is a repository or working folder holding, or about to hold, work later sessions will change; a new one the user is starting counts. The workflow skills offer, build, read for and gate on no project surface in a projectless session and still run whole.
_Avoid_: No repo (a project need not be a git repository).

**Project Surfaces**:
The files a project keeps for every session and contributor — its North Star, Glossary, Decision Records under its ADR Conventions, and, where it chose one, Verification Harness — plus the project-surfaces section of the Project Context File that points sessions at them and records the Surfaces Version. `/setup-project` installs them; normal runs keep them current where their work touches them.
_Avoid_: Setup files, scaffolding.

**Glossary**:
The project's vocabulary file (`CONTEXT.md` by default), made resident in every session through the Project Context File, defining each term the project has settled so no session silently misreads one. A term is added when the project settles it.
_Avoid_: Dictionary, docs.

**ADR Conventions**:
A project-owned file stating what deserves a decision record and how to write one, self-contained so a reader with no tooling can follow it; where it exists it outranks any tool's shipped default on everything except cadence.
_Avoid_: ADR format, ADR template.

**Derived Index**:
An index that asserts nothing its records don't, and is rebuilt from them rather than edited alongside them — so staleness is a repairable lag rather than lost information.
_Avoid_: ADR list, table of contents.

**Decision Record**:
One file (an ADR) recording a decision with downstream impact — its context, the alternatives, the consequences, who decided, and the check that enforces it — append-only once published, so a later session meets why the project decided something before it decides again. A newer record supersedes or amends it; the old record's Status says so.
_Avoid_: Design doc, meeting notes.

**Verification Harness**:
A project's recommended but optional one command, for agents and people alike, for controlling what future runs will change — starting it in a known state, driving it, observing it, stopping it — and for checking that it still does its job — `--help` says everything — reading one Recipe per feature, skill, document walk or eval suite, and one for the checks run across the whole tree, so every check the project keeps is listed and run through it; the underlying commands stay usable while iterating, and the evidence a change rests on comes through the harness. It commits no evidence: a run writes its output to an evidence directory git ignores, `list` lists the recipes, and `affected` picks what a change runs from its diff. The shape setup-project ships — the tool, its subcommands, control commands such as `reset`, the settings and recipe fields — is a default each project adapts to fit itself and its people; what every harness owes is one place to learn how to verify, ask-first following cost, and the Fit to Trust jobs. Normal runs build it and keep its control, its speed and its checks sound where the work touches it, never a separate maintenance pass. Setup installs it by default, and a project may opt out and verify its own way; the verification bullet of the Project Context File records which, and runs then verify through that way and never build or gate on a harness the project did not choose — while still keeping sound, in their own form, the checks the project has, since the line is build versus maintain. A harness on disk with no bullet counts as chosen. It replaced the verification surface, feature map and reader-task list of earlier setups.
_Avoid_: Verification surface, feature map, reader-task list, test suite, control skill.

**Recipe**:
One Markdown file in the Verification Harness: what a thing is, how a user reaches it, the scenarios that exercise it (each an exact command and what it proves), and its traps. A walk recipe has a fresh reader do a task from a document alone; an eval recipe starts a behavior suite without redefining how the suite grades; a suite recipe runs the project's own whole-tree checks — lint, types, tests, build — each scenario calling its existing command.
_Avoid_: Feature-map entry, reader task, test case.

**Scenario**:
One exercise in a Recipe — an exact command and what it proves — which the Verification Harness runs, writing its Evidence locally and reporting whether it passed, failed or could not be reached; a fixed-workload Scenario also carries its Time Line in the Recipe.
_Avoid_: Test case, step.

**Evidence**:
What a gate verdict or a Scenario's outcome rests on — a command's output, the scenario summary a run writes to the harness's git-ignored evidence directory, or a quoted region of an artifact; what a pull request rests on is shown in its description. A summary claim is not evidence. In a North Star, evidence is also one of the four states, in the same sense: something observed, not asserted.
_Avoid_: Proof, claim, report.

**Time Line**:
The run time a fixed-workload Scenario is held to on one kind of machine — a `Line:` in its Recipe, set from a passing run plus headroom for noise, and changed only by the change that changes that check: lowered when it makes the check faster, raised with its reason written beside it, or held by a freeze naming a debt Ticket. A run on a kind of machine with no line reports its time and compares nothing; a crossing counts only when an immediate re-run crosses too.
_Avoid_: Budget, timeout, SLA.

**Ask-first**:
The mark on a Recipe whose run costs something a person should weigh — money or quota, load on shared systems, effects outside the repository — with its reason; run time alone is not a cost. By default the harness runs it only with `--yes`, given when a person ran it or agreed; the project's setting can change that. It follows what a run costs, not its kind: a local browser or CLI drive is unmarked.
_Avoid_: Paid, model-session, slow.

**Fit to Trust**:
Whether a check a project keeps — a Verification Harness recipe, or a test, script or checklist step in the project's own form — can be relied on for what a change touches, judged by the jobs it does — a cold proof run of one scenario passes and leaves evidence that survives cleanup, health is checkable, runs are isolated, PASS means the real path, touched checks are fast enough (none over its time line without a reason), what the change touches is controllable through the harness or the project's own scripts, a failure explains itself, and it was seen to fail on a scratch break of what it proves — never by whether it has every part or the shipped tooling. A touched check that fails a job is repaired within scope in its own form.
_Avoid_: Complete, conformant, healthy.

**Surfaces Version**:
The integer, listed in setup-project's `CHANGES.md`, that a project's context file records in its project-surfaces section. Setup-project writes it when it installs or updates the surfaces, and figure-out writes it when the user declines the whole update offer. The recorded number decides whether figure-out offers an update — none at the newest version — and lets a setup-project run mark which of its offers are new since then; a setup-project run audits the whole setup whatever number is recorded, and compares in full when none is. Unrelated to the plugin's own version.
_Avoid_: Plugin version, setup version, template version.

**Lock**:
A check installed from a correction so the corrected class of mistake fails for every later contributor — a type or structure, a lint or architecture test, an invariant test, or one owning site — with a declared scope; its repository-wide hits that a run leaves unfixed are reported as debt.
_Avoid_: Rule (that is prose), guard, concurrency lock.

**Debt**:
What a run found and did not fix: unfixed lock hits, refactor flags from workaround comments, constraint comments awaiting encoding, new suppressions, reshapes outside the change's scope, and product regressions the verification harness exposed. A run names it in its completion report, in the "Debt left" section of every pull request it opens, and on its Ticket. A later run whose work reaches the same area offers to fold it in, and `orchestrate` tickets up the debt of the runs it lands.
_Avoid_: Tech debt (too broad), TODO, backlog.

**Seed**:
The deliberately under-produced vocabulary and decision corpus `/setup-project` reconstructs from a project's history — a starting point that names what it could not recover, never a complete record.
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
An append-only, out-of-repo journal `/do` keeps by default (`--no-log` opts out) recording deviations from the Initial Approach or Deliverable order, Process Guidance departures, dead-end memory, and operational events — execution history never lives in the Manifest. It is keyed to the Manifest rather than to the invocation, so a relaunched or compacted run re-finds the record its predecessor wrote.
_Avoid_: Execution notes, amendments log, changelog.

**Door**:
A standalone skill fronted on one discovery surface as the zero-enrollment entry into manifest-dev.
_Avoid_: Wedge, funnel.

**House**:
The full understanding-first loop (figure-out → define → do) that every Door opens into; the retention engine behind the Doors.

**North Star**:
A project's standing statement of what it is for — its purpose and who it is for and not for, its goal, the principles it holds even against evidence, one measure for each part of the goal, the bets it rests on, and the open questions no section holds, followed by the titles of its `Strategy` decision records in effect — holding what decisions are judged against and never what they chose, which live in decision records; resident in every session and informing rather than binding, every position carrying one of four states (evidence, hypothesis, ruled, or empty with its filling condition), and positions moving only on the owner's ruling. Projects set up before surfaces version 8 keep the older nine-field form until they update.
_Avoid_: Steering layer, strategy doc, business context.

**Autonomy Ladder**:
The levels at which manifest-dev is adopted, each useful without the ones above it and without anyone else on the team adopting it: one Skill on its own; one piece of work understood, defined and verified; Project Surfaces kept by every run; a shared Ticket Store; and the queue running under Orchestrate — Auto Tickets end to end and others up to a ready pull request, debt ticketed up as it is found — with people stepping in only for a blocker, judgment, taste or authority.
_Avoid_: Maturity model, adoption funnel, tiers (those are the North Star, Ticket and Manifest).

**Taste**:
A durable personal steering preference persisted only by offer-and-ratify — captured as preference, rationale, and flip condition in a harness memory file.
_Avoid_: Preference, style, judgment.

**User's Call**:
A decision where two careful people with the same evidence could reasonably decide it differently, and the difference would matter to the user; the run's own confidence does not settle it. A run checks the user's Taste entries at one, decides it on the evidence when none bears, and lists it first wherever decisions are reported.
_Avoid_: Low-confidence decision, judgment call.

**Ticket**:
A self-sufficient prose work packet holding one independently schedulable lifecycle unit and everything a stranger — person or agent, with or without manifest-dev — needs to pick it up, do it, and judge it done, per the ticket convention (`skills/ticket-up/references/TICKET_CONVENTION.md`).
_Avoid_: Story, issue, task.

**Shaped Ticket**:
A Ticket whose decision space is closed — no open question remains whose answer would change what gets built or what done means — ready to execute regardless of which workflow produced it, carrying a plain-prose definition of done.

**Question Ticket**:
A Ticket whose decision space is still open — however much prior context it carries; done means the question is answered with evidence and recorded.
_Avoid_: Spike.

**Auto**:
An opt-in grant on either kind of Ticket permitting unattended automation to take it end to end, landing included — given by a person at the `ticket-up` boundary, or by `orchestrate --autonomous` to a Ticket an agent wrote wherever the grant criterion holds, never by the run that found the work, and naming its grantor. Absent the grant, automation may work the Ticket up to a ready pull request or a drafted answer, when its author has write access and no person is assigned, but never completes or lands it.
_Avoid_: Autonomous ticket, agent-ready.

**Ticket Type**:
An optional, single-valued naming of a Ticket's chief nature, carried so an operator's automation policy can select which work automation runs now without re-reading it — absent where none of the store's values fits, and never matched by a type query when absent.
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
The harness-neutral execution move that receives one exact Ticket, claims or recovers it, invokes `auto` — or resumes the Manifest its attempt record carries — and works it to a ready pull request, keeping the attempt record (its branch, run facts, progress and Manifest) on that same Ticket; it lands only when told to, through the one landing procedure, and leaves its completion record or its escalation record on the Ticket; dispatch and backlog selection stay outside it.
_Avoid_: Auto picker, ticket trigger.

**Escalation Mark**:
The durable record an escalated attempt leaves on a Ticket saying a person is needed — the thing that holds unattended dispatch off, so the claim does not have to and the Ticket stays takeable; cleared once the person answers — by the person, or by `orchestrate` recording their explicit answer as the continuation, either way clearing any automation claim left on it — and rendered by each venue's own reference.
_Avoid_: Blocked status, escalated state.

**Orchestrate**:
The dispatch move that works one effort's ready Tickets, or the whole store's, several at a time: it sorts every Ticket from the store and git alone, keeping no state of its own; proposes a plan and waits for approval by default, or acts on its own under `--autonomous`; launches each Ticket through Run Ticket in its own session; lands finished work one Ticket at a time; tickets up the debt runs leave; and keeps a status page and one list of what waits on the person.
_Avoid_: Ticket sweep, batch runner, scheduler.

## Relationships

- A **Manifest** contains one or more **Deliverables**.
- A **Deliverable** has one or more **Acceptance Criteria**.
- A **Manifest** has zero or more **Global Invariants**, applied across all Deliverables.
- A **Task File** can contribute **Quality Gates** and **Defaults** to `/define`.
- A **Quality Gate** becomes an acceptance-style gate in a **Manifest**.
- **Ticket-up** is the only workflow boundary that authors **Tickets** in a **Ticket Store**. A finished **Manifest** becomes one **Shaped Ticket** by default; explicit delegation may split it on existing **Deliverable** boundaries.
- A separate **Question Ticket** exists only when its question needs independent assignment, priority, blocking, or closure; related questions sharing one lifecycle stay grouped.
- `next-ticket` claims and presents the **Ticket** it names, which is what makes several sessions reading one **Ticket Store** get different ones — and it separates them only where the store's venue is a live surface every worker reads, never across separate checkouts of a file store. It never executes the pick.
- **Run Ticket** receives one exact **Ticket** from a person or dispatcher and invokes `auto` for one attempt; it never selects from the store or enforces **Auto** eligibility at dispatch. For repository work it uses one durable branch and pull request across attempts, and its Ticket closes only once a landing is observed, never on a merely mergeable branch.
- **Orchestrate** passes each **Ticket** it launches to **Run Ticket** in a session of its own, and takes each finished run's landing turn itself, one **Ticket** at a time; a run started by hand stops at its ready pull request the same way. A file store gets no parallel runs: **Orchestrate** runs its **Tickets** one at a time in its own session.
- **Orchestrate** never launches a **Ticket** carrying an **Escalation Mark**; a human picker applies no such filter, which is what lets escalated work compete for attention on the ordinary priority rule. A third failed launch in a row hands the **Ticket** to a person through an **Escalation Mark**.
- The **Auto** grant requires that neither doing a **Ticket** nor judging it done needs any human's knowledge, taste, or authority — necessary but never sufficient: the author still chooses to grant.
- A **Ticket** remains the identity of its work across execution attempts: a successful attempt closes it, while an escalated attempt records its evidence and releases the same open **Ticket**'s claim under an **Escalation Mark**; a follow-up **Ticket** represents only separate work.
- A follow-up **Ticket** receives **Auto** only through a grant at its own `ticket-up` boundary after it meets the grant criterion — a person's, or `orchestrate --autonomous`'s; whatever its source carries, the run that found the work never grants it.
- Absence of **Auto** keeps completion and landing with a person: unattended work takes such a **Ticket** only up to a ready pull request, only when its author has write access and no person is assigned, and never touches venue items that were never written as **Tickets**.
- **Auto** says whether automation may finish a **Ticket** and is the grantor's call; a **Ticket Type** says which work an operator runs today and is the query's — keeping rollout schedule out of the grant.
- Every venue a **Ticket Store** runs on has a **Venue Reference**.
- A **Ticket Store** holds one or more **Efforts**, each with its own front file and destination — so the priority rule's "impact" is measured within an **Effort**, and comparing across them takes the **North Star**'s goal and measures, the measure the destinations alone don't supply.
- Each level of the **Autonomy Ladder** works without the ones above it; at the top, **Orchestrate** runs the queue through **Run Ticket**, and a person steps in at an **Escalation Mark**, a **User's Call** or a **Taste** offer.
- **Project Surfaces** live in the project and are read by every session through the **Project Context File**; the **Glossary** and the **Decision Records** are two of them, and the **Verification Harness** runs one **Scenario** at a time, writing its **Evidence** locally, while each **Recipe** carries its **Time Lines**.
- A **North Star** informs every session by residency and never binds; the one binding route is `/define` routing a principle whose violation would be unsafe or irreversible to a **Global Invariant**.
- A project-owned North Star conventions file (emitted by `setup-project` beside the doc) governs the **North Star**'s form wherever it exists, with the plugin's shipped default applying otherwise — the same precedence the **ADR Conventions** carry; cadence stays with figure-out.
- A chosen option lives in a **Decision Record**, never in the **North Star**; a guiding one carries the area `Strategy`, and the **North Star** lists the titles of those in effect as a **Derived Index** of them.
- `setup-project` installs and seeds a **North Star**; figure-out's docs mode keeps it current under the update asymmetry — evidence lowers a position's state, only the owner's ruling changes a position, and each position change is remembered as a decision record.
- `next-ticket` reads the **North Star**'s goal and measures for cross-**Effort** comparison and surfaces a candidate that would cross one of its principles; `/define`'s marketing task file gates outward-facing claims against its goal and principles.
- A **Default** becomes **Process Guidance** in a **Manifest**, except one whose violation would be unsafe or irreversible, which becomes a **Global Invariant** so it binds.
- The **Bearer Test** governs which advisory-tier **Quality Gates** a **Manifest** omits; defect-finding dimensions, deterministic project gates, and safety-critical **Global Invariants** are never eligible.
- A figure-out **Read** ships with the **Evidence Ledger** it rests on.
- **Parent-before-child Crux Priority** orders figure-out's crux selection before impact tie-breaking among same-level questions.
- `/define` encodes the understanding a figure-out **Read** establishes into a **Manifest** rather than re-deriving or re-investigating it.
- Every **Acceptance Criterion** and **Global Invariant** is one **Gate Text** in the **Manifest**; `/do` points an evaluator at it by ID rather than copying it into a prompt.
- **Gate Extension** and gate altitude are independent axes of one **Gate Text**; `/define` sets both at write time, and an instance reported mid-run is evidence a gate's extension is too narrow rather than grounds for a sibling gate.
- `/do` owns the **Do/Verify Loop**: it implements **Deliverables**, judges failed-or-unverified **Acceptance Criteria** and **Global Invariants** against the evidence each names, repairs FAILs, and routes BLOCKED gates.
- Every gate evaluation returns PASS, FAIL, or BLOCKED with the concrete evidence behind it.
- Every **Acceptance Criterion** and **Global Invariant** is either a **Judgment Gate** or a **Deterministic Gate**; the kind is a property of the gate itself, declared in its **Gate Text**.
- The **Ratchet** governs how the **Do/Verify Loop** re-verifies **Judgment Gates** after repairs; **Deterministic Gates** re-run freely.
- The **Ratchet** is run-level `/do` behavior, never **Manifest** content.
- Gate text is immutable to the run: every **Acceptance Criterion** and **Global Invariant** changes only on the user's say-so, through the skill that authored it.
- A **Skill** may invoke other **Skills** and may run through host **Agent** contexts.
- A **Host Continuation Backstop** is an outer guard for unattended runs; it does not replace the **Do/Verify Loop**.
- A **Phase Checkpoint** can protect a handoff between workflow phases, while terminal completion stays tied to the final deliverable's acceptance evidence.
- **Babysit PR** and **Review PR** can run asynchronously on the same pull request: **Review PR** applies quality pressure, while **Babysit PR** drives the author-side lifecycle toward green and mergeable.
- **Review PR** in manifest mode independently re-verifies a **Manifest** against the pull request head.
- The **Judgment Layer** runs inside **Review PR** (both modes) as non-binding questions, kept distinct from a **Manifest**'s binding **Acceptance Criteria** and from the defect fleet.
- A **Steering Message** is encoded by autonomous amendment, with judgment calls audited as Known Assumptions and pivots recorded in the **Execution Log**.
- `/do` keeps an **Execution Log** keyed to the **Manifest**, which is what lets a relaunch reopen the same file.
- **Babysit PR** uses **PR Grounding** so newer comments do not override stronger sources of intent by recency alone.
- **CI One-Shot** is a constrained mode of **Babysit PR**.
- One **Door** per discovery surface; every **Door** opens into the same **House**.
- A **Re-host** preserves **Spine** content verbatim while making its **Altitude** typographically legible.
- A **Taste** entry is ratified by the user and routed by scope to a user-level or project-level memory file; it is never inferred and applied silently, and it stays distinct from the review-time **Judgment Layer**.
- `/setup-project` installs a project's **ADR Conventions**, its glossary, and the **Project Context File** wiring that keeps sessions reading both; a **Seed** is layered on top wherever the project has history, and is never a substitute for the wiring.
- figure-out loads the **ADR Conventions** at bootstrap and writes records under them, which is what makes the project's copy govern rather than the shipped default; cadence — when a session offers to record a decision — stays with figure-out and is not the project's to set.
- A **Derived Index** is rebuilt from the decision records per the **ADR Conventions**, in the same act that writes a record and restatuses whatever it supersedes.
- **Seed** entries destined for the glossary are ratified in one batch before any is written, because the glossary is resident in every session; figure-out's inline capture needs no such batch, its warrant being that the user just used the term.

## Flagged ambiguities

_None yet. Grow this section as figure-out docs-mode sessions surface clashes or canonicalizations._
