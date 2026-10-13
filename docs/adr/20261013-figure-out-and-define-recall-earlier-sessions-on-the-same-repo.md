# ADR: figure-out and define recall earlier sessions on the same repository and topic

## Status
Accepted

## Area
define / figure-out

## Decided by
The user

## Context
Each skill reads back only its own file. figure-out reads a log when it resumes that same log; define reads a Manifest when it is given that Manifest's path to amend; do reopens the log keyed to its own Manifest. Nothing looks across sessions, so a new session on a related topic starts from nothing while earlier investigations — their evidence, rulings, dead ends, and out-of-scope calls — sit unread beside it. On one machine the workflow's home held over 300 logs and nearly 200 Manifests. An investigation into this design proposed, as a new idea, a tool that an earlier session on the same repository had already tested. Logs also did not record which repository they were about.

## Decision
- figure-out recalls once an investigation concerns work in the active repository: a bug, change, design, or decision. define recalls when it writes a new Manifest. Each scans the workflow's logs and Manifests for sessions on the same repository whose topic overlaps.
- Recall is proportional. A general or quick question that the repository's history cannot bear on loads nothing. The scan matches each log's first lines, which name its topic and repository, before reading any file whole. It lists recent pull requests in one query and reads only their "Debt left" sections. How much it reads scales with what missing an earlier ruling would cost.
- It reads only the leading conclusion, the rulings, and the out-of-scope calls of the logs it opens, not whole logs.
- It carries what it finds as dated leads from an earlier session, to check before relying on them, under the same rule that already makes verified status decay. A recalled claim never counts as verified evidence by itself.
- A ruling found there that never became a decision record or a Taste entry is offered for capture.
- Each log opens with a title naming its topic and a line naming the repository it is about, so recall matches by repository and nothing carries from one repository's sessions into another's.
- Local logs are a personal cache: a cloud runner or a teammate never sees them. Recall therefore also reads what any runner can reach — open debt tickets and the "Debt left" sections of recent pull requests on the change's paths. Anything that must reach every runner lives in the repository or on the forge: decisions in records, corrections as locks, proof in the verification surface, debt in pull requests and tickets. A ruling found only in a local log is offered for capture as a record for that reason.
- do does not recall: its Manifest already carries the context. auto receives recall through figure-out and define.

## Alternatives Considered
- **No recall**: each session repeats or contradicts work that is already on disk.
- **Recall at the start of every figure-out investigation**: figure-out also serves general and small questions, where recall slows the session and spends tokens on history that cannot bear on the answer.
- **Recall in every skill, including do**: do's Manifest already holds what it needs, so the cost buys nothing there.
- **Read whole logs**: costs too many tokens and pulls in detail that has gone stale.
- **Treat recalled claims as facts**: an earlier session can be wrong or superseded; in the motivating case, two logs on the same day disagreed about the same tool.

## Consequences

### Positive
- A session working on the repository starts from what earlier sessions learned and ruled.
- Rulings that were never recorded get a second chance to become records.

### Negative
- A session that changes the repository spends tokens on the scan; one that does not spends none.
- A topic match can be wrong, and a recalled lead can be stale; the label and the repository match limit both.
- A session that looked unrelated can miss an earlier ruling that would have applied.

## Enforced by
partly — eval cases `43-recalls-earlier-work` and `46-general-question-skips-recall` measure it once run; how deep a recall should go for the stakes stays judgment.

## Source
- Session: figure-out investigation of steering agents toward maintainable first versions.
- Related: 20260611-figure-out-evidence-ledger-and-independent-rederivation
- Related: 20261013-new-capabilities-live-inside-the-four-workflow-entry-points
