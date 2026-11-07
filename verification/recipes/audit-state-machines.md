---
kind: skill
covers: claude-plugins/manifest-dev/skills/audit-state-machines
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# audit-state-machines

Audits a codebase for implicit and explicit state machines, models each one, and reports every bug the model shows and the code confirms, with a fix and an offer to turn the findings into Tickets.

<!-- The courier scenario holds docs/adr/20261107-a-figure-out-wrapper-sweeps-existing-code-for-state-machines.md. -->

## How a user reaches it

- `/audit-state-machines [path or area] [--no-log]`; with no argument the whole repository.
- Phrases its description matches: "audit the state machines", "find implicit state machines", "check the status logic across the app".
- No workflow skill calls it; it is an optional extra. Review applies the same check to a change through `code-bugs`.

## Scenarios

### courier
Run: `scripts/drive-skill.sh audit-state-machines verification/prompts/audit-state-machines-courier.md --scaffold verification/fixtures/audit-state-machines`
Proves: the read lists all six machines in the fixture — the delivery status, the photo upload's two flags, the refund status, the shop plan, the support ticket status and the address splitter's mode — and says what it searched. It reports three confirmed bugs, each with its sites by file and line, the reaching sequence and the model that found it: the nightly reconcile can move a delivered parcel back into transit; a retry after a failed upload leaves the failure flag set, so a finished upload still shows the error; a declined refund stays pending with no way out, and a new request is refused. It reports no bug in the shop plan. Each buggy machine, all three implicit, gets the make-explicit fix; the ticket status, written from two files with no bug, gets a lower-ranked make-explicit recommendation; the address splitter gets none. It offers Tickets, writes none, and leaves the fixture's files unchanged. The prompt names no bug.
Check: read

## Gotchas

- It is a thin wrapper over figure-out's autonomous mode: an investigation defect is usually in figure-out, and a checking defect in `review-code/references/code-bugs.md` → *State machines*.
- `tests/test_audit_state_machines.py` holds the wrapper's shape: it runs figure-out with `--autonomous` and `--no-docs` and points at the shared section, which exists.
- Models land under `~/.manifest-dev/models/`, outside the scratch project; read them there when grading.
