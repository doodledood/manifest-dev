# TECH_DESIGN Task Guidance

Standalone technical design documents. Composes onto `DOCUMENT.md`, and through it onto
`PROSE_FLOOR.md` — the documentation register, so its style gate is the one `DOCUMENT.md`
defines (the `review-writing` skill with `register=docs`) and the human-voice register does not
apply. The gates below are what a design document needs beyond that.

## Quality Gates

| Aspect | Threshold |
|--------|-----------|
| Audience layering | The doc serves the identified first-screen persona and the identified deeper technical persona without requiring other files; references serve the chosen role (absorbed prose, evidence anchors, or allowed citations) |
| Decisions coverage | Against the enumerated source records, every accepted decision, rationale, and load-bearing rejected alternative survives in the prose; citations or source names do not leak when the chosen absorption policy forbids them |
| Image review | The evaluator opens every image and confirms accuracy against surrounding prose, placement where it adds value, value beyond decoration, correct labels/spelling, style alignment with pinned references, and acceptable taste (composition, whitespace, color harmony, no clip-art feel) |
| Content frozen | The doc introduces no new design decisions, constraints, or unresolved claims beyond the enumerated canonical source union, including retired sources via git history when identified |

## Defaults

*Domain best practices for this task type.*

- **Verify generated image labels** — Open each generated image after creation; regenerate or repair images with misspellings, hallucinated labels, or unreadable text before treating them as done
- **Probe document placement** — If the design doc carries assets, ask whether it should live in its own directory with an assets path instead of as a loose markdown file
- **Probe ownership and estimates** — Ask whether owner areas, rollout responsibility, effort, or timeline numbers belong in the doc; don't assume numeric estimates are wanted
