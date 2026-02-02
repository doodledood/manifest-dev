# FEATURE Task Guidance

New functionality: features, APIs, enhancements.

## Risks

- **Scope creep** - feature expands beyond original intent
- **Breaking consumers** - changes to API, DB schema, config break downstream; probe: who consumes this?
- **Missing edge cases** - happy path works, edge cases crash
- **Security blind spot** - auth, user data, external input not reviewed
- **Silent production failure** - works in dev, no observability in prod

## Trade-offs

- Scope vs time
- Flexibility vs simplicity
- Feature completeness vs ship date
- New abstraction vs inline solution
