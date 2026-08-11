---
name: define
description: 'Manifest builder. Turns shared understanding into a verifiable Manifest with Deliverables, Acceptance Criteria, Global Invariants, and an Initial Approach. Use when planning features, scoping refactors, debugging complex issues, or when the user asks to define, scope, plan, spec out, make a manifest, or break down a task.'
argument-hint: '[task] [<manifest-path> to amend] [--babysit <pr-url>]'
user-invocable: true
---

## Where the manifest goes, and what runs first

Encode the conversation's shared understanding as a Manifest at `~/.manifest-dev/manifests/manifest-{ts}.md` (create the dir; `~` = `$HOME` / `%USERPROFILE%`) — a durable home so manifests survive OS temp cleanup across multi-day work. Fall back to a writable temp path (`/tmp/`, else `$TMPDIR` / `%TEMP%`) only when the home directory isn't writable. If the transcript lacks shared understanding, invoke `manifest-dev:figure-out` first; propagate `--autonomous` when invoked from `/auto` or `/do`'s amendment path. **Pre-flight:** if `--babysit <pr-url>`, load `references/BABYSIT_MODE.md` and follow its synthesis flow; if `$ARGUMENTS` contains a manifest file path, amend (see below); else fresh.

## Encoding discipline

figure-out reaches shared understanding of the *problem*; /define handles manifest-specific *encoding* judgment calls — invariant vs process guidance, AC scope and pass threshold, gate kind. Surface the load-bearing encoding decisions briefly with a recommended answer before encoding; auto-decide the rest and mark `(auto)` + matching ASM. The manifest is the acceptance contract — what the user accepts as *"I'd ship the outcome of executing this."*

**Problem first.** Intent opens with the Problem — one specific story of what breaks or grates today, not an abstract need — because it is the baseline the rest of the manifest is written against: gates are pitched at what would actually relieve it, and whoever judges the result later weighs the work against that baseline rather than against an ideal. Appetite follows: the size of change the problem is worth, bounding complexity and surface rather than time or tokens, and the criterion for how many Deliverables to cut and how much to gate beyond what task files supply. Out of bounds records what the work deliberately leaves alone, and each bound is stated exactly once: one that must hold is written as the Global Invariant that binds it and appears nowhere else, while the rest stay a plain list that gains no shadow gate. A bound written twice is two texts that can drift apart, and only one of them binds. Elicit whatever the conversation left unset — these are encoding decisions, not re-investigation. A session that cannot name a pain has found a stop signal rather than an empty field: return to `manifest-dev:figure-out`, or conclude there is nothing worth building. With no user to ask, invoke `manifest-dev:figure-out --autonomous` to find the pain; only when that comes back empty, carry the thinnest Problem the evidence honestly supports with an `ASM-*` recording its thinness — and prefer returning no manifest to inventing one. All of that governs a fresh session. An amendment derives the fields from the manifest's own content plus the amendment's context and records a thin result as an `ASM-*`; it never halts, since a run may already be in flight and the manifest already exists.

**Cutting Deliverables.** A Deliverable is a slice that can be finished on its own and exercised end-to-end — put in front of its real use: run, read, or otherwise judged in the situation it is for, not merely inspected as present. That is what lets its Acceptance Criteria judge whether it works rather than whether it exists; a Deliverable cut along a layer ("the data model", "the endpoints", "the outline", "the sources") can only be gated on existence, the weakest thing a gate can check. Signs a cut is wrong: you can't say how done it is, the name is generic rather than specific to this work, or it's too large to finish soon.

**Ordering Deliverables.** Order by uncertainty — the Deliverable whose approach is least proven leads, so an unworkable direction surfaces while there is still room to change course; record why in the Order rationale line. Real dependencies still bind; uncertainty orders what they leave free. An amendment places a new Deliverable where uncertainty puts it rather than at the end by default.

**Safety-critical candidates.** Any candidate whose violation would be unsafe or irreversible — secrets and credentials, untrusted input, destructive or irreversible actions on shared state, such as merging, publishing, or overwriting a branch others build on — becomes a Global Invariant, holding across every Deliverable rather than only the one that happens to touch it, whatever its origin: a task-file Default, the interview, or a steering amendment. A gate is judged on its own text alone — an evaluator reads it from the Manifest but treats nothing else there as binding on its verdict — so sharpen the invariant until it can be judged from what the work leaves behind — the artifacts produced and the project state around them; for code, the diff, the repository, and the pull request with its comments. Never drop it for resisting verification: dropping is the outcome this routing exists to prevent. Where only part of it is reachable — a clause about what the run *did*, leaving no artifact — gate the reachable part and record the rest as an `ASM-*` entry naming what is not gated and what enforces it instead, so the unreachable half is visible rather than quietly narrowed away.

