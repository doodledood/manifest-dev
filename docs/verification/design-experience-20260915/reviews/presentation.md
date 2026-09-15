# Blind presentation review

Independent fresh-context review; labels were hidden until this verdict was returned. This is the review response with local evidence paths normalized; its wording and findings are preserved. The operator separately ran the checker with working Chromium; see the main report for combined coverage.

**A:** candidate | **B:** intermediate | **C:** baseline | **D:** baseline-repeat

## Verdict

**Preference: C, then B ≈ D, then A — moderate confidence.**

Reviewed as a **five-slide, 90-second projected proposal with later phone reading**. All four sustain a truthful bounded-pilot argument. I found **no CRITICAL or HIGH defect, and no MEDIUM-level failure established within the inspected scope**. The differences are principally information design, pacing, and small-screen convenience—not basic correctness.

Screenshots referenced below are in `../screenshots/review-presentation/`. No HTML or repository files were changed.

## A — Strong opening and safeguards; heavier finish

**Gains**
- The oversized, two-color opening gives “two more hours / six Saturdays” clear priority. The hatched extension distinguishes proposed hours without relying on color alone, while preserving the correct **4:2 duration ratio**. See `../screenshots/review-presentation/A-desktop-1.png`.
- The dark cost slide creates a useful pause. The following staffing slide makes interested volunteers versus confirmed coverage particularly explicit.
- Evidence limitations stay attached to their respective figures; neither survey responses nor visits are presented as demonstrated post-14:00 demand.

**Losses**
- The sequence devotes separate slides to money and staffing, then introduces all three learning activities alongside authorization on slide 5. That makes the ending carry more new information than B or D’s ending. It remains coherent, but is a less evenly paced 90-second argument. See `../screenshots/review-presentation/A-desktop-3.png` through `../screenshots/review-presentation/A-desktop-5.png`.
- It communicates the evidence mainly through large numbers and explanatory text; C makes the crucial measured/unmeasured distinction visible.

**LOW — phone return effort.** `../samples/candidate-presentation.html` hides `.slide-jumps` below 850px. At 390px, returning from the decision to evidence requires three Back actions; the other variants retain direct slide selection. Position remains visible and the sequence is not lost. Retaining compact numbered controls would remove this friction.

Phone slides 2 and 5 require scrolling; their final qualifications and continuation decision were reachable. See `../screenshots/review-presentation/A-390-2-scrolled.png` and `../screenshots/review-presentation/A-390-5-scrolled.png`.

## B — Balanced proposal structure and economical phone adaptation

**Gains**
- The progression—proposal → evidence → cost/readiness → learning → decision—separates explanation from the final authorization.
- Gold first identifies the added hours, returns as the measurement window, then fills the closing slide. That creates continuity around what trustees are being asked to test, rather than an arbitrary palette change.
- Cost and staffing are together. At 390px, both the volunteer uncertainty and start condition fit on slide 3; the complete authorization also fits on slide 5.
- Only the evidence slide requires scrolling at 390px, by approximately **94px**.

**LOW — projected focus treatment competes with composition.** Arrow-key navigation moves focus to the heading and draws a large rectangular outline around it. This is visible across `../screenshots/review-presentation/B-desktop-2.png` through `../screenshots/review-presentation/B-desktop-5.png`, adding a prominent frame that is absent on initial arrival. Preserve accessible focus, but use a less visually dominant treatment for the programmatically focused heading.

**Behavioral trade-off:** B alone restores each slide’s previous scroll position. That helps resume phone reading, but returning to a scrolled evidence slide can leave its heading partly above the content viewport. I reproduced this twice. The slide number remains correct, and scrolling restores the heading; this is not lost sequence.

Compared with C, its evidence gap is explained rather than strongly pictured. Compared with D, its compact six-part cost strip consumes less phone space.

## C — Preferred: the evidence gap drives the whole argument

**No graded defect established in the tested sequence.**

