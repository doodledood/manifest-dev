# Moving an existing verification setup into the harness

A project set up before v4 may carry up to three verification pieces: a verification surface
(a harness, an eval suite, or a reader-task list, with its own README and statuses), a feature
map (an index plus one file per feature, each with a `Status:` line), and the context-file
bullets that named them. v4 replaces all of them with one harness, as
`../VERIFICATION_HARNESS.md` describes. Offer the move as one item, showing what it writes; the
version guide that loaded this file offers the context-file bullet and the ask-first setting as
items of their own.

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
  `evidence/<recipe>/<stamp-or-date>.md` summaries. A Markdown summary already named with a stamp
  (`20260101T120000Z`) or a date (`2026-01-01`) moves there keeping its name and gets
  `- **Outcome:** verified` when its entry was `verified (DATE)`. Any other evidence —
  screenshots, transcripts, files with other names — stays where it is or moves beside the
  summary keeping its name, and for an entry that was `verified (DATE)` a new summary
  `evidence/<recipe>/<DATE>.md` records the scenario, `- **Outcome:** verified`, and where those
  files are. An entry verified with no evidence at all becomes `unverified`, and the report says
  so. Hand-kept `Status:` lines are removed, since
  statuses now come from evidence.
- **Costly recipes get the `ask-first` mark** with the reason: any scenario that starts an agent
  session, uses a paid API or cloud resources, runs far longer than the usual tests, loads a
  shared environment, or has effects outside the repository. Free drives stay unmarked.
- **The tool** is copied as `verify` and `verify.mts` — TypeScript by default, ported where the
  user asks for another language or the project cannot run Node, per `../VERIFICATION_HARNESS.md`.
- **The project's customizations stay**: extra sections, its own wording, its own locations. A
  project whose verification lived at a non-default path may keep it there and set the path
  lines at the top of the tool.
- **The old pieces go**: the feature-map directory, the reader-task list, a harness or feature-map
  README and their repository checks are removed once their content is in recipes, and the tests
  that checked them are replaced by one that runs `verify check`. An eval suite's README is not
  one of them.
