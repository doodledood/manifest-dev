---
name: define
description: 'Manifest builder. Turns shared understanding into a verifiable Manifest with Deliverables, Acceptance Criteria, Global Invariants, and an Initial Approach. Use when planning features, scoping refactors, debugging complex issues, or when the user asks to define, scope, plan, spec out, make a manifest, or break down a task.'
argument-hint: '[task] [<manifest-path> to amend] [--babysit <pr-url>]'
user-invocable: true
---

## Where the manifest goes, and what runs first

Encode the conversation's shared understanding as a Manifest at `~/.manifest-dev/manifests/manifest-{ts}.md` (create the dir; `~` = `$HOME` / `%USERPROFILE%`) — a durable home so manifests survive OS temp cleanup across multi-day work. Fall back to a writable temp path (`/tmp/`, else `$TMPDIR` / `%TEMP%`) only when the home directory isn't writable. If the transcript lacks shared understanding, invoke `manifest-dev:figure-out` first; propagate `--autonomous` when invoked from `/auto` or `/do`'s amendment path. **Pre-flight:** if `--babysit <pr-url>`, load `references/BABYSIT_MODE.md` and follow its synthesis flow; if `$ARGUMENTS` contains a manifest file path, amend (see below); else fresh.

## Encoding discipline

figure-out reaches shared understanding of the *problem*; /define handles manifest-specific *encoding* judgment calls — invariant vs process guidance, AC scope and pass threshold, phase ordering (fast vs slow), trade-offs to record as `[T-N]`. Surface the load-bearing encoding decisions briefly with a recommended answer before encoding; auto-decide the rest and mark `(auto)` + matching ASM. The manifest is the acceptance contract — what the user accepts as *"I'd ship the outcome of executing this."*

**Problem first.** Intent opens with the Problem — one specific story of what breaks or grates today, not an abstract need — because it is the baseline the rest of the manifest is written against: gates are pitched at what would actually relieve it, and whoever judges the result later weighs the work against that baseline rather than against an ideal. Appetite follows: the size of change the problem is worth, bounding complexity and surface rather than time or tokens, and the criterion for how many Deliverables to cut and how much to gate beyond what task files supply. Out of bounds records what the work deliberately leaves alone; an entry that must hold stays listed as the scope statement and gains the Global Invariant that binds it. Elicit whatever the conversation left unset — these are encoding decisions, not re-investigation. A session that cannot name a pain has found a stop signal rather than an empty field: return to `manifest-dev:figure-out`, or conclude there is nothing worth building. With no user to ask, invoke `manifest-dev:figure-out --autonomous` to find the pain; only when that comes back empty, carry the thinnest Problem the evidence honestly supports with an `ASM-*` recording its thinness — and prefer returning no manifest to inventing one. All of that governs a fresh session. An amendment derives the fields from the manifest's own content plus the amendment's context and records a thin result as an `ASM-*`; it never halts, since a run may already be in flight and the manifest already exists.

**Cutting Deliverables.** A Deliverable is a slice that can be finished on its own and exercised end-to-end — put in front of its real use: run, read, or otherwise judged in the situation it is for, not merely inspected as present. That is what lets its Acceptance Criteria judge whether it works rather than whether it exists; a Deliverable cut along a layer ("the data model", "the endpoints", "the outline", "the sources") can only be gated on existence, the weakest thing a gate can check. Signs a cut is wrong: you can't say how done it is, the name is generic rather than specific to this work, or it's too large to finish soon.

**Ordering Deliverables.** Order by uncertainty — the Deliverable whose approach is least proven leads, so an unworkable direction surfaces while there is still room to change course; record why in the Order rationale line. Real dependencies still bind; uncertainty orders what they leave free. An amendment places a new Deliverable where uncertainty puts it rather than at the end by default.

