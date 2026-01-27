# DOCUMENT Task Guidance

Task-specific guidance for document deliverables: specs, proposals, reports, documentation.

## Document Quality Gates

Surface which quality aspects matter. Mark recommended defaults based on task context.

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Structure completeness | general-purpose | All required sections present and complete |
| Audience fit | general-purpose | Language and depth match target reader |
| Clarity | general-purpose | No ambiguous terms or undefined jargon |
| Consistency | general-purpose | Terminology and style uniform throughout |
| Accuracy | general-purpose | Claims supported, no contradictions |

**Encoding**: Add selected gates as Global Invariants with subagent verification:
```yaml
verify:
  method: subagent
  agent: general-purpose
  model: opus
  prompt: "Review document for [quality aspect] issues"
```

## Document-Specific AC Patterns

**Structural**
- "Contains [section] with [requirements]"
- "Follows [template] structure"
- "Includes [appendix/glossary/references]"

**Content**
- "Covers [topics]"
- "Addresses [question]"
- "Explains [concept] for [audience]"

**Quality**
- "No undefined jargon"
- "Acronyms expanded on first use"
- "All claims cite sources"
- "Consistent terminology throughout"

**Process**
- "Reviewed by [stakeholder]"
- "Approved by [role]"
