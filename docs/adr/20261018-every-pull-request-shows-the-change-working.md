# ADR: Every pull request shows the change working

## Status
Accepted; amended by 20261107-a-pull-request-shows-one-example-before-and-after: the description also shows one short example of the change before and after

## Area
PR lifecycle

## Decided by
The user

## Context
A run's pull request carries its decisions and its debt, and a reviewer judges the change from
its diff. Nothing shows the change working, and nothing keeps the description short: one recent
pull request in this repository changed 297 files, with a description few readers would finish.
A person deciding whether to land a held Ticket, or a reader checking an unattended one, needs
proof that the change works to trust it with minimal review — the bar the North Star's *Promise*
sets. Since version 2.99 (September 2026), the GitHub CLI can attach images and videos to a pull
request's description or comments with `--attach`, through the same upload the web editor uses.

## Decision
- Every Manifest whose work ships through a GitHub pull request carries a Quality Gate: the pull
  request shows the change working. It applies whether `run-ticket` runs the work or not, and it
  lives with define's pull-request gates.
- The top of the description reads in about a minute: what changed and why, how it was shown
  working, the decisions with the user's calls first, and the debt left. Long lists fold.
- The proof comes from runs of the checks the change touches, on a local or dev instance, or on a
  preview deploy where the project's CI already makes one — never production. A user path in a UI
  shows as screenshots, and motion as a short GIF or video.
- Images and videos are attached to the pull request with `gh pr create`, `gh pr edit` or
  `gh pr comment` and `--attach`, so GitHub stores them as it stores files dropped into the web
  editor. No branch, other repository or service is involved, and nothing needs cleaning up.
- Where the upload is unavailable — a `gh` older than 2.99, GitHub Enterprise Server, a token the
  upload refuses, or a network that blocks it — the media still reaches the pull request. It is
  committed to a branch named `pr-media/<pull request number>`, which shares no history with the
  code and is never merged, and each file is linked by that commit. The description says why the
  media is linked rather than attached, and the branch stays after the pull request closes, since
  the links depend on it.
- Only when neither way works is the proof command output alone, and the description names what
  was tried.

## Alternatives Considered
- **Only for `run-ticket`'s pull requests**: every pull request has a reader who needs the proof.
- **A Default instead of a gate**: whether a description shows the change working can be read
  from the pull request, so by the task-file rule it is a gate.
- **Release assets or an external host for images**: an external host adds a service and its
  credentials, and release assets fill the project's release list with screenshots.
- **Upload through a browser session**: relies on undocumented endpoints and session cookies.
- **Commit images on the change's own branch**: puts binaries into the target branch's history.
- **One orphan evidence branch as the first way**: works wherever git does, but every clone
  downloads every pull request's images, and the branch sits in the branch list for good — costs
  worth paying only where the upload is unavailable.
- **One evidence branch per pull request, deleted at close**: keeps clones clean, but nothing
  deletes it on its own, so every landing path and every evidence push carries a cleanup step,
  and deleting it breaks the images in the closed pull request. The fallback keeps the branch
  instead, so nothing has to clean it up.
- **One shared media branch for every pull request's fallback**: one branch in the list instead
  of many, but runs working in parallel would race to push to it.
- **Text alone where the upload is unavailable**: leaves a UI change's reviewer without the
  screenshots that show it, wherever the upload fails — and a hosted agent session's network can
  refuse it outright, as a proxy refusing GraphQL and any non-JSON request body does.
- **A hidden ref per pull request**: out of the branch list and out of clones, but a hosted agent
  session may push only branches; a test push from one was refused.

## Consequences

### Positive
- A reviewer sees the change work without running it.
- Where the upload works, the repository gains nothing to clean up: no branch and no stored files
  of its own.
- Where it does not, a UI change still shows its screenshots, from any session that can push a
  branch.
- The description stays readable however large the change.

### Negative
- The upload needs `gh` 2.99 or later, write access to the repository, and a token the upload
  accepts (the one `gh auth login` stores, or a classic personal access token).
- Each fallback leaves a `pr-media/<number>` branch for good, and a clone that fetches every branch
  downloads its images.
- Linked media is expected to render for readers with access to the repository; that has been seen
  only on a public repository.
- GitHub Enterprise Server does not offer the upload yet.
- Images do not render in email notifications or for viewers without access to the repository.
- A change with no runnable surface shows its proof as command output only.

## Enforced by
partly — `tests/test_pr_lifecycle_proof_gate.py` fails if the proof gate templated in
`claude-plugins/manifest-dev/skills/define/tasks/PR_LIFECYCLE.md` loses the one-minute top of the
description, the one example shown before and after, the never-production rule, images attached with `--attach`, the kept
`pr-media/<number>` branch where the upload is unavailable, or text alone only when neither works,
or if a rule dropping the `check-pr` lifecycle gate would drop it too; that define composes it into every Manifest shipping through a GitHub pull request, and
whether a description meets it, stay judgment.

## Source
- Session: figure-out on running unattended Ticket work with many agents at once (2026-10-18).
- Related: see also 20261018-the-harness-commits-no-evidence-and-time-lines-live-in-recipes,
  20261018-orchestrate-lands-and-run-ticket-stops-at-a-ready-pull-request
