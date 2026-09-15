# Design-skill pilot: less instruction, no demonstrated quality gain

**The original-skill sample was preferred in all three blind reviews.** The revised package is substantially smaller, but this pilot does not establish better design. The repeat original-skill samples also lost to the first originals in all three briefs, so preference alone does not separate skill effects from generation variation.

[Open the working comparison gallery](index.html). Each sample is an unedited, offline HTML page, not just a screenshot. Try the controls before reading the [landing](reviews/landing.md), [analytics](reviews/analytics.md), and [presentation](reviews/presentation.md) reviews. These are fictional test artifacts, not production products.

## What changed

The builder starts with the person encountering or using the artifact: their purpose, path or repeated work, information needed together, intended feeling, and delivery conditions. Form follows that account. Art direction, information design, and interaction design remain complementary; animation and minimalism are not requirements. The reviewer judges task fit before surface treatment.

The old numbered procedure and broad craft library became an experience-led core with three conditional references. Word counts include frontmatter and use whitespace splitting; they are not model-token or cost measurements.

| Surface | Original | Revised |
|---|---:|---:|
| Core | 3,269 | 1,031 |
| Reachable references | 6,353 | 1,228 |
| Entire instruction package | 9,622 | 2,259 |

The core is about 68% shorter and the full package about 77% shorter. This is a load reduction, not a quality score. The [decision record](../../adr/20260915-design-keeps-experience-goals-and-conditional-constraints.md) explains the architecture and its risks.

### Reference audit

| Original surface | Disposition and grounds |
|---|---|
| `craft.md` — 2,515 words | Removed the general composition, type, spacing, and motion manual. Retained coherent direction, a compact system, representation choice, and actual motion inspection in the core. Those outcomes have task/consistency grounds; the full recipe catalog had no comparative prompt-effectiveness evidence. |
| `registers.md` — 1,640 | Removed the genre taxonomy and fixed recipes. Preserved the consequential projected-talk versus standalone-reading distinction in `experience.md`; genre and use context still govern review. |
| `calibration.md` — 135 | Removed the dated style catalog. References may still inform a concrete design choice; they are not a universal house style. |
| `floors.md` — 799 → 514 | Retained access measurements with levels, units, and exceptions; keyboard/focus, dynamic state, recovery, motion alternatives, and language/direction checks. These are constraints, not evidence that a particular prompt formulation works. |
| `figures.md` — 575 → 292 | Retained representation choice, faithful scales, uncertainty/missingness, and equivalent access. Removed implementation tutorial material. The earlier figureless-memo failure supports the representation outcome, not a compulsory illustration per claim. |
| `experience.md` — 689 → 422 | Retained state continuity, consequences, and actual-host verification. Removed the broad medium catalog while keeping distinctions that change the work or its verification. |

The relevant prior observations and their boundaries are recorded in the ADR's Source section. Research provenance and instruction efficacy are different questions; this pilot settles neither every retained line nor every deletion.

## Method and frozen inputs

Twelve outputs cover three fixed briefs: [Relay landing](briefs/landing.md), [Harbor analytics](briefs/analytics.md), and [Alder Library presentation](briefs/presentation.md). Each has four samples:

| Filename prefix | Package and generation |
|---|---|
| `baseline` | Original package at commit `160acfc3`; first generation. |
| `baseline-repeat` | The same original package; a fresh generation in the later batch. |
| `intermediate` | New core with the old reference library, apart from a repaired task-model pointer. This is **not** a no-reference control. |
| `candidate` | Final core and three rewritten references. It also includes two core clarifications and changed loading pointers, so it is **not** a clean ablation of reference removal. |

All used `openai/gpt-6-astra`, fresh contexts without the design discussion, a 12-turn limit, and the same [generation contract](briefs/generation-contract.md). Only file reads were used. Generators returned one complete HTML file plus a design note; they could not render, repair, fetch assets, or write files. The operator extracted the fenced HTML and added a trailing newline, then froze it. No sample received a post-generation edit or a retry selected for quality.

