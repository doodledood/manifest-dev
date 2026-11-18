# ADR: Pull request review adds a rendered design review when a change alters what a person sees

## Status
Accepted

## Area
Code review

## Decided by
The user

## Context
Pull request review with no Manifest ran a fixed fleet of code dimensions, plus the prompt review
when a diff touched prompts. Nothing in it judged what a person sees: a page, a screen, a
rendered message. A change that reads as sound code can still hide a control at a phone's width,
cover a button, or break a flow, and only a render shows it. The design review already existed
and already judged rendered artifacts, including UX and usability, but only Manifest runs called
it. This decision sits inside the North Star's *Purpose*: it is one more way delegated work earns
enough trust to use with minimal review.

## Decision
With no Manifest, pull request review adds the design review whenever the reviewed range changes
something a person sees and judges rather than calls — a screen, a page, a rendered email, a
slide — the same way it adds the prompt review for prompts. Markdown documents, prose and prompt
files are not such a change; the docs and prompt reviews keep them. The design review judges the
result rendered at the head commit in a scratch location: static files directly, and the
project's own documented preview or build only for a pull request whose branch lives in the
repository or one the caller says to trust, in an environment holding none of the caller's
credentials. With no render reachable, it reports its scope blocked with what would enable it.
Its findings pass through the same consolidation and publication policy as every other
reviewer's. The design review's description and define's design-quality row name UX and
usability, so a person looking for a UX review finds this one.

## Alternatives Considered
- **A separate UX reviewer skill**: a second skill beside the design review — the design review already judges usability on the rendered artifact, and two reviewers of one surface would compete for the same findings.
- **Leave the design review to Manifest runs**: keep pull request review to code dimensions — a pull request reviewed without a Manifest, which is most of them, would keep missing what only a render shows.

## Consequences

### Positive
- A defect that only the rendered page shows has a named reviewer on the pull request path, rather than depending on a code reviewer choosing to render.

### Negative
- Each such review renders the change, which costs time and a browser where the review runs; where nothing can be rendered, that part of the review reports blocked rather than passing.
- The evidence is one case driven before and after the change. On the plugin before it, the reviewer found the case's defect on its own both times it was driven — once by adding the design review unprompted, once inside the code-bugs dimension — at 202k and 217k tokens and 309 and 342 seconds; after it, the design review ran as a listed step and carried the defect, at 216k tokens and 383 seconds, and did not run for a change to Markdown alone. The gain shown is that the design review runs reliably, not that more defects are caught.
- Untested: whether the design review holds a change to a plain design guide document the project keeps, and whether pull request review hands the project's principles on to it. A drive shows it applying a principles skill reached through the context file's pointer, and nothing more.

## Enforced by
none — which reviewers a review runs is an instruction in `review-pr`'s text; the `design` scenario in `verification/recipes/review-pr.md` checks it by a drive, not by a test.

## Source
- Session: maintainer rulings while defining the change
- Related: See also [20261118-starter-principles-ship-as-sets-a-project-owns](20261118-starter-principles-ship-as-sets-a-project-owns.md)
