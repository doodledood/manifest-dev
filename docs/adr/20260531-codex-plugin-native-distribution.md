# ADR: Codex plugin-native distribution (retire installer.sh)

## Status
Accepted

## Context

manifest-dev distributes to non-Claude CLIs by syncing the Claude Code plugin into `dist/` via `/sync-tools`. Claude Code is the source of truth; Codex/Gemini/OpenCode are generated targets.

The Codex target historically shipped a curl/`npx skills` **installer.sh** that copied skills, generated **agent TOML stubs**, merged a multi-agent `config.toml`, installed `.rules`, and namespaced every component (`-manifest-dev` suffixes) at install time. That design was forced by the Codex of early 2026 (v0.107, the version `sync-tools/references/codex-cli.md` is still pinned to): no plugin system, no hooks (Issue #2109, community PRs rejected), and only a TOML multi-agent paradigm that couldn't represent Claude-style scoped subagents.

That constraint no longer holds. Codex **v0.135** (May 2026) ships a native, Git-based plugin + marketplace system that mirrors Claude Code almost 1:1:

- `codex plugin marketplace add owner/repo[@ref]` (git/https/ssh/local, `--sparse`) → `codex plugin add <plugin>@<marketplace>`.
- Repo layout: a marketplace root containing `.agents/plugins/marketplace.json` (lists plugins, each `source.path: ./plugins/<name>`) + `plugins/<name>/.codex-plugin/plugin.json`. Reference model: `github.com/openai/plugins` (148 plugins).
- Plugins carry **skills** (open standard, copied unchanged), **subagents as `agents/*.md`** (same `name`/`description` frontmatter as Claude Code), and even **hooks** (`hooks/hooks.json`, full event set incl. `Stop` block/continuation and `PreCompact`/`PostCompact`).

So the installer's entire reason to exist — that plugins couldn't carry agents, hooks, rules, or config — has evaporated.

## Decision

Distribute manifest-dev to Codex as a **plugin marketplace**: the repo becomes a Codex marketplace (rooted at `dist/codex/`), and Codex users install exactly as Claude Code users do — `codex plugin marketplace add doodledood/manifest-dev` then `codex plugin add <plugin>@manifest-dev`. **Retire `installer.sh`** and its TOML-stub generation, `config.toml` merge, `.rules`, and install-time namespacing.

The plugin ships **skills + the reviewer agents as `agents/*.md`** (near-verbatim from the Claude Code agents — no TOML conversion). `/sync-tools` is rewritten to generate `.codex-plugin/plugin.json` per plugin and the marketplace's `.agents/plugins/marketplace.json`, then copy skills and agents into `dist/codex/`.

**Enforcement hooks are deliberately omitted on Codex** (not "impossible" — omitted by choice). The `/do` completeness intent already lives in the skill prompt ("verify every Acceptance Criterion and Global Invariant before `/done`"); the `Stop` hook is only a *backstop* against a Claude-specific premature-stop failure mode; Codex's always-on `update_plan` loop is persistent enough in practice (confirmed by the maintainer's usage); and porting the hooks' detection layer would require rewriting `parse_do_flow` against Codex's officially-unstable session-transcript format, where a discrete "`/do` invoked" signal may not even exist. The omission is reversible — Codex supports hooks now, so if `/do` ever proves to bail early in practice, hooks can be added later.

## Alternatives Considered

- **Minimal repackage** (skills-only plugin; keep `installer.sh` for agents/rules/config): keeps the stale TOML-stub/config-merge machinery alive, forgoes shipping agents via the plugin, and leaves two install paths. Rejected — more complexity for less capability.
- **Full parity including ported hooks**: blocks the whole migration on high-risk reverse-engineering of Codex's undocumented, explicitly-unstable transcript to reliably detect an active `/do` — a backstop Codex likely doesn't need. Rejected as disproportionate risk/effort.
- **Plugin-native + thin `installer.sh` fallback** (for Codex versions predating the plugin system): extra maintenance surface for a shrinking population on old Codex. Rejected in favor of a single clean path, since the plugin system is both the present and the future.

## Consequences

### Positive
- Install matches Claude Code UX — "add the repo as a plugin" — eliminating the curl/`npx` installer.
- Deletes the TOML-stub generator, `config.toml` merge, `.rules`, install-time namespacing, and `install_helpers.py` from the Codex path; `/sync-tools` simplifies substantially.
- Reviewer agents become real Markdown subagents instead of approximated TOML stubs.
- The stale "hooks impossible / advisory only / agents are stubs" capability model is replaced by an honest, current one.

### Negative
- `/do` completeness on Codex is **advisory** (model discipline via the skill prompt), not hard-enforced — it relies on Codex's native persistence rather than a Stop-block backstop.
- Drops support for Codex versions predating the plugin system (no fallback installer).
- Exact marketplace discovery (repo-root auto-discovery vs `--sparse dist/codex`) must be verified empirically at implementation.
- `/sync-tools` and `sync-tools/references/codex-cli.md` (pinned to the obsolete v0.107 model) both need a substantial rewrite.

## Rollout

Staged across two PRs to keep the change additive until proven in the wild:

1. **PR 1 (additive)** — add the Codex marketplace under `dist/codex/` (`.agents/plugins/marketplace.json` + the two plugin packages) and rewrite `/sync-tools` to generate it. `installer.sh` stays as the safety net; nothing is removed.
2. **PR 2 (retire)** — once the plugin path is confirmed working, delete `installer.sh`, the TOML-stub / config-merge / namespacing machinery, and the stale `codex-cli.md` model.

The marketplace mechanism was validated locally on Codex v0.135 (2026-05-31): a two-plugin marketplace rooted at `.agents/plugins/marketplace.json` installed cleanly via `codex plugin marketplace add <root>` + `codex plugin add <plugin>@<mp>`. Skills and `agents/*.md` both rode into an isolated, versioned plugin cache (`~/.codex/plugins/cache/<marketplace>/<plugin>/<version>/`) intact — no manual namespacing needed, and the `config.toml` footprint is a single `[plugins."<plugin>@<mp>"] enabled = true`. The one open check is the git source: whether `codex plugin marketplace add owner/repo --sparse dist/codex` resolves the subdir root the same way the local path did.

## Source
- Session: figure-out --with-docs, 2026-05-31
- Related: See also 20260518-verifier-fail-hints-are-directives (the `/do` verification model these hooks backstopped)
