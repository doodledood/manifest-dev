# ADR: Require explicit, non-free-handed skill invocation in verify.prompt templates, not bare "activate"

## Status
Accepted

## Context

An investigation into `/do`'s verifier compliance — sampling repeated verifier sessions against identical underlying branches — found that `verify.prompt` templates telling a general-purpose verifier to "Activate the manifest-dev:X skill…" produce inconsistent literal skill invocation. In a meaningful share of sampled sessions, the verifier never actually invoked the skill at all: instead of loading the named skill's rubric, it free-handed the check with its own ad hoc inspection commands and reported findings directly. Compliance was high when the review instructions stood alone, but dropped sharply once they were embedded inside a larger manifest — the realistic shape of how these templates actually ship — showing the ambiguity gets worse under the exact conditions real usage creates, not better.

The instruction-following gap was not merely cosmetic: across the sampled sessions, one skip of the skill produced a different verdict (a FAIL where every other sampled session — whether or not it invoked the skill — returned PASS) on identical underlying code, showing that skipping the skill is not a stylistic variation but can concretely change the outcome a manifest-driven run acts on.

Four literal `verify.prompt:`-embedded template strings used the ambiguous "Activate the manifest-dev:X skill…" phrasing: the review-code pattern in `define/SKILL.md`'s yaml block, the check-pr example in `define/SKILL.md`'s prose, the review-code example in `define/tasks/CODING.md`'s prose, and the check-pr yaml block in `define/tasks/PR_LIFECYCLE.md`. These are the templates `/define` copy-pastes into real manifests, so the ambiguity ships into every manifest that uses them.

## Decision

Reword the four `verify.prompt`-embedded template strings from "Activate the manifest-dev:X skill…" to an explicit directive that forbids a free-handed substitute — e.g. *"Invoke the manifest-dev:review-code skill for real, with dimension=<dimension>; do not free-hand this review by reconstructing the rubric from memory instead of actually invoking the skill."* The forcing function is the "do not free-hand … instead of actually invoking" clause, not a specific tool name: these four strings are distributed, repo-agnostic template text (`sync-tools` copies them into the OpenCode, Codex, and Pi packages), and naming a Claude-Code-specific primitive like "the Skill tool" would bake a harness-bound primitive into portable prompt text — the same failure mode the universal-goal-setting-language ADR closed for `/goal`. Checked against `sync-tools`'s own conversion tables: Codex's operational-tool-name remap list (`codex-cli.md`) has no entry for "Skill" (unlike Bash/Read/Edit/etc., which do), and Pi's conversion doc (`pi-cli.md`) never substitutes a "Skill tool" phrase at all — so a literal "Skill tool" instruction would ship unconverted to those hosts. The nested-spawn-avoidance warning ("tell that agent to activate a skill — never to spawn another agent") and the PASS/FAIL/BLOCKED verifier contract are preserved unchanged in meaning. Descriptive prose elsewhere in these files that uses "activate a skill" to describe the mechanism itself (not a copy-pasteable template) is left as-is — only the literal template strings change.

## Alternatives Considered
- **Leave the wording as "activate"**: Rejected — the sampled evidence shows this phrasing is followed inconsistently, especially once the review instructions are embedded inside a larger manifest, and the one sampled skip that diverged in outcome produced the investigation's only differing verdict, i.e. skipping the skill is not merely stylistic, it can flip a verdict.
- **Add a `verify.agent` field naming a specialized subagent instead of a skill**: Rejected — the codebase already documents (and this ADR's own evidence context confirms) that every verifier is a general-purpose subagent; introducing an agent field would require a broader schema change and duplicate what the skill mechanism already provides.
- **Rely on the verifier's own judgment to decide when a rubric is thorough enough without the skill**: Rejected — the sampled sessions show the free-handed path *can* independently find real issues, but whether the verifier invokes the skill is unpredictable across repeats of the same prompt, which is not a property a manifest author can rely on.
- **Name "the Skill tool" literally in the reworded instruction** (the first draft of this fix): Rejected — CLAUDE.md requires distributed skill files to stay repo-agnostic, and `sync-tools`'s Codex/Pi conversion tables have no rule to translate that phrase, so it would ship unconverted to hosts with no tool literally called "the Skill tool." The forcing function ("do not free-hand … instead of actually invoking the skill") achieves the same compliance goal without naming a harness-specific primitive.

## Consequences

### Positive
- `verify.prompt` templates now carry an unambiguous, tool-anchored instruction, closing the gap between "author intent: run the review-code rubric" and "verifier behavior: sometimes free-hands it instead."
- The four templates change without touching the underlying dimension/skill semantics, so no manifest schema or skill behavior changes are required.

### Negative
- Manifests authored before this fix, or hand-written outside the templates, still use the older "activate" phrasing and are not retroactively updated by this change.
- Explicit "do not free-hand" phrasing adds a few words to every templated `verify.prompt`, slightly lengthening the generated manifest text.

## Source
- Related: 20260704-isolate-branch-specific-verifiers-via-disposable-worktrees
