# Blind analytics review

Independent fresh-context review; labels were hidden until this verdict was returned. This is the review response with local evidence paths normalized; its wording and findings are preserved. The operator separately ran the checker with working Chromium; see the main report for combined coverage.

**A:** intermediate | **B:** baseline | **C:** baseline-repeat | **D:** candidate

## Verdict

**B is my narrow preference for this repeated-use ferry analytics brief. A and D are close alternatives with different costs; C has the clearest interaction defect.** Confidence is **moderate** in that preference and **high** in the verified numerical consistency.

All four render a coherent, usable analytical view—not placeholder cards. None showed a critical failure, misleading quantitative scale, stale displayed measure, or fabricated explanation for delays.

**Evidence:** HTML files are under `../samples/`. Fresh screenshots and interaction records are under `../screenshots/review-analytics/`; screenshot names below refer to that directory.

## What held across all four

I rendered **1440×900, 390×844, and 320×844**, selected all three routes in both cohorts, returned between cohorts, and repeated keyboard interactions with ordinary and reduced-motion preferences.

- **Arithmetic and state stayed consistent.** For example, Weekend/East Bank showed **84/96 = 87.5%, −3.5 percentage points from 91%, three cancellations** everywhere applicable. A and D additionally showed the correctly derived nine late arrivals.
- Initial state was Weekday/West Pier. Cohort changes retained the selected route in these samples, while the investigation recommendation changed to East Bank for Weekend. Recommendation and selection remained separately labeled.
- All preserved sample-data status, the scheduled-trip denominator including cancellations, and the absence of causal evidence.
- The comparison bars used shared **0–100% scales**, with prior-period markers and exact values. No consequential truncation or inconsistent mapping found.
- All worked offline; no page errors or external resource requests were observed.
- No horizontal overflow was detected at 320px. That is not a complete accessibility certification.

## A — compact and calm, with weaker detail navigation

**Gains**

A has the shortest phone comparison region of the four: roughly **523px**, versus B’s 646, C’s 685, and D’s 912 in the tested Weekend state. Its route, rate, change, scheduled volume, and prior rate stay tightly grouped without feeling cramped. At 320px, route names and numerical columns remain intact.

The serif headings, restrained navy, ferry mark, and ruled surfaces form a credible harbor-operations identity. The dark detail panel clearly separates inspection from comparison. Its outcome bar and count table distinguish late arrivals from cancellations; the cancellation pattern supplies an additional visual distinction.

**LOW — navigation/use cost.** At 390px, selecting a route updates the detail below the comparison but provides no direct route-detail link. After selecting East Bank by keyboard and advancing through the remaining controls, focus left the page controls while the detail still began below the viewport. The task remained possible through scrolling, but inspecting counts required a separate navigation step without a shortcut.

- **Evidence:** `../screenshots/review-analytics/A-ordinary-route-focus.png`, `../observations/review-analytics/A-ordinary-navigation.txt`; route handlers in `../samples/intermediate-analytics.html:1237`.
- **Improvement:** offer an explicit, correctly labeled detail jump without forcing every route selection to move the viewport.

**Losses relative to B/D:** the comparison rows show scheduled volume rather than the on-time numerator/denominator pair; the latter requires detail inspection. This is a valid trade-off, not missing data.

## B — best overall balance

**Gains**

B puts the operational loop into the strongest desktop grouping. At 1440×900, all three comparisons, the selected route’s counts, the rate calculation, and cancellation-denominator explanation fit together. The joined comparison/detail surface makes their relationship particularly clear.

The priority strip is actionable: **“Inspect East Bank”** both selects the recommended route and moves focus toward its detail. Visible radio controls communicate selection directly; arrow-key route selection works. The compact heading area gives more space to evidence than the other variants.

Its serif display type, naval header, rust decline signal, and restrained chart rails are distinctive without competing with the numbers. Numerators and denominators appear in each comparison row.

**LOW — detail jump stops short of the complete inspection.** On the 390px keyboard path, activating “East Bank details” focused the heading but left it around mid-screen. Scheduled and on-time counts appeared near the bottom, while cancellations and the denominator explanation still required another scroll.

- **Evidence:** `../screenshots/review-analytics/B-ordinary-detail-navigation.png`, `../observations/review-analytics/B-ordinary-navigation.txt`; `../samples/baseline-analytics.html:1201–1202`.
- **Improvement:** after focusing the detail heading, position the detail region nearer the viewport’s start so the available height exposes its counts.

