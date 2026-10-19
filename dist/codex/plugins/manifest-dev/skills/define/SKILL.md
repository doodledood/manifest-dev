---
name: define
description: 'Manifest builder. Turns shared understanding into a verifiable Manifest with Deliverables, Acceptance Criteria, Global Invariants, and an Initial Approach. Use when planning features, scoping refactors, debugging complex issues, or when the user asks to define, scope, plan, spec out, make a manifest, or break down a task.'
argument-hint: '[task] [<manifest-path> to amend] [--babysit <pr-url>]'
user-invocable: true
---

Encode the conversation's shared understanding as a Manifest at
`~/.manifest-dev/manifests/manifest-<ts>.md` (create the dir; fall back to a
writable temp path only if home is not writable); how you interview is yours. No
shared understanding in the transcript → invoke `figure-out` first, propagating
`--autonomous` when the caller is unattended. A manifest path in the arguments
means amend: targeted changes only, IDs stable, no renumbering.

Project surfaces — setup and its update, the verification harness and its recipes, decision
records, the glossary, the North Star — belong to a project: a repository or working folder
holding, or about to hold, work later sessions will change — a new one the user is starting
counts — which this work concerns. A chat with no workspace, a home or scratch folder, a folder
holding one finished artifact, or a question that does not concern the folder the session runs in
is none. There, offer, build, read for, gate on or record none of them, and write the Manifest as usual,
its own gates checking the work directly. One-off work inside a project is still project work: it
keeps the gate of every recipe whose paths it touches.

Before encoding a new Manifest for work in a project, read what earlier work left on it —
logs and Manifests for this repository, open Tickets on the work's paths, and pull requests' "Debt left"
sections — following `../figure-out/references/RECALL.md`. For a project, note in the digest when its
surfaces version, read from the context file on disk, is missing or older than setup-project's newest, without stopping to update, and
record it as an `ASM-*` entry. Record each offer flagged upstream as its own `ASM-*` entry, so the
completion report names it.

figure-out reaches understanding of the *problem*; this skill owns the *encoding*
calls — invariant versus guidance, what a gate ranges over, where it binds, its
kind. Surface the load-bearing ones with a recommended answer; auto-decide the
rest and mark them `(auto)` with a matching `ASM-*`.

Where the host offers a question-selection capability — a way to put a question
to the user as options to pick from, with room to answer in their own words —
ask through it by default, with your recommended answer as each ask's first
option. Key calls are mostly independent of each other, so batch them there into
as few turns as they allow; a call whose answer would change another's goes
first, and the other waits for it. Without that capability, or once the user has
asked you to ask in prose, write the ask in plain text, one ask per turn. An
unattended caller is asked nothing: decide each call within its delegation and
record it as below.

An amendment from an unattended executor is unattended: self-answer within the
caller's delegation, ask no questions, and wait for no approval. Validate a
delegated Appetite revision before applying it: the broader work serves the
requested outcome, its benefit justifies the added complexity and maintenance,
it has not already been done as excess, and it crosses no explicit exclusion or
binding requirement. Preserve those requirements unless user steering explicitly
changes them. A request outside that delegation returns an evidenced blocker
without changing the Manifest. Record material autonomous decisions as `(auto)`
items with matching `ASM-*` entries naming the rationale and impact if wrong. An
`ASM-*` entry that records a user's call starts its text with `User's call:` and
names the alternative not taken and what decided it, so the user can find it
among the rest.

**The user's call.** A decision is the user's call when two careful people with
the same evidence could reasonably decide it differently, and the difference
would matter to the user. Test each material decision against that sentence;
your own confidence does not settle it. At a user's call, check the user's Taste
entries — ratified preferences in a `## Taste` section of a loaded memory file.
Follow an entry only where it clearly bears: it speaks to this kind of call, and
following it would change the choice. A general lean that would tilt almost any
call, such as less effort or lower cost, does not bear on its own. Otherwise
decide on the evidence. Wherever decisions are reported, list the user's calls
first, each with the alternative not taken and what decided it — the entry
followed, or that no entry applied.

**Taste on reversal.** When the user, present in the session, reverses a call an
earlier run made and states why, and the reason is a preference another user
could want the opposite of — not a behavior every session owes — offer a Taste
entry before the handoff. Show it
verbatim in three parts: the preference, naming the kind of call it covers; the
rationale, built on the reason the user stated, never one you inferred; and when
it should yield. Name the memory file it would go in, and ask whether it is
standing or for this case only; "this case only" is a no. Only the user's
explicit yes to that text writes it, inside that file's `## Taste` section,
changing nothing else. When an existing entry decided the reversed call, raise
the clash instead — has the entry's default moved, or is this an exception? Show
any revision or removal verbatim, and apply it only on the user's explicit yes
to that text. An unattended session makes no offer.

