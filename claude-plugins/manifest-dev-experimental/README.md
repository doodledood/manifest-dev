# manifest-dev-experimental

Maximally-slim parallel rework of the `manifest-dev` plugin. The discipline: trust model capability, specify only what's non-default, drop scaffolding that defends against failures the model handles fine when given clean posture. Lives alongside `manifest-dev` until promotion.

## Skills

- **`/figure-out`** — relentless probing. Walks every branch of the decision tree (design, diagnostic, commitment, exploratory), tackles the next load-bearing question first, gives recommended answers, returns to dropped threads, explores instead of asking when discoverable.
- **`/define`** — encodes shared understanding into a verifiable Manifest. Auto-invokes `figure-out` when the transcript lacks understanding. Supports `--babysit <pr-url>`, `--canvas`, `--autonomous`.
- **`/do`** — executes a Manifest by spawning one verifier subagent per Acceptance Criterion (using `verify.prompt:` verbatim), respecting `phase:` ordering, calling `/done` when every AC passes or `/escalate` when blocked. Mid-/do user messages default to invoking `/define` for amendment.
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

- **`/verify` is gone.** Its protocol moves inline into `/do`: spawn a subagent per AC, aggregate, route to `/done` (all PASS) or `/escalate` (any BLOCKED, or unrecoverable FAIL). No separate skill, no return-block YAML protocol, no auto-trigger-full-final state machine, no selective `--scope`, no `--deferred` flag.
- **`/do` absorbs amendment routing.** Mid-/do user messages default to invoking `/define` for amendment; pure questions answered inline. No separate Self-Amendment escalation type.
- **Schema collapsed to four fields**, all verification is always-subagent. The previous `method:` / `inner_method:` / `command:` / `timeout:` / `manual` value / `deferred-auto` method are gone — the verifier subagent runs whatever bash, file reads, or external tools it needs from its prompt.
- **One mode instead of three.** `--mode` and `--interview` flags are gone; defaults are quality-first. `Mode:`, `Interview:`, and `Medium:` top-level manifest fields are gone too — experimental is single-mode, local-only.
- **`/escalate` collapsed to one type** (blocking). The previous six-type taxonomy and `references/TEMPLATES.md` are gone.
- **PR-lifecycle composition auto-detects** from the local `origin` remote (no `--platform` flag).
- **`figure-out` owns the interview.** `/define`'s epistemic stance, interview style modes, and discovery-question disciplines live in `/figure-out`, which `/define` auto-invokes on cold-start.
- **Reviewers catch what slim discipline loses.** No separate rubric files; `change-intent-reviewer` and `prompt-reviewer` catch regressions during /verify-style audits of changed prompts.

## Hooks and agents

Hooks (`hooks/`) and reusable agents (`agents/`) are duplicated from the core plugin so this plugin runs standalone. Two hooks fire: `stop_do_hook` (blocks premature stops; injects a terse "reload /do" reminder) and `post_compact_hook` (restores manifest context after session compaction).

**Cross-plugin isolation.** Both this plugin's hooks and `manifest-dev`'s hooks use strict namespace matching: only their own plugin's skill invocations register. When both plugins are installed alongside, neither plugin's hooks fire on the other's flow — `/manifest-dev-experimental:do` triggers only experimental hooks; `/manifest-dev:do` triggers only main hooks.

The `criteria-checker` agent (the most-invoked verifier in this plugin) inherits the default tool set — no `tools:` allowlist — so users with MCP servers or extra CLI tools configured can verify against them. Read-only behavior is enforced by the agent's prompt, not by the tool list.

## Status

Experimental. Skills produce the same outcomes as the core plugin but with radically slimmer prompts and a tighter machine contract. The plan: use experimental, observe what fails, fix with specific lines (not blanket additions), promote to core when validated.
