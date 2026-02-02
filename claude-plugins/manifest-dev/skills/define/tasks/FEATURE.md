# FEATURE Task Guidance

New functionality: features, APIs, enhancements.

## Risks

- **Scope creep** - feature expands beyond original intent
- **Breaking consumers** - changes to API, DB schema, config break downstream; probe: who consumes this?
- **Missing edge cases** - happy path works, edge cases crash
- **Security blind spot** - auth, user data, external input not reviewed
- **Silent production failure** - works in dev, no observability in prod

## Scenario Prompts

- **Mental model mismatch** - works as built, not as expected; probe: what does user think this does?
- **Partial state corruption** - crashes midway, data inconsistent; probe: what if it fails halfway?
- **Invisible dependency** - relies on unguaranteed assumption; probe: what must be true for this to work?
- **Permission gap** - feature accessible to wrong users; probe: who should/shouldn't access this?
- **Backward compatibility break** - existing clients fail; probe: versioning? migration path?
- **Migration missing** - new schema, old data incompatible; probe: existing data? rollback?
- **Feature flag complexity** - flag combinations create untested states; probe: flag interactions?
- **Integration timing** - depends on service that isn't ready; probe: deployment order? feature dependencies?
- **Undo/rollback impossible** - user can't recover from action; probe: reversible? confirmation needed?
- **Documentation drift** - feature ships, docs don't match; probe: what docs need updating?
- **Notification/feedback gap** - action succeeds silently; probe: does user know it worked?
- **Mobile/offline behavior** - works online, breaks offline; probe: connectivity assumptions?

## Trade-offs

- Scope vs time
- Flexibility vs simplicity
- Feature completeness vs ship date
- New abstraction vs inline solution
