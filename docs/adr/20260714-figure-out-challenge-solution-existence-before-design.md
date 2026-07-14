# ADR: figure-out challenges solution existence before descendant design

## Status
Accepted

## Context

`figure-out` reaches shared understanding by walking the branches that could change its Read and settling the highest-level crux first. Its opening instruction previously grouped design choices together with diagnostic hypotheses and commitment questions as branches to walk.

In solution-shaped investigations this let a proposed requirement, component, mechanism, or process step become a branch to elaborate simply because it had been raised. Parent-before-child ordering then operated inside that assumed solution frame: risks and open questions generated descendant mechanisms before the parent structure had shown it earned its place. The skill could still simplify, but only after the design had already accreted — the attention spent designing structure that was later removed could not be recovered.

Two presumptions were being conflated. Unresolved truths — evidence, hypotheses, viable rivals, commitments, adverse fog — should survive until evidence removes them. Proposed solution structure is a choice, not a claim about reality, and should have to earn its existence before its design is explored.

## Decision

Refine the opening of `## The loop` so `figure-out`:

- preserves every unresolved evidence, hypothesis, genuinely viable rival, commitment question, and patch of fog that could still change the Read;
- when the conversation turns toward a solution, challenges its structure before designing it;
- treats any requirement, component, mechanism, or process step introduced in a recommended answer as not-yet-adopted, and makes "Do we need this at all?" the next question — regardless of whether the agent or the user proposed it;
- recommends, in ordinary prose, keeping the element when its benefit justifies its cost under the full goal and constraints, removing or folding it into something simpler when it does not, or leaving its existence unresolved when a child probe is needed to decide;
- explores design only after the element earns existence, and repeats the challenge for each meaningful child.

The judgment must be surfaced as natural conversation. It is expressly **not** presented as verdict labels, schemas, tables, or checklists.

## Alternatives Considered

- **No change; rely on generic simplicity guidance:** Rejected — a broad outcome preference does not govern branch order, and the skill's own instruction to walk every branch dominated it.
- **Keep the behavior as a private, user-level composition rule:** Rejected — the accretion arises from the skill's own opening, so a private remedy would leave every consumer with the defect.
- **Add a terminal deletion/simplification pass before naming the Read:** Rejected — it can only prune structure after the attention to design it has already been spent, and it duplicates a check better placed upstream.
- **A standalone artifact-judgment skill:** Deferred — post-formation judgment is already covered by the review-time premise check, and no separate need outside `figure-out` is established. It would not prevent accretion during deliberation.
- **An explicit verdict enum (`EARNED | DELETE | ABSORB | UNRESOLVED`):** Rejected as the shipped surface — it makes the observability robust but turns a natural deliberation into a form. A plain recurring question carries the same discipline without the schema.

## Consequences

### Positive
- Proposed solution structure is challenged before its design tree expands, reducing effort spent on mechanisms that do not survive scrutiny.
- Exhaustive treatment of evidence, hypotheses, rivals, commitments, and adverse fog is preserved; the existence challenge is scoped to constructed structure.
- Parent-before-child ordering gains an explicit admission step for solution structure without changing its role elsewhere.
- The interaction stays conversational; no new schema or process ceremony is introduced.

### Negative
- The skill must distinguish proposed solution structure from unresolved truths and from goals or constraints the user has fixed.
- Some descendant probing is still needed to judge whether a parent earns existence, so the change reduces speculative elaboration rather than eliminating judgment.
- A poorly stated goal or constraint set can still lead to under- or over-scoped structure; the "keep it unresolved" outcome is the release valve.

## Source
- Grounding: observed prompt behavior where solution mechanisms accreted during solution-shaped deliberation before their necessity was tested; the correction was validated by isolated prompt A/B evaluation against the unchanged opening, plus edge checks on a non-build decision, a diagnosis, and a reliability-critical design.
- Related: 20260703-figure-out-fog-discipline
- Related: 20260709-figure-out-reweight-by-rehosting-not-extraction
