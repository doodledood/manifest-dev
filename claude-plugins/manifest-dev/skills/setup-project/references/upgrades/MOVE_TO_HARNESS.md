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
- **The checks the project runs across the whole tree get a recipe too** — its lint, type checks,
  test suite, build or gate runner, as scenarios calling the project's own commands, per
  `../VERIFICATION_HARNESS.md` → *Build on what exists*. An old surface listed only what users
  reach, so moving its entries alone would leave these checks outside the harness.
- **Statuses and committed evidence do not move.** The harness keeps no status and commits no
  evidence: a run writes its output to the evidence directory on the machine that ran, which git
  ignores (`../VERIFICATION_HARNESS.md` → *The parts*). Hand-kept `Status:` lines are removed, and
  so is committed evidence of the old surface, with the other old pieces below. Transcripts,
  screenshots or other files a recipe's scenario still points to stay where they are, and the
  recipe says where. The report names each entry whose last status was `failed` or `unreachable`,
  so that work is not lost with the line.
- **Drift is kept as a `Drift` line.** An entry whose status was `stale (DATE): <what differs>`
  gains `Drift (DATE): <what differs>` in its recipe, so the next run that reads the recipe meets
  it; the run that repairs the recipe removes the line.
- **Costly recipes get the `ask-first` mark** with the reason: any scenario that starts an agent
  session, uses a paid API or cloud resources, loads a shared environment, or has effects outside
  the repository. Run time alone is not a reason. Free drives stay unmarked.
- **The tool** is copied as `../VERIFICATION_HARNESS.md` → *The parts* says.
- **The project's customizations stay**: extra sections, its own wording, its own locations. A
  project whose verification lived at a non-default path may keep it there and set the path
  lines at the top of the tool.
- **The old pieces go**: the feature-map directory, the reader-task list, a harness or feature-map
  README, committed evidence and their repository checks are removed once their content is in
  recipes, and the tests
  that checked them are replaced by one that runs `verify check`. An eval suite's README is not
  one of them.
