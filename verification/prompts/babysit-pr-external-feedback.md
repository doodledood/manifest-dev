First run `python3 prepare-snapshots.py` to bind the replay to the scratch HEAD.
Use `pr-state.json` as the current PR API observation under this project's local replay protocol.
Run /manifest-dev-tools:babysit-pr https://github.com/example/review-fixture/pull/1
--manifest ./manifest.md --ci, using ./execution-log.md as the existing journal.
