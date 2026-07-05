# ADR: Front `/figure-out` as the Door; the define/do loop remains the House

## Status
Accepted

## Context
manifest-dev's discovery surfaces (README first screen, repo metadata, directory listings, docs pages) need a single clear entry point. Presenting the integrated methodology first demands enrollment before any value is felt — a newcomer must buy the whole `/figure-out` → `/define` → `/do` arc to get anything — while the strongest first impression comes from one standalone skill solving a pain the visitor already has, felt within the first minute.

Choosing which skill fronts those surfaces (the Door) is a positioning decision. Candidate pains and their 2026 landscape: "the agent says done but it isn't" is now intercepted first-party — Claude Code bundles zero-setup `/run` and `/verify` skills — with several third-party verify skills on skill marketplaces besides; PR-lifecycle tending has established incumbents; "the agent builds the wrong thing because it never understood the problem" remains open, and manifest-dev's `/figure-out` — an adversarial understanding partner that investigates before it claims — is the repo's differentiated answer to it and fully standalone. Within the system itself, understanding is also load-bearing: the define/do machinery only works on top of a proper understanding session.

A register comparison across candidate first screens settled the presentation: an accusation register with a harness-generic subject reads strongest, since manifest-dev deliberately targets multiple agent CLIs, not one harness.

## Decision
Front `/figure-out` as the Door — the standalone, zero-enrollment entry point — on manifest-dev's discovery surfaces:

- **README first screen**: accusation register with a harness-generic subject ("Your agent builds the wrong thing, confidently"), the explicit 60-second first-felt moment, an inline take-what-you-want blessing (every skill works standalone), and the one-line `npx skills add doodledood/manifest-dev --skill figure-out` install.
- **Naming splits by surface**: the README headline stays harness-generic (multi-CLI support is a real differentiator on the identity surface); query-capture docs pages, GitHub topics, and directory listings use harness-specific language, because searchers name their harness.
- **The define/do loop is the House, not a footnote**: it is the other half of the value and the retention engine. Below the fold, the README presents the full understanding-first loop as the destination the Door opens into, and `/figure-out`'s natural handoff to `/define` remains the organic path deeper.
- **No new build gates distribution**: metadata, README work, directory submissions, and docs pages proceed on existing skills.

## Alternatives Considered
- **A standalone verify-style skill as the Door** (front the "says done but isn't" pain): Rejected — Claude Code now occupies that surface first-party with a bundled zero-setup `/verify`, plus a crowded third-party field; building a competing entry point would take days and enter last.
- **`/babysit-pr` as the Door**: its pain surface has proven demand — Rejected as identity: established incumbents own the surface and it isn't the repo's differentiated core. Kept as a secondary grab on directory listings.
- **Methodology-first front door (status quo README)**: Rejected — it demands enrollment before value is felt, the exact shape a Door exists to avoid.

## Consequences

### Positive
- Distribution work is un-gated immediately; nothing waits on a build.
- The repo fronts its genuinely differentiated asset (an adversarial understanding partner) rather than competing with a first-party default.
- Door-level behavior (installs, clones, conversion into the House) becomes directly measurable, replacing guesswork about what newcomers respond to.

### Negative
- `/figure-out`'s first-minute impact on newcomers is a hypothesis until measured; if the fronted Door doesn't convert, the positioning must be reopened rather than pushed harder.
- A harness-generic headline sacrifices some search capture on the identity surface — accepted, mitigated by harness-specific capture pages.
- The two-layer presentation must be maintained so the House doesn't decay into a footnote; the loop is half the value.

## Source
- Related: 20260705-keep-plugin-first-layout-npx-skills-compatible, 20260606-figure-out-process-trust-vs-define-do-artifact-trust