**Safety-critical candidates.** Any candidate whose violation would be unsafe or irreversible — secrets and credentials, untrusted input, destructive or irreversible actions on shared state, such as merging, publishing, or overwriting a branch others build on — becomes a Global Invariant, holding across every Deliverable rather than only the one that happens to touch it, whatever its origin: a task-file Default, the interview, or a steering amendment. A gate may be evaluated with no context beyond its own instructions, so sharpen the invariant until it can be judged from what the work leaves behind — the artifacts produced and the project state around them; for code, the diff, the repository, and the pull request with its comments. Never drop it for resisting verification: dropping is the outcome this routing exists to prevent. Where only part of it is reachable — a clause about what the run *did*, leaving no artifact — gate the reachable part and record the rest as an `ASM-*` entry naming what is not gated and what enforces it instead, so the unreachable half is visible rather than quietly narrowed away.

**Known Assumptions.** Consume `Known Assumption candidate` items from the latest figure-out Read: encode each still-unresolved candidate that survives the triage below as an `ASM-*` entry with its default and impact if wrong; omit candidates that later evidence or the user resolved. Do not copy the full Evidence Ledger into the Manifest.

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

*Composition:* code-change tasks combine `CODING.md` (base gates) with the specific FEATURE/BUG/REFACTOR; text-authoring combines `WRITING.md` with BLOG/DOCUMENT, and TECH_DESIGN composes onto DOCUMENT/WRITING; Research composes `research/RESEARCH.md` with `research/sources/`. Domains aren't mutually exclusive (a bug fix that refactors uses both). `PR_LIFECYCLE.md` composes when the output ships through a GitHub PR (auto-detected from a github.com `origin`; probe if origin is missing or a github-enterprise host), including tech-design docs shipped as PRs — it templates one AC per repo whose `verify.instructions:` activates the `check-pr` skill under whichever `/do` verification mode is selected. The instructions are the steering surface for per-PR nuances (labels, approvers, flaky-CI/retrigger overrides). **Exception:** PROMPTING does not compose with CODING unless the task also changes executable code.

*Content types:* **Quality Gates** (`## Quality Gates`) → INV-G*/AC-* (omit clearly inapplicable with stated reasoning); **Defaults** (`## Defaults`) → PG-* pre-interview, user reviews and removes if N/A — a safety-critical Default routes to a Global Invariant instead, per **Safety-critical candidates** above, judged by consequence rather than wording; **Reference files** (`tasks/**/references/*.md`) → gate-evaluation lookup data, not loaded during /define.

## Writing the gates

**Gate altitude.** A gate binds the outcome the user cares about, at the altitude of the Problem and Appetite; a mechanism chosen merely as the means to that outcome belongs in the advisory layer, where /do may depart and name the departure — the Initial Approach or Process Guidance, on the usual split between direction and how-to-work. Test each candidate: if /do satisfied the intent a better way, would this gate go false anyway? Then it is pinning a means — raise it until it isn't. Judgability is the floor: never raise past what the work leaves behind can settle, and where the two meet, keep the highest altitude that stays judgable and record the part of the outcome no artifact reaches as an `ASM-*`, the same way a partially reachable safety invariant is handled. The asymmetry is what makes this worth the care: /do cannot amend gate text on its own reading, so an over-concrete gate becomes an escalation the moment a legitimate pivot happens.

The test reaches means, never ends. Where a mechanism was deliberately chosen as the thing that must hold, that mechanism *is* the outcome, and raising it away is the erosion this discipline exists to prevent. Deliberate choosing is the whole test, not membership in a list: it covers a safety-critical invariant, a criterion the user pinned by reacting to something concrete, a bound Out of bounds set, a gap settled during the Known Assumptions triage precisely because it must not be departed from, the claim a task file's Quality Gate pitches — and anything else chosen the same way. For a task-file gate that means keeping the altitude the task file pitched, not its literal text: instantiating its template and adding run-specific steering is expected, while the licensed removal stays omission with stated reasoning. Under-specification is guarded from the other side — a Deliverable exercised end-to-end lets its gates judge behavior rather than presence.

