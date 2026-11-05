---
kind: suite
covers: scripts/native_drive.py, scripts/NATIVE_DRIVES.md, scripts/drive-skill.sh, scripts/walk.sh, scripts/lib, tests/test_native_drive.py
---
# Model drive adapters

Free contract checks for host selection, copied inputs, native result validation and the retained
Claude path. These checks use fixture receipts; they do not measure model behavior. Actual
behavior cases run through their skill or document recipes.

## How a user reaches it

- `scripts/verify drive model-drives`.
- `scripts/NATIVE_DRIVES.md` describes the native session handoff.

## Scenarios

### contracts
Run: `.venv/bin/pytest tests/test_native_drive.py tests/test_drive_scripts.py -q`
Proves: the active host selects its own model interface, an incomplete native request cannot pass,
wrong or failed results are rejected, source snapshots and per-turn inputs remain bound to their
result, and the existing Claude launch, isolation, evidence and cancellation checks still hold.

## Gotchas

- Fixture receipts are unit-test inputs, never real model evidence.
- Codex native requests must be dispatched by the invoking session's actual model capability.
- The native detailed transcript remains in its host session; local evidence retains the terminal
  replies, model settings, source snapshots and artifacts, with cost and turn-limit gaps explicit.
