# AGENTS.md — manifest-dev Workflow Context

## Overview

manifest-dev provides manifest-driven workflows for AI coding agents. The core flow is:

```
/define → manifest → /do (executes + verifies inline) → /done
```

- **/define** — Interactive manifest builder. Probes for requirements, quality gates, edge cases. Outputs a manifest with deliverables, acceptance criteria, and global invariants.
- **/do** — Manifest executor. Reads the Manifest in full, then pursues a state where every Acceptance Criterion and Global Invariant holds as written, deciding order, method and amount of checking for itself. Every gate declares its kind: a deterministic gate re-runs in full, a judgment gate reads the full change once and then judges only prior findings' repairs and the delta. It fixes failures, amends through /define rather than editing the Manifest, keeps a default-on execution log keyed to the Manifest, and stops via /done, /escalate, or a pending summary. Caller overlays can narrow retry cadence, e.g. CI one-shot runs report wait-only states instead of sleeping.
- **/done** — Plain-prose completion summary called by /do once every criterion holds on fresh evidence.
- **/escalate** — Structured blocker handoff for unrecoverable failures or pending external action.

Supporting workflows:
- **/auto** — End-to-end autonomous: /figure-out → /define → /do in one command. It stays goal-free through understanding and definition; /do owns the completion backstop from execution onward. An interrupted earlier phase is restarted by the caller.
- **/figure-out** — Truth-convergent thinking partner. /define auto-invokes it when the problem space is foggy.
- **/figure-out-team** — /figure-out's discipline applied to a multi-party async Slack conversation.
- **/ticket-up** — Authors convention-compliant Tickets from a Manifest, direct work, independently managed questions, or source-linked follow-ups. A Manifest stays one coherent Ticket by default; explicit delegation can split it on Deliverable boundaries.
- **/next-ticket** — Reads the Ticket store, claims the single best ready Ticket, and presents it without starting execution.
- **/run-ticket** — Claims or recovers one exact Ticket, runs /auto, completes required protected landing, then records DONE or ESCALATED evidence on that same Ticket. Backlog selection stays outside it.
- **/sweep-tickets** — Scheduled one-Ticket correctness path: resumes one interrupted automation-owned Auto Ticket, otherwise selects one ready Auto Ticket, invokes /run-ticket, and stops.
- **/init-context** — Sets a repository up with project-owned ADR conventions, a glossary, and the context-file wiring that keeps sessions using them, seeding them from the project's own history where there is any.
- **/review-writing** — Reviews prose against the project's writing standards in its own register: documentation or human-voiced writing. Detects the register, applies it plus the shared floor, and reports graded findings. Distinct from review-code's prose-value dimension, which asks whether prose in a diff earns its place.
- **/design** — Builds or restyles a user-visible artifact — page, dashboard, document, deck, form, game — modelling the loop the artifact serves and deciding purpose and register before code, tokens before markup, and verifying against rendered evidence.
- **/review-design** — Reviews a user-visible artifact against the same design standards: renders it (or returns BLOCKED rather than judging from source), runs machine checks, exercises its states, and reports graded findings. A design gate's body activates it under the selected mode.
- **Tools skills** — /babysit-pr, /eli5, /handoff, /prompt-engineering, /review-pr, /teach-me, and /walk-pr ship alongside the core skills under their original names. /babysit-pr is the author-side companion to /review-pr and supports CI one-shot advancement via `--ci`; /teach-me turns a body of work — the session, a PR, an ADR, or any topic — into an incremental teaching loop with mastery checks.

## Manifest Schema — Gate Text

Every Acceptance Criterion and Global Invariant is **one text**: a title, a body, and an optional why. The
text a reviewer reads is the text that binds — there is no separate evaluator-facing copy, and no
field selecting execution topology or model.

```markdown
#### AC-1.1 — Health endpoint answers under load

Done when /health returns 200 on all 50 concurrent requests, with no 5xx.

Why: the load balancer drops a node after one failed check.

Deterministic gate.
```

The title summarizes the body's headline requirement and never adds to it; the why is optional and
binds nothing. Where the procedure that settles a criterion *is* what done means, it belongs in the
body. `kind` is the only structured metadata, carried on the closing line.

`kind` declares what settles the gate. A `deterministic` gate re-runs in full every round; a
`judgment` gate reads the whole change once and afterwards judges only its prior findings' repairs
and the changed delta. A gate mixing a command with a judgment is `judgment`. A manifest whose gate
omits `kind` is invalid, as is one whose gates carry a `verify` block or state a `phase` — both are
the superseded schema and there is no migration path.

/do points an evaluator at a gate by ID, giving it the manifest path rather than a copy of the
gate's text, so nothing can reword a gate between authoring and evaluation.

Each gate evaluation returns **PASS**, **FAIL**, or **BLOCKED**. BLOCKED routes via /escalate (external action pending — deploy, human approval).

## PR Lifecycle

PR-lifecycle gate bodies activate the `check-pr` skill under the selected mode through `tasks/PR_LIFECYCLE.md` task guidance. `/define --babysit <pr-url>` synthesizes a lifecycle manifest from an existing PR. /babysit-pr uses manifest/PR grounding and runs the lifecycle; /do drives the PR to a mergeable state and stops — the merge button is left to a human or GitHub auto-merge.

## Code review

Quality review is the **`review-code` skill** (one dimension per invocation, each loading its own reference): `change-intent`, `code-bugs`, `contracts`, `type-safety`, `defect-class` (defect-finders, no LOW+); `operational-readiness`, `code-design`, `code-maintainability`, `code-simplicity`, `code-testability`, `test-quality`, `docs`, `prose-value`, `context-file-adherence` (advisory, no MEDIUM+). A gate body activates `review-code` with the dimension; the skill owns each dimension's threshold, so the gate names the dimension and stops.

## Agents

manifest-dev ships no agents. `/do` uses host execution contexts according to the selected mode; formerly-agent capabilities ship as skills (`check-pr`, `poll-slack`, and the tools-side `review-prompt`).

## Unattended Execution

Run `/do` with a durable goal-setting/continuation backstop whose contract is the auditable all-criteria-PASS condition when you want the host CLI to keep `/do` running across turns: every manifest gate listed with fresh evidence, not a summary claim. For `/auto`, continuation begins at execution: `/do` sets the goal with the absolute Manifest path after definition. Understanding and definition have no continuation goal; when figure-out runs first, its full autonomous Read anatomy remains a checkpoint before `/define`. Use a host-native goal-setting capability when available; otherwise copy the completion contract the skill prints into your continuation mechanism.
