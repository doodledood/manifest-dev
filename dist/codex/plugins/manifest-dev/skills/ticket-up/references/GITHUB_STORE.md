# GitHub Issues venue

Renders the ticket convention onto GitHub Issues. Use whatever GitHub access the session has — `gh` CLI, the GitHub API, or GitHub MCP tools; the mapping is the contract, the client is incidental. Confirm the target repository before creating anything.

## Mapping

| Convention | GitHub realization |
|---|---|
| Store | The repository's issues, grouped under one **tracking issue** per effort |
| Front file | The tracking issue's body: destination, priority override, context pointers, and the standing automation settings when set (a `Paused:` line, a `Status page:` line). No ticket list — GitHub's own child list is the grouping, and it stays current with nobody editing it |
| Coordination record | One marked comment per outcome assignment on the tracking issue, following `../../orchestrate/references/OUTCOME.md` → *The coordination record*. Use its comment ID for direct reads and update in place. Remove ended assignments from the active context pointers; the ended comment and closed source issues remain the archive |
| Ticket | An issue; the full ticket anatomy is the issue body |
| Effort membership | The native **sub-issue** relation, with the effort's tracking issue as the parent |
| Effort | An `effort:<slug>` label, on every ticket and on its tracking issue — same slug the files venue would use for the directory name |
| Kind | Labels `shaped` / `question` on tickets; the tracking issue carries `effort` (create any that are absent) |
| Auto grant | An `auto` label on the ticket (create it when absent), plus one comment carrying `<!-- manifest-dev-auto-grant -->` that names the grantor — the person, or `orchestrate --autonomous` — and when. A decision to withhold a grant is recorded in the same comment, with its reason; a grant `orchestrate` asks a person for is recorded as a withhold naming that person as asked, written before it asks, and the person's answer edits that same comment. Where two such comments exist, `AUTOMATED_EXECUTION.md` → *The attempt record* says which decides. No label means ungranted. The label remains durable authority; runners do not pulse it to trigger retries. A person withdraws a grant by removing the label, and a person's decline removes it too; the comment stays, so `orchestrate` can see the ticket was already judged |
| Author's write access | The issue author's permission on the repository (`gh api repos/<owner>/<repo>/collaborators/<login>/permission`): `admin`, `maintain` or `write` passes. Triage cannot write, so it does not pass |
| Type | A `type:<slug>` label on the ticket, from the store's type vocabulary (create the label when absent). At most one per issue. A ticket carrying no type gets no such label, and a query selecting on type passes it over |
| Depends on | A `Depends on: #N` line in the body of the **blocked** issue, plus a native blocked-by relation where the repo has them. Not sub-issues — an issue has one parent, and membership holds it |
| Revisit when | A `Revisit when: <condition> — read <where>` line in the body of a deferred issue, next to its `Depends on:` line when it has one. No label: the condition is read at its source, never cached as issue state. A picker reads it there; selection never edits the line; an assigned change needs explicit authority |
| Claimed | Assignee; unassigned and open means takeable. A human assignee pauses unattended work. The configured automation assignee marks a run in progress, waiting to land, or interrupted; the run facts in the attempt record, not the assignee, say whether a run is live |
| Attempt record | One comment carrying `<!-- manifest-dev-run-ticket-attempt -->`, written by the automation identity and edited in place. Its author is the REST comment's `user`; its last editor is the GraphQL comment's `editor` (`gh api graphql`), empty when nobody edited it after its author. A comment holds about 65,536 characters; a Manifest that does not fit continues in a comment carrying `<!-- manifest-dev-run-ticket-manifest -->` |
| Completion record | One comment carrying `<!-- manifest-dev-run-ticket-completion -->`, edited in place |
| Landing | `gh pr merge <number> --match-head-commit <sha>` with the repository's merge method, so a head that moved is refused; then read the pull request back and confirm it is merged |
| Up-to-date branches or merge queue | The target branch's protection requires branches to be up to date (`required_status_checks.strict`), or a ruleset routes merges through a merge queue. Either closes the race between two orchestrators landing on one branch |
| Done / roll-off | After required work is merged or otherwise landed, close the issue with the landing reference in the completion record. Nothing to delete anywhere: a closed child stays in the tracking issue's list as progress, and `is:open` queries stop returning it |
| Escalation mark | An `escalated` label on the ticket (create it when absent). Unattended dispatch passes over a labelled issue entirely — the label, not an assignee, is what holds automation off once an attempt has handed the work to a person. It is state a person clears after recording the continuation context, or `orchestrate` clears on the person's explicit answer in its conversation; no run removes it on its own. Whoever clears it removes the `escalated` label and any automation assignee, which returns the issue to unattended eligibility |
| Escalated attempt | Add the handoff comment carrying `<!-- manifest-dev-run-ticket-escalated -->`, apply the `escalated` label, leave `auto` unchanged, and remove the automation assignee — never a person's — so the issue is takeable again and a picker ranks it with everything else. A later escalation updates that same comment rather than adding another. |
| Ticket context | Everything the issue carries beyond its body: its comments, including attempt and handoff records; linked pull requests; and its labels and assignee. A picker reads these as part of the Ticket rather than reading the body alone |
| Priority | Derived by the convention's rule, or the store's stated override — never stored as an order |
| Ready | Open, unassigned, every `Depends on:` issue closed, and any `Revisit when:` condition read as met at its source; an issue whose source cannot be read is named to the person, not passed over in silence. Unattended dispatch narrows that further: it also requires the absence of the `escalated` label, and either the `auto` label or an author with write access |
| Tidy pass | Re-groom: close stragglers, unassign stale claims, surface `escalated` issues whose blocker looks resolved rather than unlabelling them — clearing that label belongs to the continuation step that records what changed — refresh the tracking issue's destination and pointers |

The label earns its place next to the parent relation by answering a different question. Reading membership off the parent means already knowing which tracking issue to open; one open-issues query comes back with labels attached to every ticket, which names every effort in play from a cold start. The tracking issue carries both labels for the same reason they are two labels: `effort:<slug>` says which effort, `effort` says this is the front file rather than a ticket — so one query returns the group and can still tell its parts apart.

## Emitting

1. Create the ticket issues first, then the tracking issue, then attach each ticket to it as a sub-issue — the relations need real numbers.
2. Issue bodies are the same self-sufficient prose as the files venue — a GitHub reader gets no manifest-dev context either.
3. On the first run against a repo, show the operations about to be performed (issues, labels, tracking issue, sub-issue links) and get a confirm before creating — issues are outward-facing and noisy to undo.

Record the venue in `tickets/store-config.md`, naming GitHub and the repository, so `next-ticket`
and later runs read the same store without re-asking.

For unattended execution, also record the stable GitHub automation assignee — the account
unattended runs write as — and a human escalation recipient in the same config. They must be
distinguishable. `run-ticket` prefers a person named by the Ticket, then this project contact, then
the initiating human; it never invents a mention. Read `AUTOMATED_EXECUTION.md` for the records,
the identity rule and the landing procedure.
