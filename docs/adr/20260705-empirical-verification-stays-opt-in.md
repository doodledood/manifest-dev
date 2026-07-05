# ADR: Empirical skill-behavior verification stays opt-in, not a mandatory gate

## Status
Accepted

## Context
manifest-dev skills and prompts get amended frequently, and a wording change's actual effect on the live model's behavior (does it now invoke the tool it's supposed to, does the intended structural change in the request actually land) is not something a diff review alone can confirm — only running the change against a real backend and inspecting the captured traffic can. The `manifest-dev-tools:prompt-engineering` skill is gaining an empirical verification framework (`scripts/behavior_lab/`) that runs a baseline vs. amended arm through a real harness (Claude Code today, Codex/Pi stubbed for later) and asserts on the captured behavior. The open question was whether running this framework should be **mandatory** — wired into some existing gate (a `review-code` dimension, a `check-pr`/`babysit-pr` requirement, a CLAUDE.md rule) that fires on every skill/prompt wording change — or **opt-in**, a capability a developer reaches for deliberately.

## Decision
The framework stays opt-in. It ships as tooling under `prompt-engineering` that a developer invokes when they want live-traffic proof a wording change had its intended effect. Nothing auto-triggers it: no `review-code` dimension checks for it, no PR-lifecycle skill requires it, no CLAUDE.md rule mandates it for skill/prompt changes.

Rationale: running even one arm through a real harness costs live API budget and real wall-clock time across one or more live agent sessions — auto-triggering that on every skill/prompt wording change would tax unrelated, low-risk edits (typo fixes, rewording for clarity) the same as high-risk ones. A single live sample of LLM behavior is also noisy — the same prompt can produce different tool-use decisions run to run — so a hard automatic PASS/FAIL gate risks blocking merges on sampling noise before the framework has a track record establishing how many repeats make a result trustworthy.

## Alternatives Considered
- **Mandatory gate on every skill/prompt-wording diff** (new `review-code` dimension or CLAUDE.md rule): rejected — forces live API spend and latency on every change regardless of risk, and a single noisy live sample isn't a reliable hard gate.
- **Mandatory but sampled/budget-capped** (e.g., only on reviewer request, or a capped percentage of changes): rejected for now — needs scheduling/CI infrastructure that doesn't exist yet and repeat-count tuning with no usage history to base it on. Revisit once the opt-in tool has been used enough to know what a trustworthy repeat count and false-positive rate look like.

## Consequences

### Positive
- Developers can get real evidence for risky or uncertain wording changes without imposing cost/latency on every change.
- Keeps this framework's initial scope to "build the capability" — the harder policy question (what triggers it, who owns the API cost, acceptable noise tolerance) is deferred to a later decision informed by actual usage.

### Negative
- Purely opt-in means a regression-causing wording change can ship unverified if the developer doesn't think to run the harness — no CI backstop catches this systematically today.

## Source
- Manifest: `manifest-20260704-163918.md` (amended in this session to fold in this decision)
- Session: figure-out session, 2026-07-05
