# ADR: Deliberation renders run the design skill at prototype weight

## Status
Accepted — extended by 20260901-design-derives-structure-from-a-written-task-model: a task-model decision was added between purpose and register, and it too runs in full at prototype weight, so three decisions now do rather than the two this record named. The weight's own rules — minimal token block, floors only where the fidelity concentrates, roughness kept elsewhere, verification skipped — all stand. Further extended by 20260902-design-chooses-an-encoding-per-claim-figures-are-information-not-decoration: the legibility floors held on the judged surface now include the page being at rest at load, and the task model that runs in full carries its encoding line.

## Area
Design skills

## Context

The design skill shipped with a carve-out in its description: deliberately rough prototypes rendered mid-deliberation were excluded, on the reasoning that roughness is the point of a deliberation render — concentrated fidelity tells the reader which axis to react on, polish invites reaction to incidental detail, and a stray reaction hardens into a binding criterion. That carve-out was an assumption decided autonomously during the build, not a ruling. The owner then ruled the other way: prototyping and sensing renders should utilize the design skill. The tension the carve-out guarded is real and had to survive the reversal — a prototype run through the full skill would be polished everywhere, which is exactly the failure the roughness principle prevents.

## Decision

Deliberation renders go through the design skill, at a named reduced weight rather than in full. The skill itself defines **prototype weight** in its `SKILL.md`: purpose and register decisions run in full (a render in the wrong register draws reactions to the wrong thing), a minimal token block is declared, the legibility floors hold only where the fidelity concentrates, everywhere else stays visibly unfinished — finishing it is a defect at this weight — and the verification loop is skipped entirely, because the reader's reaction is the verification and the artifact is disposed of either way. The description's carve-out is replaced by a sentence naming this mode.

The rendering flows wire in at their own rendering step: figure-out's prototyping section and just-figure-out's render line each direct the session to invoke the design skill at prototype weight when a prototype renders as a page, with a by-hand fallback (pick the register, keep the judged surface legible, leave the rest rough) for installs where the skill is absent. Prototypes that are words rather than pages — breadboards, outlines, command sessions — are untouched.

## Alternatives Considered

- **Keep the carve-out**: preserves the roughness principle with zero coupling — not chosen because the owner ruled renders should use the skill, and because the carve-out threw away the part of the skill that helps a prototype (register fit, legibility of the judged surface) along with the part that harms it (polish, verification).
- **Full-weight invocation from the rendering flows**: simplest wiring — not chosen because a fully designed prototype is polished on incidental regions, inviting stray reactions that carry into binding criteria; the failure mode the original carve-out existed to prevent.
- **Define prototype weight in figure-out instead of the design skill**: keeps the design skill single-purpose — not chosen because two rendering flows (figure-out, just-figure-out) would each restate the weight rules and drift; the skill owning its own reduced mode gives the rule one home that every caller shares, and keeps the mode available to callers not yet written.

## Consequences

### Positive
- Prototype renders get the two things the skill can give them without damaging them: a correct register and a legible judged surface.
- The roughness principle survives as an explicit rule of the mode ("finishing it is a defect at this weight") instead of an unstated norm.
- One home for the weight rules; rendering flows carry only the trigger and a one-line fallback.

### Negative
- Every rendered prototype now pays a skill load mid-deliberation.
- The weight boundary is judgment, not mechanism: a session can over-apply the skill and polish a prototype anyway; nothing structural prevents it.

## Source
- Session: owner ruling on 2026-09-01, reversing an assumption auto-decided in the design-skill-pair build.
- Related: 20260901-design-skill-pair-distills-research-eval-deferred, 20260826-prototyping-and-scratch-are-one-mechanism, 20260830-rendering-contract-folds-into-figure-out
