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
  [--scaffold <eval-case-dir>] [--tools] [--max-turns N]`. It needs Docker (colima on macOS) and
  a Claude credential: with a Claude subscription, run `claude setup-token` once and export the
  token as `CLAUDE_CODE_OAUTH_TOKEN` (the container cannot read the macOS keychain your login
  uses); with an API key, export `ANTHROPIC_API_KEY`. When both are set the subscription token is
  used, and its usage counts against the subscription's limits. Each drive starts a model
  session, so skill recipes are ask-first.
- Health first: `scripts/verify doctor` runs `scripts/drive-skill.sh preflight`, which checks
  Docker, the image and the credential and starts no model session (it may start Docker and
  build the image). `scripts/drive-skill.sh doctor` goes
  further: it starts one throwaway session (model quota) and checks that the plugin loaded and
  its skills are listed. A drive whose session did not load the
  plugin or the named skill exits 3 and is recorded `unreachable`, never counted.
- Each drive runs in the pinned eval container with its own home and a scratch project, this
  checkout mounted read-only: it neither reads nor leaves anything in your `~/.manifest-dev`, and
  the container is removed afterwards. Where a recipe names `~/.manifest-dev/…`, that is the
  drive's own home, kept with the full evidence. The scratch project is built from the matching
  eval case's `scaffold.sh` where a scenario passes `--scaffold`.
- Walk recipes run `scripts/walk.sh`: a fresh reader in the same container, with no tools and no
  plugins, given only the named documents; its account is the evidence. Each walk is one model
  session, so walk recipes are ask-first.
- Before running an ask-first recipe or an eval case, ask the owner, naming it and why. A prompt
  change marks the eval cases it covers stale rather than running them.
- `--dry-run` on a skill or walk recipe prints the container command, the credential that would
  be used and where evidence would go, and starts nothing.
- Prompts live in `verification/prompts/`, one file per scenario, exactly as a user would type
  them. Name the skill in the prompt (`use the define skill …` or `/manifest-dev:<skill>`):
  auto-activation from a description varies by phrasing, as
  `claude-plugins/manifest-dev/evals/README.md` → *Why the prompts name the skill* says.
- Skills that act on GitHub, Slack or a shared Ticket store are driven only against a throwaway
  repository, channel or store the run owns. Their effects reach other people and do not undo.
- Read what a skill did from the transcript and the files it wrote, never from its own account.
  A drive prints its summary — model, plugins and skills loaded, entry point, prompt, files
  written, final reply — which `verify` keeps as the evidence; the full transcript, scratch
  diff and the session's `~/.manifest-dev` stay on the driving machine under
  `${MANIFEST_DEV_FEATURES_EVIDENCE:-~/.local/state/manifest-dev-features}/<recipe>/<stamp>/`.
  Then `verify judge` records the verdict.
- An entry point that could not be driven — no GitHub access, no Slack, no Ticket store — is
  never reported verified because another entry point worked; the evidence names its scenario.
- A drive shows a skill runs, not that it beats the no-plugin baseline: the behavior suites
  under `claude-plugins/manifest-dev/evals/` measure that, with their own statuses in their
  READMEs, which the `eval` recipes start and do not redefine.
