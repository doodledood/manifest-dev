# ADR: Front `/figure-out` as the adoption Door; the define/do loop remains the House

## Status
Accepted

## Context
manifest-dev gets praise but not usage (69 stars, discovery-layer metadata empty, no directory presence). A 2026-07-04 handoff report diagnosed the cause as artifact shape — an integrated methodology whose payoff reveals only after a ~2-day trial — and prescribed one build: a standalone `verify-lite` skill on the "Claude says done but it isn't" pain, gating all distribution behind it.

This session re-grounded that prescription against the mid-2026 ecosystem and found claim decay on its central leg: Claude Code now bundles first-party, zero-setup `/run` and `/verify` skills that intercept exactly that pain at the moment it occurs, and skill marketplaces already list several third-party verify skills. Meanwhile the repo already ships standalone-capable skills — `/figure-out` (fully standalone) and `/babysit-pr` (advertised as setup-free) — so no build gates distribution. The maintainer holds that `/figure-out` is the differentiated core ("proper understanding is half the battle"; the define/do machinery doesn't function without it), while also insisting manifest-dev is the full picture — understanding plus the define/do loop, not a figure-out repo with extras.

A register probe (three divergent README first-screen mocks) extracted the presentation criterion: accusation register, harness-generic subject.

## Decision
Front `/figure-out` as the Door — the standalone, zero-enrollment entry point — on the repo's discovery surfaces:

- **README first screen**: accusation register with a harness-generic subject ("Your agent builds the wrong thing, confidently"), the explicit 60-second first-felt moment, an inline plunder-blessing ("every skill works standalone — take what you want"), and the one-line `npx skills add doodledood/manifest-dev --skill figure-out` install.
- **Naming splits by surface**: the README headline stays harness-generic (multi-CLI is a real differentiator on the identity surface); query-capture pages, GitHub topics, and directory listings use harness-specific language ("claude code …"), because strangers search their harness's name.
- **The define/do loop is the House, not a footnote**: it is the other half of the value and the retention engine. Below the fold, the README presents the full understanding-first loop as the destination the Door opens into (the "loop was never the hard part" essay belongs there), and `/figure-out`'s in-product handoff to `/define` remains the organic upsell.
- **No new build gates distribution**: metadata, README surgery, directory submissions, and query pages proceed immediately on existing skills.

## Alternatives Considered
- **`verify-lite` wedge (the handoff report's recommendation)**: a new standalone verify skill fronting the "says done but isn't" pain, gating all distribution — Rejected: the surface is now occupied first-party by Claude Code's bundled zero-setup `/verify` (plus a crowded third-party field); days of build to enter last, and the gating sequenced real distribution behind an unnecessary artifact. The report predates this ecosystem fact.
- **`/babysit-pr` as the Door**: its pain surface is demand-proven (the report's own comparable, `a5c-ai/babysitter`, reached ~20× manifest's stars via directory placement) — Rejected as identity: an incumbent owns the surface and it isn't the repo's differentiated core. Kept as a secondary grab on directory listings.
- **Methodology-first front door (status quo README)**: Rejected — it is the diagnosed failure shape: enrollment demanded before value is felt, producing praise instead of adoption.

## Consequences

### Positive
- Distribution work is un-gated immediately; nothing waits on a build.
- The repo fronts its genuinely differentiated asset (an adversarial understanding partner) rather than competing with a first-party default.
- Fronting the Door and watching install/clone/conversion behavior is the cheapest available test of the biggest open question — whether the value transfers to strangers at all (currently N≈2).
- Owner conviction and door choice align, which sustains the follow-through the plan needs.

### Negative
- `/figure-out`'s 60-second feltness for strangers is unverified; if fronted and installs don't convert, artifact shape must be reopened rather than pushed harder.
- A harness-generic headline sacrifices some search capture on the identity surface — accepted, mitigated by harness-specific capture pages.
- Two-door-plus-house presentation must be maintained so the House doesn't decay into a footnote (the maintainer's explicit concern).

## Source
- Session: figure-out adoption-strategy session, 2026-07-05 (log: `~/.manifest-dev/logs/figure-out-log-20260705-054411.md`)
- Amends the recommendation of the external 2026-07-04 handoff report (originating KB: `docs/adr/20260703-manifest-verify-lite-wedge-two-door.md` in that KB, not this repo)
- Related: 20260705-keep-plugin-first-layout-npx-skills-compatible
