---
kind: skill
covers: claude-plugins/manifest-dev/skills/do
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# do

Executes a Manifest with full autonomy until every Acceptance Criterion and Global Invariant holds on fresh evidence, then reports what changed and the basis for each gate.

## How a user reaches it

- `/do <manifest-path> [--no-log]`.
- Phrases its description matches: "execute the manifest", "run the plan", "implement it".
- `auto` after define; `babysit-pr` after its Manifest; `run-ticket` through `auto`.
- It changes the Manifest only through define, turns corrections into locks and lists the debt it leaves, builds or repairs the project's verification harness and the recipes the Manifest touches (found with `verify affected`, a crossed time line paid down or frozen under a debt Ticket), and arms a goal or prints a goal block so the run survives interruption.

## Scenarios

### execute
Run: `scripts/drive-skill.sh do verification/prompts/do-execute.md --max-turns 120`
Proves: the run ends in `/done` or `/escalate`; the log file exists at `~/.manifest-dev/logs/do-<name>-<hash>.md`. The completion report gives a basis per gate and lists the user's calls first.
Check: read
Workload: varies

### no-log
Run: `scripts/drive-skill.sh do verification/prompts/do-no-log.md --max-turns 120`
Proves: no `do-*.md` log is written for that Manifest.
Check: read
Workload: varies

## Gotchas

- It changes files, commits, and may push or open pull requests as its Manifest allows. Never drive it on this checkout.
- A plan approval is not a request to run; it says the Manifest is ready and stops.
- An external process still running is a wait, never success.
- Checked indirectly by the define suite's executor-facing cases under `claude-plugins/manifest-dev/evals/define/`; `tests/test_goal_contract_blocks.py` pins the goal block verbatim.
