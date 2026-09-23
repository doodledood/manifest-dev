# ADR: Design starts from the person and their moment; the example catalogs are retired

## Status
Accepted

## Area
Design skills

## Context

The `design` skill supplied art direction through five catalogs of curated example sites. Every run loaded the catalog for its genre and studied several examples before composing. The catalogs were drawn mostly from software products and developer-facing material, and they recorded one owner's preferences at one point in time.

Recent models produce strong visual work without guidance. The open question was whether the catalogs still improved results or mainly steered every artifact toward the catalogs' own look.

Four rounds of blind comparisons tested this. Each round generated the same briefs under different prompts in isolated contexts, with rounds 1 to 3 also including a no-skill baseline, and the owner ranked the results without knowing which prompt produced which page:

1. **Round 1:** bakery, charity, and developer-tool landing pages. The catalog skill and the no-skill baseline were roughly even. The catalog skill won only the developer tool, the one brief inside its catalog's domain, and took about twice the time and 1.4 times the tokens. A prompt asking the model to state audience, goal, feeling, and a "must not tip into" guardrail came last on all three briefs. The guardrails it chose were defensive (not kitsch, not pity, not hype), which likely made the pages plain. All nine pages shared one palette and type treatment across unrelated subjects.
2. **Round 2:** jazz club, payroll software, and hospice volunteering. A three-sentence prompt, the subject-first prompt, beat the no-skill baseline on all three. It asks the model to make the audience feel something, to find the visual idea in the subject's materials, rituals, and artifacts, and to take palette, type, and texture from the subject rather than a house style.
3. **Round 3:** a product-manager explainer, a live slide deck, and a support-ticket tool. The subject-first prompt won the explainer and the deck and came last on the tool, where it turned a screen used all day into a themed costume. A variant adding "sketch three ideas and build the least obvious" never won.
4. **Round 4:** a kitchen order display, a child's party invitation, and a library annual report. The subject-first prompt, extended with the person's moment (who is there, what they came to do, how long they stay), won two of three: the kitchen display, on practicality, and the invitation, without losing its delight. It lost the library annual report.

These results come from one judge and one model, with HTML artifacts only. Run-to-run noise was not measured, and the intensity wording adopted below was not tested separately. Within a single brief, prompts that differed still converged on the same visual concept; the wording mainly changed emphasis.

## Decision

Replace the skill with a short prompt built on one principle: the person and their moment decide which feeling the artifact should create and how strongly, and the subject supplies the material that creates it.

The prompt asks who is present, what they came to do, and how long they will stay. It asks for the feeling that moment wants, at the strength it wants, unless the request names a strength. It takes the visual idea, palette, type, and texture from the subject and the audience's world rather than from a house style. Explicit requirements and an existing design system outrank it, and refinement keeps what works and changes what the feedback names. Artifact type is not modelled separately; it stands in for the moment, and the moment is what the prompt names.

Delete the five catalogs. `review-design` keeps ownership of its standards and HTML checker as before, and still consults `design` for art direction beneath the brief and any established design system.

## Alternatives Considered

- **Keep the catalogs:** tied with the no-skill baseline at roughly twice the time, won only inside its own domain, and pulled unrelated subjects toward one look.
- **An audience, feeling, and guardrail statement:** came last on every brief it was tried on; asking the model to reason about feelings and their limits likely made it cautious.
- **The no-skill baseline:** strong, but lost to the subject-first prompt on five of six briefs across rounds 2 and 3.
- **Sketch three ideas and build the least obvious:** produced different metaphors from the same subject and never won.
- **A rule specific to work tools:** would fix the observed tool failure as a special case. The moment framing covers the same failure without encoding artifact types.

## Consequences

### Positive

- A design run loads two paragraphs instead of a catalog and several external sites, so it is faster and cheaper.
- Visual direction comes from each artifact's own subject and audience rather than one fixed profile, which reduces the shared look across unrelated work.
- Tools used for hours and one-time delight pieces are covered by the same principle.

### Negative

- The evidence is narrow: one judge, one model, HTML only, with noise unmeasured. The new prompt may underperform on other media or models.
- The prompt does not break the convergence on one concept within a single brief.
- The intensity wording ("quiet to spectacular — unless the request says otherwise") has not been tested on its own.
- The catalogs no longer ship, so the owner preferences they recorded are no longer available to runs.

## Source

- Supersedes 20260916-design-is-reference-calibrated-guidance: the guidance-only boundary and `review-design`'s ownership of its standards and checker are carried forward here; the curated catalogs and required reference study are retired.
- Related: 20260915-design-keeps-experience-goals-and-conditional-constraints
