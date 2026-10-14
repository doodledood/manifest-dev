# Walk: Set a project up — 2026-10-14

- **Scenario:** fresh-reader
- **Outcome:** verified

Reader: a fresh context given only `claude-plugins/manifest-dev/README.md` → *Project surfaces*,
asked to end able to say what setting a project up installs and how an older setup gets updates.

## Result: able to answer

The reader named all four surfaces and the wiring, and said an older setup is updated by running
`/setup-project` again, which audits the whole setup and offers each gap, and that `/figure-out`
offers it when the recorded version is behind or a surface is broken.

Stuck or guessed at:
- Whether the run applies changes itself or waits for each one to be accepted. Fixed: the row
  now says each gap is offered "for you to accept or decline".
- Where the surfaces version is recorded. Fixed: "in your context file".
- Not changed, by design of a summary table: what each surface is and which files it writes; the
  section is an index and the skill's own text carries the detail.

## Re-walk after the need-scoped rewording (same day)

The `/setup-project` row changed after the walk above (setup offers only what the project needs; no
hand-off). A fresh reader, given only *Project surfaces*, again named the four surfaces and the
wiring, and said an older setup is updated by running `/setup-project` again — it audits the whole
setup and offers each gap to accept or decline, marking what changed since the version recorded in
the context file, and `/figure-out` offers it when that version is behind or a surface is broken.
That is the task's end state. Its remaining guesses (what each surface is, which file the context
file is) are what a summary table leaves to the skill's own text, as before.
