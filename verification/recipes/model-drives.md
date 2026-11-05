---
kind: suite
covers: scripts/native_drive.py, scripts/NATIVE_DRIVES.md, scripts/drive-skill.sh, scripts/walk.sh, scripts/drive-skill-claude.sh, scripts/walk-claude.sh, scripts/lib, tests/test_native_drive.py
---
# General-agent evidence and explicit CLI instruments

Free contract checks for provider-independent preparation, copied inputs, actual result validation,
missing-capability decisions and the approved same-host CLI instruments. These checks use fixture receipts; they do not measure model behavior. Actual
behavior cases run through their skill or document recipes.

## How a user reaches it

- `scripts/verify drive model-drives`.
- `scripts/NATIVE_DRIVES.md` describes the native session handoff.

## Scenarios

### contracts
Run: `.venv/bin/pytest tests/test_native_drive.py tests/test_drive_scripts.py -q`
Proves: all host markers use the same general-agent preparation, an incomplete request cannot pass,
wrong or failed results are rejected, source snapshots and per-turn inputs remain bound to their
result, missing agents require a user decision, unapproved or foreign-host fallbacks are rejected, and the retained CLI launch, isolation, evidence and cancellation checks still hold.

## Gotchas

- Fixture receipts are unit-test inputs, never real model evidence.
- The running host starts the actual general agent. A helper never selects a provider or launches one.
- `general-agent-drive multi-turn`, skill recipes and document walks exercise the real flow.
- The native detailed transcript remains in its host session; local evidence retains the terminal
  replies, model settings, source snapshots and artifacts, with cost and turn-limit gaps explicit.