This tests generation under supplied instructions, **not the skill's complete autonomous build–verify–repair loop**. There was no seed pairing, cross-model replication, or audience study. Original-repeat and final outputs share the later generation batch. The probes were written after the first original/intermediate outputs existed and before inspecting final/repeat outputs; [probes.md](probes.md) discloses that potential anchoring. This is not a held-out benchmark.

[inputs.json](inputs.json) holds package/brief hashes and the blind mapping. Each JSON file in `generation/` records its actual model, times, reads, artifact hash, and the exact generator note in `design_note`. Notes are JSON strings so intentional Markdown trailing spaces survive without disabling whitespace checks. Effective instruction words read, rather than the entire available library:

| Brief | Original | Original repeat | Intermediate | Final |
|---|---:|---:|---:|---:|
| Landing | 7,272 | 7,407 | 6,726 | 2,259 |
| Analytics | 7,847 | 7,847 | 7,301 | 2,259 |
| Presentation | 9,487 | 9,487 | 7,301 | 2,259 |

Three independent reviewer contexts received opaque A–D copies, the brief, and both original and revised review standards. They did not receive the generation notes or arm mapping before returning their verdicts. They rendered and exercised the artifacts, then judged against the brief and observed consequences where the standards differed. All three reported no verdict difference attributable solely to the choice of ruler. One reviewer per brief and moderate-confidence preferences are not independent audience evidence.

## Findings in actual use

| Brief | Gains in the final sample | Losses and preferred sample |
|---|---|---|
| Landing | Clear explanation of receipt versus completed work; coherent stationery treatment; reversible local feedback works. | More enclosing layers, smaller project text, and another explanatory section. Original fits offer, full sample, action, receipt, and commercial terms together at desktop size. Ranking: original → repeat → final → intermediate. |
| Analytics | Cohesive ledger treatment, truthful numerator/denominator pairs, complete outcome breakdown, and a useful phone detail jump. | Spacious rows and repeated local axes increase comparison scrolling. Original provides the strongest desktop co-visibility. Final and intermediate are close alternatives; repeat has the clearest keyboard defect. |
| Presentation | Strong opening, proportional hours diagram, explicit cost and staffing safeguards. | Learning activities arrive with authorization on a heavier final slide; phone direct-slide controls are hidden. Original makes the key evidence gap visible: 400 observed visits versus unmeasured later demand. Ranking: original → intermediate ≈ repeat → final. |

Two MEDIUM findings occurred outside the final samples and remain unfixed in the evidence:

- **Intermediate landing:** acknowledgement text changes but its SVG clock/check icons do not. Setting a `.hidden` property on those SVG elements fails to change the attributes controlling their visibility. [Acknowledged state](screenshots/review-landing/D-received.png).
- **Repeat-original analytics:** phone arrow-key selection can change the route while its visible name/rate/change remain below the viewport; scrolling follows the clipped radio rather than the substantial visible row. [Focused state](screenshots/review-analytics/C-ordinary-route-focus.png).

No MEDIUM-or-higher final-sample finding was established in the inspected scope. That is not proof of superiority or complete accessibility. The final presentation's missing phone jump controls are a LOW convenience loss; its argument and previous/next navigation remain usable. Other LOW findings and trade-offs are preserved in the individual reviews.

### Investigating the recurring shifts

The source shows a clear implementation change: **all six original-package samples use a multi-step named spacing scale; none of the six new-core samples do.** Original samples define 7–9 such values and reference them 74–98 times. One intermediate declares a single unused spacing value; some new-core samples share layout gutters. They still use palette/type roles and reusable CSS rules, so this is not evidence that they have no design system.

The likely mechanism is the core's removal of an explicit token-declaration/audit procedure; the shift already appears in the intermediate, before reference removal. The [source and layout measurements](observations/source-and-layout.json) preserve the counts. This loss of explicit spacing discipline may matter for maintenance. It was investigated rather than counted automatically as a visual defect: all three rendered reviews found no corresponding material system-drift finding, and no maintenance task was tested. The rewrite retains the compact-system obligation without restoring a token-only rule. Repeated visual drift or higher update cost in maintained artifacts would overturn that choice.

