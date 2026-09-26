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

figure-out reaches understanding of the *problem*; this skill owns the *encoding*
calls — invariant versus guidance, what a gate ranges over, where it binds, its
kind. Surface the load-bearing ones with a recommended answer; auto-decide the
rest and mark them `(auto)` with a matching `ASM-*`.

An amendment from an unattended executor is unattended: self-answer within the
caller's delegation, ask no questions, and wait for no approval. Validate a
delegated Appetite revision before applying it: the broader work serves the
requested outcome, its benefit justifies the added complexity and maintenance,
it has not already been done as excess, and it crosses no explicit exclusion or
binding requirement. Preserve those requirements unless user steering explicitly
changes them. A request outside that delegation returns an evidenced blocker
without changing the Manifest. Record material autonomous decisions as `(auto)`
items with matching `ASM-*` entries naming the rationale and impact if wrong.

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
  convenience: re-cut it, don't encode it. Order least-proven first within real
  dependencies, so an unworkable direction surfaces while there is room to turn.
- Every Acceptance Criterion and Global Invariant is one text — title, body,
  optional why — stating what done means, the evidence to inspect, and the
  threshold between PASS and FAIL, precise enough that two evaluations read the
  same thing. The title never adds a requirement the body omits, and the why
  binds nothing.
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
  Appetite.
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
instead. Per-repo for multi-repo manifests. These carry encoder data only —
figure-out's own probe files are a separate set this skill never reads, and any
`tasks/**/references/*.md` is gate-evaluation lookup data, not loaded here.

| Domain | Indicators | File |
|---|---|---|
| Coding | Any code change; base review dimensions for intent, bugs, operational readiness, design, tests, docs, context adherence | `CODING.md` |
| Feature | New functionality, APIs, enhancements | `FEATURE.md` |
| Bug | Defects, errors, regressions, "broken" | `BUG.md` |
| Refactor | Restructuring, cleanup, pattern changes | `REFACTOR.md` |
| UI | Anything a person sees and judges rather than calls — screens, decks, rendered documents, emails, games | `UI.md` |
| PR lifecycle | Shipping a change through CI, review, approvals | `PR_LIFECYCLE.md` |
| Prompting | LLM prompts, skills, agents, system instructions | `PROMPTING.md` |
| Prose floor | Any prose deliverable — the rules holding in both registers (base) | `PROSE_FLOOR.md` |
| Writing | Human-voice register: prose, articles, copy, social, creative | `WRITING.md` |
| Document | Documentation register: specs, proposals, reports, formal docs | `DOCUMENT.md` |
| Tech design | Design docs consolidating finished understanding | `TECH_DESIGN.md` |
| Research | Investigations, analyses, comparisons | `research/RESEARCH.md` |
| Blog | Blog posts, articles, tutorials | `BLOG.md` |
| Marketing | Landing pages, launch posts, ads, pricing and positioning copy | `MARKETING.md` |

FEATURE/BUG/REFACTOR compose onto `CODING.md`, adding `UI.md` where the change
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
manifest's surface within the artifact's life, and log the missing bearer as a
fact — "no future reader exists", never "unlikely to find much". Weigh surface
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

Give a plain-language digest — the pain, the plan, what gets built, the
guardrails, how it is verified. No codes, no schema vocabulary; it reads like
talking to a colleague. The pain matters most, being the one thing only the user
can confirm and the surface where an invented Problem gets caught. Wait for a yes
unless the caller is unattended or this is an amendment. Then emit the handoff
(`<manifest-path>` is the absolute path you wrote):

```text
Manifest complete: <manifest-path>

To execute: /do <manifest-path>
For unattended execution, invoke /do <manifest-path> as the execution entrypoint. /do reads the manifest and owns the manifest-completion contract: it sets that completion contract when the active harness exposes a goal-setting or continuation capability, or prints the manual copy-paste contract when not. /define does not set a separate /do goal.
```
