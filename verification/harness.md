---
ask-first: ask
doctor: scripts/drive-skill.sh preflight
---
- Recipes cover every user-invocable skill in the two plugins (one recipe per skill, named after
  it), the design instruments, the tasks readers bring to the user-facing documents (kind
  `walk`), the two behavior suites (kind `eval`), and this repository's own checks
  (`property-suite`, which runs `scripts/check.sh` and is free: run it after every change). `tests/test_verify.py` runs
  `verify check` with the project's tests and fails when a user-invocable skill has no recipe.
- Every run starts from a checkout at the commit under test with the virtual environment active
  (`source .venv/bin/activate`; `scripts/setup.sh` creates it). `scripts/verify` needs Node 22.18
  or newer and says so, exiting 3, when it is missing.
- Skill and walk recipes prepare host-owned general-agent tasks through `scripts/drive-skill.sh`
  and `scripts/walk.sh`. The scenario is the brief, with copied resources and scratch fixtures;
  the helper injects no skill body and launches no provider CLI. The parent dispatches a fresh
  agent, continues it across user turns, records actual replies and grades the artifacts.
- `scripts/NATIVE_DRIVES.md` owns preparation, dispatch instructions and input-bound evidence.
  Preparation exits 3 until real completed agent results are recorded. A successful finalization
  is still read against the recipe's `Proves` text; it is not itself a behavior verdict.
- Without general agents, warn and ask what to do. A same-host script fallback needs explicit
  user approval, never automatic provider selection. Claude's retained CLI instruments have
  separate approval guards and their existing isolation, resume and cancellation checks.
- `scripts/verify doctor` checks local helper prerequisites, without a model run. The calling
  host checks its actual general-agent capability; a shell cannot introspect that tool.
- Walks give only the task and document snapshots; after opening its brief the reader uses no
  further tools. Each real drive or walk consumes model quota and is ask-first. Ask the owner
  before those runs unless already authorized. A prompt change marks measured eval cases it
  leaves unrun stale; individual drives do not establish suite uplift.
- `--dry-run` prepares nothing and starts no agent or CLI; it describes the task and evidence path.
- Prompts live in `verification/prompts/`, one file per scenario, exactly as a user would type
  them. Explicit invocation scenarios name the skill (`use the define skill …` or `/manifest-dev:<skill>`); discovery scenarios leave the choice to the general agent. State which behavior the scenario exercises.
- Skills that act on GitHub, Slack or a shared Ticket store are driven only against a throwaway
  repository, channel or store the run owns. Their effects reach other people and do not undo.
- Read what a skill did from the transcript and the files it wrote, never from its own account.
  A drive prints its host-specific summary — CLI or native identity, model, copied input,
  files written and actual reply — which `verify` keeps as the evidence; the full
  Claude transcript and workflow records, or the native terminal replies and run records, stay
  beside the scratch project under
  `${MANIFEST_DEV_FEATURES_EVIDENCE:-~/.local/state/manifest-dev-features}/<recipe>/<stamp>/`.
  The native host retains its detailed session record; native cost and hard turn-limit gaps are
  explicit in the summary. Whoever drove it reads that against the scenario's `Proves` line and shows the verdict in the
  pull request's proof.
- An entry point that could not be driven — no GitHub access, no Slack, no Ticket store — is
  never reported verified because another entry point worked; the evidence names its scenario.
- A drive shows a skill runs, not that it beats the no-plugin baseline: the behavior suites
  under `claude-plugins/manifest-dev/evals/` measure that, with their own statuses in their
  READMEs, which the `eval` recipes start and do not redefine.
