---
kind: suite
covers: .
---
# property-suite

This repository's own checks: lint and format, type checks, and the property suite under
`tests/`, which asserts properties of the shipped prompts, the dist copies and `scripts/verify`
itself. Every scenario calls `scripts/check.sh`, the one list of checks the contributor docs also
point to. It is free and fast, so run it after every change rather than once at the end.

## How a user reaches it

- `scripts/check.sh --fix` from the context file's *Development Commands* and *Before PR*.
- `README.md` → *Development* and `CONTRIBUTING.md` → *Pre-Submission Checklist*.

## Scenarios

### lint
Run: `scripts/check.sh lint`
Proves: ruff and black report nothing to change in `claude-plugins/` and `tests/`.
Line: 1.3 s on linux-x64-4cpu

### types
Run: `scripts/check.sh types`
Proves: mypy passes on `tests/`, and `scripts/verify.mts` with its shipped copy type-check in
strict mode.
Line: 2.8 s on linux-x64-4cpu

### tests
Run: `scripts/check.sh tests`
Proves: every property test passes, run across every CPU.
Line: 40.5 s on linux-x64-4cpu; raised: The suite grew from 597 tests on 2026-10-18 to 852, the 2026-10-18 suite still runs in 29-30 s on this kind of machine, so the old tests are no slower and the time is in the tests added since.

## Gotchas

- It covers the whole tree, since the tests read every shipped Markdown file, so `affected`
  selects it for every change.
- The suite needs the virtual environment at `.venv` and `npm --prefix scripts ci` done;
  `scripts/setup.sh` does both. `scripts/check.sh` runs the tools from `.venv` whether or not it is
  active, and stops with a pointer to `scripts/setup.sh` when it is missing. A missing tool fails
  loudly rather than skipping its check.
