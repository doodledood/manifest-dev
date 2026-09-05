# Figures — choose the representation and preserve its meaning

Use the task model to choose a representation: photographs or screenshots for observed appearance and context; diagrams for structure, containment, relationships or sequence; charts for quantitative patterns; tables for exact lookup and mixed-attribute comparison. An illustration can explain or express; motion and interaction can reveal change or alternatives. These can complement each other. Use `craft.md` for imagery and temporal composition.

## Information and composition

1. **Choose what the reader needs to see.** A hierarchy, distribution, geography, process and comparison call for different structures. Depict the relevant relationship; not every diagram is a flow and not every chart has one predetermined conclusion.
2. **Make encodings truthful.** Position, enclosure, size, connectors, color and line treatment convey meaning. Define relevant notation and label directional relationships. Keep referents stable between marks, text, controls and neighboring views.
3. **Compose the explanation.** Titles orient, labels identify, annotations explain and prose qualifies. Place each where its relationship is clear; sentences may belong beside a feature. Match complexity to the actual question and audience, preserving uncertainty and necessary context.
4. **Compare with a meaningful frame.** Comparable panels share the relevant structure, units and scales unless a difference is deliberate and clear. A table and chart can supply complementary precision and pattern. Inspect what the reader must remember or reconstruct.
5. **Preserve evidence and access.** Verify factual images, marks and labels against supplied sources. Supply equivalent information appropriate to the task, including relationships, uncertainty or interaction states; a single takeaway or data table may not be enough. Distinguish illustration and simulation from observation.

## Production and delivery

Choose plotting, diagramming, image or native layout tools suited to the artifact and required editability. Small inline diagrams can use hand-authored SVG; these mechanics apply when that is the chosen medium:

1. **Size by `viewBox`.** Set a content-appropriate `viewBox`; allow CSS to scale it while checking actual label size. Recompose, annotate differently or split when a narrow display loses meaning.
2. **Theme by role.** `currentColor` can inherit a suitable foreground; use distinct roles for categories, states or the creative direction. Inspect actual text and graphical elements against their rendered backgrounds under the applicable text/non-text contrast requirements and exceptions.
3. **Use native geometry and clear notation.** SVG paths and markers can draw directional relationships. Shared baselines and sizes support equal roles; purposeful variation can encode differences.
4. **Check text and references.** Keep critical labels controllable and legible in the final output. IDs are unique where figures share a document; internal references resolve. Give meaningful graphics appropriate names and descriptions; hide them from assistive technology only when a sufficient equivalent is available.
5. **Inspect the destination.** Check crop, resolution, supported themes, export, reading order and interaction in the delivered medium. A browser preview does not certify a native document or video.

## Quantitative graphics

Choose the chart for the analytical question: magnitude, change, distribution, relationship, part-to-whole or spatial pattern. Geographic area is useful when location matters; ranking alone may be clearer in aligned marks.

Map each encoded variable faithfully through its own scale. Use a baseline appropriate to the encoding, disclose consequential truncation or transformations, and keep comparison domains consistent where required. Axis ticks can extend beyond observed values; x and y need not share a scale. Inspect units, denominators, aggregation, missingness, uncertainty, dates and observed versus projected values. Interpolation and smoothing must not invent a pattern. Styling and motion preserve these relationships while making them legible and compelling.
