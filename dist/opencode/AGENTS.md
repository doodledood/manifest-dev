# AGENTS.md — manifest-dev Workflow Context

## Overview

manifest-dev provides manifest-driven workflows for AI coding agents. The core flow is:

```
/define → manifest → /do (executes + verifies inline) → /done
```

- **/define** — Interactive manifest builder. Probes for requirements, quality gates, edge cases. Outputs a manifest with deliverables, acceptance criteria, and global invariants.
- **/do** — Manifest executor. Implements deliverables, weighs process guidance, adapts approach when reality diverges, and evaluates every gate by pointing an evaluator at that gate in the Manifest rather than at a copy of its text. `per-gate` is the independent default; `consolidated` is an opt-in mode for gate sets that are large and individually cheap, and `self` an opt-in lower-assurance one. Optional `--verifier-model` applies to independent modes. It aggregates PASS / FAIL / BLOCKED, fixes failures, and re-evaluates — command-backed gates in full, judgment gates over their prior findings' repairs and the changed delta after one full look, with `--exhaustive-verification` restoring full re-sampling. Caller overlays can narrow retry cadence, e.g. CI one-shot runs report wait-only states instead of sleeping.
- **/just-do** — Goal-based Manifest executor beside /do. Pursues a state where every Acceptance Criterion and Global Invariant holds as written, deciding order, method, and amount of checking for itself — no gate ledger, no verification modes, no execution log. The Manifest is read-only to the run: a statement gone false or a user redirect stops it for /define amendment and relaunch. Sets the host's goal/continuation backstop when one exists; otherwise prints the goal for the user to activate and re-invoke.
- **/just-auto** — Goal-based autonomous chain beside /auto: figure-out --autonomous, then define --autonomous, then just-do with the resulting Manifest path — no approval waits, no verification flags, one chain-spanning goal armed up front (printed-and-proceeded on hosts without a goal capability).
- **/done** — Plain-prose completion summary called by /do after every criterion has fresh PASS evidence under the selected mode.
- **/escalate** — Structured blocker handoff for unrecoverable failures or pending external action.

Supporting workflows:
- **/auto** — End-to-end autonomous: /figure-out → /define → /do in one command. It forwards `/do`'s verification options without putting them in the Manifest. Its unattended parent goal should treat full autonomous Read anatomy as a checkpoint before manifest creation when figure-out runs, then use manifest written plus /do gate-ledger PASS as the terminal condition. Supports `--babysit <pr-url>` for tending an existing PR end-to-end.
- **/figure-out** — Truth-convergent thinking partner. /define auto-invokes it when the problem space is foggy.
- **/figure-out-team** — /figure-out's discipline applied to a multi-party async Slack conversation.
- **/chat-surface** — Shapes where a conversation lands so each response is understood at the lowest cognitive load its content allows — skimmable claims, tables and diagrams where they beat a sentence, asks set apart with their recommendation. Runs in text mode (monospace forms, no artifact) or html mode (a live auto-updating HTML page with charts, SVG diagrams, and decision cards). Use when another skill activates a surface (e.g. figure-out --surface text or --surface chat-surface), or when the user asks for the chat surface, a rendered chat view, or a richer view of the conversation.
- **/ticket-up** — Authors convention-compliant Tickets from a Manifest, direct work, independently managed questions, or source-linked follow-ups. A Manifest stays one coherent Ticket by default; explicit delegation can split it on Deliverable boundaries.
- **/next-ticket** — Reads the Ticket store, claims the single best ready Ticket, and presents it without starting execution.
- **/run-ticket** — Claims or recovers one exact Ticket, runs /auto, completes required protected landing, then records DONE or ESCALATED evidence on that same Ticket. Backlog selection stays outside it.
- **/sweep-tickets** — Scheduled one-Ticket correctness path: resumes one interrupted automation-owned Auto Ticket, otherwise selects one ready Auto Ticket, invokes /run-ticket, and stops.
- **/init-context** — Sets a repository up with project-owned ADR conventions, a glossary, and the context-file wiring that keeps sessions using them, seeding them from the project's own history where there is any.
- **/review-writing** — Reviews prose against the project's writing standards in its own register: documentation or human-voiced writing. Detects the register, applies it plus the shared floor, and reports graded findings. Distinct from review-code's prose-value dimension, which asks whether prose in a diff earns its place.
- **Tools skills** — /babysit-pr, /handoff, /prompt-engineering, /re-pitch, /review-pr, /teach-me, and /walk-pr ship alongside the core skills under their original names. /babysit-pr is the author-side companion to /review-pr and supports CI one-shot advancement via `--ci`; /teach-me turns a body of work — the session, a PR, an ADR, or any topic — into an incremental teaching loop with mastery checks.

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

Run `/do` with a durable goal-setting/continuation backstop whose contract is the auditable all-criteria-PASS condition when you want the host CLI to keep `/do` running across turns: every manifest gate listed with fresh evidence and evaluator provenance under the selected mode, not a summary claim. For `/auto`, use one full-chain parent goal whose terminal condition is manifest written plus `/do` gate-ledger PASS; when figure-out runs first, its full autonomous Read anatomy is a checkpoint before `/define`. Use a host-native goal-setting capability when available; otherwise copy the completion contract the skill prints into your continuation mechanism.
