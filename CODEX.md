# Codex Support

This repository now includes a root-level `skills/` directory (symlinked to the existing Claude plugin skills) so it can be installed and used as Codex skills without duplication.

## Install

- Using $skill-installer (recommended):
  - Ask Codex: "Install Codex skills from GitHub repo kinnrot/manifest-dev."
  - The installer will detect the `skills/` directory at the repo root and copy the skills.
  - Select skills to install: `define`, `do`, `verify`, `done`, `escalate`.

- Manual:
  - Copy or symlink each folder under `skills/` to `$CODEX_HOME/skills/`.

## Use

- `$define` — interview-driven manifest creation; produces a `manifest.md`.
- `$do` — executes toward the manifest; writes/reads a log file.
- `$verify` — runs verifiers for Global Invariants and Acceptance Criteria.
- `$done` — summarizes completion once all checks pass.
- `$escalate` — structured escalation when blocked.

Tip: Run `$do` in a fresh thread after `$define` completes, or compact first.
