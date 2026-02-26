# FEATURE Task Guidance

New functionality: features, APIs, enhancements.

## Quality Gates

- **Requirements traceability** — every specified requirement maps to implementation; nothing lost between spec and code
- **Behavior completeness** — all specified use cases and interactions implemented, not just the happy path
- **Error experience** — feature failures produce clear, actionable feedback to the user, not silent failures or raw stack traces
- **Documentation updated** — all affected documentation (API docs, user guides, READMEs, changelogs) identified and updated with the feature

## Risks

- **Scope creep** - feature expands beyond original intent
- **Breaking consumers** - downstream consumers not identified before changing interfaces; probe: who consumes this? how will they know?
- **Missing edge cases** - happy path works, edge cases crash
- **Security blind spot** - auth, user data, external input not reviewed
- **Silent production failure** - works in dev, no observability in prod

## Scenario Prompts

- **Mental model mismatch** - works as built, not as expected; probe: what does user think this does?
- **Partial state corruption** - crashes midway, data inconsistent; probe: what if it fails halfway?
- **Permission gap** - feature accessible to wrong users; probe: who should/shouldn't access this?
- **Backward compatibility break** - existing clients fail; probe: versioning? migration path?
- **Migration missing** - new schema, old data incompatible; probe: existing data? rollback?
- **Feature flag complexity** - flag combinations create untested states; probe: flag interactions?
- **Integration timing** - depends on service that isn't ready; probe: deployment order? feature dependencies?
- **Undo/rollback impossible** - user can't recover from action; probe: reversible? confirmation needed?
- **Notification/feedback gap** - action succeeds silently; probe: does user know it worked?
- **Mobile/offline behavior** - works online, breaks offline; probe: connectivity assumptions?
- **Performance degradation** - feature works at test scale, degrades at production volume; probe: data volume? concurrent users? growth rate?
- **Orphaned resources** - feature creates data/state that grows unboundedly with no cleanup path; probe: what does this create? who cleans it up?
- **Graceful degradation missing** - feature fails and takes down surrounding functionality; probe: blast radius? what else breaks?
- **Accessibility gap** - feature works but excludes users; probe: keyboard navigation? screen readers? color contrast?

## Trade-offs

- Scope vs time
- Flexibility vs simplicity
- Feature completeness vs ship date
- New abstraction vs inline solution
- User-facing polish vs implementation effort
- Graceful degradation vs fail-fast

## Defaults

*Domain best practices for this task type.*

- **Document load-bearing assumptions** — Identify what must remain true for the feature to work; surface invisible dependencies