**Losses:** the priority action adds height on phones. B omits A/D’s late-arrival breakdown and outcome graphic, although those additions are not required by the brief. Its full-width rails are less compact than C’s desktop matrix.

## C — strongest desktop matrix, weakest narrow-screen keyboard path

**Gains**

C’s desktop comparison is the most table-like: route identity, bar, current/prior rate, and change form aligned columns. The heavier bars and explicit column headings make the comparison field more visually substantial than B’s thin rails. Cancellation counts are available for all routes without selecting them.

The navy detail panel and teal marks are consistent and readable. Its detail anchor works particularly well: it brings the complete selected-route panel into the phone viewport, with visible focus.

**MEDIUM — keyboard selection can leave the newly selected route’s evidence offscreen.** Starting at 390×844, I tabbed into route selection and pressed ArrowDown to select East Bank. State updated correctly, but the viewport stayed at the page top: only the beginning of East Bank’s focus outline appeared at the bottom. Its name, rate, and change were below the viewport.

The focusable radio is a clipped 1px element; the visible label occupies the substantial row. Browser scrolling follows the small input rather than ensuring the visible row is exposed.

- **Evidence:** `../screenshots/review-analytics/C-ordinary-route-focus.png`; reproduced in reduced motion, with correct selected state recorded in `../observations/review-analytics/C-reduced-keyboard.txt`. Relevant styling: `../samples/baseline-repeat-analytics.html:113` and `../samples/baseline-repeat-analytics.html:264`.
- **Improvement:** keep native radio semantics while ensuring the visible selected row is scrolled into view on keyboard navigation.

**Losses:** at 320px, the three-column row squeezes route metadata into multiple lines—“8” above “cancellations,” and “North Quay” wraps. Nothing disappeared, but the comparison became taller and more fragmented than A/B/D. Scheduled volumes are available in detail rather than alongside the cancellation counts.

## D — strongest unified visual identity, most spacious comparison

**No MEDIUM-or-higher defect found in the exercised scope.**

**Gains**

D’s green ink, warm paper, serif route headings, circular ferry mark, and restrained ledger treatment form the most unified visual direction. Unlike the other variants’ dark detail panels, its lighter detail surface keeps comparison and inspection at similar visual weight.

It preserves numerator/denominator pairs in the comparison and supplies a complete outcome ledger in detail. The phone detail link brings route, cohort, rate, prior-period change, all counts, and denominator explanation into one viewport.

- **Evidence:** `../screenshots/review-analytics/D-desktop-weekend-east.png`, `../screenshots/review-analytics/D-ordinary-detail-navigation.png`.

**Losses:** D spends the most vertical space before and within the comparison. At 1440×900, North Quay sits against the lower edge; on the phone, repeated per-route axes, previous-rate captions, and spacious rows increase scrolling. Those repeated axes preserve local context, so this is a cost/benefit trade-off—not a requirement to adopt another layout.

Its secondary labels are smaller than C’s. They remained readable in the inspected renders, but provide less enlargement headroom.

## Behavior, motion, and remaining boundaries

- Pointer selection and keyboard cohort/route changes worked across all four. Selection styling and labels changed together.
- **No authored animation was observed.** State changes were immediate; ordinary and reduced-motion runs preserved the same information and controls. Motion’s absence is appropriate here, not a quality penalty.
- Sampled text contrast against solid rendered backgrounds produced no failures. This did not exhaustively test graphical contrast, forced colors, or every focus state.
- **Unverified:** actual screen-reader announcements, 200% text-only enlargement, physical phone/touch ergonomics, and other browser engines. The design-check script completed but skipped its own rendered checks because Playwright was unavailable; the browser evidence above was gathered separately.
- Full-page captures were supplementary; viewport screenshots established clipping, focus, and navigation findings. No HTML was changed.

## Old versus current ruler

**No finding or ranking difference is attributable solely to the ruler.** Both support the numerical-fidelity, context, interaction, and rendered-evidence judgments above. I did not convert spacing-token counts, missing animation, or preferred layout patterns into defects.

The preference is a design judgment about these observed encounters—not evidence of human comprehension, preference, or general efficacy.
