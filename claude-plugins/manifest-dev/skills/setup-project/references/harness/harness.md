---
ask-first: ask
doctor: scripts/control-notes doctor --quiet
start: scripts/control-notes launch --data-dir .runs/$VERIFY_RUN_ID
running: scripts/control-notes ps
logs: scripts/control-notes logs --data-dir .runs/$VERIFY_RUN_ID
reset: scripts/control-notes reset --data-dir .runs/$VERIFY_RUN_ID
stop: scripts/control-notes stop --data-dir .runs/$VERIFY_RUN_ID
---
- `verify start` launches an instance on its own data directory, `.runs/<run id>/` (git-ignored),
  seeds notes titled `Quarterly plan` and `Grocery list`, serves the UI on a free port it picks,
  and prints the URL, which `.runs/<run id>/url` also holds. A run never drives an instance it
  did not start, so runs side by side never meet.
- Browser steps reach controls by role and accessible name, never by CSS selector or position.
- `verify doctor` checks the instance is up, on the expected build, with this run's data directory.
- A failed run's evidence keeps the instance's server log, through `logs:`.
- Agent-session recipes need a credential for the agent CLI in the environment; they are ask-first
  because each run uses model quota.