**Gains**
- The strongest information-design decision is slide 3: **400 observed visits beside an explicitly unmeasured “?”**, with both two-hour windows labeled. The graphic does not turn missing evidence into zero or imply that existing visits predict later demand. See `../screenshots/review-presentation/C-desktop-3.png`.
- Separating survey interest from the door-count limitation earns its two slides: the sequence moves from a reason to investigate to the specific unanswered question.
- The survey’s 60% band is faithful to 72/120, and its nonrepresentative-sample qualification receives substantial visual weight.
- The paper/ink treatment, serif typography, proportional hours band, dark evidence-gap slide, and gold authorization form a coherent civic/editorial direction.
- **All five slides fit at 390×844**, including evidence qualifications, cost, staffing uncertainty, and the learning plan. At 320px, the two time windows deliberately stack rather than squeezing their contents.

**Losses / boundary**
- Slide 5 does not repeat the confirmed-staffing start condition. Slide 4 states it clearly immediately beforehand, so the actual sequence remains conditional; I do **not** treat every slide as a standalone contract. Nevertheless, B and D have more self-contained final authorization screens. C’s final slide should not be detached and used alone as the complete approval record.
- At 320px, slides 3–5 need scrolling; the closing slide needs roughly 163px. All lower content remained reachable. See `../screenshots/review-presentation/C-320-5-scrolled.png`.

C wins because its strongest visual distinction expresses the reason for a pilot—not merely the proposal’s quantities.

## D — Strongest final terms; useful graphics with some phone overhead

**Gains**
- The six equal cost slips give the total a concrete, inspectable construction: six Saturdays at $180.
- Slide 4 visually gathers visits, feedback, and staffing feasibility into one continuation decision. On phones it becomes a readable vertical sequence without preserving unnecessary connector geometry.
- The final dark slide is especially complete: duration, opening hours, $1,080, staffing prerequisite, and review requirement remain together at 390px. See `../screenshots/review-presentation/D-desktop-5.png` and `../screenshots/review-presentation/D-mobile-5-matched-reduced.png`.
- Its restrained typography and closing emphasis provide a coherent encounter without requiring animation.

**Losses**
- The six individually labeled cost slips repeat information already supplied by “Six Saturdays × $180.” At 390px they become two rows and push the volunteer-availability detail below the initial viewport. About **146px of scrolling** exposes the full lower section. The heading already says “Confirm staffing first,” so the prerequisite is not absent, but the repetition has a visible adaptation cost. See `../screenshots/review-presentation/D-mobile-3.png` and `../screenshots/review-presentation/D-390-3-scrolled.png`.

**LOW — crowded time labels at 320px.** On slide 1, the rendered boxes for “14:00” and “16:00” have only **2.83px** between them, making the times run together visually (`../screenshots/review-presentation/D-320-1.png`). Slightly smaller narrow-screen time labels or a recomposed axis would separate them without changing the scale.

B and D are effectively tied: B is more economical on phones; D gives the learning relationship and closing terms stronger visual form.

## Verification, motion, and limits

- Exercised all five slides; completed two forward/backward keyboard circuits and two previous/next pointer circuits per variant. Tested Home/End boundaries twice, button focus/Enter activation, direct arrival at slide 3, reload, and browser Back/Forward. Position and active slide stayed synchronized.
- Inspected **1440×900, 390×844, and 320×844**. Checked lower scroll content; no horizontal overflow was measured.
- All four preserve the supplied evidence limitations, **$180 × 6 = $1,080**, unconfirmed volunteer availability, confirmed staffing before starting, and a review before continuation.
- **Motion:** navigation is immediate. All 40 matched normal/reduced-motion screenshot pairs were byte-identical. No transition delay or active animation was observed. Stillness is appropriate here, not a missing feature.
- No runtime errors or external resource requests were recorded. Sampled rendered text-color checks found no contrast failure; that is not a complete accessibility audit.
- Both standard checkers reported zero findings, with manual-review notes and skipped automated renders. The browser review supplied the rendered evidence; the checker result was not used as a clean bill of health.
- **Unverified:** actual projection distance, lighting, physical-phone touch behavior, 200% text resizing, screen-reader announcements, and audience comprehension or delivery timing.

## Old/new standards

**No verdict difference survived application of the brief.** A literal headlines-only or word-budget reading of the older guidance could over-penalize A’s shorthand and necessary qualifications. The actual sequence—not mandatory assertion syntax—governed this comparison. Likewise, spacing-value counts and absence of motion did not become defects without an observed consequence.
