# GitHub Issues venue

Renders the ticket convention onto GitHub Issues. Use whatever GitHub access the session has — `gh` CLI, the GitHub API, or GitHub MCP tools; the mapping is the contract, the client is incidental. Confirm the target repository before creating anything.

## Mapping

| Convention | GitHub realization |
|---|---|
| Store | The repository's issues, grouped under one **tracking issue** per effort |
| Front file | The tracking issue's body: destination, priority override, context pointers — plus its one piece of native mechanics, a list of the **open** tickets with their edges in priority order; a closed ticket's line is deleted at close, so the list never accumulates history |
| Ticket | An issue; the full ticket anatomy is the issue body |
| Kind | Labels `shaped` / `question` (create them if absent) |
| Depends on | A `Depends on: #N` line in the issue body; additionally sub-issue or native blocked-by relations where the repo has them — the body line is canonical, relations are convenience |
| Claimed | Assignee; unassigned and open means takeable |
| Done / roll-off | Close the issue with the outcome as a closing comment; delete its line from the tracking issue's open list |
| Priority | The tracking issue lists tickets in priority order (the convention's default rule, or the store's stated override) |
| Ready | Open, unassigned, and every `Depends on:` issue closed |
| Tidy pass | Re-groom the tracking issue: close stragglers, unassign stale claims, reorder |

## Emitting

1. Create the ticket issues first, then the tracking issue referencing them by number (edges need real numbers).
2. Issue bodies are the same self-sufficient prose as the files venue — a GitHub reader gets no manifest-dev context either.
3. On the first run against a repo, show the operations about to be performed (issues, labels, tracking issue) and get a confirm before creating — issues are outward-facing and noisy to undo.

Record the venue choice per **Custom store** persistence in SKILL.md (a `store-config.md` naming GitHub and the repo), so `next-ticket` and later runs read the same store without re-asking.