**Every manifest carries a ceiling.** The gates above all state a floor — what the work must reach. Emit one Global Invariant stating where it stops: what *this run* adds carries nothing that no Acceptance Criterion, Global Invariant, or Deliverable required — for code, the diff the run produces, read against the repository around it — and nothing that nominally serves one of those while far exceeding the surface the Appetite allows. The subject is what the run adds, never the artifact it started from: a manifest synthesized over existing work, as `--babysit` does from a pull request, takes that work as given and ranges only over what the run does next. Bounded on one side only, the contract gives an executor disposed to thoroughness nothing to read as a limit, and restraint written into the advisory layer is departed from legitimately, since only gates bind.

Keep it a conformance question, never a necessity one. It asks whether the change exceeded what was agreed, taking the manifest's premise as given exactly as every other gate does — it never asks whether the work was worth doing. That second question is premise-questioning: circular for a gate to ask, human-answerable rather than artifact-answerable, and owned by review rather than by the manifest. The distinction is what keeps this gate legal, so hold it in the wording: the other criteria ask whether the change *reaches* what was agreed, and this one asks whether it *stops there*. Nothing in its instructions may license the evaluator to judge whether the work was necessary, motivated, or worthwhile.

Set `phase: 1`, so it runs every repair round beside the other gates. Within a round the gates re-verify anyway, so excess caught there is removed alongside that round's other fixes; excess caught once everything is green forces a fresh round against a diff where the extra work has entangled with passing gates. Running every round is also what makes the limit legible to the next round rather than to the last one.

Carry the manifest's Problem, Appetite, and Out of bounds inline in its `verify.instructions`, along with what the work owes — the Deliverables and the other gates, the ceiling excluding itself — and, listed separately as authorized rather than owed, whatever the Initial Approach and Process Guidance directed. *Gate altitude* deliberately keeps chosen mechanisms out of gates, so the work will show mechanisms the manifest called for and no criterion names — a flag, a rollback path, a module layout — and a ceiling reading only the gates fails them. Keep the two lists apart: Process Guidance is departable, and filing it under what the work owes hands the evaluator binding vocabulary for the advisory layer. The authorized list names the mechanisms the manifest expected, never the only ones permitted — `/do` may pivot the Initial Approach by naming the deviation rather than amending, so work reaching a listed Deliverable by a route the list does not name is required by that Deliverable, not excess. Say so in the instructions; a ceiling that reads the list as exhaustive escalates on the first legitimate pivot. Inline rather than by reference: reopening the manifest for semantic context would expose Process Guidance as though it bound and make modes judge different contracts. Write the enumeration of what the work owes last, once the Deliverables and their criteria exist: filled in schema order it lists a set the manifest has not finished stating, and the gate then reads everything written after it as excess.

Carry two carve-outs with it, since each names work that is required while no criterion names it. **Inherited rather than added** — the artifact a manifest was synthesized over, as `--babysit` does with a pull request's existing diff, and anything arriving from outside the run, such as a base branch merged into the head. Wherever a ceiling's enumeration stops covering work the run already completed — one added to a manifest already under execution, or one whose criteria an amendment has since replaced — that work is inherited too, and it is the one inherited category leaving no signal of its own: name it outright, listing the Deliverables it finished under the criteria in force at the time, since the verifier reading one undifferentiated diff cannot otherwise tell it from what comes next. List what those criteria required, never every surface the run has touched — the looser form would let excess already produced be relabelled inherited and stop being judged at all. **Discharging what a criterion required** — including sweeping a changed rule into every copy and surface that holds it: other files stating it, distributed or generated copies, callers, and the READMEs that describe it. That work lands in files no criterion named, and a ceiling blind to it fails the sweep `/do` is separately obliged to perform.

