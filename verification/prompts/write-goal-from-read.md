/manifest-dev-tools:write-goal turn the read we just reached into a goal i can paste into the goal field:

**Read: add a `--json` flag to `notes list`, printing the same notes as a JSON array.** Confidence: high.

What it will be: `notes list --json` prints a JSON array to stdout, one object per note with exactly the keys `id`, `title`, `created`, in that order, `created` as an ISO 8601 UTC timestamp. Without the flag, the output stays byte-for-byte what it is today. An empty notebook prints `[]`.

How it will be checked: `pytest tests/test_list_json.py` passes, with tests that run `notes list --json` on the fixture notebook in `tests/fixtures/three-notes/` and parse the output, plus one that compares the plain `notes list` output to `tests/fixtures/three-notes/expected.txt`. `make test` exits 0. The work stops at a ready pull request; nothing is merged or released.

Ruled out: a `--format yaml|json|csv` option. Only JSON has a user who asked for it, and a format switch is a second design to maintain.

Evidence: `notes/cli.py:41` builds the plain listing from `store.all()`; the issue asking for this names a script that pipes the list into `jq`.

Rival considered: printing JSON Lines instead of one array. Set aside because `jq` handles an array directly and the issue's script expects one.

Would overturn it: a second consumer that needs streaming output for very large notebooks.

Offer (not taken): add a `--pretty` flag for indented JSON in the same change.
