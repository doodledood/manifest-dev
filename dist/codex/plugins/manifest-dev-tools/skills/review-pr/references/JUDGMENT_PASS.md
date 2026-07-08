# Judgment pass (premise check)

The reviewer-fleet dimensions find defects inside a change whose intent is taken as given — they drop anything the author chose deliberately. The judgment pass adds the one thing they structurally cannot: it asks whether the change **earns its keep** — whether it should exist, in this shape, at this footprint, given the pain it claims to solve.

**The single question:** *Does this change — its existence, its approach, and its footprint — earn its keep against the pain it solves, and is anything the pain requires missing?*

It runs as a **wide-context pass** — fed the PR description, conversation, and (in manifest mode) the manifest's Intent that the narrow-lens fleet never receives. It is **non-blocking**: every finding is a question the author answers, never a gate. (The host wires *how* it runs — a parallel subagent whose findings the coherence pass consolidates, gated to once per PR; see the review-pr SKILL and `MANIFEST_MODE.md`.)

## Altitude — whole-PR only

The judgment pass operates on the **PR as a whole, or a major component of it** — the big question, never line-level ones. It must never fire on a small-item nitpick — an unused parameter, a single narrow helper, one incidental line; those belong to the defect dimensions or are dropped. The surface, omission, and precedent triggers fire only on a **material footprint**: a subsystem, a new public API area, a cluster of knobs, an established pattern — never a single incidental item.

Whole-PR altitude is unconditional: whenever the pass runs, it reads the **entire PR head**, not just the incrementally-reviewed range on a loop or re-review pass, so its question always concerns the whole change. Judgment findings are therefore exempt from any reviewed-range bounding that scopes defect findings to the latest delta. (Because generation is gated to once per PR, the pass runs on the first pass over the PR rather than every round — the host owns that gate.)

## The evidence bar

The pass exists to *remove* noise (unjustified changes, orphaned surface). It becomes noise the instant it fires on taste. So every trigger fires **only on concrete, nameable evidence** — something you can point at. "I'd have done it differently" is not evidence and stays dropped, exactly as the defect dimensions drop intentional choices. When in doubt, stay silent: a missed premise question costs less than an arrogant one.

## Triggers

Each trigger carries what it **fires on** (concrete evidence) and what it **never fires on** (taste / nitpick).

### 1. Necessity
- **Fires on:** the change, or a major part of it, duplicates a capability that already exists (point to it), guards a condition that cannot occur, or solves a problem no consumer, caller, or issue actually has.
- **Never:** "I wouldn't have built this," with no already-exists or no-consumer anchor to point at.

### 2. Pain reconstructable
- **Fires on:** the pain the change claims to solve cannot be reconstructed from any source — PR description, commits, linked issue, or (manifest mode) the manifest's Intent. Surfaced as a question ("what pain does this solve?"), not a verdict.
- **Never:** the pain is stated but you personally find it unconvincing.

### 3. Surface proportionality
- **Fires on:** the change adds material surface — a new public API area, a cluster of options or flags, a new configuration concept — with no consumer in the same change and no stated need for one.
- **Never:** one unused parameter or a single narrow helper — that is a defect-dimension / dead-code concern, not this pass.

### 4. Solution-shape
- **Fires on:** a materially simpler or more direct solution to the *same* pain is concretely nameable — the one-line-upstream fix, the existing primitive that removes the whole mechanism.
- **Never:** "I'd architect it differently," with no concretely simpler solution to point at.

### 5. Omission-vs-pain
- **Fires on:** the change leaves out something the *stated pain* demonstrably requires — a path or consumer the pain needs that is absent from the change and uncovered elsewhere. Name the missing piece.
- **Never:** "you could also add X," where X is not required by the stated pain.

### 6. Irreversibility
- **Fires on:** the change touches a named one-way-door surface — a schema migration, a public API signature, a persisted data format, a security boundary. The finding is "this is hard to undo — deliberate?", not a defect claim.
- **Never:** reversible internal code.

### 7. Precedent
- **Fires on:** the change introduces a *new* pattern already repeated within it, or clearly positioned to be copied — point to the pattern and its likely propagation.
- **Never:** a one-off you simply dislike stylistically.

## Findings are a distinct class — not a severity

A judgment finding is **not** placed on the defect severity scale (low / medium / high / critical). That scale measures defect badness and blocking weight; a premise question is a different axis — non-blocking, yet sometimes the most important thing about the PR. Each judgment finding carries exactly:

```
{ trigger, concrete evidence, author-facing question }
```

and **no severity**. This is load-bearing, not cosmetic:

- The holistic-coherence pass drops Low-severity findings before posting — the **only** place a drop-Low filter exists, and only because it posts publicly. A judgment finding tagged Low would be silently deleted there. So judgment findings are **exempt from the drop-Low filter** and carry their own inclusion rule: **surface if the evidence-gate fired and the PR does not already cover the point.** They are still deduped and merged like any other finding.
- No other context has a drop-Low filter. Manifest-mode contract verification and `/do` gate verification keep low findings by their own acceptance thresholds; the judgment class is orthogonal to all of that.

## Synthesis — one question per root

When several triggers fire on the **same** root — necessity + solution-shape + surface all pointing at one over-built change — collapse them into **one** "does this earn its keep, here's why I ask" question. Never post one comment per trigger. This reuses the holistic pass's existing dedupe/merge; it adds no new capping machinery. Enumeration is exactly how this pass would become the noise it exists to remove.

## Non-blocking — always a question, never a gate

Every judgment finding is posted as an author-answerable question through the existing review voice and posting path. The judgment pass:

- **never** blocks a merge, submits `request_changes`, or auto-`approve`s;
- adds **no** new posting path — findings ride the existing single batched review and hidden self-marker;
- in **manifest mode**, is strictly additive — the manifest contract's PASS/FAIL is computed exactly as before, untouched by any judgment finding.

If nothing clears the evidence bar, the pass stays silent. Silence is the expected default on a sound change.
