# DOCUMENT Task Guidance

Specs, proposals, reports, formal documentation.

## Quality Gates

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Structure completeness | general-purpose | All required sections present |
| Audience fit | general-purpose | Language and depth match target reader |
| Clarity | general-purpose | No ambiguous terms or undefined jargon |
| Consistency | general-purpose | Terminology and style uniform throughout |
| Accuracy | general-purpose | Claims supported, no contradictions |

## Risks

- **Wrong audience** - too technical or too shallow for readers; probe: who reads this, what do they know?
- **Missing sections** - template or standard not followed; probe: is there a required structure?
- **Stale on arrival** - content outdated by time of publication
- **No review gate** - published without stakeholder sign-off; probe: who must approve?

## Scenario Prompts

- **Stale on arrival** - accurate when written, outdated by publication; probe: how fast does this domain change?
- **Wrong reader assumptions** - too much or too little context; probe: what does reader already know?
- **Missing stakeholder concern** - answers wrong questions; probe: what will stakeholders look for?
- **Contradicts other docs** - conflicts with existing documentation; probe: related docs that need alignment?
- **Missing prerequisites** - assumes knowledge reader doesn't have; probe: what must reader know first?
- **No clear next steps** - reader finishes, doesn't know what to do; probe: what action follows reading?
- **Terminology mismatch** - uses terms differently than codebase/team; probe: glossary needed? terms defined?
- **Approval ambiguity** - unclear who signs off; probe: approval process? required reviewers?
- **Maintenance orphan** - no owner to update when things change; probe: who maintains this?
- **Format mismatch** - wrong format for consumption context; probe: where is this read? how?
- **Missing examples** - abstract explanation, no concrete cases; probe: would examples help?
- **Buried critical info** - important details hidden in middle; probe: what must reader not miss?
- **Scope ambiguity** - unclear what's covered vs not; probe: explicit scope boundaries?

## Trade-offs

- Comprehensive vs readable
- Formal vs accessible
- Detail vs brevity
