# Moving an existing verification setup into the harness

A project set up before v4 may carry up to three verification pieces: a verification surface
(a harness, an eval suite, or a reader-task list, with its own README and statuses), a feature
map (an index plus one file per feature, each with a `Status:` line), and the context-file
bullets that named them. v4 replaces all of them with one harness, as
`../VERIFICATION_HARNESS.md` describes. Offer the move as one item, showing what it writes.

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
- **Eval cases stay where they are**; a recipe of kind `eval` names the suite and starts it.
- **Existing harness commands are adopted by delegation**: a scenario's `Run:` calls the
  project's existing script rather than a rewrite of it.
- **Evidence moves with its recipe** to `evidence/<recipe>/`, keeping its file name. An entry
  whose status was `verified (DATE)` and has evidence gets `- **Outcome:** verified` added to
  that evidence, so the derived status stays what it was; an entry verified with no evidence
  becomes `unverified`, and the report says so. Hand-kept `Status:` lines are removed, since
  statuses now come from evidence.
- **Costly recipes get the `ask-first` mark** with the reason: any scenario that starts an agent
  session, uses a paid API or cloud resources, runs far longer than the usual tests, loads a
  shared environment, or has effects outside the repository. Free drives stay unmarked.
- **The project's customizations stay**: extra sections, its own wording, its own locations. A
  project whose verification lived at a non-default path may keep it there and set the two path
  lines at the top of the tool.
- **The old pieces go**: the feature-map directory, the reader-task list, the surface README and
  their repository checks are removed once their content is in recipes, and the tests that
  checked them are replaced by one that runs `verify check`.
- **The context file** gets the one verification bullet from the template; the
  verification-surface and feature-map bullets are removed.
- **The ask-first setting** is offered as its own choice, with `ask` as the default, and written
  to `harness.md`.