**Known Assumptions.** Consume `Known Assumption candidate` items from the latest figure-out Read: encode each still-unresolved candidate that survives the triage below as an `ASM-*` entry with its default and impact if wrong; omit candidates that later evidence or the user resolved. Do not copy the full Evidence Ledger into the Manifest. A risk worth acting on is not an assumption by default: route it to the gate that would catch it, to the Deliverable order that surfaces it early, or to an `ASM-*` when its cost is work redone — the Manifest has no field for risks nothing acts on.

Triage by what being wrong would cost. Work redone is an assumption and belongs here; an approach invalidated is not — settle that gap before the manifest ships, either by invoking `manifest-dev:figure-out` to resolve it or by choosing a good-enough answer outright and recording it where it will hold — as a gate when the choice must not be departed from, as Initial Approach direction when it is guidance rather than obligation — naming what it trades away either way. The Initial Approach is departable by design, so a choice parked there is one /do may weigh; that is the whole test for which of the two it is. Left as an assumption instead, it surfaces mid-run, where a stalled unattended execution costs far more than settling it here would have. With no user to settle it — an autonomous run or a mid-/do amendment — invoke `manifest-dev:figure-out --autonomous` and record what it settles as that decided element, marking that decision `(auto)` with a matching ASM pointing at it rather than standing in for it.

**Criteria pinned by reaction.** Criteria the user pinned by *reacting* to something concrete during figure-out — a mock, a reference, a chosen direction — are success criteria, not flavor: encode them as an Acceptance Criterion or Global Invariant, judged against the criterion the reaction named rather than the artifact that provoked it. Never route one to Process Guidance or the Initial Approach, where /do may weigh it away. This routes onto existing structure; it adds no new manifest section.

## Task files

Identify task type and load the matching file(s) from `tasks/` — their Quality Gates and Defaults auto-encode before the interview, per *Content types* below (surface each as it lands so the dialogue carries the encoding forward). These define task files carry **encoder data only**; probing fuel lives in figure-out's own parallel probe files (`skills/figure-out/tasks/`) — the two sets are decoupled. Per-repo for multi-repo manifests.

| Domain | Indicators | File |
|--------|------------|------|
| Coding | Any code change; base review-code dimension gates for intent, bugs, operational readiness, design, tests, docs, context adherence | `CODING.md` |
| Feature | New functionality, APIs, enhancements | `FEATURE.md` |
| Bug | Defects, errors, regressions, "not working", "broken" | `BUG.md` |
| Refactor | Restructuring, "clean up", pattern changes | `REFACTOR.md` |
| PR lifecycle | Shipping a change through CI, review, approvals | `PR_LIFECYCLE.md` |
| Prompting | LLM prompts, skills, agents, system instructions | `PROMPTING.md` |
| Writing | Prose, articles, copy, social, creative (base) | `WRITING.md` |
| Document | Specs, proposals, reports, formal docs (base: Writing) | `DOCUMENT.md` |
| Tech design | Design docs consolidating finished understanding into audience-fit standalone technical documentation (base: Document) | `TECH_DESIGN.md` |
| Research | Investigations, analyses, comparisons | `research/RESEARCH.md` |
| Blog | Blog posts, articles, tutorials (base: Writing) | `BLOG.md` |

*Composition:* code-change tasks combine `CODING.md` (base gates) with the specific FEATURE/BUG/REFACTOR; text-authoring combines `WRITING.md` with BLOG/DOCUMENT, and TECH_DESIGN composes onto DOCUMENT/WRITING; Research composes `research/RESEARCH.md` with `research/sources/`. Domains aren't mutually exclusive (a bug fix that refactors uses both). `PR_LIFECYCLE.md` composes when the output ships through a GitHub PR (auto-detected from a github.com `origin`; probe if origin is missing or a github-enterprise host), including tech-design docs shipped as PRs — it templates one AC per repo whose body activates the `check-pr` skill under whichever `/do` verification mode is selected. That body is the steering surface for per-PR nuances (labels, approvers, flaky-CI/retrigger overrides). **Exception:** PROMPTING does not compose with CODING unless the task also changes executable code.

