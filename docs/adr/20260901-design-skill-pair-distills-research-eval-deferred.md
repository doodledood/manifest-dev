# ADR: Design ships as a doer/evaluator skill pair distilling external research; effectiveness eval deferred

## Status
Accepted — extended by 20260902-design-chooses-an-encoding-per-claim-figures-are-information-not-decoration: the distillation boundary in choice 3 now also covers material drawn from host-shipped skills, carried as rules without provenance or dependency on the host; a new `references/figures.md` joins the shared standards home. Placement, the pair, and the deferred eval all stand.

## Area
Design skills

## Context

AI-generated visual artifacts — pages, dashboards, decks, documents — come out subpar by default, and the failures are structural: distinctiveness gets spent on surface styling while functional UX (empty/error/loading states, recovery, affordances) collapses; style instructions without verification don't hold across a build; static aesthetic ban-lists just rotate the monoculture. A substantial research effort (maintained outside this repo, in the owner's knowledge base) distilled what reliably works into register tables, a ranked floor inventory, per-domain craft checklists, and verification procedures. Nothing in manifest-dev used it: `/define`'s UI task file carried two thin gates and no doer skill existed. The owner ruled that the skill gets built here, in the main plugin.

## Decision

Four coupled choices:

1. **Placement: the main plugin.** `design` and `review-design` live in `claude-plugins/manifest-dev/skills/`, beside the workflow skills that activate them, not in a separate tools plugin. The `/define` UI task file names `review-design` as its evaluating skill; same-plugin placement is what makes that activation a plain reference with no fallback table.

2. **A doer/evaluator pair, not one skill.** `design` builds and restyles; `review-design` evaluates, in a fresh context, on rendered evidence or returns BLOCKED. The split mirrors the existing writing skills: an author re-reading its own build re-reads its intentions, so the gate's value depends on the evaluator not being the builder. The shared standards live once, under `design/references/`, and `review-design` loads them by relative path — the two cannot drift apart.

3. **Distillation boundary.** The shipped files carry the research's operative content — rules as actions with their concrete numbers — and none of its provenance: no citations, study names, evidence grades, or links back to the source corpus; no manifest-dev maintainer vocabulary. Dated calibration content (currently-overused looks) ships visibly dated so a future refresh can find and replace it. The boundary exists because shipped skills stand alone in other people's repos, and because provenance prose is weight the running session pays for without acting on.

4. **Effectiveness eval deferred; effectiveness is a hypothesis.** The research specifies a blind pairwise evaluation (generate with and without the skill across briefs, judge blind with a cross-family model) as the acceptance test for whether the skill actually improves output. That harness is not built here. Until it runs, "this skill produces better design than no skill" is explicitly a hypothesis, not a measured result — the skill ships on the strength of the research it distills, and the blind pairwise eval is the outstanding acceptance bar. Standing risk accepted: the skill could underperform vanilla generation on some genres and this ships anyway; the eval is what would detect that.

## Alternatives Considered

- **A separate tools plugin**: keeps the main plugin lean — not chosen because the gate wiring is the point: `/define`'s task file activates `review-design`, and cross-plugin activation would need fallback criteria for installs that lack the second plugin.
- **One combined skill with a review mode**: fewer files — not chosen because the evaluator must run fresh-context against the builder's output, and a single skill invites the builder to self-grade; the pair makes the separation structural.
- **Shipping the research corpus wholesale as references**: maximal fidelity — not chosen because the corpus carries provenance, evidence grading, and repo-external links that shipped skills must not depend on, and its bulk would be paid by every session that loads a reference.
- **Blocking release on the pairwise eval**: honest gating — not chosen because the harness (hundreds of generations, cross-family judging) exceeds this change's appetite; deferral with effectiveness named as hypothesis keeps the claim honest at lower cost.

## Consequences

### Positive
- Any artifact built under a manifest with UI scope gets a register decision, a token system, floor checks, and rendered-evidence verification by default.
- One standards home: evaluator and builder read the same files, so a rule sharpened once holds in both.
- The dated calibration section makes cliché-rotation a maintenance task with a findable surface instead of a silent decay.

### Negative
- The skill's effectiveness is unmeasured until the deferred eval runs; regressions against vanilla generation would go undetected meanwhile.
- The calibration file rots on a months scale and needs refreshing by observation.
- `review-design`'s relative-path load (`../design/references/`) assumes whole-plugin installs; single-skill installs fall back to search-by-name and degrade to judgment without the standards when that fails.

## Source
- Session: autonomous figure-out → define → do run, 2026-09-01, from the owner's ruling to build the skill here.
- Related: 20260703-progressive-disclosure-triggers-live-in-loading-layer (the references' loading-table structure follows it).
