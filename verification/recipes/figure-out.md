---
kind: skill
covers: claude-plugins/manifest-dev/skills/figure-out
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# figure-out

Presses on a topic with the user until both understand it, and ends with a named read: a conclusion, its confidence, the evidence, and what would overturn it. It changes nothing in the project except the docs it keeps current.

## How a user reaches it

- `/figure-out [topic] [--no-docs] [--no-log] [--autonomous] [--team]`.
- Phrases its description matches: "think through a decision", "dig deeper", "investigate why something is happening".
- `auto` when shared understanding is missing; `define` when the transcript has none; `figure-out-team` with `--team`.
- On a project, docs mode keeps the glossary, decision-record offers, North Star updates, the setup offer and recipe drift markers current; `--no-docs` and `--no-log` turn the docs and the log off.
- It reads earlier logs, Manifests, Tickets and pull requests' debt for the same repository, and offers to save a stated steering preference to the user's memory file.
- It offers a disposable draft and calls design for its look.
- Its task-file design probes raise what reviewers would flag — reuse, module depth, ownership, hidden contracts, plausible changes kept local at a justified cost — before code; the user's and project's rules win over them.

## Scenarios

### current-setup
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/45-current-setup-offers-nothing/prompt.md --scaffold claude-plugins/manifest-dev/evals/45-current-setup-offers-nothing`
Proves: the reply says the setup is current, lists nothing the project lacks, does not suggest a setup run, moves to the topic with one ask, and names a log under `~/.manifest-dev/logs/`, which the drive's summary lists; the summary shows no files written.
Check: read
Workload: varies

### one-version-behind
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/53-update-offer-from-v8/prompt.md --scaffold claude-plugins/manifest-dev/evals/53-update-offer-from-v8`
Proves: the reply offers the update and names only what v9 adds — the *Purpose* opening with the end asked of the owner and its measures tested against it, on the owner's ruling rather than written by the run; the `Revisit when` signpost the strategy list shows; the outside-Purpose note in the ADR conventions; the check that rebuilds the index and the list — and nothing v1 to v8 gave.
Check: read
Workload: varies

### from-v1
Run: `scripts/drive-skill.sh figure-out verification/prompts/figure-out-from-v1.md --scaffold verification/scaffolds/project-at-v1`
Proves: the reply offers the update and names only what v2 to v9 add, including the move to one harness, the North Star reshape and its *Purpose* opening with the end.
Check: read
Workload: varies

### strategy-signpost
Run: `scripts/drive-skill.sh figure-out verification/prompts/figure-out-strategy-signpost.md --scaffold verification/scaffolds/deferred-ticket-store`
Proves: the reply names the newsletter strategy choice's signpost as met — `signals/website-visits.md` shows more than twenty outside visits a month — as a lead for the owner to reopen the choice, and the summary's files show no record, no North Star list and no `Revisit when` line changed.
Check: read
Workload: varies

### design-before-code
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/48-reuse-and-shallow-layer/prompt.md --scaffold claude-plugins/manifest-dev/evals/48-reuse-and-shallow-layer`
Proves: the read reuses the existing `overdue_loans` and `send_to_member` and questions the requested forwarding class, before any code.
Check: read
Workload: varies

### autonomous
Run: `scripts/drive-skill.sh figure-out verification/prompts/figure-out-autonomous.md --scaffold claude-plugins/manifest-dev/evals/45-current-setup-offers-nothing`
Proves: no question waits for an answer; each self-answered ask appears as a flagged assumption on the read.
Check: read
Workload: varies

### decision
Run: `scripts/drive-skill.sh figure-out verification/prompts/figure-out-decision.md`
Proves: the transcript shows the session reading `figure-out/tasks/DECISION.md`, and the read judges the three routes against the stated aim of getting people experimenting before money; names the craft-fair demo as the step that cannot be undone and weighs each route from that moment rather than from the decision date; weighs a mix of the routes that removes a route's worst case; and weighs "more glazes later" on every route rather than ranking one down for it.
Check: read
Workload: varies

### decision-counterparty
Run: `scripts/drive-skill.sh figure-out verification/prompts/figure-out-decision-counterparty.md`
Proves: the transcript shows the session reading `figure-out/tasks/DECISION.md`; the read treats the regional roaster's price as a choice that answers the user's bid, reasoned from the roaster's incentives and from whether its "beat any price" stance would hold at the user's numbers before any chance on it is relied on — a chance derived from that reasoning, or the user's 40% checked against it, passes, and the 40% taken as given with no look at the roaster's side fails; and the read states the chance of being undercut at which the choice between cutting and holding would flip, and compares the user's 40%, or the chance it derived in its place, with it.
Check: read
Workload: varies

### decision-close-call
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/63-decision-close-call-is-not-close/prompt.md`
Proves: the transcript shows the session reading `figure-out/tasks/DECISION.md`, and before it chooses, the read works out what a bad market year does under the loan covenant, or that the 3-in-10 estimate sits right at the chance where the choice flips; and it lets avoiding that outcome decide, rather than calling the options even and picking by habit or taste — the case's two graders, `does-not-call-it-close-and-stop` and `picks-a-rule-for-ruin`, applied to the final reply.
Check: read
Workload: varies

### decision-small-choice
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/64-decision-small-and-undoable/prompt.md`
Proves: the transcript shows the session reading `figure-out/tasks/DECISION.md`, and the final reply names one lamp with a short reason and stops — no map of futures, failure exercise, list of decision rules or weighted table, and no question in place of a pick — the case's grader `picks-without-ceremony` applied to the final reply.
Check: read
Workload: varies

## Gotchas

- The eval cases' `prompt.md` files open with the case's front matter; `scripts/drive-skill.sh` sends only the body below it.
- A drive's headless session offers no question-selection capability, so the reply asks in plain text, one ask per turn; asking through the capability, the default on a host that offers one, shows only in an interactive session.
- The reply ends at its one ask. A full read — conclusion, confidence, evidence, what would overturn it — needs the user's answers, which a one-prompt drive does not give; that path is the eval suite's. A prompt that passes `--autonomous`, as the decision cases' prompts do, is the exception: the session answers its own asks and ends at the read.
- Without the skill named in the prompt it may not fire; the eval README measures how often.
- A user's agreement is not a go: it never edits code, so "it didn't implement" is the intended outcome, not a failure.
- Docs mode writes into the project (glossary, records, surfaces line); the drive's scratch project absorbs it.
- The context file's surfaces version is an HTML comment, and the host strips comments from the copy it loads into the session; a run that reports no version without reading the file from disk has hit that, not a missing line.
- `--team` needs Slack access; without it the team entry point is `unreachable`.
- Also checked by the figure-out behavior suite, `claude-plugins/manifest-dev/evals/` (tags `figure-out`, `figure-out-plugin-only`), all `unmeasured` or stale per `claude-plugins/manifest-dev/evals/README.md`; `tests/test_eval_cases.py` keeps its case list in step.
- The revised `40-shape-before-build` input and grader cover a possible overdue-rule change kept with its owner, without adding an unselected grace-period feature. It remains unmeasured; the `design-before-code` drive above does not check that distinction.
- Not yet driven: the bare slash command, the description phrases, auto, define, figure-out-team.
