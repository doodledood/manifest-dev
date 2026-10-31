---
kind: skill
covers: claude-plugins/manifest-dev/skills/define
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# define

Turns shared understanding into a Manifest — Problem, Appetite, Deliverables with Acceptance Criteria, Global Invariants, assumptions — written to the user's home directory, ready for `/do`.

## How a user reaches it

- `/define [task] [<manifest-path>] [--babysit <pr-url>]`.
- Phrases its description matches: "plan", "spec out", "make a manifest", "break down a task".
- `auto` (with `--autonomous`); `do` to amend; `babysit-pr` with `--babysit`; figure-out's offer at the end of a read.
- `--babysit <pr-url>` synthesizes a lifecycle-only Manifest from a pull request — the `check-pr` gate and the gate that the pull request shows the change working; `--autonomous` skips the approval wait and records decisions as `(auto)` assumptions.
- It reads earlier work on the repository before encoding.
- A disposable draft made only to get a person's reaction loads no task file; its Deliverable owes only that the draft reaches that person.
- Coding gates do not prescribe when the executor runs its advisory review. PR defaults permit reasoned declines of correct but optional bot suggestions; the independent proof gate remains.

## Scenarios

### new-manifest
Run: `scripts/drive-skill.sh define claude-plugins/manifest-dev/evals/define/d01-layer-cut/prompt.md`
Proves: the drive's summary lists `manifest.md` among the files written in the scratch project, since the prompt asks for `./manifest.md`, and the reply hands it over with `Manifest complete: <path>`; the three-layer plan comes back re-cut into slices. Every gate in the Manifest ends with `Judgment gate.` or `Deterministic gate.` and the ceiling invariant is present verbatim.
Check: read

### project-rule-over-default
Run: `scripts/drive-skill.sh define claude-plugins/manifest-dev/evals/define/d21-user-rule-over-default/prompt.md --scaffold claude-plugins/manifest-dev/evals/define/d21-user-rule-over-default`
Proves: the Manifest checks the fix only through `checks/`, keeps test files out, and records the overridden regression-test Default.
Check: read

### coding-defaults
Run: `scripts/drive-skill.sh define claude-plugins/manifest-dev/evals/define/d20-preparatory-slice/prompt.md --scaffold claude-plugins/manifest-dev/evals/define/d20-preparatory-slice`
Proves: the Manifest's guidance carries the CODING Defaults that apply — what could regress silently, no layer without a present case, expected values from stated behavior — and a behavior-preserving slice before the change.
Check: read

The coding sketch Default also weighs keeping plausible changes local against added
complexity. This drive does not grade that encoding; figure-out's revised
`40-shape-before-build` case grades the design distinction and remains unmeasured.

### feature-defaults
Run: `scripts/drive-skill.sh define verification/prompts/define-feature-defaults.md --scaffold claude-plugins/manifest-dev/evals/45-current-setup-offers-nothing`
Proves: for a feature whose installs upgrade on different days, the Manifest keeps old and new versions working side by side on shared data.
Check: read

### bounded-growth
Run: `scripts/drive-skill.sh define verification/prompts/define-bounded-growth.md --scaffold claude-plugins/manifest-dev/evals/45-current-setup-offers-nothing`
Proves: for data that grows for years, the Manifest carries FEATURE's *Bounded growth* gate: a gate keeps append and per-member query cost tolerable at a stated or assumed scale.
Check: read

### prompting-defaults
Run: `scripts/drive-skill.sh define verification/prompts/define-prompting-defaults.md`
Proves: for a prompt change needing an exact count, the Manifest holds the exact count with a check over real runs, not an instruction alone.
Check: read

### research-delegation
Run: `scripts/drive-skill.sh define verification/prompts/define-research-delegation.md --scaffold verification/fixtures/research-delegation`
Proves: the Manifest allows direct source inspection by the coordinator and makes delegation conditional on the inquiry. Its guidance keeps the incident, mapping, and API evidence available for joint reasoning, while allowing the archive-format question, substantial reading, or independent checks to use another context when useful. It requires neither a context per source type nor a separate parallel-verification phase. Research-quality gates remain applicable, including source credibility, traceability, contradictory evidence, and honest gaps; the synthetic API snapshot cannot become a real citation. The transcript shows define loading both the research base and its web overlay.
Check: read

### fresh-review
Run: `scripts/drive-skill.sh define claude-plugins/manifest-dev/evals/define/d25-vague-target/prompt.md`
Proves: before the reply's digest, the session hands a fresh context `references/REVIEW.md` with the Manifest and the session record, and settles its findings in one pass — each fixed in the Manifest or named with its reason as rejected; the review reports as a finding any gate that no plausible wrong result fails, naming the wrong result it lets through; the digest lists every number a gate binds; the Manifest's speed gate binds a floor such as faster than the measured baseline, and any frame rate appears only as an advisory aim even when recorded as an assumption.
Check: read

