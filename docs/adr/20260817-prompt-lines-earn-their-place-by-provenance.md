# ADR: A prompt line earns its place by provenance, not by a counterfactual judgment

## Status
Accepted

## Area
Prompt architecture

## Context

`prompt-engineering` decided whether a line belonged by asking the author *"would the model produce this behavior without this line?"* That question asks for a prediction about the model's own counterfactual behaviour, which is not reliably answerable from the inside: a line can pass it on careful reasoning and turn out inert the moment it is actually removed and the prompt re-run. Applied honestly to a real skill, it kept lines twice that a single run showed changed nothing.

The skill also had a merit test with no cost side. "Does this line earn its place" answers keep-or-cut and says nothing about placement, so everything that passed landed flat in one file. The skill had grown to 686 lines while teaching that content should close a real gap and stop — its own `review.md` listed *over-engineering — ten phases for a simple task* as an anti-pattern.

Both effects showed up in what it produced: skills that were long, enumerated sources and steps their runs could have found for themselves, and explained their own rules back to the model.

## Decision

**Provenance is the primary test.** A line earns its place when it carries one of three things: a ruling the requester made, knowledge from outside what the run will itself read, or a counteraction to a model default someone has watched happen. A line whose only source is the author's own reasoning over material the run will also read is cut — a conclusion available in that material is one the run re-derives, so writing it down buys nothing and spends load on every invocation. The mechanism is what makes the verdict predictable in advance rather than discoverable only by running.

The counterfactual question survives in second place, applied to what provenance already admitted: it may cut a line provenance allowed, never keep one provenance rejected.

**Authoring runs upward from the goal sentence** rather than drafting broadly and pruning. Pruning fights sunk cost — every line cut is one already argued for — and reliably lands long.

**Two budgets and an information ladder decide placement.** Context load is what always-loaded material costs every turn; cognitive load is what a person pays to know a document exists. Surviving content is placed on a ladder — steps, in-file reference, disclosed reference behind a pointer — rather than merely kept.

**Two failure modes get named because they survive the rules above.** A draft that traces cleanly still feels thin, and the pull is to fill it out with a ranking section, a definition, an extra source — so the skill states that a thin result is the correct outcome. And some additions are not padding but decisions belonging to whoever made the request; those are asked about, not settled in the file under their name.

Structurally: `skills.md`, `agents.md` and `knowledge-skills.md` merge into one `mechanics.md`; `review.md`'s anti-pattern and pre-ship tables dissolve into the levers they restated; the paste-ready blocks move under `system-prompts.md`, the artifact they serve, so authoring a skill can no longer reach them; `metaprompting.md` keeps its job, losing only its pointer to the deleted `review.md`. 686 lines to 347.

Two downstream surfaces move with it. `define`'s prompting task file required a new skill to carry a Gotchas section — content a new skill can satisfy only by inventing it, which the skill it gates forbids — and carried a skill-type taxonomy default; both are removed and a provenance gate replaces them. `review-prompt` leads with the provenance question and no longer treats an absent section as a finding.

The two-budget framing and the information ladder are taken from Matt Pocock's `writing-for-agents`.

## Alternatives Considered

- **Keep the counterfactual question as primary and sharpen its wording.** Rejected: the failure is structural rather than lexical. No phrasing makes a model a reliable predictor of its own counterfactual behaviour.
- **Require an ablation run for every line** — remove it, re-run, keep only what changes the output. Rejected as more machinery than the problem is worth, and heavier than any comparable reference. Running stays available as a tiebreak for a contested line, which is where the disagreement is genuinely about the model's default.
- **Graft the new levers onto the existing structure.** Rejected: the catalogs were where the bulk lived, and a load model added to a 686-line document teaching restraint would have been contradicted by the document carrying it.
- **Delete the paste-ready blocks outright.** Rejected: they close real gaps for deployment system prompts. Re-scoping them under that artifact keeps the value and removes the leak, since the old pointer fired for *any prompt type*.

## Consequences

### Positive
- The admission test is answerable from memory instead of requiring a prediction, and it names the class that produces over-specification.
- Placement has a cost model, so surviving content can be pushed down a ladder rather than only kept or cut.
- Authoring a skill can no longer reach prose written for a deployment loop.
- The skill now holds to the discipline it teaches, which its previous size did not.

### Negative
- Provenance can be argued into permitting a line by relabelling an author's conclusion as an observed default; the third class is the soft spot, and only evidence of having watched the default keeps it honest.
- A behaviour that a run would re-derive from a corpus it reads *slowly or unreliably* is now cut, trading a small loss of reliability for the load saved. Where that matters, the line returns as an observed default.
- Merging three references into one means an author writing an agent loads skill and knowledge-skill material too.
- The rewrite is validated by authoring runs judged in fresh contexts rather than by production use; the sample is small.

## Source
- Related: supersedes no record; the skill's prior structure was never recorded as a decision.
