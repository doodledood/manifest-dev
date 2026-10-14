---
ask-first: ask
doctor: scripts/control-notes doctor --quiet
---
- Runs start from `scripts/control-notes launch --data-dir /tmp/notes-verify-$RUN_ID`, which seeds
  notes titled `Quarterly plan` and `Grocery list` and serves the UI at `http://127.0.0.1:4173`.
  A run never drives an instance it did not start.
- Browser steps reach controls by role and accessible name, never by CSS selector or position.
- `verify doctor` checks the instance is up, on the expected build, with this run's data directory.
- Agent-session recipes need a credential for the agent CLI in the environment; they are ask-first
  because each run uses model quota.
