# Figures — what to draw, and how to draw it

The reference behind the task model's encoding line: what a figure depicts once a claim has earned one, how options are compared, the inline-SVG mechanics that keep a hand-drawn figure legible in both themes, and the one rule for charts. Each rule is an action with its check. Whether a claim gets a figure at all is decided in the task model, not here — the test is that a cold reader would otherwise assemble a mechanism from prose, and that a sentence does not say it faster.

## What to draw

1. **Depict the mechanism, not its name.** A box labeled "cache" says less than the sentence did; the path a request takes through it, the two stores it sits between, and the arrow that disappears when the cache is removed say what the words cannot. Show the parts the argument hinges on — the boundary crossed, the hop added, the data that moves — and leave out the parts it does not. Check: cover the labels; the shapes and arrows alone should still show something happening.
2. **Comparing options? Draw the difference.** Two architectures side by side, a before and an after, the one edge each option adds or removes — the reader must be able to point at what they are choosing between. A separate labeled box per option with nothing connecting it to the system is a restated option list, not a comparison. Check: the two panels share a skeleton and differ where the decision differs, and nowhere else.
3. **Match complexity to the stakes.** A one-hop question is a three-box figure; a migration that reroutes writes through a queue needs the queue, the writer, the reader, and the ordering arrow. Draw as much as the decision turns on — no forced minimalism, no inventory of the whole system. Check: every element removed would lose a fact the decision needs; every element added would add none.
4. **Label the arrows.** An unlabeled arrow is "related somehow"; `writes`, `invalidates`, `polls every 30s` is information. Put the meaning on the mark itself; a legend earns its place only when one encoding (dashed, colored, doubled) repeats across the figure.
5. **One figure, one claim.** The caption states what the picture shows, in a sentence a reader could repeat. A figure that needs a paragraph to explain is two figures, or a figure and a table.
6. **The figure replaces the prose.** Once a claim is drawn, the paragraph that assembled it in words goes; what stays beside the figure is the caption and whatever the prose said that the figure does not. Check: read the paragraph nearest each figure — if it narrates the figure, cut it.

## Inline SVG mechanics

Hand-author inline `<svg>` with native shapes (`rect`, `circle`, `line`, `polyline`, `path`) and `<text>` — no library, no runtime, no external image.

1. **Size by `viewBox`.** Set `viewBox="0 0 W H"` and let CSS scale it (`max-width: 100%; height: auto`); choose W and H for the content, never a preset. Flows read left to right; layered stacks read top to bottom.
2. **Theme with `currentColor`.** Strokes, text, and arrowheads in `currentColor` inherit the page's foreground in light and dark alike. Reserve one literal hue for the one element that carries meaning — the option leaned toward, the hop under discussion — and check it against both grounds by number, the same contrast floor as text.
3. **Arrowheads are markers or polygons.** A `<defs><marker>` referenced by `marker-end="url(#arrow)"`, or a small `<polygon>` at the line's end — never an image, never a Unicode arrow in `<text>` standing in for a line.
4. **Keep labels legible.** Roughly 11–13px at the drawn scale, `text-anchor` for alignment, a word or three per label; sentences belong in the caption below the figure, not in the drawing. Check at the narrow viewport: a figure that shrinks its labels below the floor gets a wider `viewBox` split across two figures, not smaller type.
5. **Align to a grid.** Shared baselines, equal box sizes for equal roles, even gaps — most of what makes a hand figure read as deliberate. Eyeballed offsets read as noise. Use the page's spacing values for the gaps.
6. **Wrap and name it.** Every `<svg>` sits in a `<figure>` with a `<figcaption>` stating the claim, and carries `role="img"` plus an `aria-label` carrying the same claim for readers who cannot see it. The caption and the label say the same thing.
7. **Stay self-contained.** No `<script>`, `<style>`, or `<foreignObject>` inside the SVG; gradients, patterns, and `<use>` reference ids in the same fragment (`href="#id"`), and ids are unique across the page when several figures share it. Long decorative path data means the drawing wants a graphics tool — simplify instead.

## Charts

1. **Draw to one scale.** Every mark in a chart is placed by the same scale, and every axis label names a value the chart actually reaches — a bar drawn to look right rather than to its value is a false claim. Chart text, gridlines, and marks take their colors from the page's tokens, never a library default; series colors follow the color-construction rules in `craft.md`. One chart, one comparison; a chart the reader cannot restate in a sentence is decoration.