*Content types:* **Quality Gates** (`## Quality Gates`) → INV-G*/AC-* (omit only per *The omission valve* below); **Defaults** (`## Defaults`) → PG-* pre-interview, user reviews and removes if N/A — a safety-critical Default routes to a Global Invariant instead, per **Safety-critical candidates** above, judged by consequence rather than wording; **Reference files** (`tasks/**/references/*.md`) → gate-evaluation lookup data, not loaded during /define.

**The omission valve.** A task-file Quality Gate is omitted only with stated reasoning, on either of two grounds: it is clearly inapplicable, or — advisory-tier gates only — it fails the bearer test. Each advisory dimension protects a specific future activity: maintainability, simplicity, and design fitness protect future modification; testability and test quality protect future regression-catching; docs and prose value protect future readers; operational readiness protects production operation; context-file adherence protects the next contributor meeting consistent code. Omit the gate when that activity will not occur on this manifest's surface within the artifact's life — the costs its findings would name have no bearer, or only trivial exposure. The full set is the default and doubt includes. The logged reasoning names the missing bearer as a fact — "no future reader exists", "scheduled for deletion" — never a probability; "unlikely to find much" omits nothing. Weigh surface and stakes together, never size alone: a one-line change on a payment path keeps the full sweep, because bearers are everywhere on it. The valve operates identically on autonomous runs, where the logged reasoning is the audit. Never eligible: defect-finding dimensions, deterministic project gates, safety-critical Global Invariants, and the ceiling.

## Writing the gates

**One gate, one text.** A gate is a **title**, a **body**, and — where it earns its place — a **why**. There is no second, evaluator-facing copy: the text a reviewer reads is the text that binds. The title summarizes the body's headline requirement and never adds to it — a requirement existing only in the title is a defect, not a shorthand. The body states what done means. The why is optional and binds nothing, under that same non-additive rule: write it where the body's purpose would not be obvious to someone meeting this gate cold, and omit it where the body already says why it matters. `kind` is the only structured metadata a gate carries.

Write the body so the check follows from the definition rather than sitting beside it. Where the procedure that settles a criterion *is* what done means — "done when a request to /health returns 200" — that procedure belongs in the body; where a skill is the definition of done, the body names that skill and its dimension. What does not belong is anything true of every gate in the run: `/do` supplies the comparison evidence is read against and the PASS/FAIL/BLOCKED contract every evaluation returns, so a gate restating either is writing another copy of a rule that already has one home.

**Gate text discipline.** A gate's body is a prompt the moment an evaluator follows it, and it is also the line a reviewer reads — so write it to the evaluator's precision, not to the comfort of prose. That is the failure this single-text shape is most exposed to: a body drifting into readable-but-vague description states an aspiration where the old evaluator-facing copy stated a check, and gates come out worse than they were. Before writing gate bodies, invoke the prompt-engineering skill if it is available; if not, apply its core discipline inline. State the goal, the evidence to inspect, the threshold that separates PASS from FAIL, and any non-obvious context the evaluator needs to judge correctly — a known false-positive shape, a distinction two readings would blur, the one place a defect of this kind actually hides. That context belongs in the **body**, not the why: it tells the evaluator what to inspect, which is part of what done means, where the why only explains why the criterion is worth having. An evaluator that has to infer it will infer it differently each time. /define owns the manifest interview — invoke prompt-engineering for its calibration and come back here.

Name the evidence precisely enough that two evaluations read the same thing. `/do` supplies the run-wide comparison, so a gate names its evidence in the terms that gate needs — which artifact, which surface, which commits — and only states a comparison of its own where it genuinely needs a different subject than the run-wide default, such as reading every commit on the branch rather than the net diff, because a gate reading only the net diff cannot see what appeared and was removed inside the branch.

**Gate extension.** Altitude asks what kind of thing a gate binds; extension asks how many things it ranges over. The two are independent, and only the first has a rule — so a gate can state an outcome, name its evidence precisely, be correctly typed, and still range over only the instances that existed the day it was written. It then goes green while the next instance ships, and the run learns about that one when a person trips over it, which is the most expensive way to find anything. Where a criterion is *no X anywhere in region R*, write the body so the evaluator enumerates R and derives the instances rather than checking an inventory the author wrote down. The authoring test: if someone adds a new instance of this defect class tomorrow, does the gate catch it, or only the ones listed today?

