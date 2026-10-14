# manifest-dev feature map

How to reach and drive each feature this repository ships: every user-invocable skill in the
two plugins, and the design instruments command-line tools. Read this index, then open the
feature file that matches the report or the change. Each file follows the shape in
`claude-plugins/manifest-dev/skills/setup-project/references/VERIFICATION_SURFACE.md` →
*The feature map*. Where a skill lives in the source is read from the source; this map says
how a user reaches it and how a run drives it.

## Baseline preconditions

- A checkout of this repository at the commit under test, with the virtual environment active
  (`source .venv/bin/activate`; `scripts/setup.sh` creates it).
- Docker running (colima on macOS) and a Claude credential in the environment or the shell
  profile: with a Claude subscription, run `claude setup-token` once and export the token as
  `CLAUDE_CODE_OAUTH_TOKEN` (the container cannot read the macOS keychain your login uses); with an
  API key, export `ANTHROPIC_API_KEY`. When both are set the subscription token is used. The
  subscription token is Anthropic's documented way to run the unmodified Claude Code CLI from a
  script; its usage counts against your subscription's limits.
- Health first: `scripts/features/drive.sh doctor` exits `0`. It starts one throwaway session and
  checks that the plugin loaded and its skills are listed. A session that only answers proves
  nothing, so a drive whose session did not load the plugin or the named skill is reported
  `unreachable`, never counted.
- Skills are driven with `scripts/features/drive.sh <feature> <prompt-file> [--scaffold
  <eval-case-dir>] [--tools]`. Each drive runs in the pinned eval container with its own home and
  a scratch project, this checkout mounted read-only: it neither reads nor leaves anything in
  your `~/.manifest-dev`, and the container is removed afterwards. Where an entry names
  `~/.manifest-dev/…`, that is the drive's own home, kept with the evidence.
- The scratch project is built from the matching eval case's `scaffold.sh` where one exists.
- Skills that act on GitHub, Slack or a shared Ticket store are driven only against a
  throwaway repository, channel or store the run owns. Their effects reach other people and do
  not undo.
- The design instruments are local command-line tools and run directly with `node`; see their
  entry.

## Driving conventions

- Name the skill in the prompt (`use the define skill …` or the slash command, written
  `/manifest-dev:<skill>`). Auto-activation from a description varies by phrasing;
  `claude-plugins/manifest-dev/evals/README.md` → *Why the prompts name the skill* says why.
- Take commands and flags literally. A flag counts only as a top-level argument, not quoted
  inside the topic.
- Read what the skill did from the transcript and the files it wrote, never from its own
  account of what it did.
- `scripts/features/drive.sh --dry-run` prints what a drive would start and where its evidence
  would go, without starting it.

## Proof and skip rules

- Every drive keeps its full evidence — transcript, scratch-project diff and new files, the
  session's `~/.manifest-dev` — under
  `${MANIFEST_DEV_FEATURES_EVIDENCE:-~/.local/state/manifest-dev-features}/<feature>/<stamp>/`,
  on the machine that drove it, and writes a summary — model, plugins and skills loaded,
  prompt, files written, final reply with local paths removed — to
  `docs/features/evidence/<feature>/<stamp>.md`, which is committed. A `verified` status names
  the summary that backs it; the full evidence is for the person who drove it, not for the
  repository. A local tool driven without the container (the design instruments) gets the same
  kind of summary by hand: each command, its exit code and its output, in that feature's
  evidence folder.
- Record the feature and the entry point with every piece of evidence; the summary carries
  both.
- An entry point that could not be driven — no GitHub access, no Slack, no Ticket store — is
  recorded as `unreachable` with the prerequisite and what was tried. It is never reported as
  verified because another entry point worked.
- The behavior cases in `claude-plugins/manifest-dev/evals/` are the measured check where an
  entry names them; a drive from this map shows the feature runs, not that it beats the
  no-plugin baseline.

## Statuses

Each entry's `Status:` line reads `unverified`, `verified (YYYY-MM-DD)` (with `; not driven: …`
naming any entry point the drive did not use), `stale (YYYY-MM-DD): <what differs>`, or
`unreachable (YYYY-MM-DD): <prerequisite>`, as `claude-plugins/manifest-dev/skills/setup-project/references/VERIFICATION_SURFACE.md`
→ *The feature map* defines. A run that changes what an entry covers updates and drives it; a run
that finds an entry it is not changing drifting marks it `stale` with the dated line.

## Features

Workflow (`manifest-dev`):

- [figure-out](./figure-out.md) — reach shared understanding of any topic; the investigation entry point.
- [figure-out-team](./figure-out-team.md) — the same investigation, run in a Slack channel or thread.
- [define](./define.md) — turn understanding into a Manifest.
- [do](./do.md) — execute a Manifest until every gate holds.
- [auto](./auto.md) — figure-out, define and do chained without approval stops.
- [setup-project](./setup-project.md) — install and audit a project's North Star, glossary, decision records and verification surface.
- [check-pr](./check-pr.md) — read-only PASS/FAIL on one pull request's readiness.
- [ticket-up](./ticket-up.md) — write Tickets into the project's store.
- [next-ticket](./next-ticket.md) — pick and claim the Ticket to work on now.
- [run-ticket](./run-ticket.md) — run one exact Ticket end to end and record the outcome on it.
- [sweep-tickets](./sweep-tickets.md) — scheduled recovery or start of one Auto Ticket.

Review and design (`manifest-dev`):

- [review-code](./review-code.md) — review a change along one quality dimension.
- [review-writing](./review-writing.md) — review prose against the writing standards.
- [design](./design.md) — design guidance for a page, document, deck or prototype.
- [review-design](./review-design.md) — review a rendered artifact against its task and medium.
- [design-instruments](./design-instruments.md) — the `design-tools.mjs` and `design-check.mjs` command-line tools.

Tools (`manifest-dev-tools`):

- [babysit-pr](./babysit-pr.md) — tend your own pull request through CI, threads and mergeability.
- [review-pr](./review-pr.md) — review someone else's pull request and post the comments.
- [walk-pr](./walk-pr.md) — walk a pull request together, one sub-change at a time.
- [handoff](./handoff.md) — write a context payload a fresh agent can continue from.
- [manifest-to-goal](./manifest-to-goal.md) — turn a Manifest into a pasteable goal.
- [prompt-engineering](./prompt-engineering.md) — write or improve a prompt, skill or agent.
- [review-prompt](./review-prompt.md) — review a prompt without changing it.
- [teach-me](./teach-me.md) — be taught a change or topic, step by step.
- [eli5](./eli5.md) — a picture explainer of a topic.