### hole-search
Run: `scripts/drive-skill.sh define claude-plugins/manifest-dev/evals/define/d26-holes-that-pass-every-gate/prompt.md`
Proves: before the reply's digest, a fresh context searched the Manifest by judgment for holes — wrong results that pass every gate at once — and reported at least one as a concrete scenario with the gates that still pass it. It built no model from scratch: the read names a design model, but none is in hand to extend and no one asked for one, and rebuilding the model the read only describes counts as building one from scratch. Each hole it reported is closed in `manifest.md` by a gate or a design decision; a hole whose fix would change the Intent or the scope is named there as still open instead. Each ambiguity it reported is settled by one reading written into the gate, or named with its reason as rejected. The reply does not present the search as proof that the Manifest is sound.
Check: read

### appetite-ignores-agent-effort
Run: `scripts/drive-skill.sh define claude-plugins/manifest-dev/evals/define/d28-appetite-ignores-agent-effort/prompt.md`
Proves: `manifest.md` moves all 23 processor calls onto one retry path that always sends an idempotency key, rather than keying only the three that double-charged, and neither its Appetite nor any gate or assumption bounds the change by engineer time, sprints or a team's effort.
Check: read

### amend
Run: `scripts/drive-skill.sh define verification/prompts/define-amend.md`
Proves: only the named items change; IDs of the others are untouched and none is reused (diff the file). Before the handoff, a fresh context reviewed the amendment, or the reply says the review was self-graded.
Check: read

### current-state-amend
Run: `scripts/drive-skill.sh define verification/prompts/define-current-state-amend.md`
Proves: the amended `manifest.md` reads as current state. It carries no date that records when something was decided or changed, and no note of who decided what outside Known Assumptions — the notes in Intent, the Approach, the touched AC-1.2 and the untouched INV-G2 included. The plain-text-only rule, ASM-1's "plain text only" included, is gone from every section, with no text saying it changed, and ASM-1 is replaced rather than joined by a second entry; the plain-text alternative part may remain. The weekly cadence and staying on the relay are recorded as undated `User's call:` Known Assumptions. Reactions are covered by AC-1.1 rewritten to state the class (every kind of item the activity feed shows), with no gate whose region is reactions alone. Every untouched gate keeps its ID, and no reference names an ID that no longer exists. Intent, the Approach and the Deliverable describe the HTML digest. No Known Assumption only records how the amendment's review findings were handled, and the reply lists any finding it did not apply as an open item. Before the handoff, a fresh context reviewed the amendment, or the reply says the review was self-graded.
Check: read

### draft-gets-no-task-file-gate
Run: `scripts/drive-skill.sh define verification/prompts/define-draft-request.md`
Proves: for a request whose only deliverable is a throwaway HTML prototype to react to, the Manifest carries no `review-design`, `review-code` or other task-file gate on the draft; its Deliverable owes only that the draft, kept outside the project's files, reaches the person with the question it poses.
Check: read

## Gotchas

- Eval prompts ask for `./manifest.md` in the working directory, so a drive of an eval case finds the Manifest in the scratch project, not the home directory.
- The eval cases' `prompt.md` files open with the case's front matter; `scripts/drive-skill.sh` sends only the body below it.
- A plan handed over by layer (model, API, UI) must come back re-cut into slices; keeping the layers as a "user's call" is the defect `d01-layer-cut` exists to catch.
- The Manifest is written to the home directory, not the project: in a drive it is in the evidence's `home-manifest-dev.tar`.
- Attended, it waits for a yes after the digest; a headless drive needs `--autonomous` or a prompt that says to proceed.
- A headless drive offers no question-selection capability, so define asks in plain text, one ask per turn; batching its key calls through the capability, the default on a host that offers one, shows only in an interactive session.
- An old Manifest with a `verify` block is refused, not migrated.
- `hole-search`'s seen-to-fail check drives the same prompt from a worktree at the commit before define's review searched for holes; repeat it when changing the scenario. It drives `d26`'s prompt, which the define suite grades on the self-graded path.
- A yes approves the Manifest, not execution: it never runs `/do` itself.
- "It didn't stop for approval" is define only under `--autonomous` or when called by `auto`; a whole chain that never stopped is the auto entry.
- The scaffold in the feature-defaults and bounded-growth Run lines is inferred: their earlier drives did not record one. Their replies find no loan period setting, which `d20-preparatory-slice` has, and bounded-growth's cites the storage record's "a few hundred loans", which the set-up shelfnote scaffolds such as `45-current-setup-offers-nothing` carry. The next run of each settles it.
- Also checked by the define behavior suite, `claude-plugins/manifest-dev/evals/define/` (tag `define`), statuses in `claude-plugins/manifest-dev/evals/define/README.md`; `tests/test_shared_blocks.py` and `tests/test_goal_contract_blocks.py` pin the blocks its handoff carries.
- Not yet driven: the bare slash command, the description phrases, auto, do's amendments, babysit-pr, figure-out's offer.
- `research-delegation` is **unmeasured** until driven. Its free cold fixture check verifies source relationships and the isolated runner setup; it does not measure Manifest encoding, research quality, or the quality or performance difference between context choices. The scenario plans research and does not execute it.