*Gate text discipline* pulls the other way, and the tension is worth naming because it is what produces closed gates: precision is cheapest to reach by naming specific things, so the harder an author tries to be exact, the more likely the body enumerates instances. Resolve it by making the **procedure** exact rather than the inventory — *"read every element rendered between the page header and the primary surface, and for each determine what makes it mount, unmount, or change height"* is exact enough that two evaluators do the same thing and open enough to reach next month's element. Where the enumeration can be executed rather than judged, prefer that: an open gate that runs as a command is cheap enough to hold every round.

The region is not the author's to draw freely. An Acceptance Criterion's region is the surface of the Deliverable it hangs under; a Global Invariant, having no owning Deliverable, takes the Manifest's surface bounded by Appetite. That anchoring is what keeps an open gate clear of the ceiling — work inside the owning Deliverable's surface is work that Deliverable required, which the ceiling already exempts — and it is what makes a narrow Deliverable yield a narrow region with no separate clause: a Deliverable named for one added component ranges over that component, while one named for a whole surface ranges over everything on it, from the same rule.

**Gate altitude.** A gate binds the outcome the user cares about, at the altitude of the Problem and Appetite; a mechanism chosen merely as the means to that outcome belongs in the advisory layer, where /do may depart and name the departure — the Initial Approach or Process Guidance, on the usual split between direction and how-to-work. Test each candidate: if /do satisfied the intent a better way, would this gate go false anyway? Then it is pinning a means — raise it until it isn't. Judgability is the floor: never raise past what the work leaves behind can settle, and where the two meet, keep the highest altitude that stays judgable and record the part of the outcome no artifact reaches as an `ASM-*`, the same way a partially reachable safety invariant is handled. The asymmetry is what makes this worth the care: even where /do's advance delegation reaches, an over-concrete gate costs an amendment-and-re-verification cycle the moment a legitimate pivot happens — and wherever the manifest reads its mechanism as deliberately chosen or its provenance as unclear, it still becomes an escalation.

The test reaches means, never ends. Where a mechanism was deliberately chosen as the thing that must hold, that mechanism *is* the outcome, and raising it away is the erosion this discipline exists to prevent. Deliberate choosing is the whole test, not membership in a list: it covers a safety-critical invariant, a criterion the user pinned by reacting to something concrete, a bound Out of bounds set, a gap settled during the Known Assumptions triage precisely because it must not be departed from, the claim a task file's Quality Gate pitches — and anything else chosen the same way. Make that choosing legible in the manifest: where nothing else shows it — a criterion pinned by reaction, a triage settlement — say so in the gate's why, because `/do` holds an advance delegation to repair a gate shown to pin an *incidental* mechanism (raising it to the outcome it served, raise-only) and that delegation stops at mechanisms the manifest shows were deliberately chosen, reading unclear provenance as deliberate; safety-critical invariants and bounds routed from Out of bounds are already legible as deliberate from the manifest itself. For a task-file gate that means keeping the altitude the task file pitched, not its literal text: instantiating its template and adding run-specific steering is expected, while the licensed removal stays omission with stated reasoning. Under-specification is guarded from the other side — a Deliverable exercised end-to-end lets its gates judge behavior rather than presence.

**Every manifest carries a ceiling.** The gates above all state a floor — what the work must reach. Emit one Global Invariant stating where it stops, because a contract bounded on one side only gives an executor disposed to thoroughness nothing to read as a limit, and restraint written into the advisory layer is departed from legitimately, since only gates bind. Ship the text below as written: it is the same gate in every manifest, it is the one gate told to read the whole Manifest rather than being judged on its own text alone, and its calibration is what keeps it both legal and affordable — a conformance question and never a necessity one, carve-outs stated as categories rather than as a baseline commit the evaluator diffs against, and a pitch that passes on a well-scoped run. The only thing an amendment adds to it is the inherited-work naming described under *Amendment* below.

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

**Declare every gate's kind.** `kind` is required on every Acceptance Criterion and Global Invariant, the ceiling included, and takes `deterministic` — the verdict comes from a command or check returning the same outcome for the same artifact state — or `judgment`, the verdict being a model's judgment over an open finding space that a fresh evaluation resamples. There is no default and nothing is inferred: a gate without it makes the Manifest invalid, since the declaration is what decides how `/do` re-verifies that gate — a Deterministic Gate in full every time, a Judgment Gate once in full and thereafter over its prior findings' repairs and the delta. **A gate that mixes the two is `judgment`** — a command whose result is one input to a judgment does not make the gate deterministic, and its commands run in full either way. That is the error to watch for: the command is the visible half, so a mixed gate gets labelled `deterministic` and its judgment half then resamples every round, which is the churn the Ratchet exists to remove. Re-sampling is a run-level choice, bought for every gate at once with `/do`'s `--exhaustive-verification`; a gate's own body never asks for it.

