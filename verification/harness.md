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
- Skill recipes drive a real session through `scripts/drive-skill.sh <recipe> <prompt-file>
  [--scaffold <eval-case-dir>] [--tools] [--max-turns N]`. It needs only the `claude` CLI on
  PATH, signed in as you (`claude auth login`, or `ANTHROPIC_API_KEY`), the same way locally and
  in a cloud session; no container is involved, and usage counts against your own plan or key.
  Each drive starts a model session, so skill recipes are ask-first.
- Health first: `scripts/verify doctor` runs `scripts/drive-skill.sh preflight`, which checks
  that `claude` is on PATH and signed in and starts no model session. `scripts/drive-skill.sh
  doctor` goes further: it starts one throwaway session (model quota) and checks that the plugin
  loaded and its skills are listed. A drive that cannot start, whose session did not load the
  plugin or the named skill, or whose session ended in an error, exits 3 and is recorded
  `unreachable`, never counted.
- Each drive runs `claude` directly. Its working directory is a scratch project in the drive's
  evidence directory, outside this checkout, and it is handed a copy of the plugin rather than the
  checkout's own. It starts with no user settings and no MCP servers of yours (`--setting-sources
  project,local --strict-mcp-config`), so your settings, hooks, and installed plugins do not load.
  Whether your personal memory file stays out is not something `claude --help` states. The
  scratch project is built from the matching eval case's `scaffold.sh` where a scenario passes
  `--scaffold`, with the checkout's path in `DRIVE_CHECKOUT`; a scaffold that seeds a home
  directory is not driven, since the session's home links to yours. That home links to every
  entry of yours except `~/.manifest-dev`, which starts empty. The session signs in as you, and
  recall, which reads `~/.manifest-dev`, finds none of the Manifests and logs of your own work,
  which could name what a scenario grades. It is not a sandbox: your home stays reachable by its
  real path. The links are removed when the drive ends. Where a recipe names `~/.manifest-dev/…`, that is the
  session's own; the drive copies what it wrote into the full evidence and lists it in the
  summary. Stopping a drive stops its session, which runs in the drive's own process group.
- Walk recipes run `scripts/walk.sh`: a fresh reader started the same way in an empty scratch
  directory, with no tools and no plugins, given only the named documents; its account is the
  evidence. Each walk is one model session, so walk recipes are ask-first.
- Before running an ask-first recipe or an eval case, ask the owner, naming it and why. A prompt
  change marks the eval cases it covers stale rather than running them.
- `--dry-run` on a skill or walk recipe prints the session command, the CLI version that would
  run it and where evidence would go, and starts nothing.
- Prompts live in `verification/prompts/`, one file per scenario, exactly as a user would type
  them. Name the skill in the prompt (`use the define skill …` or `/manifest-dev:<skill>`):
  auto-activation from a description varies by phrasing, as
  `claude-plugins/manifest-dev/evals/README.md` → *Why the prompts name the skill* says.
- Skills that act on GitHub, Slack or a shared Ticket store are driven only against a throwaway
  repository, channel or store the run owns. Their effects reach other people and do not undo.
- Read what a skill did from the transcript and the files it wrote, never from its own account.
  A drive prints its summary — CLI version, model, plugins and skills loaded, entry point,
  prompt, files written, final reply — which `verify` keeps as the evidence; the full
  transcript, the scratch project and what the session wrote to `~/.manifest-dev` stay on the
  driving machine under
  `${MANIFEST_DEV_FEATURES_EVIDENCE:-~/.local/state/manifest-dev-features}/<recipe>/<stamp>/`.
  Whoever drove it reads that against the scenario's `Proves` line and shows the verdict in the
  pull request's proof.
- An entry point that could not be driven — no GitHub access, no Slack, no Ticket store — is
  never reported verified because another entry point worked; the evidence names its scenario.
- A drive shows a skill runs, not that it beats the no-plugin baseline: the behavior suites
  under `claude-plugins/manifest-dev/evals/` measure that, with their own statuses in their
  READMEs, which the `eval` recipes start and do not redefine.