The Manifest is the acceptance contract — what the user accepts as "I'd ship the
outcome of executing this" — and `/do` executes it later with none of this
conversation's context, so everything binding lives in the gate texts themselves.
For work others will use or extend, include ease of doing that correctly in the
existing quality gates or relevant Acceptance Criteria. Judge concrete burdens
the work creates or perpetuates, proportionate to its useful life and explicit
bounds; sound existing structure needs no redesign.
That gives a floor that isn't ceremony:

- Follow the schema in `references/SCHEMA.md` exactly — it is what the executor
  parses, and it carries the ceiling invariant every manifest ships verbatim.
- Open Intent with the **Problem**: one specific story of what breaks or grates
  today, the baseline everything else is pitched against. A session that cannot
  name a pain has found a stop signal, not an empty field — return to figure-out,
  or conclude there is nothing worth building. Appetite follows: the size of
  change the problem is worth, bounding complexity and surface rather than time.
- Cut each **Deliverable** as a slice that can be finished on its own and
  exercised end-to-end — put in front of its real use, not merely inspected as
  present — which is what lets its criteria judge whether it works rather than
  whether it exists. A slice cut along a layer ("the data model", "the sources")
  can only be gated on existence, and *it compiles* or *the file exists* are
  inspections rather than uses. A request framed as layers is the requester's
  convenience: re-cut it, don't encode it. A requested cut, even a numbered list of
  Deliverables, settles scope, not where the cuts fall, so keeping its layers is never a
  user's call: keep its scope and re-cut its layers, recording the re-cut as an `(auto)`
  choice the requester can veto. Order least-proven first within real
  dependencies, so an unworkable direction surfaces while there is room to turn.
- **Make the change easy first.** When the shape of a change that crosses a function
  boundary — figure-out's sketch, or one drawn here for a direct request — shows that the area
  it touches resists it (a value threaded through layers, state with more than one writer, a
  missing seam, a workaround the change would extend), cut a behavior-preserving preparatory
  Deliverable before the change itself: scoped to what this change needs, pinned by existing or characterization
  tests, and able to land as its own pull request. Recorded debt on the work's path that
  still stands, checked against the current code, joins it — offered to an attended user,
  decided within the caller's delegation when unattended. Debt off the path stays where it is.
- **Verification comes before the work it checks.** In a project, the verification bullet of the
  context file's project-surfaces section records how the project checks that its work still does
  its job: its verification harness — one command with a recipe per thing it checks, as
  setup-project's `references/VERIFICATION_HARNESS.md` describes — or its own way, named there; a
  harness already on disk with no bullet counts as chosen, and an `ASM-*` suggests recording its
  bullet. The harness is the project's choice,
  never the run's. Building is the choice's; keeping sound is every run's: in any form, a check the
  work touches that is broken, drifting or not fit to trust (`../setup-project/references/VERIFICATION_HARNESS.md`
  → *Fit to trust*) is repaired within scope, ahead of the work that relies on it.
  - **Harness:** where it lacks what the work needs, or a recipe the work touches is drifting or not
    fit to trust, cut building or repairing it, scoped to what the change touches, as the first Deliverable, ahead of
    any preparatory slice; unattended runs build it too. A Manifest that touches anything a recipe
    covers, or a path one should cover but does not, carries a gate that each touched recipe is
    added or updated and run, and what it found reported. A recipe marked ask-first is run only where
    the project's setting or the user allows — a user who approves a Manifest whose gate runs it has
    agreed; otherwise its gate holds that the recipe is updated and that the run it still owes is
    named in the report.
  - **Its own way, or no bullet yet:** gates verify through the means the bullet names, or with no
    bullet through the verification assets the project keeps — its tests, scripts and checklists —
    and no gate or Deliverable builds a harness the project did not choose. A touched check of
    theirs that fails *Fit to trust* is repaired in its own form, cut as the first Deliverable like a
    harness repair. Where none of them can check what the work touches, the first Deliverable adds
    that check in the project's own form. With no bullet and no harness on disk, record the harness as a recommendation the report carries, as an `ASM-*`,
    never as work.
- **A recorded check still to be built is built.** Search the project's decision records for
  `Enforced by` lines reading `not yet`. When the work implements or touches such a decision, a
  gate holds that the named check exists, fails when the decision is reversed, and carries a
  comment citing the record, and that the record's line names the check in place of `not yet`.
