# FEATURE Task Guidance

New functionality: features, APIs, enhancements.

## Risks

- **Scope creep** - feature expands beyond original intent
- **Breaking consumers** - changes to API, DB schema, config break downstream; probe: who consumes this?
- **Missing edge cases** - happy path works, edge cases crash
- **Security blind spot** - auth, user data, external input not reviewed
- **Silent production failure** - works in dev, no observability in prod

## Scenario Prompts

Consider these failure scenarios when probing:

- **Mental model mismatch** - feature works as implemented but users expect different behavior; probe: what does the user think this does?
- **Partial state corruption** - operation fails midway, leaving data inconsistent; probe: what if this crashes halfway through?
- **Invisible dependency** - feature relies on assumption that isn't guaranteed; probe: what must be true for this to work?

## Trade-offs

- Scope vs time
- Flexibility vs simplicity
- Feature completeness vs ship date
- New abstraction vs inline solution
