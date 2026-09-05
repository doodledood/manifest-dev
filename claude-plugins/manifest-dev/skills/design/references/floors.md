# Web requirements and craft defaults

Apply requirements to the actual artifact. Standards carry levels and exceptions;
style and dimension examples are starting points, not universal pass/fail rules.
A review failure needs an applicable requirement, brief/system constraint or
observable consequence for the task.

## Function and access

1. **Applicable states.** Design loading, empty, failure, recovery and successful
   states where they can occur. Acknowledge actions promptly and preserve input.
   Show determinate progress only when meaningful progress is measurable; otherwise
   provide truthful status. Skeletons are an option when they match the content,
   not a required loading pattern. State continuity loads from `experience.md`.
2. **Consequential actions.** Prefer useful undo where possible; make irreversible
   outcomes clear before commitment. A confirmation names the outcome, not Yes/No.
   Avoid routine confirmations that add no decision value.
3. **Text contrast.** For WCAG 2.2 AA, normal text needs at least 4.5:1; large text
   at least 3:1 (18pt, or 14pt bold: 24 CSS px, or 18⅔ CSS px bold). Compare the
   unrounded ratio against the threshold. Placeholder and secondary text are not
   exempt. Apply the criterion's exceptions, including inactive controls, decorative
   or incidental text and logotypes. Check actual backgrounds and states; image,
   alpha, gradients and unsupported colors require appropriate measurement.
4. **Non-text meaning.** Required control/state and graphical distinctions need
   applicable non-text contrast; color alone must not carry meaning. Preserve
   labels and equivalent access to images, figures and charts.
5. **Keyboard and semantics.** Use suitable native controls, meaningful names,
   visible labels, sensible reading/focus order and visible keyboard focus.
   A browser's visible default focus can be sufficient. Removing it needs an
   effective replacement; a `:focus-visible` selector alone proves nothing.
6. **Targets.** WCAG 2.2 AA target size is 24×24 CSS px, subject to spacing,
   equivalent-control, inline, user-agent and essential exceptions. Its enhanced
   44×44 criterion is AAA with its own exceptions. Use comfortable targets for
   the supported input and actual platform guidance; CSS px, pt and dp are not
   interchangeable. These criteria do not by themselves establish legal compliance.
7. **Enlargement and reflow.** Check 200% text resizing without loss under the
   applicable criterion. For vertical-scrolling web content, check reflow at
   320 CSS px; horizontal-scrolling content uses 256 CSS px height. Necessary
   two-dimensional content has exceptions; the surrounding content still reflows.
   A 390px screenshot or a `clamp()` formula alone does not settle these checks.
8. **Motion.** Respect reduced-motion needs while preserving feedback, using an
   immediate state change or a suitable reduced effect. WCAG's interaction-motion
   criterion is AAA and concerns disabling nonessential motion; a particular CSS
   block is a technique, not the requirement. Also inspect applicable autoplay
   pause/stop controls and flash limits.
9. **Forms and recovery.** Explain what failed and how to recover, adjacent to the
   relevant field and through appropriate announcements. Preserve valid input,
   support suitable autocomplete and password-manager/paste behavior. Check actual
   validation timing rather than marking unfinished input wrong. Apply redundant
   entry, authentication and dragging criteria with their stated exceptions.

## Coherent craft

- **Grouping and alignment.** Related content should read as related. Keep a
  coherent spacing system and give each gap a clear owner. Logical start edges
  support the writing direction; numeric alignment supports comparison. Mixed
  alignment, borders plus shadows or a nonstandard gap are not defects by syntax.
- **Color and themes.** Choose roles that realize the creative direction and make
  states distinguishable. Neutral-heavy palettes and a restrained accent are useful
  options, not mandatory proportions. Black backgrounds, colored headings and
  gradients can be appropriate. Test every supported theme; define the intended
  canvas background when the artifact is meant to stand alone.
- **Type and measure.** A 65–70ch prose column and 16–18px body type are starting
  examples for some web reading, not universal limits. Verify actual language,
  glyphs, size, enlargement and reading context. WCAG sets no general minimum body
  font size. Use consistent numeric precision and localized units; distinguish
  missing data from zero and uncertainty from known values.
- **Density.** Match information density to the task, input and expertise. Offer
  a compact mode when useful; do not add one automatically. Preserve grouping,
  legibility, applicable targets and recovery under compaction.
- **Copy and structure.** Controls name outcomes. Headings and labels help find
  the relevant content. Numbering encodes sequence where sequence matters; other
  visual grouping earns its place through meaning or the creative direction.
- **Entry state.** Orientation and necessary controls are available on arrival.
  Demonstration data is labeled; real empty states are truthful. Make continuation
  discoverable. Narrative, learning and other temporal or interactive tasks may
  use sequence or deliberate reveals, with appropriate equivalent access.

## Unsupported rationales

Do not justify a choice with a universal golden ratio, a 20% whitespace boost,
a fixed scan pattern, a 40% complexity target, a threefold complexity penalty,
or a claim that an automated scan establishes accessibility. Choose on the
artifact's task and evidence. Numerical templates and style examples need no
invented scientific authority to be useful defaults.
