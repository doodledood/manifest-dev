# Moving an existing verification setup into the harness

A project set up before v4 may carry up to three verification pieces: a verification surface
(a harness, an eval suite, or a reader-task list, with its own README and statuses), a feature
map (an index plus one file per feature, each with a `Status:` line), and the context-file
bullets that named them. v4 replaces all of them with one harness, as
`../VERIFICATION_HARNESS.md` describes. Offer the move as one item, showing what it writes. The
context-file bullet and the ask-first setting are items of their own, offered by the version guide
that loaded this file or, where the project records no version, by the update pass.

Keep everything the project wrote; change only its shape:

- **Feature-map entries become recipes**, one per entry, named after the entry's file. *How to
  get to it* becomes *How a user reaches it*; each labeled step of *Driving it* that runs a
  command becomes a scenario with that command as `Run:` and its observable result as `Proves:`
  (`Check: read` where a person had to read the result); the index's baseline preconditions,
  driving conventions and proof rules move to the settings notes in `harness.md`; *Gotchas*
  stays; *How it is checked* becomes a gotcha or a scenario that runs the named check;
  *Sub-features* that a scenario does not exercise go under *How a user reaches it* or are
  dropped where they only restate the description.
- **Reader tasks become walk recipes**, one per task: the `Where:` line becomes the recipe's
  *How a user reaches it* and `covers`, *Ends able to* becomes the scenario's `Proves:`, and the
  scenario runs a fresh reader given only those documents (`Check: read`).
- **An eval suite stays as it is** — its cases, its README with baselines and noise floor, its
  statuses; a recipe of kind `eval` names the suite and starts it.
- **Existing harness commands are adopted by delegation**: a scenario's `Run:` calls the
  project's existing script rather than a rewrite of it.
- **Evidence keeps its files and gains a summary the tool reads.** The tool reads only
  `evidence/<recipe>/` Markdown files whose names carry a stamp (`20260101T120000Z`) or a date
  (`2026-01-01`), and from each takes two lines:
  - `- **Scenario:** <name>`, only where one of the recipe's scenarios carried the old check, with
    that scenario's exact name; leave it out otherwise, so the summary stands for the whole recipe;
  - `- **Outcome:** <outcome>`: `verified` for an entry that was `verified (DATE)`, `failed` or
    `unreachable` for one that was, and no line for any other status, which reads as `unjudged`.

  A Markdown summary already named that way moves there keeping its name and gains those lines.
  For an entry that had other evidence — screenshots, transcripts, files with other names — those
  files stay where they are or move beside the summary keeping their names, and a new summary
  `evidence/<recipe>/<DATE>.md` carries the two lines and says where they are. An entry with no
  evidence at all starts `unverified`, unless the next step gives it a Drift line, and the
  report names each one.
- **Drift is kept as a `Drift` line**, the form the tool reads, so the entry shows `stale` until
  a run repairs it and removes the line. An entry whose status was `stale (DATE): <what differs>`
  gains `Drift (DATE): <what differs>` in its recipe. Where git shows a covered path changed after
  an entry's evidence DATE, its recipe gains `Drift (<today>): <path> changed after the check of
  DATE`: the summary's time comes from the move, not the run, so without the line it would read
  current. Hand-kept `Status:` lines are then removed, since statuses now come from evidence.
- **Costly recipes get the `ask-first` mark** with the reason: any scenario that starts an agent
  session, uses a paid API or cloud resources, loads a shared environment, or has effects outside
  the repository. Run time alone is not a reason. Free drives stay unmarked.
- **The tool** is copied as `../VERIFICATION_HARNESS.md` → *The parts* says.
- **The project's customizations stay**: extra sections, its own wording, its own locations. A
  project whose verification lived at a non-default path may keep it there and set the path
  lines at the top of the tool.
- **The old pieces go**: the feature-map directory, the reader-task list, a harness or feature-map
  README and their repository checks are removed once their content is in recipes, and the tests
  that checked them are replaced by one that runs `verify check`. An eval suite's README is not
  one of them.
