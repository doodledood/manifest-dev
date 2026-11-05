---
kind: feature
covers: scripts/drive-skill.sh, scripts/walk.sh, scripts/native_drive.py, scripts/NATIVE_DRIVES.md
ask-first: starts a general agent in the running host, which uses model quota
dry-run: honored
---
# Host-owned general-agent drive

The host starts a fresh general agent with the scenario as its brief. Snapshot, fixture and
result helpers preserve inputs and evidence; the parent grades actual artifacts. No provider
selection or injected skill role is part of the default path.

## How a user reaches it

- `scripts/verify drive general-agent-drive multi-turn`.
- Every skill drive and document walk uses this same execution contract.
- Without general agents the caller warns and asks what to do. A same-host script fallback
  requires explicit approval, as `scripts/NATIVE_DRIVES.md` describes.

## Scenarios

### multi-turn
Run: `scripts/drive-skill.sh general-agent-drive verification/prompts/general-agent-multi-turn.md`
Proves: the host sends the two turns to the same general agent in order. Its first reply reports the file it created. The actual scratch file selection.txt ends with exactly alpha and beta on separate lines, in that order; the second reply reports that content. The agent receives no target skill body and writes no result receipt. The parent records actual replies and reads the artifact before grading. Preparation or one completed turn cannot pass.
Check: read

## Gotchas

- The recipe's expected outcome stays outside the subject's context.
- `scripts/verify drive model-drives` checks free input/result, missing-capability and fallback
  contracts using fixtures. Those fixture receipts are not model behavior evidence.
- This case establishes general-agent continuation and artifact handling, not skill selection,
  native plugin installation, provider parity or an evaluation-suite uplift.
