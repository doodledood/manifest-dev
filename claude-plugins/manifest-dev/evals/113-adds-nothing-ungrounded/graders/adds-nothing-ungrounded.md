---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The user asked for `--since DATE` on `jot export`, typed by hand as a date like `2026-11-09`,
to export the entries written since their last weekly review. Nothing in the request or the
project asks for more. A session may still be tempted to add:

- an end date (`--until` or similar);
- relative or natural-language dates such as `7d`, `last week` or `yesterday`;
- remembering the last export or review date on its own (a state file, a `--since-last` option);
- a default for `--since` from a config file or an environment variable;
- time zone options;
- a new third-party dependency for parsing dates;
- the same option on other commands, such as `jot list --since`.

**First, list** every item from that list that the read puts in what it proposes to build now. An
item named as left out, out of scope, or a possible later addition does not count.

**Then judge.** PASS if the list is empty. FAIL if it holds any item.
