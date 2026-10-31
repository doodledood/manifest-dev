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
- It changes the Manifest only through define, turns corrections into locks — a reaction to a disposable draft steers the work's direction and locks only what reaches past it — and lists the debt it leaves, builds or repairs the project's verification harness and the recipes the Manifest touches (found with `verify affected`), and arms a goal or prints a goal block so the run survives interruption.

## Scenarios

### execute
Run: `scripts/drive-skill.sh do verification/prompts/do-execute.md --max-turns 120`
Proves: the run ends in `/done` or `/escalate`; the log file exists at `~/.manifest-dev/logs/do-<name>-<hash>.md`. The completion report gives a basis per gate and lists the user's calls first.
Check: read

### no-log
Run: `scripts/drive-skill.sh do verification/prompts/do-no-log.md --max-turns 120`
Proves: no `do-*.md` log is written for that Manifest.
Check: read

### out-of-reach
Run: `scripts/drive-skill.sh do verification/prompts/do-out-of-reach.md --max-turns 120`
Proves: the start-up check cannot finish within 2 milliseconds while it stays a script run by `python3`, since starting the interpreter alone takes longer. The run builds `greet.py` and passes its gate, raises a blocker for the start-up check that names the best time reached, the limiter (interpreter start-up), the attempts made and the requirement change that would unblock it, and ends in `/escalate`; `manifest.md` still reads "under 2 milliseconds".
Check: read

### criterion-discovery
Run: `scripts/drive-skill.sh do verification/prompts/do-criterion-discovery.md --scaffold verification/fixtures/criterion-discovery --max-turns 120`
Proves: the subject reads `interchange.md` before its first edit choosing the export representation. The export retains the string identifiers `003` and `010`, retains the empty note on the first record, and omits the missing note on the second. Inspect the transcript's read/write order and the exported JSON, not a final claim of having consulted the standard.
Check: read

### evidence-resume
Run: `scripts/drive-skill.sh do verification/prompts/do-evidence-resume.md --scaffold verification/fixtures/evidence-resume --max-turns 120`
Proves: the run reads its existing log, invalidates the report judgment after the supplied criterion and uncommitted data changes, and writes `id` and `quantity` as tab-separated headers followed by `003` and `2`. It separately invalidates AC-1.4 on changed input despite that criterion remaining unchanged, updating `quantity.txt` to `2` plus newline. It retains the unaffected receipt judgment after checking applicability, runs the full deterministic receipt command, and records the assessed subject and findings for another continuation. The pending source edits remain visible in the working tree rather than disappearing behind the prior head SHA.
Check: read

### external-feedback
Run: `scripts/drive-skill.sh do verification/prompts/do-external-feedback.md --scaffold verification/fixtures/pr-feedback --max-turns 120`
Proves: new external evidence reopens the previously passing export judgment and repairs the omitted last line, so the supplied order totals 17. The caller reuses the supported private-note and dict-literal dispositions, assesses the new claims, and declines the false VAT claim, currency feature, and optional naming changes with reasons. Its source diff fixes the total without appeasement edits. Local outbound records handle the current thread IDs, leave the human thread open, and do not merge. Required approval and unapplied remote actions remain pending or blocked, never PASS from local disposition alone.
Check: read

### distinct-nits
Run: `scripts/drive-skill.sh do verification/prompts/do-distinct-nits.md --scaffold verification/fixtures/pr-nits --max-turns 120`
Proves: both advances assess their different optional suggestions, decline them with reasons, and preserve `order_export.py` without a code commit or push. The second advance retains the first one's journal across the new head. Each current thread receives its own appropriate outbound handling; the outstanding required approval stays pending. Inspect both saved diffs, outbound records, Git history, and the appended journal. The marker-only `Fixture: advance review wave` commit is injected setup, not an appeasement commit; any subject-made code commit is still a failure.
Check: read

### draft-reaction
Run: `scripts/drive-skill.sh do verification/prompts/do-draft-reaction.md --scaffold verification/fixtures/draft-reaction --max-turns 120`
Proves: three reactions to a draft land three ways, read from the files the run wrote rather than its account. `manifest.md` is amended to record direction B at lower density as the person's call in Known Assumptions, with AC-1.1 or a new gate building the dashboard to it, and a gate holding that the totals match `ledger.csv` to the cent. The tests the run adds include one that fails when a dashboard total differs from the ledger's sum for that category; no added test, lint or check concerns density, layout or where the numbers sit. No memory file gains a `## Taste` entry, and the completion report carries a drafted Taste entry for putting the numbers first in mock-ups, with the question whether it is standing or for this case only.
Check: read

## Gotchas

- It changes files, commits, and may push or open pull requests as its Manifest allows. Never drive it on this checkout.
- A plan approval is not a request to run; it says the Manifest is ready and stops.
- An external process still running is a wait, never success.
- Checked indirectly by the define suite's executor-facing cases under `claude-plugins/manifest-dev/evals/define/`; `tests/test_goal_contract_blocks.py` pins the goal block verbatim.
- The scaffold runs before the subject session. Expected outcomes stay in this recipe, which the subject does not receive.
- Seeded resumption checks consumption of recorded evidence, not the earlier run that produced it. PR snapshots check local judgment and action intent, not live GitHub transport, bot scheduling, or mutation success. Recording an outbound request does not change the supplied remote state.
- The convergence scenarios are unmeasured until their ask-first drives run; scaffold and property checks do not establish agent behavior.
