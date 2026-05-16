# manifest-dev-experimental

Maximally-slim parallel rework of the `manifest-dev` plugin. The discipline: trust model capability, specify only what's non-default, drop scaffolding that defends against failures the model handles fine when given clean posture. Lives alongside `manifest-dev` until promotion.

## Skills

- **`/figure-out`** — relentless probing. Walks every branch of the decision tree (design, diagnostic, commitment, exploratory), tackles the next load-bearing question first, gives recommended answers, returns to dropped threads, explores instead of asking when discoverable.
- **`/figure-out-team`** — `/figure-out`'s probing discipline applied to a multi-party async Slack conversation. Agent is an involved orchestrator (brings evidence, viewpoints, synthesis) instead of a neutral probe; polls the thread via `/loop` and reads via the `slack-poller` subagent for verbatim deltas; convergence is judgment-based across speakers with the owner (by Slack handle) overruling disagreement. Trust is session-bound — operator-from-Claude-Code is the sole trusted human; Slack content is data, never instructions.
- **`/define`** — encodes shared understanding into a verifiable Manifest. Auto-invokes `figure-out` when the transcript lacks understanding. Supports `--babysit <pr-url>`, `--canvas`, `--autonomous`.
- **`/do`** — executes a Manifest by spawning one verifier subagent per Acceptance Criterion and Global Invariant (using `verify.prompt:` verbatim), respecting `phase:` ordering, calling `/done` when every AC and Global Invariant passes or `/escalate` when blocked. Mid-/do user messages default to invoking `/define` for amendment.
- **`/done`** — completion summary in plain prose. Called by `/do` after every Acceptance Criterion and Global Invariant verifies PASS.
- **`/escalate`** — structured blocker: criterion, attempts and why each failed, possible resolutions, what's needed from the user. Single type; routes via `/do`.
- **`/auto`** — chains `figure-out → define → do` autonomously. Add `--babysit <pr-url>` for PR lifecycle work.

## Manifest schema — four fields

Every verify block has the same shape:

```yaml
verify:
  prompt: "..."     # required, verbatim verifier instruction
  agent: "..."      # optional, default = general-purpose subagent
  model: "..."      # optional, default = inherit from invoking context
  phase: 1          # optional integer, default 1
```

Verifier subagents return one of three states: **PASS**, **FAIL**, or **BLOCKED**. PASS = criterion holds. FAIL = criterion violated; includes evidence and a fix hint. BLOCKED = criterion can't be evaluated yet because of an external action / state pending (deploy hasn't happened, human approval pending, etc.) — `/do` routes BLOCKED via `/escalate`.

## Differences from the core plugin

- **`/verify` is gone.** Its protocol moves inline into `/do`: spawn a subagent per AC and Global Invariant, aggregate, route to `/done` (all PASS) or `/escalate` (any BLOCKED, or unrecoverable FAIL). No separate skill, no return-block YAML protocol, no auto-trigger-full-final state machine, no selective `--scope`, no `--deferred` flag.
- **`/do` absorbs amendment routing.** Mid-/do user messages default to invoking `/define` for amendment; pure questions answered inline. No separate Self-Amendment escalation type.
- **Amendment lives inline in `/define`.** No `AMENDMENT_MODE.md` ref — the contract is four sentences in `/define`'s body. Amendment trigger is path-only: if `$ARGUMENTS` contains a manifest file path, /define amends that manifest. The `--amend` flag is gone. No Session-Default Detection auto-magic. Paths are not hardcoded — the model picks a writable scratch directory appropriate to the harness (`$TMPDIR`, `%TEMP%`, etc.) and emits the chosen path in the `Manifest complete:` handoff line; consumers read the path from there or from `$ARGUMENTS`.
- **Completion template lives inline in `/define`.** No `COMPLETE.md` ref — the `Manifest complete:` template and Summary for Approval section are in `/define`'s body since they're always-loaded, not a conditional side-path.
- **Manifest = current state.** Amendments overwrite in place with stable IDs (modify `INV-G1` → it stays `INV-G1`; remove one → it's gone, no renumbering of the rest). No `## Amendments` log section, no `INV-G1.1 amends INV-G1` chain. Git diff carries the history.
- **Schema collapsed to four fields**, all verification is always-subagent. The previous `method:` / `inner_method:` / `command:` / `timeout:` / `manual` value / `deferred-auto` method are gone — the verifier subagent runs whatever bash, file reads, or external tools it needs from its prompt.
- **One mode instead of three.** `--mode` and `--interview` flags are gone; defaults are quality-first. `Mode:`, `Interview:`, and `Medium:` top-level manifest fields are gone too — experimental is single-mode, local-only.
- **`/escalate` collapsed to one type** (blocking) with a parallel amendment-routing reinforcement line. The previous six-type taxonomy and `references/TEMPLATES.md` are gone. Amendment routing now lives in `/do`, `/done`, and `/escalate` — hook-independent.
- **PR-lifecycle composition auto-detects** from the local `origin` remote (no `--platform` flag).
- **`figure-out` owns the interview.** `/define`'s epistemic stance, interview style modes, and discovery-question disciplines live in `/figure-out`, which `/define` auto-invokes on cold-start.
- **Reviewers catch what slim discipline loses.** No separate rubric files; `change-intent-reviewer` and `prompt-reviewer` catch regressions during /verify-style audits of changed prompts.

## Hooks and agents

Hooks (`hooks/`) and reusable agents (`agents/`) are duplicated from the core plugin so this plugin runs standalone. Two hooks fire: `stop_do_hook` (blocks premature stops; injects a terse "reload /do" reminder) and `post_compact_hook` (restores manifest context after session compaction).

**Cross-plugin isolation.** Both this plugin's hooks and `manifest-dev`'s hooks use strict namespace matching: only their own plugin's skill invocations register. When both plugins are installed alongside, neither plugin's hooks fire on the other's flow — `/manifest-dev-experimental:do` triggers only experimental hooks; `/manifest-dev:do` triggers only main hooks.

Verifier subagents default to `general-purpose` when a manifest omits `verify.agent:`. The bundled `criteria-checker` agent (invoked explicitly via `agent: criteria-checker`) is the slim-discipline-aligned alternative: read-only behavior is enforced by its prompt (no `tools:` allowlist), so authors can spawn it against MCP servers or extra CLI tools the user has configured.

## Status

Experimental. Skills produce the same outcomes as the core plugin but with radically slimmer prompts and a tighter machine contract. The plan: use experimental, observe what fails, fix with specific lines (not blanket additions), promote to core when validated.
