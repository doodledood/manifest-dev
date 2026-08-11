# GitHub Issues venue

Renders the ticket convention onto GitHub Issues. Use whatever GitHub access the session has — `gh` CLI, the GitHub API, or GitHub MCP tools; the mapping is the contract, the client is incidental. Confirm the target repository before creating anything.

## Mapping

| Convention | GitHub realization |
|---|---|
| Store | The repository's issues, grouped under one **tracking issue** per effort |
| Front file | The tracking issue's body: destination, priority override, context pointers. No ticket list — GitHub's own child list is the grouping, and it stays current with nobody editing it |
| Ticket | An issue; the full ticket anatomy is the issue body |
| Effort membership | The native **sub-issue** relation, with the effort's tracking issue as the parent |
| Effort | An `effort:<slug>` label, on every ticket and on its tracking issue — same slug the files venue would use for the directory name |
| Kind | Labels `shaped` / `question` on tickets; the tracking issue carries `effort` (create any that are absent) |
| Auto grant | An `auto` label on the ticket (create it when absent). No label means ungranted — automation leaves the issue alone entirely, which also covers issues that were never tickets |
| Type | A `type:<slug>` label on the ticket, from the store's type vocabulary (create the label when absent). At most one per issue. A ticket carrying no type gets no such label, and a query selecting on type passes it over |
| Depends on | A `Depends on: #N` line in the body of the **blocked** issue, plus a native blocked-by relation where the repo has them. Not sub-issues — an issue has one parent, and membership holds it |
| Claimed | Assignee; unassigned and open means takeable |
| Done / roll-off | Close the issue with the outcome as a closing comment. Nothing to delete anywhere: a closed child stays in the tracking issue's list as progress, and `is:open` queries stop returning it |
| Priority | Derived by the convention's rule, or the store's stated override — never stored as an order |
| Ready | Open, unassigned, and every `Depends on:` issue closed |
| Tidy pass | Re-groom: close stragglers, unassign stale claims, refresh the tracking issue's destination and pointers |

The label earns its place next to the parent relation by answering a different question. Reading membership off the parent means already knowing which tracking issue to open; one open-issues query comes back with labels attached to every ticket, which names every effort in play from a cold start. The tracking issue carries both labels for the same reason they are two labels: `effort:<slug>` says which effort, `effort` says this is the front file rather than a ticket — so one query returns the group and can still tell its parts apart.

## Emitting

1. Create the ticket issues first, then the tracking issue, then attach each ticket to it as a sub-issue — the relations need real numbers.
2. Issue bodies are the same self-sufficient prose as the files venue — a GitHub reader gets no manifest-dev context either.
3. On the first run against a repo, show the operations about to be performed (issues, labels, tracking issue, sub-issue links) and get a confirm before creating — issues are outward-facing and noisy to undo.

Record the venue in `tickets/store-config.md`, naming GitHub and the repository, so `next-ticket` and later runs read the same store without re-asking.
