# Pi CLI Package Conversion Guide

Reference for generating the Pi target from the Claude Code plugin sources.

## Capability Model

Pi is an Agent Skills host and package host. For manifest-dev, the Pi target is deliberately skills-first: ship the portable skills plus prompt-template slash aliases, and rely on the active host's goal-setting / continuation capability when one is available.

| Pi Capability | Why manifest-dev cares |
|---------------|------------------------|
| Repo-root package install | Users can run `pi install git:github.com/doodledood/manifest-dev@ref` and update with Pi's package flow. |
| `package.json` `pi` manifest | Source-owned install contract for generated skills and prompt templates. |
| Agent Skills loading | The full manifest-dev workflow can ship as ordinary package skills. |
| `/skill:<name>` commands | Every skill remains directly invocable when skill commands are enabled. |
| Prompt templates | Package-local templates provide `/do`, `/auto`, and `/babysit-pr` convenience aliases that expand to the matching skill invocation with `$ARGUMENTS`. |
| Host continuation / goals | When available, skills set a durable completion contract; when absent or disabled, the workflow remains prompt-level with no continuous host enforcement. |

## Claude Code Component Mapping

| Claude Code Source | Pi Target |
|--------------------|-----------|
| Skills | Package skills under `dist/pi/skills/`, with Pi target substitutions. |
| `/do`, `/done`, `/escalate` | Ordinary package skills. `/do` runs the portable main-agent verifier protocol; `/done` and `/escalate` are invoked by `/do` as skills. |
| `/auto`, `/babysit-pr` | Ordinary package skills. Prompt-template aliases expose `/auto` and `/babysit-pr` as convenience commands. |
| Reviewer/verifier skills | `check-pr`, `poll-slack`, `review-prompt`, and `review-code` ship as ordinary skills; verifier prompts activate them by bare skill name. |
| Agents | None — manifest-dev ships no agents. |
| Extensions | None for this target. Do not generate Pi TypeScript extensions for manifest-dev unless a future ADR restores a host-specific runtime tier. |
| Prompt templates | Generate only user-facing slash aliases, not verifier prompts. |
| Installer scripts | Not generated. Pi package manager owns install, update, remove, and project-local scope. |

## Distribution Model

```
package.json                             # source-owned Pi package metadata
dist/pi/
├── README.md
├── skills/                              # full compatible skill payload
├── prompts/                             # /do, /auto, /babysit-pr aliases
├── component-namespaces.json            # ownership audit metadata
└── .sync-meta.json
```

The Pi package manifest shape is:

```json
{
  "name": "@doodledood/manifest-dev-pi",
  "version": "1.3.0",
  "private": true,
  "type": "module",
  "keywords": ["pi-package", "manifest-dev", "agent-skills"],
  "pi": {
    "skills": ["./dist/pi/skills"],
    "prompts": ["./dist/pi/prompts"]
  }
}
```

There is no `pi.extensions` entry, no `packages/manifest-dev-pi-tools` workspace, and no runtime helper export. Bump the repo-root package version when Pi package metadata, generated Pi skills/prompts, or Pi docs change.

## Skill Handling

Copy all workflow skills from both source plugins, including:

- Core: `auto`, `review-code`, `define`, `do`, `done`, `escalate`, `figure-out`, `figure-out-team`, `check-pr`, `poll-slack`
- Tools: `adr`, `babysit-pr`, `handoff`, `prompt-engineering`, `review-prompt`, `review-pr`, `teach-me`, `walk-pr`

Apply these substitutions:

1. **Strip plugin qualifiers from skill references → bare names.** Pi invokes skills as `/skill:<name>` and has no plugin namespace. Rewrite `manifest-dev:<skill>` / `manifest-dev-tools:<skill>` to `<skill>` in copied skill bodies.
2. **Omit Claude session-file handoff lines** where the target cannot provide an exact equivalent.
3. **Preserve universal goal-setting backstop guidance.** If the active harness exposes goal-setting or continuation, the model should set the durable completion contract directly; otherwise it prints/carries the copy-pasteable fallback. Do not hardcode one host's primitive as the principle.

## Prompt Templates

Generate package-local prompt templates under `dist/pi/prompts/`:

- `do.md` → `/do <manifest-path>` expands to `Use the do skill with: $ARGUMENTS`
- `auto.md` → `/auto <task>` expands to `Use the auto skill with: $ARGUMENTS`
- `babysit-pr.md` → `/babysit-pr ...` expands to `Use the babysit-pr skill with: $ARGUMENTS`

These templates are aliases only. The skill bodies own behavior.

## Runtime Boundary

Pi no longer owns manifest-dev verifier fanout, manifest parsing, verdict aggregation, done/escalation gating, verifier concurrency flags, or wait-pending runtime tokens. `/do` follows the same portable verifier protocol as other hosts: the main agent reads the Manifest, enumerates AC/GI gates, launches independent verifier executions using each `verify.prompt` verbatim, repairs FAILs, reports genuine BLOCKED blockers, and calls `done` only after all gates PASS.

A host-provided goal/continuation feature is an optional outer backstop. If none exists or it is disabled, manifest-dev still runs normally, but no continuous host-level enforcement is guaranteed.

## Namespacing

Pi package resources are scoped by package source, so install-time suffixing is not used. Keep original skill and prompt names. Still generate `component-namespaces.json` for cross-target auditability; it records source ownership and alias decisions, not installer behavior.

## Installation

Primary repo-root install from a local checkout:

```bash
pi install .
```

Temporary one-run install:

```bash
pi -e .
```

Project-local install:

```bash
pi install -l .
```

Git install from the repository root:

```bash
pi install git:github.com/doodledood/manifest-dev@<ref>
```

Update:

```bash
pi update
pi update --extensions
```

Remove:

```bash
pi remove git:github.com/doodledood/manifest-dev
```

Do not generate `install.sh` for Pi. Pi's package manager is the installer.

## README Requirements

Pi README must document:

- install/update/remove/local-development flows
- included `/skill:<name>` commands
- `/do`, `/auto`, `/babysit-pr` prompt-template aliases
- optional host continuation / goal-setting recommendation, including the suggested `pi-plugins` goal-controller package link as one possible Pi continuation provider
- explicit fallback: without a continuation capability, `/do` is prompt-level and may not continue automatically across turns

## Context File Adaptation

Operational `CLAUDE.md` references that mean "this CLI's context file" should become generic "context file" language or `AGENTS.md` only where that target convention is intended. Do not rewrite comparative or historical mentions.
