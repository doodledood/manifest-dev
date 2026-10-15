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
- Its task-file design probes raise what reviewers would flag — reuse, module depth, ownership, hidden contracts — before code; the user's and project's rules win over them.

## Scenarios

### current-setup
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/45-current-setup-offers-nothing/prompt.md --scaffold claude-plugins/manifest-dev/evals/45-current-setup-offers-nothing`
Proves: the reply says the setup is current, lists nothing the project lacks, does not suggest a setup run, moves to the topic with one ask, and names a log under the drive's `~/.manifest-dev/logs/`; the summary shows no files written.
Check: read
Workload: varies

### one-version-behind
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/53-update-offer-from-v4/prompt.md --scaffold claude-plugins/manifest-dev/evals/53-update-offer-from-v4`
Proves: the reply offers the update and names only what v5 adds — control commands for the overdue page in place of its fixed port, dropping `full-suite`'s run-time-only ask-first mark, the tool and the bullet — and nothing v1 to v4 gave.
Workload: varies

### from-v1
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/47-update-offer-from-previous-version/prompt.md --scaffold claude-plugins/manifest-dev/evals/47-update-offer-from-previous-version`
Proves: the reply offers the update and names only what v2 to v5 add, including the move to one harness.
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

## Gotchas

- The eval cases' `prompt.md` files open with the case's front matter; `scripts/drive-skill.sh` sends only the body below it.
- The reply ends at its one ask. A full read — conclusion, confidence, evidence, what would overturn it — needs the user's answers, which a one-prompt drive does not give; that path is the eval suite's.
- Without the skill named in the prompt it may not fire; the eval README measures how often.
- A user's agreement is not a go: it never edits code, so "it didn't implement" is the intended outcome, not a failure.
- Docs mode writes into the project (glossary, records, surfaces line); the drive's scratch project absorbs it.
- The context file's surfaces version is an HTML comment, and the host strips comments from the copy it loads into the session; a run that reports no version without reading the file from disk has hit that, not a missing line.
- `--team` needs Slack access; without it the team entry point is `unreachable`.
- Also checked by the figure-out behavior suite, `claude-plugins/manifest-dev/evals/` cases `01` to `51` (tags `figure-out`, `figure-out-plugin-only`), all `unmeasured` or stale per `claude-plugins/manifest-dev/evals/README.md`; `tests/test_eval_cases.py` keeps its case list in step.
- Not yet driven: the bare slash command, the description phrases, auto, define, figure-out-team.
