# DOCUMENT Task Guidance

Documentation register: specs, proposals, reports, formal documentation. Composes onto
`PROSE_FLOOR.md`.

**Register.** These gates judge whether prose is clear, consistent, and usable instruction. They
replace the human-voice register rather than adding to it — a deliverable under this task type is
not judged on rhythm variation, tonal shifts, humor, or deliberate imperfection, and their absence
is never a finding here.

## Quality Gates

| Aspect | Skill | Threshold |
|--------|-------|-----------|
| Documentation style | `review-writing`, `register=docs` | no MEDIUM+ |
| Structure completeness | — | All required sections present |
| External consistency | — | No contradictions with identified reference documentation (conditional: only when comparison docs surfaced during interview) |
| Scope clarity | — | What's covered and what's not stated explicitly |

The style claim states the chosen acceptance policy. Its Evidence activates `review-writing`
with `register=docs` and that policy, as `SKILL.md` → *Specialized gates activate a skill* says.
The table supplies the usual Medium+ policy; reviewer standards and the shared prose floor
stay with the skill. It is a Judgment Gate, which is what tells `/do` how it re-verifies.

Terminology consistency, formatting conventions, headings, lists, numbers, dates, links, and code
references all fall inside that one gate; they do not need gates of their own.

## Defaults

*Domain best practices for this task type.*

- **Fix terminology before drafting** — choose the term for each recurring concept once and reuse it exactly; a synonym introduced for variety reads as a new concept
- **Front-load each section** — the first sentence carries the point, so a reader scanning headings and openers gets the document
- **One mode per document** — tutorial, how-to, reference or explanation; split and link rather than mixing them
- **Generate or link what code owns** — a flag, a default or a count that code or configuration owns is generated or linked, not restated, and any count or tree is true at the commit with the command that regenerates it
- **One copy of each fact** — a fact another document already states is linked, not repeated