**Say what an expensive gate costs to re-run.** Where re-running a criterion costs far more than a round of repairs — a long end-to-end suite, a deploy-dependent check — say so in its body, since nothing else tells `/do` that this evaluation is worth spending on a settled state rather than one a repair is about to move. Where the cost is obvious from what the body already asks for, it needs no note.

**Encoding specialized gates.** When a gate needs specialized behavior, its body tells the selected evaluator to **activate a skill** — there is no field that assigns one. Code-quality gates activate the `review-code` skill with a dimension; other specialized checks activate their own (`check-pr`, `review-prompt`). Pattern:

````markdown
#### AC-1.1 — <title stating the outcome the dimension protects>

Done when the manifest-dev:review-code skill, activated with dimension=<dimension>, reports
nothing at or above that dimension's threshold.

Judgment gate.
````

**Name the dimension; the bar comes with it.** `review-code` defines each dimension's bar in its own table, and a gate carrying a second copy can contradict the skill it activates — a defect-finder gate mistakenly written at MEDIUM silently weakens a bar nobody changed.

The 14 dimensions are change-intent, code-bugs, contracts, type-safety, defect-class (defect-finders); operational-readiness, code-design, code-maintainability, code-simplicity, code-testability, test-quality, docs, prose-value, context-file-adherence (advisory). Those roles orient the author — which gate catches defects and which surfaces taste — while the thresholds themselves stay `review-code`'s. All fourteen are Judgment Gates; the nine advisory ones form the whole-change quality sweep, whose one full look `/do` spends after the defect-finders and the project's mechanical gates are settled, per `tasks/CODING.md`. `defect-class` is the one that applies only where the change fixes a defect, which is why `tasks/BUG.md` encodes it rather than `tasks/CODING.md`. A gate body runs inside `/do`'s selected execution envelope, so it tells that evaluator to **activate** the skill — never to spawn another agent, which would bypass the gate's PASS/FAIL/BLOCKED contract. For a non-review-code specialized check, name its skill the same way, e.g. *"Done when the manifest-dev:check-pr skill reports the pull request ready — PR: …"*.

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
put in front of so its criteria judge whether it works rather than whether it exists]

#### AC-1.1 — [Title]

