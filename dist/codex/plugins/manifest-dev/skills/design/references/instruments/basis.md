# Research basis and judgment boundaries

This map covers design concerns across web interfaces, information graphics, documents, decks, games and expressive artifacts. An instrument measures a piece of the concern. It does not turn every guideline into a numerical rule.

| Concern | Available evidence | What still needs context or other evidence |
|---|---|---|
| Proximity, contiguity, common region, labels and connectors | Named geometry/competitors, co-visibility, declared temporal links | Intended meaning, useful comparison groups, optical grouping, causal explanation |
| Alignment, repetition, spacing and tokens | Selected box edges/dimensions, actual text/font properties | Intentional asymmetry, role consistency, optical fit, governing system |
| Hierarchy and reading layers | Type/action inventories, thumbnail/blur/grayscale views, local edge map | Where attention should go and whether it goes there; these views are not gaze maps |
| Density, externalized memory and expertise | Named task facts visible together, clipping, declared routes | Whether compactness or disclosure helps the particular task; no universal item/word budget |
| Copy, headings, labels, errors and information scent | Strings, candidate names, state traces, geometry | Meaning, specificity, honesty, tone, accessibility equivalents and appropriate repetition |
| Type, numerals, scripts and fallback | DOM advances/properties, multi-size/direction/text-scale views | Typeface voice, legibility, glyph quality, script coverage, actual fallback/swap and optical shaping |
| Color roles, contrast, dark mode and category distinctions | Supported samples and Chromium vision/theme previews | Complete paint coverage, meaningful redundancy, cultural conventions, gamut and comfort |
| Semantics, keyboard, focus, targets and forms | DOM candidates/attributes, pointer samples, supplied focus/recovery traces | Accessibility tree, assistive announcements, actual touch devices and standards exceptions |
| Responsive layouts, bidi, translation and mobile reach | Size/direction/text-scale probes, languages, clipping | Correct translations, mirroring exceptions, browser chrome/keyboards/notches, physical ergonomics |
| Data stories, quantitative encodings and provenance | Declared values/linear coordinates/ranges, units and source fields | Source truth, nonlinear/projection choices, uncertainty, equivalents and suitability of representation |
| Teaching, examples, dependencies and multimedia | Declared order/prerequisites, co-visibility, temporal overlap/exposure | What the learner knows, useful reveals, mental models and measured retention/transfer |
| Journeys, agency, continuity, conversion and trust | Declared paths plus actual supplied state/recovery probes | Unnecessary asks, motivation, anxiety, traffic, long-term outcomes and effects on other people |
| Motion, feedback, rhythm, interruption and endings | Active animation inventory, temporal declarations, repeated probes | Perceived smoothness, input-to-photon/frame time, comfort and expressive purpose |
| Imagery, icons, crop and documentary evidence | Asset dimensions/alternatives, images-off and small-size previews | Relevance, identity, truth, recognizability and actual delivery channels |
| Decks, posters, documents, email and physical delivery | Matched views, angular-size arithmetic, Chromium PDF export | Projection/print/reading distance, native page/slide hosts, actual email-client matrix |
| Games, explorables, spectacle and emotional encounters | Task/state traces, active motion and local visual descriptors | Fun, novelty, awe, delight, genre fit, remembered experience and repeated audience response |
| Outcome/evaluation validity | Known-fact checks, adversarial contrasts, separate response axes/missingness | Constructed fixtures and model reviews are not measured human performance or preference |

## Sources and scope

The computational foundations include [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [Gestalt grouping literature](https://doi.org/10.1037/a0029333), [cognitive load and multimedia learning](https://doi.org/10.1016/j.learninstruc.2010.04.007), and [HEART goals, signals and metrics](https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/). They support particular questions with their own scope, not a universal aesthetic score.

Image-based research supplies useful measurement candidates with population and artifact limits. [Reinecke and Gajos](https://www.eecs.harvard.edu/~kgajos/papers/2014/reinecke14visual.pdf) model website appeal using image properties and demographic context. This toolkit's descriptors do not reproduce their predictor or establish personal preference. [Visualization complexity research](https://arxiv.org/abs/2510.08332) finds that different properties work differently across visualization types. The local edge map here is adjacent-pixel variation; it is **not** [feature congestion](https://persci.mit.edu/research/clutter), whose published method is a different model. Likewise, [learned visual importance](https://arxiv.org/abs/1708.02660) is not interchangeable with our variation map. No learned gaze/importance estimator is bundled.

Numerical design conventions, practitioner examples and isolated experiment effects remain starting hypotheses in their original settings. Size/spacing scales, hue/font counts, word budgets, motion durations and aesthetic fashions do not become universal pass thresholds. Shortest paths can remove necessary safeguards; contrast alone can erase categorical meaning; fewer edges or words can remove essential facts. Real audience comparisons should keep outcome axes separate, record missingness, preserve unfavorable cases and distinguish owner preference from broad population claims.

The runtime guidance is intentionally narrower than a development research corpus. Evaluation fixtures and tuning history belong beside the development harness, so ordinary design runs load only the instruments relevant to the question.