State the carve-outs as categories, not as a baseline commit the evaluator compares against — this scopes how the carve-outs are expressed, and leaves the Evidence line to name what the run produced as precisely as *Gate evaluation instruction discipline* requires of any gate — for code in a repository, that is the diff range. A pinned ref fixes at authoring time a boundary that keeps moving — the run resumes, someone pushes, the base gets merged in — and it means nothing for a manifest whose deliverable is prose or one spanning several repositories. The categories hold in all of those, and where a case is genuinely ambiguous the calibration below already resolves it toward required work.

Pitch it to pass on a well-scoped run. Read as "minimal diff" it fails work a Deliverable plainly required, and each failure re-stales every gate whose subject moved — costing more than the excess it exists to catch. Tell the verifier to treat an unclear case as required work, and to leave small, incidental, or imperfect changes inside an artifact already in scope alone: this gate catches work nobody asked for, not work done imperfectly.

A skeleton, since this prompt carries more than any other gate's and the guard has to reach the verifier rather than only the author:

```yaml
verify:
  instructions: |
    Check this change against the scope it was authorized to have. This is a conformance
    check: take the intent below as given, and do not judge whether the work was necessary,
    motivated, or worthwhile.
    Problem: ...
    Appetite: ...
    Out of bounds: ...
    Required: <the Deliverables, and the other Acceptance Criteria and Global Invariants — not this one>
    Also authorized: <whatever the Initial Approach and Process Guidance directed — the
    mechanisms expected, not the only ones permitted; work reaching a Required item by
    another route is required by that item>
    Required although no criterion names it: <work inherited rather than added>, and work
    discharging what a criterion required, including sweeping a changed rule into every copy
    and surface that holds it.
    Evidence: <what this run produced — for code in a repository, the diff range named per
    Gate evaluation instruction discipline, e.g. origin/main...HEAD>
    FAIL only on work none of the above accounts for, or work nominally serving one of them that
    far exceeds the Appetite's surface. Treat an unclear case as required work, and leave
    small, incidental, or imperfect changes inside an artifact already in scope alone.
    Return PASS, FAIL, or BLOCKED.
  kind: judgment
  phase: 1
```

**Gate evaluation instruction discipline.** Before writing `verify.instructions` fields, invoke the prompt-engineering skill if it is available; if not, apply its core discipline inline. These instructions are prompts when an evaluator follows them: state the goal, evidence to inspect, PASS/FAIL/BLOCKED contract, and non-obvious context. Do not run a separate prompt-engineering interview — /define owns the manifest interview. Name the evidence precisely enough that two evaluations read the same thing: which ref a comparison uses — `origin/main` rather than `main`, since a local ref can sit stale in a fresh or shallow clone and fail the gate on the wrong evidence — and whether the subject is the branch tip or every commit on it, because a gate reading only the net diff cannot see what appeared and was removed inside the branch.

**Declare every gate's kind.** `verify.kind` is required on every Acceptance Criterion and Global Invariant, the ceiling included, and takes `deterministic` — the verdict comes from a command or check returning the same outcome for the same artifact state — or `judgment`, the verdict being a model's judgment over an open finding space that a fresh evaluation resamples. There is no default and nothing is inferred: a gate without it makes the Manifest invalid, since the declaration is what decides how `/do` re-verifies that gate — a Deterministic Gate in full every time, a Judgment Gate once in full and thereafter over its prior findings' repairs and the delta. **A gate that mixes the two is `judgment`** — a command whose result is one input to a judgment does not make the gate deterministic, and its commands run in full either way. That is the error to watch for: the command is the visible half, so a mixed gate gets labelled `deterministic` and its judgment half then resamples every round, which is the churn the Ratchet exists to remove. A user who wants one criterion re-sampled in full every round, at that cost, says so in that criterion's own instructions; the run-level `--exhaustive-verification` flag is the other way to buy the same thing for every gate at once.