[Body, on the same terms as a Global Invariant's.]

Why: [optional context, binds nothing — omit where the body already carries it]

[Judgment | Deterministic] gate.
````

`kind` is the only structured metadata, and the closing line carries it: it is required and never inferred. IDs are the heading's own — stable, and independent of position.

**Verdicts.** Gate evaluations return **PASS**, **FAIL**, or **BLOCKED** (waiting on external action); `/do` owns what each verdict routes to. Automate verification. A criterion that resists it becomes a judgment-based gate whose body names the concrete evidence the evaluator checks against — not a Process Guidance entry; if it genuinely cannot be written as a gate, sharpen or drop it — a criterion nothing checks is not a criterion. A drop leaves a trace: record it as an `ASM-*` entry naming what was dropped, why it resisted gating, and the impact if that judgment is wrong, so nothing the user cared about disappears unrecorded. Nothing deliberately chosen as the thing that must hold may be dropped — the same set *Gate altitude* protects from being raised away, on the same reasoning. Those sharpen into a judgment-based gate instead; the drop is for criteria that were never verifiable to begin with. Where only part of such a criterion is reachable, gate the reachable part and record the rest as an `ASM-*`, exactly as under *Safety-critical candidates*. Criteria that wait on human or external action (deploys, approvals, in-flight CI) stay ACs — the evaluator surfaces the wait per its own contract, as BLOCKED or as a FAIL carrying a wait finding, until it clears. Auto-decided items carry `(auto)` after the ID with a matching ASM entry.

## Amendment

A manifest path in `$ARGUMENTS` means amend. Read it fully. Before preserving anything, validate every Acceptance Criterion and Global Invariant against the current schema: a title, a body, an optional why, and a stated kind (`judgment` or `deterministic`). A gate carrying a `verify` block of any shape — `instructions`, `prompt`, `model`, or a description paired with a separate evaluator text — is the superseded schema. So is a gate stating a `phase`, a field this workflow no longer has, and so is a gate with no stated kind or one whose kind is unrecognised. In any of those cases stop and require fresh `/define` regeneration without passing the incompatible Manifest as an amendment input; never amend, translate, or partially preserve an incompatible schema, and offer no migration path. Otherwise apply targeted changes only — preserve unaffected items verbatim. IDs are stable and independent of list position (modify in place; insert or remove without renumbering). No `## Amendments` log — git is history. Autonomous when caller is `/auto` or `/do` — a mid-/do user message is fire-and-forget steering, so don't ask back or wait; interactive otherwise. In autonomous amendment, every judgment call the steering text doesn't settle is auto-decided per the `(auto)`/ASM discipline — the user's audit trail. An amendment arriving as `/do`'s envelope repair — raising a gate shown to pin an incidental mechanism to the outcome it served — is validated against the delegation's bounds before it is applied: the raised gate still catches the outcome the original claimed, and the repair weakens nothing and touches no deliberately chosen mechanism. A repair that fails that validation is not applied in weakened or partial form — it returns to `/do` to escalate.

**Reconcile the frame, not just the leaves.** An amendment that widens scope, or changes a rule the manifest already states, leaves Intent, Architecture, the Order rationale, and any scope-bounding Process Guidance describing the older and smaller task — and those sections read as unaffected precisely because nothing is editing them, so the staleness is invisible rather than merely unaddressed. Re-read them against what the manifest now covers, and re-read the existing gates over the widened area for under-coverage: a criterion written when a rule lived in three places does not reach the fourth.

The ceiling needs no copy-refresh, since it reads the current manifest each time it runs — an amendment that widens the Appetite or redirects the Architecture is visible to it immediately. Two cases still need writing down, because they are information the manifest holds nowhere else, and both are named the same way — in the ceiling's own body, under work inherited rather than added, listing the Deliverables already finished under the criteria in force at the time. One is an amendment that *replaces* a criterion rather than adding one, which must name the work completed under what it superseded. The other is a ceiling *backfilled* onto a manifest already under execution — a `--babysit` synthesis, or a manifest that never carried one — where everything the run has finished predates the gate entirely. Without it the ceiling reads that finished work as excess and fails exactly what the amendment required. Bound the naming to what the criteria then in force required, never to every surface the run has touched — the looser form would let excess already produced be relabelled as inherited and stop being judged at all. Writing it changes the ceiling's text, so that gate returns to the ledger unverified and re-verifies like any other changed gate.

**An instance report names the gate that missed it.** Steering arrives as instances — this moves, that number is duplicated — and the reflex is to add a criterion for the instance. Ask first which gate should already have caught it: where one claims the class the instance belongs to and missed it, its region was drawn narrower than the class, so widen that gate rather than adding a sibling beside it. A sibling leaves the hole open and grows the manifest by one gate per instance, and several Deliverables accumulating against the same surface is the visible symptom. This is *Gate extension* applied at amendment time, and it runs ahead of *reconcile the frame* rather than beside it: that direction looks for under-coverage after scope widens, where this looks for the gate that already failed before it does.

**An amendment that changes a decision produces a gate.** Adding work and reversing a rule the system already states are different amendments; the second needs its own Acceptance Criterion. Edited prose and a decision record note the decision but check nothing, so the change ends up verified only by whatever broad gate happens to overlap the same files — and "does the diff match its stated intent" goes green over a redesign without ever asking whether the new design holds.

## Flags

`--babysit <pr-url>` — load `references/BABYSIT_MODE.md`; synthesizes a lifecycle-only manifest from a PR. `--autonomous` skips summary approval and lets figure-out self-answer. When the task spans multiple repos (manifest declares `Repos:` in Intent), load `references/MULTI_REPO.md`.

## Summary for Approval

Before Complete, write a plain-language digest — the pain and how big a change it is worth, the plan, what gets built, the guardrails, how it is verified — no codes, no YAML, no schema vocab. The pain matters most here: it is the one thing only the user can confirm, and this is the surface where an invented or wrong Problem gets caught. **Test:** reads like talking to a colleague, not a compressed manifest. Approval → Complete; feedback → revise; `/do` → handoff; decline → exit silently. Skip the wait when caller is `/auto` or `/do` amendment, or the user signals "enough".

## Complete

Emit the load-bearing handoff (`<manifest-path>` is the absolute path you wrote):

```text
Manifest complete: <manifest-path>

To execute: /do <manifest-path>
For unattended execution, invoke /do <manifest-path> as the execution entrypoint. /do reads the manifest and owns the manifest-completion contract: it sets that completion contract when the active harness exposes a goal-setting or continuation capability, or prints the manual copy-paste contract when not. /define does not set a separate /do goal.
```
