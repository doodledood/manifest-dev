# ADR: Require explicit, non-free-handed skill invocation in verify.prompt templates, not bare "activate"

## Status
Accepted

## Context

A cache-staggering experiment (`tests/cache-experiment/run_arms.py`, postgres-provider-split manifest fixture `manifest-20260627-194010.md`, four arms × 5 repeats) captured verifier-session JSON transcripts that surfaced an instruction-following gap: `verify.prompt` templates telling a general-purpose verifier to "Activate the manifest-dev:X skill…" frequently don't trigger a literal `Skill` tool-use call. The verifier instead free-hands the check with its own `Bash`/`git` commands and reports findings directly.

**Excerpt A-1 — skill invoked, first substantive tool call** (`arm0/35697d565ed/repeat-0/312cf7d63c768be9/diagnostics/`, session `f49256fe-fbee-4117-a68f-ccc8d3ecd319`, criterion INV-G2):
```
--- assistant tool_use: Skill ---
{"args": "dimension=context-file-adherence, review both branch diffs against repo CLAUDE.md,
advisory dimension, PASS if no MEDIUM-or-higher findings", "skill": "manifest-dev:review-code"}
```
Verdict (`arm0/35697d565ed/repeat-0/312cf7d63c768be9/INV-G2/stdout.log`): `**Status**: PASS`.

**Excerpt A-2 — skill skipped, no `Skill` tool_use anywhere in the session** (`armB/35697d565ed/repeat-3/d198d6a20e41f8b2/`, session `6e6020969d0477d5`, criterion INV-G2 — manifest inlined, today's shipped `/do` behavior). Full tool-call sequence for the session: `Bash, Bash, Bash, Bash, [text], Bash, Bash, ReportFindings`. No `Skill` tool_use block occurs; the verifier goes straight to running its own `git diff`/`git show` commands and calls `ReportFindings` directly instead of loading `review-code`'s `context-file-adherence` rubric.

**Excerpt A-3 — the same skip, on a different repeat, producing the only FAIL** (`armB/35697d565ed/repeat-1/0797eb607e3b04c2/INV-G2/stdout.log`):
```
Reported 2 CONFIRMED MEDIUM-severity findings against the core branch's `test_settings.py`:
local (mid-function) imports instead of top-of-file imports, and `conf_vars` used as a context
manager for a fixed value instead of as a decorator. The provider branch diff showed no
CLAUDE.md adherence issues.
```
This is the only FAIL among 20 sampled `INV-G2` runs across all four arms; every other repeat — skill-invoked or not — on the same underlying branches returned PASS. Compliance rates measured across sampled sessions: `INV-G2` skill-invoked in 5/5 (arm0), 5/5 (armC), 2/5 (armA), 2/5 (armB); `AC-3.2` (in the source investigation's manifest, unrelated to this manifest's own AC numbering) skill-invoked in 4/5 (arm0), 5/5 (armC), 0/5 (armA), 0/5 (armB) — compliance drops specifically in the arms where the manifest is inlined (armA/armB, today's shipped behavior).

Four literal `verify.prompt:`-embedded template strings used the ambiguous "Activate the manifest-dev:X skill…" phrasing: the review-code pattern in `define/SKILL.md`'s yaml block, the check-pr example in `define/SKILL.md`'s prose, the review-code example in `define/tasks/CODING.md`'s prose, and the check-pr yaml block in `define/tasks/PR_LIFECYCLE.md`. These are the templates `/define` copy-pastes into real manifests, so the ambiguity ships into every manifest that uses them.

## Decision

Reword the four `verify.prompt`-embedded template strings from "Activate the manifest-dev:X skill…" to an explicit directive that forbids a free-handed substitute — e.g. *"Invoke the manifest-dev:review-code skill for real, with dimension=<dimension>; do not free-hand this review by reconstructing the rubric from memory instead of actually invoking the skill."* The forcing function is the "do not free-hand … instead of actually invoking" clause, not a specific tool name: these four strings are distributed, repo-agnostic template text (`sync-tools` copies them into the OpenCode, Codex, and Pi packages), and naming a Claude-Code-specific primitive like "the Skill tool" would bake a harness-bound primitive into portable prompt text — the same failure mode the universal-goal-setting-language ADR closed for `/goal`. Checked against `sync-tools`'s own conversion tables: Codex's operational-tool-name remap list (`codex-cli.md`) has no entry for "Skill" (unlike Bash/Read/Edit/etc., which do), and Pi's conversion doc (`pi-cli.md`) never substitutes a "Skill tool" phrase at all — so a literal "Skill tool" instruction would ship unconverted to those hosts. The nested-spawn-avoidance warning ("tell that agent to activate a skill — never to spawn another agent") and the PASS/FAIL/BLOCKED verifier contract are preserved unchanged in meaning. Descriptive prose elsewhere in these files that uses "activate a skill" to describe the mechanism itself (not a copy-pasteable template) is left as-is — only the literal template strings change.

## Alternatives Considered
- **Leave the wording as "activate"**: Rejected — the captured evidence shows this phrasing is followed inconsistently (0/5–2/5 compliance in the arms matching today's shipped inlined-manifest behavior) and the one skip that diverged in outcome produced the experiment's only FAIL, i.e. skipping the skill is not merely stylistic, it can flip a verdict.
- **Add a `verify.agent` field naming a specialized subagent instead of a skill**: Rejected — the codebase already documents (and this ADR's own evidence context confirms) that every verifier is a general-purpose subagent; introducing an agent field would require a broader schema change and duplicate what the skill mechanism already provides.
- **Rely on the verifier's own judgment to decide when a rubric is thorough enough without the skill**: Rejected — Excerpt A-3 shows the free-handed path *can* independently find real issues, but the instruction ambiguity is unpredictable across repeats (2/5 to 5/5), which is not a property a manifest author can rely on.
- **Name "the Skill tool" literally in the reworded instruction** (the first draft of this fix): Rejected — CLAUDE.md requires distributed skill files to stay repo-agnostic, and `sync-tools`'s Codex/Pi conversion tables have no rule to translate that phrase, so it would ship unconverted to hosts with no tool literally called "the Skill tool." The forcing function ("do not free-hand … instead of actually invoking the skill") achieves the same compliance goal without naming a harness-specific primitive.

## Consequences

### Positive
- `verify.prompt` templates now carry an unambiguous, tool-anchored instruction, closing the gap between "author intent: run the review-code rubric" and "verifier behavior: sometimes free-hands it instead."
- The four templates change without touching the underlying dimension/skill semantics, so no manifest schema or skill behavior changes are required.

### Negative
- Manifests authored before this fix, or hand-written outside the templates, still use the older "activate" phrasing and are not retroactively updated by this change.
- Explicit "do not free-hand" phrasing adds a few words to every templated `verify.prompt`, slightly lengthening the generated manifest text.

## Source
- Manifest: `manifest-20260704-163919.md`
- Related: 20260704-isolate-branch-specific-verifiers-via-disposable-worktrees
