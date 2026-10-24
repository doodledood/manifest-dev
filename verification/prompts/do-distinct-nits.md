First run `python3 prepare-snapshots.py` to bind the replay to the scratch HEAD.
Run two one-shot advances of /manifest-dev:do ./manifest.md using the local replay protocol,
no-wait execution, and ./execution-log.md as the existing journal.

For the first advance, use `pr-nits-1.json` as the current PR API observation. Save its outbound
actions and working-tree diff to `advance-1-actions.jsonl` and `advance-1.diff`.
Then run `python3 prepare-snapshots.py --next-nits` to inject the fixture-owned push and its
new PR observation. For the second advance, use `pr-nits-2.json`. Retain the code and journal from the first advance.
Save its outbound actions and working-tree diff to `advance-2-actions.jsonl` and `advance-2.diff`.
