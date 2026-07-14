# ADR: figure-out roots the crux tree above solution-shaped topics

## Status
Accepted

## Context

`figure-out` orders its questioning by Parent-before-child Crux Priority within a crux tree rooted at the stated topic, and its opening instruction presses that topic relentlessly. A companion decision (20260714-figure-out-challenge-solution-existence-before-design) makes solution structure earn its existence — but its trigger fires when the conversation *turns toward* a solution mid-investigation.

When a topic *arrives* already solution-shaped ("add X", "include Y", "how do I make X do Y"), that trigger never fires on the frame itself: the tree roots at the stated solution, and nothing licenses stepping above the root to ask what the solution is in service of. This is the classic XY problem. Frame acceptance is also a known model default, and "press the topic relentlessly" strengthens the anchor on the user's framing rather than loosening it. A sweep of the skill's spine, references, and task files confirmed no problem-behind-the-solution instruction exists anywhere; even the FEATURE probe file, where solution-shaped topics most often land, carries no such angle. Sessions were observed where a solution-framed topic was investigated as given and the simpler design implied by the underlying problem surfaced late or not at all.

## Decision

Generalize the crux-root in `## The loop` of `SKILL.md`: when a topic arrives solution-shaped and the problem behind it is unstated — or stated but not yet established — the highest-level unresolved crux is the problem the solution serves. The stated solution demotes to one candidate answer to that crux, subject to the same existence pressure ("do we need this at all?") as any proposed element.

Combined with the existing lead-with-one-question cadence, this produces the intended runtime behavior directly: the opening turn asks what the topic is actually solving, paired with the agent's best-supported guess at the likely problem. When the user arrives with the problem already established, the crux is already settled and the challenge stays silent — no ritual firing.

Deliberately excluded from the change:

- **No explicit escape-hatch text** for a user who insists on the stated frame. The existing "you inform, they decide" posture already lets the user pin the frame; explicit defer-language would hand the model an agreement exit it will overuse.
- **No regress guard.** "Highest-level unresolved crux" already bounds how far above the frame the climb goes.

## Alternatives Considered

- **No change; read crux priority as already implying the problem is the parent crux:** Rejected — the tree is textually rooted at the stated topic, so even perfect compliance with the current wording does not produce the step above the root.
- **A discrete intake step ("at session start, if the topic looks like a solution, first ask what problem it solves"):** Rejected — it duplicates the existing structure-challenge rule behind a mode qualifier, and a scripted step fires as ceremony even when the problem work is already done. A crux rule stays silent when the crux is settled; a procedure wants to be executed.
- **Task-file-only probe (e.g., a FEATURE angle asking what problem the feature serves):** Rejected as the primary fix — the XY problem is shape-independent (a diagnosis framed as "how do I make X do Y" carries the same disease), so it belongs at spine altitude. A complementary task-file probe remains possible but is not this decision.

## Consequences

### Positive
- Solution-shaped topics get the same scrutiny as solution structure produced mid-investigation, closing the asymmetry between what the agent proposes and what the user arrives with.
- The simpler design implied by the underlying problem can surface before design attention is spent inside the arriving frame.
- Reuses existing machinery (crux priority, existence pressure, one-question cadence) — no new mechanism, schema, or intake procedure.

### Negative
- The trigger ("problem unstated or not yet established") is a judgment call; miscalibration can under-fire (rolling with the frame) or over-fire (interrogating users who already did the problem work).
- Rewording the loop's opening must redefine what the tree roots at without weakening "press the topic relentlessly"; a clumsy draft could dilute the skill's strongest anchor.

## Source
- Grounding: textual analysis of the skill's spine and a full sweep of its references and task files, plus observed sessions where solution-framed topics were investigated as given.
- Related: 20260714-figure-out-challenge-solution-existence-before-design
- Related: 20260703-figure-out-fog-discipline