The felt-experience losses are less uniform. Landing height at 1440px is 1,474/1,476px for the originals versus 1,774px final and 1,861px intermediate; rendered-document word counts are 221/230 versus 265/290, including text below the viewport. The longer explanation is real. Analytics final height, 1,180px, falls between the two originals' 1,061 and 1,191px. Final contains fewer words than either original, but more than the intermediate: 274 versus 266. Its phone comparison region is nevertheless taller, as the review documents. Total page extent and local comparison effort are different measures. Presentation uses fixed viewports; its final phone control count drops to two where the other samples retain direct slide choices.

No common material functional regression was established across the final samples. Nor was quality equivalence established. The branch keeps the smaller instruction architecture as a **reviewable, reversible choice**, exposes its losses, and retains the stronger original artifacts. It does not claim that lower instruction load improved design. Generating more until a preferred final appeared would not resolve this pilot's uncertainty.

## Verification and limits

- All twelve were rendered at 1440×900 and 390×844 and checked for applicable 320px reflow. [Initial geometry and content](observations/) and matched starting screenshots are preserved. No page-width overflow was measured.
- Reviewers exercised pointer/keyboard paths and repeated actions, ordinary and reduced motion. Analytics covered all six route/cohort combinations with consistent rates, counts, and labels. Landing acknowledgement/undo worked textually in all samples, with the intermediate icon defect above. All five-slide sequences navigated correctly.
- Analytics and presentations changed state immediately. The presentation reviewer captured 40 normal/reduced-motion pairs; [their recorded hashes](observations/presentation-motion-pairs.json) match byte-for-byte. The pair IDs identify matched-mode captures, separate from the earlier interaction screenshots cited in the reviews. Final/intermediate landing pages used brief travel/color transitions; reduced motion preserved state and recovery. This is not evidence that motion generally helps or hurts.
- Offline operation, browser errors, and external requests were checked by the reviewers; no runtime error or external request was reported. Facts, denominator semantics, and evidence limitations survived the exercised paths.
- The operator ran the existing HTML checker with installed Playwright/Chromium on every output: [checks](checks/) contain zero automatic findings, manual-review notes, and explicit skipped paint/inactive-control cases. Reviewer-local checker attempts lacked Playwright; their separate browser sessions provided the interaction evidence. Neither checker result is an accessibility certificate.
- **Unverified:** screen-reader announcements, 200% text enlargement, forced colors, physical touch, other browser engines, real projection distance/lighting, timed human delivery, audience comprehension/recall/conversion, and non-HTML media. Ordinary browser operation does not settle these.

## Reproduce or extend

Open `index.html` locally, or serve this directory with `python3 -m http.server 8768 --bind 127.0.0.1` and visit `http://127.0.0.1:8768`. No build or network asset is needed.

Reconstruct the original `design` directory from `160acfc3:claude-plugins/manifest-dev/skills/design`. For the intermediate, copy that directory, replace `SKILL.md` with `snapshots/intermediate/core.md`, and overlay the archived `references/` file. Restore `scripts/design-check.mjs` by decompressing `snapshots/intermediate/scripts/design-check.mjs.gz`. The archive preserves the frozen checker's bytes, including trailing whitespace; the core is named as evidence, not as another installable skill. The final package is this branch's source `design` directory. Confirm their files against `inputs.json`; the checker is included in snapshot identities but was not read by generators.

Run `python3 verify.py` from this directory to check frozen input/output identities and local gallery/report links. This integrity check does not rerun browser or design tests.

For each brief, give a fresh context the unchanged generation contract, brief, and assigned skill path, with the recorded model/turn limit and read-only capabilities. Preserve the response before inspection; do not silently repair or choose among retries. Record actual reference reads. New generations are replications, not byte-for-byte reproduction without a fixed sampling seed.

Run `node <design-skill>/scripts/design-check.mjs <sample.html>` where Playwright is installed; `DESIGN_CHECK_CHROMIUM` can select an existing Chromium executable. Then apply the behavioral probes in a real browser. To extend the evidence, use new briefs or maintained-artifact update tasks with independently chosen criteria—not just more attempts to reverse these rankings.
