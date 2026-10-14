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
- `--babysit <pr-url>` synthesizes a lifecycle-only Manifest from a pull request; `--autonomous` skips the approval wait and records decisions as `(auto)` assumptions.
- It reads earlier work on the repository before encoding.

## Scenarios

### new-manifest
Run: `scripts/drive-skill.sh define claude-plugins/manifest-dev/evals/define/d01-layer-cut/prompt.md`
Proves: the drive's home holds `.manifest-dev/manifests/manifest-<timestamp>.md` and the reply ends with `Manifest complete: <path>`; the three-layer plan comes back re-cut into slices. Every gate in the Manifest ends with `Judgment gate.` or `Deterministic gate.` and the ceiling invariant is present verbatim.
Check: read

### project-rule-over-default
Run: `scripts/drive-skill.sh define claude-plugins/manifest-dev/evals/define/d21-user-rule-over-default/prompt.md --scaffold claude-plugins/manifest-dev/evals/define/d21-user-rule-over-default`
Proves: the Manifest checks the fix only through `checks/`, keeps test files out, and records the overridden regression-test Default.
Check: read

### coding-defaults
Run: `scripts/drive-skill.sh define claude-plugins/manifest-dev/evals/define/d20-preparatory-slice/prompt.md --scaffold claude-plugins/manifest-dev/evals/define/d20-preparatory-slice`
Proves: the Manifest's guidance carries the CODING Defaults that apply — what could regress silently, no layer without a present case, expected values from stated behavior — and a behavior-preserving slice before the change.
Check: read

### feature-defaults
Run: `scripts/drive-skill.sh define verification/prompts/define-feature-defaults.md --scaffold claude-plugins/manifest-dev/evals/define/d20-preparatory-slice`
Proves: for a feature whose installs upgrade on different days, the Manifest keeps old and new versions working side by side on shared data.
Check: read

### bounded-growth
Run: `scripts/drive-skill.sh define verification/prompts/define-bounded-growth.md --scaffold claude-plugins/manifest-dev/evals/define/d20-preparatory-slice`
Proves: for data that grows for years, the Manifest carries *Bound what grows*: a gate keeps append and per-member query cost tolerable at a stated scale.
Check: read

### prompting-defaults
Run: `scripts/drive-skill.sh define verification/prompts/define-prompting-defaults.md`
Proves: for a prompt change needing an exact count, the Manifest holds the exact count with a check over real runs, not an instruction alone.
Check: read

### amend
Run: `scripts/drive-skill.sh define verification/prompts/define-amend.md`
Proves: only the named items change; IDs of the others are untouched (diff the file).
Check: read

## Gotchas

- Eval prompts ask for `./manifest.md` in the working directory, so a drive of an eval case finds the Manifest in the scratch project, not the home directory.
- The eval cases' `prompt.md` files open with the case's front matter; `scripts/drive-skill.sh` sends only the body below it.
- A plan handed over by layer (model, API, UI) must come back re-cut into slices; keeping the layers as a "user's call" is the defect `d01-layer-cut` exists to catch.
- The Manifest is written to the home directory, not the project: in a drive it is in the evidence's `home-manifest-dev.tar`.
- Attended, it waits for a yes after the digest; a headless drive needs `--autonomous` or a prompt that says to proceed.
- An old Manifest with a `verify` block is refused, not migrated.
- A yes approves the Manifest, not execution: it never runs `/do` itself.
- "It didn't stop for approval" is define only under `--autonomous` or when called by `auto`; a whole chain that never stopped is the auto entry.
- Earlier evidence for feature-defaults does not record which scaffold its drive used; the prompt's "this repo" is the shelfnote project, which `d20-preparatory-slice` scaffolds.
- Also checked by the define behavior suite, `claude-plugins/manifest-dev/evals/define/` cases `d01` to `d21` (tag `define`), statuses in `claude-plugins/manifest-dev/evals/define/README.md`; `tests/test_shared_blocks.py` and `tests/test_goal_contract_blocks.py` pin the blocks its handoff carries.
- Not yet driven: the bare slash command, the description phrases, auto, do's amendments, babysit-pr, figure-out's offer.