- Every Acceptance Criterion and Global Invariant is one text — title, body,
  optional why — stating what done means, the evidence to inspect, and the
  threshold between PASS and FAIL, precise enough that two evaluations read the
  same thing. For subjective quality, anchor that threshold to the user's chosen
  references and observable effect, or a named owner's acceptance; record who
  decides and what resolves disagreement. The title never adds a requirement the
  body omits, and the why binds nothing.
- Every specific in a gate or a Deliverable has a source. Where the request sets
  no bar, the threshold is the behavior it does state — a pass/fail property, a
  command, a named reference — not a number made up to look measurable. A
  specific the user did not give enters only when derived from a stated
  requirement and said so in its why, or as a choice: an `(auto)` `ASM-*`
  carrying the value and its reason, cited by the gate; otherwise cut it. The
  ones that slip in sit inside a larger check — a tolerance, sample size, or run
  length; a second pass bar beside the stated one; a sign-off; an artifact beyond
  the change itself, such as a runbook or design doc — so reread every gate body
  for them before handoff, letting the user veto a value instead of meeting it
  mid-run as a requirement.
- A target whose reachability the session did not establish binds a floor and
  advises an aim: the gate holds the floor — a sourced specific like any other,
  or a behavior such as faster than a measured baseline — and the hoped-for
  value goes to Process Guidance as the aim, so the run reaches for it without
  being trapped by it. A number the user stated stays binding: attended, ask
  whether it is a firm requirement or an aim; unattended, keep it binding and
  record in an `ASM-*` that its reachability was not established.
- Every gate declares "Judgment gate." or "Deterministic gate." — never
  inferred; an executor handed an undeclared kind is broken by it. A gate mixing
  a command with a judgment is a judgment gate.
- Bind the **outcome**, not the mechanism that serves it: if the executor met the
  intent a better way and the gate would still go false, it is pinning a means —
  raise it until it isn't, stopping at what the work leaves behind can judge.
  The test reaches means, never ends: where a mechanism was deliberately chosen
  as the thing that must hold, it *is* the outcome, and raising it away is the
  erosion this discipline exists to prevent. Make that choosing legible — in the
  gate's why where nothing else shows it — so a later reader can tell a
  deliberate mechanism from an incidental one.
- Write a gate so it ranges over its **region**, not an inventory: where the
  criterion is *no X anywhere in R*, the body makes the evaluator enumerate R and
  derive the instances, so tomorrow's instance is caught too. Make the procedure
  exact rather than the list. An Acceptance Criterion's region is its
  Deliverable's surface; a Global Invariant's is the Manifest's, bounded by
  Appetite. Distinguish the property owed across that region from the evidence
  sufficient to accept it: where exhaustive observation is infeasible, the gate
  names a closed coverage set — a list or a count, never "at least these, plus
  any others" — sourced like any other chosen specific; state its limits, and
  share evidence across gates that inspect the same surface. Representative evidence never turns an explicit
  universal requirement into a sampled one.
