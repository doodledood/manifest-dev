# Files venue

Renders the ticket convention as Markdown files in the repository. A file store is read from one
working copy: a claim or record written in one clone, worktree or branch reaches nobody working in
another until it is merged.

## Mapping

| Convention | Files realization |
|---|---|
| Store | `tickets/`, one directory per effort: `tickets/<effort-slug>/` |
| Front file | `tickets/<effort-slug>/README.md`: destination, priority override, context pointers, and the standing automation settings when set (a `Paused:` line, a `Status page:` line). Never a Ticket list or status summary |
| Ticket | `tickets/<effort-slug>/NN-<ticket-slug>.md`, opening with `Kind:`, `Status:`, `Depends on:` and `Claimed by:` lines, then the anatomy |
| Revisit when | A `Revisit when: <condition> — read <where>` line among the opening lines, after `Depends on:`, on a deferred Ticket only. A picker reads the condition at that source; nobody but a person edits the line |
| Auto grant | An `Auto: yes — granted by <grantor>` line, the grantor being the person or `orchestrate --autonomous`. No line means ungranted. A decision to withhold a grant is an `Auto withheld: <who> — <reason>` line, which grants nothing; a grant `orchestrate` asks a person for is `Auto withheld: <person> — asked`, written before it asks. A file holds one `Auto` line: a person's answer replaces the asked line in place, and where an edit leaves two, the first in the file decides. A person withdraws a grant, or declines one, by replacing any `Auto: yes` line with `Auto withheld: <person> — <reason>`, so the decision stays on record |
| Type | A `Type: <value>` line when one fits; none otherwise |
| Claimed | The `Claimed by:` line. It records intent for the next reader of this working copy and reaches nobody in another |
| Attempt, completion and escalation records | Sections at the end of the Ticket file, each opening with its marker line (`<!-- manifest-dev-run-ticket-attempt -->`, `<!-- manifest-dev-run-ticket-completion -->`, `<!-- manifest-dev-run-ticket-escalated -->`) and updated in place. Records are committed with the run's checkpoints, so they travel with its branch. Because the Ticket file is committed, the attempt section records the Manifest's path where define keeps it on this machine, never its content: the Manifest stays out of the repository as the attempt record requires, and a run resuming in another working copy, which has no file at that path, defines the work again |
| Author's write access | A Ticket file on the target branch arrived through someone with write access, so it passes. One that exists only on another branch, or in an unmerged change, does not count as a Ticket yet |
| Escalation mark | An `Escalated: yes` line among the opening lines, added with the escalation record. Unattended dispatch passes over a Ticket file that carries it. After resolving the blocker, the person records the continuation context under the escalation record and deletes the `Escalated:` line, or answers in `orchestrate`'s conversation and it does both; whoever clears the mark also empties the `Claimed by:` line when automation holds it |
| Done / roll-off | After the required work lands, record the outcome in the completion section, set `Status: done`, and move the file to `tickets/<effort-slug>/done/` |
| Ticket context | The whole file, its record sections included |
| Parallel runs | None. Claims cannot separate runs across working copies, so `orchestrate` runs one Ticket at a time inside its own session |

Record the venue in `tickets/store-config.md`, naming files, so `next-ticket` and later runs read
the same store without re-asking.
