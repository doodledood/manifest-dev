# Real-site calibration —2026-10-07

This work calibrates instruments against human-labeled screenshots and recorded search tasks before interpreting a new design trial. It does not establish design-skill uplift. Supplied artifacts remain the runtime boundary; all acquisition belongs to the caller. No source assets, participant records or private product material ship here.

## Appearance

[1506 website screenshots](https://doi.org/10.7910/DVN/XEYNYW), CC0, six source collections. Five separate human first-impression axes are retained. Fit AVI_14/CHI_13/CHI_15 (565 images), select on IJHCS_12 (184), evaluate CHI_20/ICWE_19 (756 after an exact duplicate exclusion). Exact pixels, dHash/pHash and thumbnails screen duplicate overlap; source-separated anonymous IDs cannot certify independent brands/templates. One within-test template pair shares a bootstrap group.

`site-calibration.py` separately extracts, tunes and evaluates. Every step freezes input/source hashes; a final-label marker precedes reads and remains even after failure. Ridge candidates vary scale/edge threshold, native descriptors, quadratic terms, regularization, and published AIM descriptors. Means/scales fit training only; development chooses candidates without refitting. AIM was pinned at `89cee07f5809a7fb26d11d16822ed0738318b377`; its descriptors use512px maximum-edge views here, not a published-resolution replication. Colorfulness's duplicate scaled alias is excluded from combined fits. The simpler native model is a predeclared comparator, not a new winner selected from final results.

| Native axis | Existing four-descriptor rank correlation | Refined correlation | Paired95% rank-gain interval | Decision |
|---|---:|---:|---|---|
| Complexity | .448 | .555 | [.068,.149] | Optional first-impression estimate |
| Aesthetic appearance | .369 | .445 | [.057,.097] | Experimental ranking hint |
| Craftsmanship impression | .406 | .467 | [.035,.088] | Experimental ranking hint |
| Novelty impression | .463 | .559 | [.072,.122] | Experimental ranking hint; no preferred direction |
| Technical-condition impression | .287 | .310 | [-.022,.067] | Withhold; rating error worsens |

All four retained axes improve ranking within both reserved source collections; absolute rating error is less consistent. Selected AIM+native correlations exceed native by only .001–.004, without a direct paired comparison establishing incremental value. Native complexity/novelty mean absolute errors improve; appearance/craft error gains remain uncertain. Native craftsmanship error worsens on CHI_20 despite its ranking gain. The profile therefore exposes separate estimates, not universal ratings or an overall UX score.

[Appearance report](results/appearance.json) retains all selected/native, source, error and uncertainty results. Confidence intervals resample image/duplicate groups, omit systematic rater variation, and are nominal without multiplicity adjustment. Random halves of observed ratings are descriptive agreement, not participant-blocked reliability or a predictive ceiling. Pair accuracy uses human means separated by at least 1 point; pairs share images and are not independent observations.

## Independent full-page transfer

[Banks](https://doi.org/10.7910/DVN/Z7KLIH), [ecommerce](https://doi.org/10.7910/DVN/9FKSQI), [universities](https://doi.org/10.7910/DVN/XOI0HI), CC0, study published 2024. Select140 metadata image filenames per collection by SHA256(`calibration-v1:filename`) before rating analysis:420 actual full pages. Frozen models are assessed without fitting to those labels. Both full-page and top900px crops were declared before evaluation; retain both rather than choosing by final performance. No exact/near pixel candidates matched the earlier corpus; unknown brand/template overlap remains.

Native appearance rank correlation is .290 full-page and .370 top900; the earlier model is .142 and .367 respectively. The full-page gain has paired interval support within all three genres; top900 refinement gain remains uncertain. The selected AIM+native version is .218 and .383. Perceived ease and trust axes show weak exploratory associations and are not actual task usability/trust. Labels are participant-standardized, so the 1-7 model outputs are compared by rank, not incompatible absolute-error scales. Full-page downsampling can erase text. See [external report](results/external.json).

## Recorded target search

[VSGUI10K](https://osf.io/hmg9b/), [primary code](https://github.com/aalto-ui/VSGUI10K), CC BY4.0. Website-only present-target trials follow the author aggregation: participant/block/image/target maximum recorded TIME, excluding nonpositive durations. Failed localization and long observations are retained by the source; the outcome is observed search duration, not verified time to a correct answer. Target and image scale convert to laboratory-monitor geometry (1920×1200); no physical phone claim.

Fit 106 old-source images/418 target-cue cells, development 76 images/337 cells, test 117 newer-source images/549 cells. All targets/cues for an image stay together; clean/ad variants and exact pixel duplicates are screened. Hash-select 20/84 held-out participants, excluded from fitting/development, for a stricter secondary check. Pixel/source grouping cannot certify all template/domain independence.

Cue-only control versus cue+target geometry was development-selected by log-duration error; global-image and combined arms remain separately frozen. The chosen model improves pooled correlation .269→.327, log error .564→.538 and absolute error2.470→2.407sec. Paired log-error improvement95% interval[-.041,-.011]; absolute-error interval[-.122,-.004]. Gains concentrate in image cues. Text/text+color cue gains are uncertain. On unseen participants and screens, log error improves .673→.639, but rank/seconds-error gains are uncertain. The combined arm's better final score does not replace the development-selected winner. See [search report](results/search.json).

The weak, task-specific transfer and lack of verified success do not justify a general search-time runtime predictor. Supplied target geometry remains an observation instrument.

## Known barriers and applicability

[W3C's Before and After Demonstration](https://www.w3.org/WAI/demos/bad/) provides author-annotated accessibility barriers and repairs. Four paired HTML pages expose missing alternatives and naming candidates. Real source checks caught select options/textarea values being mistaken for names and missing image alternatives inside links. The refined source parser removes those errors: missing-name candidates before/after are8→0 home,5→0 news,5→0 tickets,17→0 survey; absent image-alt attributes33→0,39→0,26→0,24→0. These are annotated demonstration facts, not population outcomes or complete accessibility certification. Source names remain candidates, with no CSS/accessible-tree execution. [Results](results/source-candidates.json).

Retired design-reference catalogs from commit `3fc997a5` supply development stress cases. Current Family/Paper animation phases change pixels without being design revisions; an explainer's intentional detail can increase complexity while carrying its subject. Comeau/Samwho introduction screenshots do not exercise their interactive teaching. Active Theory's unsupported-browser fallback is excluded from quality comparisons. Historical approval, current capture, synthetic edits and independent human ratings remain distinct.

A new frozen-profile trial on a genuine landing keeps the prior preferred revision. It exposes more product evidence and therefore scores as more complex. Two safe chrome reductions offer negligible/inconsistent gains; visual review retains the incumbent. Hiding the proof reduces phone complexity3.858→2.760 while deleting needed content and reducing named co-visibility4/4→2/4; it is rejected. No real product was changed, and no new human outcome or causal uplift is inferred.

## Reproduction and reporting repairs

Use a caller-owned directory for data and outputs, plus Pillow, NumPy, SciPy, scikit-learn and (only for AIM comparison) OpenCV/pydantic with an explicit AIM checkout. Native shipped estimates need Pillow and the standard library, not these research dependencies. Run `site-calibration.py extract|tune|evaluate --out ...`; extraction takes `--images`, `--ratings`, optional `--aim`, and `--workers`. Search uses `search-calibration.py prepare|tune|evaluate --out ...`, with `--data` on preparation. External checks use `external-calibration.py extract|evaluate --root ...`, with `--models` and optional `--aim` on extraction; the root contains the fixed sample, plan, images and published average-rating files. Help/docstrings state the input boundary. Preserve source/plan/model/input hashes and all unfavorable results.

The first search report failed on undefined Spearman for exactly constant predictions; the first external report rejected an identical duplicate published rating row. Models and inputs remained frozen. Report-only recovery represented undefined correlations as null and collapsed identical selected-ID rows, rejecting conflicts. Original consumed-label markers and frozen sources were preserved; no fitting/reselection occurred. Committed scripts fix these reporting faults for future runs. This is recovery of consumed holdouts, not a fresh test. Current script hashes consequently differ from the archived sources named in the result freezes.

The full real-site corpus is now known regression evidence. Any further metric tuning needs a new reserved evaluation set. Purpose, meaning, typography, motion, learning, emotion, physical delivery and the other concerns in the [basis map](../../claude-plugins/manifest-dev/skills/design/references/instruments/basis.md) remain in scope without invented quality grades. Their tools measure supplied facts; claiming a general quality predictor requires separate construct-specific outcome evidence.