- Check that the gates can hold **together** within the stated scope and operating
  conditions. Settle open-ended horizons and competing resource or performance
  demands before handoff, with proposed bounds grounded in the intended use and
  recorded as proposals.
  Surface unresolved tradeoffs for the owner (or return a blocker outside an
  unattended caller's delegation); preserve the ambition and explicit requirements
  until that decision authorizes a change. Completion uses the agreed evidence and
  thresholds; a new preference changes the contract rather than reopening a
  satisfied gate.
- Anything whose violation would be unsafe or irreversible becomes a Global
  Invariant — never Process Guidance, never dropped for resisting verification.
  Where only part of it is judgable from the artifacts, gate that part and record
  the rest as an `ASM-*` naming what enforces it instead.
- Encode every explicit Out of bounds exclusion once as a Global Invariant;
  anticipated omissions that may change belong in the advisory plan.
- A criterion the user pinned by *reacting* to something concrete — a mock, a
  reference, a chosen direction — is a success criterion, not flavor. Encode it
  as a gate, judged against what the reaction named. Never route one to the
  advisory layer, where it can be weighed away.
- Triage Known Assumptions by what being wrong would cost: work redone is an
  assumption and belongs in `ASM-*`; an approach invalidated is not — settle that
  gap now, as a gate where it must not be departed from or as Initial Approach
  direction where it is guidance. Left as an assumption it surfaces mid-run,
  where a stalled unattended execution costs far more.
- A criterion nothing can check is sharpened or dropped with a recorded
  assumption; only gates bind. Nothing deliberately chosen as the thing that must
  hold may be dropped.

Before writing gate bodies, invoke the prompt-engineering skill for its
calibration if it is available; a body is a prompt the moment an evaluator
follows it, and readable-but-vague prose states an aspiration where a check
belongs. Come back here — this skill owns the interview.

## Task files

Identify the task type and load the matching file(s) from `tasks/`. Their
**Quality Gates** auto-encode as `INV-G*`/`AC-*` and their **Defaults** as `PG-*`
before the interview, so the dialogue carries the encoding forward; a Default
whose violation would be unsafe or irreversible routes to a Global Invariant
instead. A rule the user has stated — in the session or in a context file — or a
convention the project states or documents overrides a conflicting Default: omit or adjust the
Default. Every Default of a loaded file ends up carried, adjusted or omitted — carrying one
changed in a `PG-*` is adjusting it — and each adjusted or omitted one is named in an `ASM-*`
with why: the rule that overrides it, or what makes it clearly inapplicable. A reader can then
tell a Default set aside on purpose from one lost. The context file's outcome rules —
naming, structure, architecture — also constrain the shape the Manifest specifies,
not only which Defaults it drops. Taste entries stay weighed per call, as above. Per-repo for
multi-repo manifests. These carry encoder data only —
figure-out's own probe files are a separate set this skill never reads, and any
`tasks/**/references/*.md` is gate-evaluation lookup data, not loaded here.

| Domain | Indicators | File |
|---|---|---|
| Coding | Any code change; base review dimensions for intent, bugs, operational readiness, design, tests, docs, context adherence | `CODING.md` |
| Feature | New functionality, APIs, enhancements | `FEATURE.md` |
| Bug | Defects, errors, regressions, "broken" | `BUG.md` |
| Refactor | Restructuring, cleanup, pattern changes | `REFACTOR.md` |
| UI | Anything a person sees and judges rather than calls — screens, decks, rendered documents, emails, games | `UI.md` |
| PR lifecycle | Shipping a change through a GitHub pull request — its proof, CI, review, approvals | `PR_LIFECYCLE.md` |
| Prompting | LLM prompts, skills, agents, system instructions | `PROMPTING.md` |
| Prose floor | Any prose deliverable — the rules holding in both registers (base) | `PROSE_FLOOR.md` |
| Writing | Human-voice register: prose, articles, copy, social, creative | `WRITING.md` |
| Document | Documentation register: specs, proposals, reports, formal docs | `DOCUMENT.md` |
| Tech design | Design docs consolidating finished understanding | `TECH_DESIGN.md` |
| Performance | A number is the point — latency, throughput, memory, cost — or a change claims to move one | `PERF.md` |
| Research | Investigations, analyses, comparisons | `research/RESEARCH.md` |
| Blog | Blog posts, articles, tutorials | `BLOG.md` |
| Marketing | Landing pages, launch posts, ads, pricing and positioning copy | `MARKETING.md` |

FEATURE/BUG/REFACTOR/PERF compose onto `CODING.md` when code changes, adding `UI.md` where the change
touches something seen; `UI.md` stands alone for a non-code visual artifact.
Text-authoring composes `PROSE_FLOOR.md` with exactly one register — `WRITING.md`
(BLOG, MARKETING compose onto it) or `DOCUMENT.md` (TECH_DESIGN composes onto
it). **The two registers never compose together:** their rules contradict each
other by design, so a deliverable takes the register of its dominant body and the
other's gates do not apply. Research composes `research/RESEARCH.md` with its
sources. `PR_LIFECYCLE.md` composes where the output ships through a GitHub pull
request. `PROMPTING.md` does not compose with `CODING.md` unless executable code
also changes.

**The omission valve.** A task-file Quality Gate is omitted only with stated
reasoning, on one of two grounds: it is clearly inapplicable, or — advisory-tier
gates only — it fails the **bearer test**. Each advisory dimension protects some
future activity (modification, regression-catching, reading, operating, the next
contributor); omit the gate only where that activity will not occur on this
manifest's surface within the artifact's life, and record the omission as an
`ASM-*` whose assumption is the missing bearer, stated as a fact — "no future
reader exists", never "unlikely to find much" — and whose impact if wrong names
what goes unreviewed. Weigh surface
and stakes together, never size alone: a one-line change on a payment path keeps
the full sweep. The full set is the default and doubt includes. Never eligible:
defect-finding dimensions, deterministic project gates, safety-critical Global
Invariants, and the ceiling.

**Specialized gates activate a skill.** Where a gate needs specialized behavior
its body tells the evaluator to *activate* a named skill — never to spawn a
further agent, which would bypass the gate's verdict contract. Code-quality gates
activate `review-code` with a dimension; other checks name their own, such as
*"Done when the `check-pr` skill reports the pull request ready"*. Name the
dimension and stop: that skill owns its own threshold, and a second copy in the
gate can contradict it.

## Amendment

A manifest path means amend. Read it fully. Validate every gate against the
current schema first: a title, a body, an optional why, a stated kind. A gate
carrying a `verify` block of any shape, or stating a `phase`, or declaring no
kind, is the superseded schema — stop and require fresh generation, without
passing the incompatible Manifest as an amendment input. Never translate,
migrate, or partially preserve it, and offer no migration path.

Otherwise apply targeted changes only, preserving unaffected items verbatim. No
amendments log — git is history.

- **Reconcile the frame, not just the leaves.** An amendment that widens scope or
  changes a stated rule leaves Intent, the Architecture, the order rationale and
  any scope-bounding guidance describing the older, smaller task — and they read
  as unaffected precisely because nothing is editing them. Re-read them against
  what the manifest now covers, and re-read existing gates for under-coverage
  over the widened area.
- **An instance report names the gate that missed it.** Steering arrives as
  instances, and the reflex is a criterion per instance. Ask first which gate
  should already have caught it: where one claims the class and missed it, its
  region was drawn narrower than the class — widen that gate rather than adding a
  sibling beside it.
- **An amendment that changes a decision produces a gate.** Adding work and
  reversing a rule the system already states are different amendments; the second
  needs its own Acceptance Criterion. Edited prose notes a decision but checks
  nothing.

## What else loads

| Reference | Loads when |
|---|---|
| `references/SCHEMA.md` | writing or validating any gate — the executor parses it |
| `references/BABYSIT_MODE.md` | `--babysit <pr-url>`, which synthesizes a lifecycle-only manifest from a pull request instead of a fresh interview |
| `references/MULTI_REPO.md` | the task spans repositories, so the manifest declares `Repos:` in Intent |

## Finishing

A new Manifest gets one review in a fresh context before the digest, attended or
unattended; an amendment gets none. The context that wrote the gates reads them
as it meant them, which is how an invented number, a dropped point or two gates
that cannot both hold survive the reread above. Hand a fresh context the paths of
`references/REVIEW.md` — its brief — this file, `references/SCHEMA.md`, the task
files this session loaded, the project context file and any loaded memory file
holding Taste entries, the Manifest, the session record — the figure-out log
when one exists, and the transcript where the host keeps one the fresh context
can read, else the conversation passed verbatim — and any model of the design
built earlier in the session, figure-out's included, so the review can extend
it. Where no isolated context is
available, review against that brief yourself and say in the digest that the
review was self-graded. Settle every finding in one pass: fix it, or reject it
and name it with the reason in the digest (unattended, in an `(auto)` `ASM-*`).
A fix that changes what the user agreed is a user's call — asked when attended;
unattended, not applied, so what the user agreed stands and the finding goes in
an `(auto)` `ASM-*`. A hole is a finding the stated Intent already rejects, so
close each one whose gate or design decision serves that Intent, attended or
unattended; only a fix that would change the Intent or the scope is the user's
call, and unattended its `(auto)` `ASM-*` names the hole as still open. An entry
that merely accepts a hole the Intent rejects does not settle it. Settle each
ambiguity by writing one reading into the gate. No second review follows.

Give a plain-language digest — the pain, the plan, what gets built, the
guardrails, how it is verified, the holes the review found and how each was
settled (a search that found none is never offered as proof the Manifest is
sound), and every number a gate holds the work to (each
threshold, bound, count or target, in plain words) so the user can veto one
before execution. No codes, no schema vocabulary; it reads like
talking to a colleague. The pain matters most, being the one thing only the user
can confirm and the surface where an invented Problem gets caught. Wait for a yes
unless the caller is unattended or this is an amendment. Then emit the handoff
(`<manifest-path>` is the absolute path you wrote):

```text
Manifest complete: <manifest-path>

To execute: /do <manifest-path>
For unattended execution, invoke /do <manifest-path> as the execution entrypoint. /do reads the manifest and owns the manifest-completion contract: it sets that completion contract when the active harness exposes a goal-setting or continuation capability, or prints the manual copy-paste contract when not. /define does not set a separate /do goal.
```

Then stop. A yes to the plan approves the Manifest, not its execution: /do runs
only when the user or a calling workflow invokes it, so the lines above are for
them, never an instruction to you.
