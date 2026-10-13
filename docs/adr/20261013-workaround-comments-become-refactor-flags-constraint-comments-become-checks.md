# ADR: A workaround comment in the project's own code becomes a refactor flag; a constraint comment becomes an offer to encode it

## Status
Accepted

## Area
Code review

## Decided by
The user

## Context
Agents copy what they find, including workarounds that a comment explains, and they cite such a comment as a reason to leave the problem unsolved. The prose-value dimension kept "a workaround for a specific bug" as a load-bearing why. Some comments stay necessary: behavior that an external dependency, platform, or protocol forces; legal headers; documented public API contracts.

## Decision
- A comment that explains a workaround in code the project owns is reported as a refactor flag in the debt list, naming the symbol to reshape. It is not deleted automatically.
- A comment that claims a constraint, such as "do not remove" or "do not change", gets an offer to encode the constraint as a type, a test, or a lint. Once the constraint is encoded, the comment goes.
- A comment about something the project cannot change stays.
- The prose-value dimension's load-bearing-why category narrows to match.

## Alternatives Considered
- **Keep workaround comments as explanation**: agents copy them as a pattern.
- **Delete every comment outside a short keep list**: it removes explanations that someone still needs.

## Consequences

### Positive
- Workarounds become visible debt instead of a pattern to copy.
- Claimed constraints become checks.

### Negative
- The debt list grows.
- Telling a comment about an external constraint from one about the project's own code takes judgment.

## Enforced by
partly — eval case `d19-workaround-comment` measures it once run; telling an external constraint from the project's own stays judgment.

## Source
- Session: figure-out investigation of steering agents toward maintainable first versions.
- Related: 20261013-corrections-become-scoped-locks-and-their-hits-become-reported-debt
