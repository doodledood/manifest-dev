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
- Skill recipes use `scripts/drive-skill.sh`; walks use `scripts/walk.sh`. The model interface
  follows the running session: Claude CLI under Claude Code, the active native model capability
  under Codex cloud. Installing a CLI does not choose the host. Both paths use scratch inputs
  outside the checkout and keep the rubric out of the worker context.
- `scripts/NATIVE_DRIVES.md` owns the Codex request, native dispatch, result recording and recipe
  resumption steps. Preparation exits 3 and remains unverified until an actual native session
  completes and its matching result is validated. There is no Claude or separate Codex CLI login.
- Under Claude Code, the driver requires the Claude CLI signed in. It starts with no user
  settings or MCP configuration, copies the plugin and isolates personal workflow records.
  `scripts/lib/claude-cli.sh` carries those launch flags and reaps the model on cancellation.
- `scripts/verify doctor` checks prerequisites without a model run. In Codex this confirms the
  local handoff protocol, not model readiness; `scripts/drive-skill.sh doctor` prepares a real
  native smoke request. In Claude it checks the CLI and sign-in before the model smoke session.
- Walks provide only the task and document snapshots. The native reader opens that input and
  answers without further tools. Each real drive or walk consumes model quota and is ask-first.
- Before running an ask-first recipe or an eval case, ask the owner, naming it and why. A prompt
  change marks the eval cases it covers stale rather than running them.
- `--dry-run` on a skill or walk recipe prints the session command, the CLI version that would
  run it and where evidence would go, and starts nothing. Native dry runs name the active host without preparing a request.
- Prompts live in `verification/prompts/`, one file per scenario, exactly as a user would type
  them. Name the skill in the prompt (`use the define skill …` or `/manifest-dev:<skill>`):
  auto-activation from a description varies by phrasing, as
  `claude-plugins/manifest-dev/evals/README.md` → *Why the prompts name the skill* says.
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
