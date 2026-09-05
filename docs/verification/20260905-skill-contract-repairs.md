# Skill contract verification — 2026-09-05

The repair covers instruction conflicts found by screening all 33 shipped skill entrypoints
and following relevant references and callers. It does not certify every sentence in every
companion file. Generated distributions are checked against source.

## Executed Git fixtures

`tests/test_review_scope.py` executes the review skill's prescribed Git commands in disposable
repositories whose default branch is `trunk`. The five cases cover committed, staged,
unstaged, untracked, and staged-then-reverted changes. Each must expose the changed file;
tracked changes must expose changed content. The untracked case tests discovery; inspecting
that file's contents remains a reviewer obligation.

## Independent policy probes

Three independent reviewers applied the edited prompts to the following hypothetical inputs.
All 30 cases produced the expected action or verdict basis. These are instruction traces,
not production executions or comparative model trials. Cases without actual code or prose
establish a route and evidence requirement, not a finding against a real artifact.

| # | Input | Expected result |
|---|-------|-----------------|
| 1 | Investigation has two discoverable checks left | Continue investigating without a permission turn |
| 2 | User acknowledges a finding with “yes” | Resume the investigation |
| 3 | Evidence leaves a deciding product preference open | Ask for that preference with the concrete trade-off |
| 4 | Supported Read; no consequential work remains | State conclusion, evidence and overturn conditions; finish |
| 5 | Accepted prototype to judge animation pacing | Expose disposable playback with simulated effects |
| 6 | `/do --verification self` invokes design review | Keep the selected evaluator and record self provenance |
| 7 | Standalone design self-review; fresh context unavailable | Disclose self-review and preserve the evidence bar |
| 8 | Default branch is `trunk`; only staged work exists | Resolve the actual base and inspect the staged patch |
| 9 | Only an untracked code file exists | Discover it and inspect its contents |
| 10 | Active host differs from another installed host | Apply the active runtime's context resolution |
| 11 | A proposal explicitly describes unbuilt behavior | Permit intended behavior; distinguish it from shipped facts |
| 12 | Voice prose has grammar, a colon title and three real reasons | Do not manufacture a shape violation |
| 13 | Generic praise replaces the author's concrete criticism | Report the demonstrated loss; do not invent experience |
| 14 | Reachable crash; neighbors omit the same validation | Report the proven in-scope failure |
| 15 | Maintainability evidence requires tracing A → B → C | Read C while keeping findings within the changed scope |
| 16 | `init-context --no-mine`; existing project lacks glossary | Create the missing glossary before wiring; skip mining |
| 17 | Required work plus an unrelated feature beyond Appetite | Retain required work; fail the unrelated addition |
| 18 | `babysit-pr --ci`; only waiting remains | Report pending and release the runner without claiming completion |
| 19 | Ordinary babysit; the same CI state | Wait and reinspect under the selected cadence |
| 20 | Queued unattended run; predecessor adds escalation mark | Revalidate after serialization and stop dispatch |
| 21 | Human explicitly resumes that marked Ticket | Permit deliberate resumption under human authority |
| 22 | Clean first review loop pass; no GitHub review posted | Checkpoint the checked head and finish without an empty review |
| 23 | H1 fixes H0 findings; follow-up review is silent | Checkpoint H1 and finish without repeating the range |
| 24 | Unchanged head; Manifest gate still waits on CI | Refresh external evidence and re-evaluate the gate |
| 25 | Slack page ends at D and more messages remain | Return D as covered cursor; drain remaining pages |
| 26 | Team deliberation ends with an active poll | Stop the poll; report cleanup failure if cancellation fails |
| 27 | Native browser/artifact delivery; no OS launcher | Deliver the interactive canvas through the available capability |
| 28 | GitHub says `CLEAN`; human thread is addressed but open | Check actual requirements; keep author resolution as workflow policy |
| 29 | PR description denies a reproduced failure | Preserve the evidence-backed defect through consolidation |
| 30 | Portfolio ranking requires recently completed work | Read bounded closed history; select only open candidates |

The probes found three stale writing claims and a conflict between pending termination and
the ledger's generic non-terminal wording. Those were corrected and independently rechecked.

## Automated verification

Run from the repository root using its existing Python development environment:

```sh
ruff check claude-plugins/ tests/
black --check claude-plugins/ tests/
mypy
python -m pytest tests/ -q -p no:cacheprovider
git diff --check
```

The suite covers distribution equality, versions, frontmatter, reachable skill references,
shared continuation blocks, Ticket contracts, and the Git fixtures above. Optional render
checks require Playwright; unavailable render checks must remain reported as skipped.

Live Ticket adapters, Slack pagination, scheduler cancellation, PR tending and canvas delivery
were not exercised. No model comparison establishes the frequency of the original stalls or
the size of the improvement. The evidence supports the corrected contracts and tested command
behavior, not a general reliability claim.
