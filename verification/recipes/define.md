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

## Scenarios

### new-manifest
Run: `scripts/drive-skill.sh define claude-plugins/manifest-dev/evals/define/d01-layer-cut/prompt.md`
Proves: the drive's summary lists `manifest.md` among the files written in the scratch project, since the prompt asks for `./manifest.md`, and the reply hands it over with `Manifest complete: <path>`; the three-layer plan comes back re-cut into slices. Every gate in the Manifest ends with `Judgment gate.` or `Deterministic gate.` and the ceiling invariant is present verbatim.
Check: read
Workload: varies

### project-rule-over-default
Run: `scripts/drive-skill.sh define claude-plugins/manifest-dev/evals/define/d21-user-rule-over-default/prompt.md --scaffold claude-plugins/manifest-dev/evals/define/d21-user-rule-over-default`
Proves: the Manifest checks the fix only through `checks/`, keeps test files out, and records the overridden regression-test Default.
Check: read
Workload: varies

### coding-defaults
Run: `scripts/drive-skill.sh define claude-plugins/manifest-dev/evals/define/d20-preparatory-slice/prompt.md --scaffold claude-plugins/manifest-dev/evals/define/d20-preparatory-slice`
Proves: the Manifest's guidance carries the CODING Defaults that apply — what could regress silently, no layer without a present case, expected values from stated behavior — and a behavior-preserving slice before the change.
Check: read
Workload: varies

The coding sketch Default also weighs keeping plausible changes local against added
complexity. This drive does not grade that encoding; figure-out's revised
`40-shape-before-build` case grades the design distinction and remains unmeasured.

### feature-defaults
Run: `scripts/drive-skill.sh define verification/prompts/define-feature-defaults.md --scaffold claude-plugins/manifest-dev/evals/45-current-setup-offers-nothing`
Proves: for a feature whose installs upgrade on different days, the Manifest keeps old and new versions working side by side on shared data.
Check: read
Workload: varies

### bounded-growth
Run: `scripts/drive-skill.sh define verification/prompts/define-bounded-growth.md --scaffold claude-plugins/manifest-dev/evals/45-current-setup-offers-nothing`
Proves: for data that grows for years, the Manifest carries FEATURE's *Bounded growth* gate: a gate keeps append and per-member query cost tolerable at a stated or assumed scale.
Check: read
Workload: varies

### prompting-defaults
Run: `scripts/drive-skill.sh define verification/prompts/define-prompting-defaults.md`
Proves: for a prompt change needing an exact count, the Manifest holds the exact count with a check over real runs, not an instruction alone.
Check: read
Workload: varies

### fresh-review
Run: `scripts/drive-skill.sh define claude-plugins/manifest-dev/evals/define/d25-vague-target/prompt.md`
Proves: before the reply's digest, the session hands a fresh context `references/REVIEW.md` with the Manifest and the session record, and settles its findings in one pass — each fixed in the Manifest or named with its reason as rejected; the review reports as a finding any gate that no plausible wrong result fails, naming the wrong result it lets through; the digest lists every number a gate binds; the Manifest's speed gate binds a floor such as faster than the measured baseline, and any frame rate appears only as an aim or a recorded assumption.
Check: read
Workload: varies

### hole-search
Run: `scripts/drive-skill.sh define claude-plugins/manifest-dev/evals/define/d26-holes-that-pass-every-gate/prompt.md`
Proves: before the reply's digest, a fresh context searched the Manifest by judgment for holes — wrong results that pass every gate at once — and reported at least one as a concrete scenario with the gates that still pass it. It built no model from scratch: the read names a design model, but none is in hand to extend and no one asked for one, and rebuilding the model the read only describes counts as building one from scratch. Each hole it reported is closed in `manifest.md` by a gate or a design decision; a hole whose fix would change the Intent or the scope is named there as still open instead. Each ambiguity it reported is settled by one reading written into the gate, or named with its reason as rejected. The reply does not present the search as proof that the Manifest is sound.
Check: read
Workload: varies

### amend
Run: `scripts/drive-skill.sh define verification/prompts/define-amend.md`
Proves: only the named items change; IDs of the others are untouched (diff the file).
Check: read
Workload: varies

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
