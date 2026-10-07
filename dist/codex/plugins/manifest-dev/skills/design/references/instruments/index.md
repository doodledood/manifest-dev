# Optional instruments

Use an instrument when a concrete design question would benefit from an observation. Choose the question and the relevant content from the brief; a tool cannot choose the goal for you. These tools are consultation aids. They have no required suite, score target, preferred direction for every number, or prescribed optimization loop.

| Question | Instrument | Evidence and limits |
|---|---|---|
| Are intended labels, references and competing items grouped as intended? | `geometry` | Named boxes, edge gaps in pixels/em, competitor margins, alignments; geometry does not establish meaning or optical alignment. |
| Can these facts be seen together at this moment? | `visibility` | Named viewport intersection, ancestor clipping and internal overflow candidates; usefulness and every paint occlusion remain contextual. |
| What happens to type, lines and numerals in this content? | `typography` | Text-node line estimates, actual font properties and DOM glyph advances; measures are neither recommended sizes nor comprehension. |
| What text, headings and actions compete for attention? | `copy` | Node-based counts, repeated strings and label inventory; repetition may be necessary and shorter may be less clear. |
| How do declared palette colors and relevant pairs compare? | `palette` command | Oklab/OKLCH, pair distances/contrast and ordered lightness; no generic safe-palette threshold or meaning. |
| What is the contrast of supported text paint? | `color` | Opaque ancestor-background samples with explicit exclusions; image/gradient/overlapping paint, exceptions and complete conformance are outside coverage. |
| What semantic, naming, language and form candidates need attention? | `access` | DOM candidates and attributes; use appropriate accessibility-tree and assistive evidence for names, reading order and announcements. |
| Do the detected controls receive the sampled pointer locations? | `targets` | Boxes and five hit samples per control; not complete hit regions, ergonomic prediction or automatic standards judgments. |
| Which media dimensions, crops and alternatives are present? | `media` | DOM asset inventory; relevance, equivalent meaning and documentary truth need judgment and provenance. |
| What animation is active in this state? | `motion` | Web Animations timing inventory; canvas/video, future triggers, smoothness and comfort are outside coverage. |
| Where does image variation concentrate? | `image` | Local adjacent-pixel edge map, histogram and colorfulness descriptors; not gaze, feature congestion, cognitive load or beauty. |
| What actually happens in a supplied interaction or recovery scenario? | `probe` command | Click, fill, key, focus, scroll, wait and observe traces, with optional screenshots; a scenario is bounded evidence. |
| What routes and costs follow from a declared task graph? | `journey` command | Reachability and shortest declared cost; does not discover navigation or predict human effort. |
| Do declared values and linear-scale mark coordinates agree? | `data` command | Differences, range, units/provenance fields and coordinate errors; caller must obtain source and rendered coordinates independently. |
| Are declared events co-present, separated, or too brief to have a rate? | `timeline` command | Interval overlap, gap, exposure and text rate; not a recommended timing or measured comprehension. |
| Are declared dependencies introduced before use? | `content` command | Presence and ordering; dependency necessity, truth and pedagogical effectiveness are contextual. |
| How do supplied response axes compare? | `survey` command | Separate descriptive aggregates and missingness; no fabricated participants or universal UX total. |
| What angular size follows from this physical size and distance? | `viewing` command | Geometric calculation; not a legibility threshold or simulation of eyesight, lighting or projection. |
| What did Chromium actually paginate? | `print` command | PDF export using print CSS; inspect the PDF pages. Native document hosts, physical print and email clients need their own evidence. |

[Usage and input shapes](usage.md) explains how to run the tools. [Research basis and judgment boundaries](basis.md) maps the broader design concerns.

An observation can justify an experiment, not the result. Compare under matched content, state, viewport and useful fidelity, then inspect the changed artifact as the person using it. Reject a better number when it removes meaning, hides needed information, weakens expression or breaks the task. Keep successful parts of the incumbent. Prefer no metric when a question is about purpose, taste or audience response and the available measurement would be contrived. Stop when the brief is served; consult again when a new question earns it.