**Encoding specialized gates.** There is no `verify.agent` field. When a gate needs specialized behavior, its instructions tell the selected evaluator to **activate a skill**. Code-quality gates activate the `review-code` skill with a dimension; other specialized checks activate their skill (`check-pr`, `review-prompt`). Pattern:

```yaml
verify:
  instructions: |
    Activate the manifest-dev:review-code skill with dimension=<dimension> and review the change.
    PASS only if no <LOW|MEDIUM>-or-higher findings. Report findings with severity.
  kind: judgment
```

The 13 review-code dimensions are: change-intent, code-bugs, contracts, type-safety (defect-finders, no LOW+); operational-readiness, code-design, code-maintainability, code-simplicity, code-testability, test-quality, docs, prose-value, context-file-adherence (advisory, no MEDIUM+). All thirteen are Judgment Gates; the nine advisory ones form the whole-change quality sweep and take a phase after the defect-finders and the project's mechanical gates, per `tasks/CODING.md`. The instructions already run inside `/do`'s selected execution envelope, so they tell that evaluator to **activate** the skill — never to spawn another agent, which would bypass the gate's PASS/FAIL/BLOCKED contract. For a non-review-code specialized check, name its skill the same way, e.g. *"Activate the manifest-dev:check-pr skill. PR: …"*.

## Manifest Schema

````markdown
# Definition: [Title]

## 1. Intent & Context
- **Problem:** [The specific story of what breaks or grates today — the baseline this work improves on]
- **Appetite:** [The size of change this problem is worth — a bound on complexity and surface]
- **Goal:** [What this work achieves, in service of the Problem]
- **Out of bounds:** [What this deliberately does not do]
- **Mental Model:** [Key concepts to understand]

## 2. Initial Approach (Complex Tasks Only)
*Initial direction, not rigid plan. Expect adjustment when reality diverges.*

