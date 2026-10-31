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

### types
Run: `scripts/check.sh types`
Proves: mypy passes on `tests/`, and `scripts/verify.mts` with its shipped copy type-check in
strict mode.

### tests
Run: `scripts/check.sh tests`
Proves: every property test passes, run across every CPU.

## Gotchas

- It covers the whole tree, since the tests read every shipped Markdown file, so `affected`
  selects it for every change.
- The suite needs the virtual environment active and `npm --prefix scripts ci` done;
  `scripts/setup.sh` does both. A missing tool fails loudly rather than skipping its check.
