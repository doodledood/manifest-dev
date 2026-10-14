# Walk: Install it in Claude Code — 2026-10-14

- **Scenario:** fresh-reader
- **Outcome:** verified

Reader: a fresh context given only `README.md`, asked to end able to install the marketplace and
the plugin and start a first `/figure-out`.

## First walk (before this change): partly

Stuck or guessed at:
- *Install* put the commands in a `bash` block though they start with `/`, so it did not say
  whether to type them in a shell or in a Claude Code session.
- *Other CLIs* gave Claude Code's install as `/plugin install manifest-dev@manifest-dev` alone,
  dropping the `marketplace add` step *Install* has.
- Nothing said where to start the first `/figure-out`.
- Also noted, not changed: no version prerequisite, no way to confirm the install, whether the
  command takes a `manifest-dev:` prefix, whether the second plugin is needed.

Fixed in the document: the commands are run inside a Claude Code session, the block is plain
text, *Install* says to start a session in the target repository and type `/figure-out <topic>`,
and *Other CLIs* carries both steps.

## Second walk (after the fix)

See the result recorded below.

Result: **yes**. Steps quoted from *Install*: run `/plugin marketplace add doodledood/manifest-dev`
and `/plugin install manifest-dev@manifest-dev` inside a Claude Code session, then start a session
in the repository and type `/figure-out <topic>`. Remaining guesses, none blocking: whether a new
session is needed after installing, whether the install is per user or per project, and that the
opening example's block read as a shell command (changed to plain text in the same change).