- **Architecture:** [High-level HOW — starting direction]
- **Risk Areas:**
  - [R-1] [What could go wrong] | Detect: [how you'd know]
- **Trade-offs:**
  - [T-1] [Priority A] vs [Priority B] → Prefer [A] because [reason]

## 3. Global Invariants
*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

- [INV-G1] Description: ...
  ```yaml
  verify:
    instructions: "..."       # required, topology-neutral gate evaluation procedure
    kind: judgment            # required: judgment | deterministic — no default, never inferred
    phase: 1                  # optional integer, default 1; higher phases run after lower pass
  ```

## 4. Process Guidance
*Advisory recommendations on HOW to work — /do weighs them and may depart, naming the departure on whichever terminal path the run reaches (and in the execution log when one is kept). Only Acceptance Criteria and Global Invariants bind; anything that must hold belongs in a gate.*

- [PG-1] Description: ...

## 5. Known Assumptions
- [ASM-1] [What was assumed] | Default: [chosen value] | Impact if wrong: [consequence]

## 6. Deliverables
*Ordered least-proven-first within dependency constraints; list order is the execution order, and Deliverable numbers are stable IDs rather than positions. Plan, not contract — /do may resequence when execution changes what the order was built on, recording the deviation.*

- **Order rationale:** [why this order; omit when there is only one Deliverable]

### Deliverable 1: [Name]

**Acceptance Criteria:**
- [AC-1.1] Description: ...
  ```yaml
  verify:
    instructions: "..."       # required, topology-neutral gate evaluation procedure
    kind: judgment            # required: judgment | deterministic — no default, never inferred
    phase: 1                  # optional integer, default 1; higher phases run after lower pass
  ```
````

**Verdicts.** Gate evaluations return **PASS**, **FAIL**, or **BLOCKED** (waiting on external action); `/do` owns what each verdict routes to. Automate verification. A criterion that resists it becomes a judgment-based gate whose instructions name the concrete evidence the evaluator checks against — not a Process Guidance entry; if it genuinely cannot be written as a gate, sharpen or drop it — a criterion nothing checks is not a criterion. A drop leaves a trace: record it as an `ASM-*` entry naming what was dropped, why it resisted gating, and the impact if that judgment is wrong, so nothing the user cared about disappears unrecorded. Nothing deliberately chosen as the thing that must hold may be dropped — the same set *Gate altitude* protects from being raised away, on the same reasoning. Those sharpen into a judgment-based gate instead; the drop is for criteria that were never verifiable to begin with. Where only part of such a criterion is reachable, gate the reachable part and record the rest as an `ASM-*`, exactly as under *Safety-critical candidates*. Criteria that wait on human or external action (deploys, approvals, in-flight CI) stay ACs — the evaluator surfaces the wait per its own contract, as BLOCKED or as a FAIL carrying a wait finding, until it clears. Auto-decided items carry `(auto)` after the ID with a matching ASM entry.

## Amendment

A manifest path in `$ARGUMENTS` means amend. Read it fully. Before preserving anything, validate every Acceptance Criterion and Global Invariant verify block against the current schema: required `instructions`, required `kind` (`judgment` or `deterministic`), optional integer `phase`, and no other fields. If any block contains `prompt`, `model`, lacks `instructions`, lacks `kind` or gives it an unrecognised value, or has another field, stop and require fresh `/define` regeneration without passing the incompatible Manifest as an amendment input; never amend, translate, or preserve an incompatible schema. Otherwise apply targeted changes only — preserve unaffected items verbatim. IDs are stable and independent of list position (modify in place; insert or remove without renumbering). No `## Amendments` log — git is history. Autonomous when caller is `/auto` or `/do` — a mid-/do user message is fire-and-forget steering, so don't ask back or wait; interactive otherwise. In autonomous amendment, every judgment call the steering text doesn't settle is auto-decided per the `(auto)`/ASM discipline — the user's audit trail.

**Reconcile the frame, not just the leaves.** An amendment that widens scope, or changes a rule the manifest already states, leaves Intent, Architecture, the Order rationale, and any scope-bounding Process Guidance describing the older and smaller task — and those sections read as unaffected precisely because nothing is editing them, so the staleness is invisible rather than merely unaddressed. Re-read them against what the manifest now covers, and re-read the existing gates over the widened area for under-coverage: a criterion written when a rule lived in three places does not reach the fourth. A gate whose `verify.instructions` carries an inline copy of anything the manifest states is frame content too, not an unaffected leaf — the ceiling invariant is one by construction, holding the Intent fields, the enumeration of what the work owes, and the separately listed set the Initial Approach and Process Guidance authorized. Refresh every copy it carries: against the amended Problem, Appetite, and Out of bounds, against the current Acceptance Criteria, Global Invariants, and Deliverables, and against the current Initial Approach and Process Guidance — as it directs work still *ahead*, since a refresh that would newly authorize work the run already completed is the laundering route `/do` forbids, and escalates rather than being written. An amendment that adds work inside the existing Appetite moves the second list while leaving the first untouched, and one that redirects the Architecture moves the third — a ceiling still carrying any superseded list reads the newly directed work as excess. An amendment that *replaces* a criterion rather than adding one needs the other half of that: name the work already completed under what it superseded, so the refreshed ceiling inherits it instead of reading it as excess. That changes the gate's verification identity, so it returns to the ledger unverified and re-verifies like any other changed gate. Left stale it judges the work against the scope the amendment replaced, and fails precisely what the amendment required. Separately, and on any amendment rather than only a widening one: a manifest written before Intent carried Problem, Appetite, and Out of bounds gets them backfilled per *Problem first*'s amendment branch, since the altitude and Deliverable-cutting rules read from them, and one written without a ceiling invariant gains one on the same pass, naming the work already completed per the inherited-work carve-out above — what the criteria in force at the time required, never every surface the run has touched.

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
