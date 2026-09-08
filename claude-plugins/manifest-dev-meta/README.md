# manifest-dev-meta

Maintainer-facing tooling for developing manifest-dev's own plugins — not tools for end users of the workflow (that's [`manifest-dev-tools`](../manifest-dev-tools)).

## Skills

| Skill | Description |
|-------|--------------|
| `/behavior-verification` | Empirical, live-traffic proof that a skill/prompt wording change actually changed the model's behavior, using a baseline-vs-amended capture-and-assert framework (`scripts/behavior_lab/`) instead of trusting that a diff reads like it should work. Opt-in — see `docs/adr/20260705-empirical-verification-stays-opt-in.md`. |

## How It Works

`behavior-verification` runs a task (a `Scenario`) through named variants (`Arm`s — e.g. baseline vs. amended wording) via a harness adapter, capturing every real request/response through a logging reverse proxy. Only Claude Code has a real harness adapter today; Codex and Pi are stubbed pending confirmed proxy-redirect support. Decode captured calls and assert on the target behavior (e.g. was a tool invoked) to compare arms directly, rather than judging from the wording alone.

## Installation

```bash
/plugin install manifest-dev-meta@manifest-dev
```
