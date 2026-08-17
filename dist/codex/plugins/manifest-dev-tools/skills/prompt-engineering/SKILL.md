---
name: prompt-engineering
description: 'Create, update, review, or discuss an LLM prompt — a system prompt, a skill, or an agent. Use when writing or improving a prompt, discussing a skill or agent, diagnosing prompt failures, or when the user says a prompt needs work.'
argument-hint: '<request>'
user-invocable: true
---

A prompt states a goal and gets out of the way. Everything else in it is load — spent on every run, taken from the attention the model would otherwise put on the work — so each line has to buy more than it costs. What follows decides three things: whether a line exists, where it sits, and how it is worded.

## Where a line came from

Ask this before asking whether the line helps. A line can be true, relevant, and still worth cutting, so usefulness does not settle it. Provenance does, and you can answer it from memory:

- **The user ruled it** — a decision, preference, or constraint they stated. Nothing derives it. Keep.
- **The world holds it, out of the run's reach** — an unwritten convention, a failure you observed, a fact outside what the run will read. Keep, and prefer a pointer to the source over a copy that can go stale.
- **It counteracts a default you have watched the model take** — keep, when the default is observed rather than feared.
- **You worked it out from material the run will also read** — cut. A conclusion available in the corpus is one the run reaches itself, so writing it down buys nothing and spends load on every invocation.

That last class is the one that feels most earned, because you did the work to reach it, and it is where over-specification comes from. Two tells: a line you could justify from the same sources the run gets, and a sentence arguing for the instruction above it — an instruction does not need advocacy, and the run is not persuaded by it.

**A choice the request left open belongs to whoever made the request.** Some of what you would add is not padding but a decision — what ranks one candidate over another, an exception to a rule they gave you, a deliverable beyond what they asked for. It reads as thoroughness and it commits them to something they never chose, under their name, in a file they will quote back later. Ask where the answer would change the work; leave it out where it would not.

**A finished prompt looks thinner than you expect it to, and that is the result rather than a warning sign.** Two rulings and a goal make a short document; the pull at that point is to fill it out — a section on how to rank, a definition of the term in its own name, a third source of evidence nobody asked for — and everything reached for that way comes from the class above. When it reads as too slight, check the goal is stated and the rulings are in it, then ship it.

The older question — *would the model do this without the line?* — asks for a prediction about the model's own counterfactual behaviour, which is not reliably answerable from the inside. Ask it second, of what provenance already admitted: it can still cut a line provenance allowed, never keep one provenance rejected.

When two people disagree about whether a line is doing work, the argument is about the model's default, so settle it by running the document with the line removed and comparing. That is a tiebreak available when it is worth the trouble, not a step every line has to pass.

## Author upward

Start from the goal sentence. Add only what the questions above admit, one line at a time.

Writing broadly and pruning afterwards costs more and lands longer: every line you would cut is one you already argued for, and the draft's own weight reads as evidence that it was needed.

## Two budgets

Everything you add spends one of two things:

- **Context load** — always-loaded material, paid every turn whether or not it fires. A skill's description, a rule in an `AGENTS.md`, anything resident.
- **Cognitive load** — what a person has to hold: which documents exist, and when to reach for each. Not a cost to drive to zero — it is what buys human judgement. Spend it where judgement matters.

Material behind a pointer escapes context load for the price of the pointer's own line. Material with no pointer rides entirely on a person remembering it.

## Where a line sits

Three rungs, ordered by how immediately the run needs the material: **steps** it performs in order, **reference** it consults on demand, and **disclosed reference** in a separate file reached by a pointer. Moving material down keeps the top legible; moving too much down hides what the run actually needs. Branching decides it — inline what every path needs, disclose what only some paths reach.

Keep a rule's statement, its bounds, and its exceptions together under one heading, so reading one brings the others. A rule split across a document is one rule that can drift into two.

A **pointer** is the line naming out-of-context material and the condition for reaching it: a skill description, a reference link. Its wording, not its target, decides whether the run gets there — so lead with the word that triggers it, give one trigger per distinct case, and cut what the target already says about itself. If material must be reached and the pointer is weak, sharpen the wording before inlining the material.

## Wording

**Reach for a word the model already holds.** A pretrained word — *relentless*, *tight*, *adversarial* — recruits priors and anchors a region of behaviour in one token, where a phrase spends several and lands weaker. When a directive is too weak, the fix is a stronger word rather than more words. A coined term recruits nothing, so you pay in definition what a real word gives free.

**State the target, not the ban.** A prohibition names the behaviour it forbids and thereby makes it available — the negation is a weak modifier on a strongly activated concept. *Write one-line comments* beats *don't write long comments*. Keep a prohibition only as a guardrail that cannot be phrased positively, and pair it with the positive target.

**End every step on a condition the run can check.** *Understanding reached* invites stopping early, because the steps still visible ahead pull attention toward being done. Sharpen the bound first; splitting the sequence only helps across a real context boundary, since an inline mention leaves the later steps in view. Wording also sets how much work the step demands: *every caller enumerated* forces the sweep that *list the callers* does not.

**Give judgment calls a rule, not an absolute.** *Always ask before assuming* over-fires; *when the missing fact would change the action, ask — otherwise proceed and label the assumption* can be applied. Reserve MUST and NEVER for real invariants.

**Keep the arousal low.** Urgency framing, all-caps imperatives and heavy praise measurably shift behaviour — toward corner-cutting under pressure, toward agreement under flattery. Normalize failure in anything iterative: *if this approach doesn't work, try another*. The opening sets the register for everything after it.

## Pruning

- **One meaning, one place.** The same rule in two files is two texts that drift, and only one of them will be read. (Repeating a *word* on purpose is the opposite move and is fine.)
- **The environment is a source of truth.** A prompt restating what `package.json`, a config file, or `--help` already answers is a cache that goes stale. Cache only what no file confesses: the unwritten convention, the reason, the gotcha.
- **Check every line for relevance**, not just correctness — a line can be true and no longer bear on what the document does. Left unchecked, a prompt accretes layers nobody dares remove.
- **Hunt no-ops sentence by sentence.** An instruction the model already follows pays load to say nothing. Delete the whole sentence rather than trimming its words.

## Edges

A line can earn its place and still break where the prompt actually runs. Check each against the conditions it will meet:

- Naming a harness-bound primitive — a specific tool, scheduler, or CLI — where the capability should be stated in plain language and the model left to find it.
- A qualifier that quietly excludes cases the principle covers (*under mode X*, *by another reviewer*).
- A mechanism stated as the only path — a fixed sequence, a hardcoded number — where the principle should stand and the number be a default.

## Updating

Find the gap a line closes before changing anything near it. The best patch usually replaces a line rather than adding one beside it — and a new explicit rule often retires an older vague hedge, so check the neighbours after the edit. Net change can be positive or negative; the target is balance, not direction.

Guard against building a wall around a single observed failure. One instance is a fix; a section is over-correction.

## References

- `references/mechanics.md` — the shapes: a skill's frontmatter, naming and layout; an agent's isolation and capability declarations; a knowledge skill whose gap is data rather than behaviour.
- `references/system-prompts.md` — a system prompt that ships in a deployment loop, and the ready-made blocks for one: verification passes, tool-call budgets, ambiguity handling, output contracts, high-risk self-checks. For that artifact only.
- `references/metaprompting.md` — diagnosing a failing prompt against logged traces.
