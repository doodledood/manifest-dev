# ADR: Design keeps experience goals and conditional constraints, not a general craft manual

## Status
Accepted

## Area
Design skills

## Context

The design pair already required purpose-led visual ambition, task fit, and verification in the delivered medium. Its builder nevertheless carried a 3,269-word numbered procedure, with another 6,353 words across six references. Common visual work triggered whole catalogs of composition, motion, typography, and genre guidance. Progressive disclosure did not make that material selective when ordinary tasks loaded most of it.

Several counters have concrete grounds: a labeling tool separated the questions from the item being judged; an architectural memo left relationships in 2,500 words of prose without figures; functional correctness could satisfy the builder and reviewer without a compelling visual idea; browser checks were applied beyond what a browser could verify. Those observations justify retaining the corresponding outcomes. They do not establish that every prescribed field, style default, or research-derived recipe improves a capable model's output.

The desired result is an audience experience that is understandable, engaging, and natural to use. Minimalism, a particular visual style, and animation are not universal ends. Research about human perception can inform design without becoming a manual every generation must follow.

## Decision

Use an experience-led core with three conditional references: web access and interaction, representation and information fidelity, and continuity and delivery. Remove the general craft manual, genre taxonomy, and dated style catalog. Let art direction, information design, and interaction design name the disciplines; spend explicit instruction on the goal, constraints, and consequential failure counters.

The core retains a written task model before arrangement, but not a fixed five-field block, region-by-region accounting exercise, or numbered decision sequence. It requires explicit representation choices for important relationships, a coherent creative direction, a compact shared system, and a check for accidental drift. These are instructions, not claims that generated artifacts fulfilled them.

The references preserve the constraints most likely to be misapplied: accessibility levels, units, and exceptions; state, focus, and recovery behavior; faithful data encodings and equivalent information; commitment semantics; and properties that require the actual delivery host. The projected-talk versus standalone-reading distinction survives without fixed word budgets: speaker-supported pacing is not audience-operated page exploration, and an aspect ratio alone does not establish presentation delivery. Mixed-direction language and dynamic access checks survive without a typography or icon recipe catalog.

The core asks the composition or behavior to carry the central idea, while copy supplies precision, qualification, voice, and meaning the form cannot carry. Simplicity does not require minimalism, sparse text, or a large hero image. Inspection distinguishes what the form communicates from what still depends on explanation; disclosure alone is not visual encoding. These clarify the experience goal rather than add another design procedure. Apple-native work receives a conditional pointer to applicable current Human Interface Guidelines, not copied platform dimensions or an Apple style for every artifact.

The builder and reviewer share these boundaries. The reviewer judges the whole encounter and actual use, and must identify a consequence rather than convict against a removed stylistic default. Motion remains optional; when present, its sequence, repetition, and reduced alternative need inspection. Prototype weight keeps the task and creative direction, concentrates fidelity on the question, and uses the reader's reaction rather than a full shipping-verification cycle.

This is a reversible prompt-architecture choice, not an established design-quality improvement. In a pilot of the initial compact core, blind reviewers preferred the first original-skill output in all three briefs, including over a second original-skill output. That pilot does not evaluate the later wording clarifications. The final samples had no established MEDIUM-or-higher finding in the inspected scope, but lost on grouping or pacing. The small pilot cannot separate instruction effects from generation variation; it does not establish equivalence either. Two core clarifications and new loading pointers also changed after the intermediate, so that comparison is not a pure ablation of reference deletion.

One recurring implementation change is clear: all six original-package samples used named multi-step spacing scales; none of the six new-core samples did. The rendered reviews found no corresponding material system-drift defect, and maintenance was not tested. Keep the compact-system obligation without restoring an exclusive token-only procedure, while disclosing this weaker implementation discipline. Repeated visible inconsistency or higher maintenance cost would be grounds to restore a focused counter.

## Alternatives Considered

- **Shorten only the core:** lowers its load but leaves common tasks loading thousands of words of broadly applicable recipes. This was evaluated as an intermediate configuration.
- **Compress all six references in place:** retains familiar paths but keeps a general design manual as the organizing idea. Three distinct constraint branches provide a smaller discovery surface.
- **Remove every reference:** smallest prompt, but loses useful units, exceptions, fidelity constraints, and delivery distinctions that prevent consequential misapplication.
- **Restore the explicit spacing-token procedure:** would preserve an implementation habit that the new core lost. The pilot establishes that change, but not its maintenance cost or a material rendered consequence. Retain the outcome and expose the loss rather than treat syntax alone as a quality verdict.

## Consequences

### Positive

- The audience's experience is the organizing goal rather than the completion of a prescribed design procedure.
- Specialized instructions load for a narrower reason, and the reviewer cannot silently resurrect the retired catalogs.

### Negative

- A deleted reminder may have helped on an untested task, medium, or model. The pilot uses one model and HTML only.
- Small-sample visual judgments and browser checks do not establish audience comprehension, recall, conversion, or reliable causal effects of prompt edits.
- More judgment remains with the generating model; fewer prescribed fields make some procedural omissions less mechanically visible.

## Source

- Apple's [Design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles), especially Simplicity, supports keeping useful detail rather than treating minimalism as the goal. [The 2017 design-principles session](https://developer.apple.com/videos/play/wwdc2017/802/) illustrates grouping, mapping, and the trade-offs of visibility. These are sources for Apple's recommendations, not independent proof of universal usability or prompt effectiveness.
- [Current Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) supply task-specific Apple-platform detail. The design skill points to applicable articles rather than carrying a copy of the source corpus.
- Amends 20260901-design-skill-pair-distills-research-eval-deferred: retains the pair and shared constraints; replaces the general research-derived reference library. General effectiveness remains unestablished.
- Amends 20260901-design-derives-structure-from-a-written-task-model: preserves written task context and co-visibility; replaces fixed fields and region-by-region trace mechanics.
- Amends 20260902-design-chooses-an-encoding-per-claim-figures-are-information-not-decoration: preserves explicit representation choice and fidelity; retires the fixed encoding line and SVG tutorial.
- Amends 20260901-deliberation-renders-run-the-design-skill-at-prototype-weight: replaces numbered decision references with the compact task/direction/fidelity boundary.
- Amends 20260905-design-defaults-to-purpose-led-visual-ambition: retains the goal across genres within the experience-led structure.
- Amends 20260905-design-obligations-follow-the-medium-and-task: retains applicability and actual-medium verification in the smaller library.
- Related: 20260817-prompt-lines-earn-their-place-by-provenance.
