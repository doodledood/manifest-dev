# Files venue

Renders the ticket convention as Markdown files in the repository. A file store is read from one
working copy: a claim or record written in one clone, worktree or branch reaches nobody working in
another until it is merged.

## Mapping

| Convention | Files realization |
|---|---|
| Store | `tickets/`, one directory per effort: `tickets/<effort-slug>/` |
| Front file | `tickets/<effort-slug>/README.md`: destination, priority override, context pointers, and the standing automation settings when set: a person's `Paused:` line; an orchestrator's pause, one `Paused:` line per cause naming the orchestrator's ID and the cause by its cause key (`AUTOMATED_EXECUTION.md` → *Transitions*), and the repair Ticket once one is named; and a `Status page:` line. An orchestrator adds, edits or removes only lines an orchestrator wrote — any orchestrator's (*Transitions*, row *Lift a pause*) — one line at a time, never rewriting the file. Never a Ticket list or status summary |
| Coordination record | A separate marked section on the front file per outcome assignment, following `../../orchestrate/references/OUTCOME.md` → *The coordination record*. Update in place in the same working copy; archive an ended assignment under the effort's existing `done/` folder with a link from the front file. Git retains earlier versions |
| Ticket | `tickets/<effort-slug>/NN-<ticket-slug>.md`, opening with `Kind:`, `Status:`, `Depends on:` and `Claimed by:` lines, then the anatomy |
| Revisit when | A `Revisit when: <condition> — read <where>` line among the opening lines, after `Depends on:`, on a deferred Ticket only. A picker reads the condition at that source; selection never edits the line; an assigned change needs explicit authority |
| Auto grant | An `Auto: yes — granted by <grantor>` line, the grantor being the person or `orchestrate --autonomous`. No line means ungranted. A decision to withhold a grant is an `Auto withheld: <who> — <reason>` line, which grants nothing; a grant `orchestrate` asks a person for is `Auto withheld: <person> — asked`, written before it asks. An `Auto: yes` line on the target branch arrived through someone with write access, as *Author's write access* reads it, so it counts. So does a line `ticket-up` wrote in this working copy during this session for the grantor it names — `orchestrate --autonomous`, or a person granting in this conversation — and it counts there only. A line arriving from another branch or an unmerged contribution grants nothing. A file holds one `Auto` line: a person's answer replaces the asked line in place, and where an edit leaves two, the first in the file decides. A person withdraws a grant, or declines one, by replacing any `Auto: yes` line with `Auto withheld: <person> — <reason>`, so the decision stays on record |
| Type | A `Type: <value>` line when one fits; none otherwise |
| Claimed | The `Claimed by:` line. It records intent for the next reader of this working copy and reaches nobody in another |
| Attempt, completion, escalation and answer records | Sections at the end of the Ticket file, each opening with its marker line (`<!-- manifest-dev-run-ticket-attempt -->`, `<!-- manifest-dev-run-ticket-completion -->`, `<!-- manifest-dev-run-ticket-escalated -->`) and updated in place, and one section per answer record, opening with `<!-- manifest-dev-person-answer -->`, appended and never edited. Records are committed with the run's checkpoints, so they travel with its branch. Because the Ticket file is committed, the attempt section records the Manifest's path where define keeps it on this machine, never its content: the Manifest stays out of the repository as the attempt record requires, and a run resuming in another working copy, which has no file at that path, defines the work again |
| Author's write access | A Ticket file on the target branch arrived through someone with write access, so it passes. A Ticket this session just authored under an explicit trusted assignment to author and dispatch it also passes in this same working copy; record that authority on the Ticket. An arbitrary local file, other branch or unmerged contribution supplies no such provenance and is not eligible for unattended dispatch |
| Escalation mark | An `Escalated: yes` line among the opening lines, added with the escalation record. Whoever clears it (`AUTOMATED_EXECUTION.md` → *Transitions*, row *Clear the mark*) records the continuation context under the escalation record, deletes the `Escalated:` line, and empties the `Claimed by:` line when automation holds it |
| Done / roll-off | After the required work lands, record the outcome in the completion section, set `Status: done`, empty the `Claimed by:` line when automation holds it, and move the file to `tickets/<effort-slug>/done/` |
| Ticket context | The whole file, its record sections included |
| Parallel runs | None. Claims cannot separate runs across working copies, so `orchestrate` runs one Ticket at a time inside its own session |

Record the venue in `tickets/store-config.md`, naming files, so `next-ticket` and later runs read
the same store without re-asking.
