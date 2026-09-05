# Craft domains

Per-domain craft guidance. Numerical examples and style choices are defaults; validate their fit to the task, medium and existing system. Applicable functional/access requirements live in `floors.md`; unfamiliar media and delivery in `experience.md`.

## Composition & layout

1. **Every gap is a grouping claim.** Grouping reads *relative* distances: within-group spacing at least one rhythm step smaller than between-group. Check each gap by asking "what does this distance say is related?" — the caught defects are a label equidistant between two fields, a heading floating between sections, a caption ambiguous between two images, toolbar icon+text pairs spaced so the pairs dissolve.
2. **Choose how groups read.** Spacing, common regions, borders, alignment and similarity can establish relationships. Use the combination the content and creative direction need; inspect whether a boundary clarifies a group or competes with it.
3. **Make hierarchy inspectable.** Name the intended reading order and check the actual render. Blur and first-impression checks can reveal competing emphasis; they cannot prove a user’s fixation order.
4. **Make the entry useful and continuation discoverable.** Put orientation and the next relevant step where the person needs them. Do not infer that a clean viewport edge always stops scrolling or that every artifact needs its primary action in the first screenful.
5. **A grid is an alignment minimizer.** One base spacing unit, few alignment edges, structure matched to task: columns for reading, modules for browsing and comparison.
6. **Refine optical balance.** Adjust apparent edges, weight and spacing while preserving the intended grouping and comparison structure. Mathematical regularity is a starting point, not a verdict on balance.
7. **Macro whitespace is a register lever, not a virtue.** Space can support presence, separation and pace; density can preserve useful context. Inspect both expression and the actual reading or comparison task rather than assigning either a universal emotional meaning.
8. **Repeated things are one object.** Siblings share edges, baselines, and internal spacing; the container's height comes from its content, never a fixed value that clips; inspect awkward grouping, clipping and overflow against the intended layout and content.
9. **Keep styling understandable.** Resolve unintended competing rules at their source. Intentional cascade, responsive overrides and accessibility overrides are not defects merely because they share a property.

## Motion

1. **Choose what time contributes.** Motion may communicate feedback, continuity, attention, transformation, rhythm, atmosphere or play. In a film, motion graphic, simulation or ambient work, it can be the content. Match its extent to that purpose rather than a fixed count of expressive moments.
2. **Compose the sequence.** Design key states, what stays stable, attention transfers, pacing, holds, transitions and endings. Coordinate animated type, imagery, camera and sound where applicable; preserve reading time, object identity and truthful relationships. A loop needs a considered return and repeated-viewing check.
3. **Compare temporal and simultaneous views.** Animation can reveal change while consuming time and memory; static sequences or small multiples preserve comparison while consuming space. Choose for the question being answered, retaining reference states where useful. A literal transition can be less clear than a symbolic one.
4. **UI timing is local guidance.** Micro-feedback around 70–150ms and transitions around 150–500ms are starting ranges, not media pacing rules. Choose easing for the movement; constant speed, springs and abrupt changes can each fit. Keep direct actions responsive and inspect trigger, feedback, interruption, reversal and repeat.
5. **Preserve control and access.** Provide pause, replay, stepping or scrubbing where the task needs them. Reduced motion preserves meaning through an immediate update, gentler effect or still sequence; inspect the alternative, not only the media query. Apply relevant flashing and other access requirements.
6. **Inspect delivery.** Measure performance; prefer efficient properties where suitable. Effects must preserve applicable input and status behavior. Judge full playback and repeated use, not only a striking frame or a smooth frame rate.

## Emotion & delight

1. **Basics are floor, delighters are ceiling.** A delight moment cannot compensate for a broken basic; evaluate expressive quality separately while preserving the basic requirements.
2. **Design the whole experience.** Carry the visual idea and care through arrival, active use, meaningful change, endings and return where those exist. Repair painful moments while developing what makes the artifact worth remembering; one spectacular frame does not finish the experience.
3. **Make expression understandable.** Preserve orientation while realizing a distinctive idea. Complexity and novelty have no universal numeric optimum; judge the actual audience, artifact and task.
4. **Celebration supports the person's own goal.** Scale it to meaning and repeated exposure; preserve control and reduced-motion access. A business event alone does not establish user benefit. Check interruption, fatigue and unwanted pressure.
5. **Interruptive personality needs precision and memory:** a high-precision trigger, memory of dismissal (never re-offer what was dismissed), no mascot face on an annoyance. Whimsy shrinks with audience size, stakes, and exposure frequency; tone goes matter-of-fact at failure moments.
6. **Place personality at moments of real emotional stakes** — anxiety at Send, relief at completion — where they serve the purpose. A familiar delight pattern is neither proof of quality nor an automatic defect; inspect its effect in context.

## Imagery & icons

1. **Art-direct the representation.** Images can supply evidence, explanation, identity, atmosphere or expression. Choose photography, illustration, diagram, metaphor or abstraction for that role; compose viewpoint, crop, light, texture, depth and placement with the type and surrounding space. Judge what the image contributes, rather than allocating illustration to fixed slots. Check asset provenance, permitted use, responsive crop and final resolution.
2. **Generated imagery must not fabricate evidence.** Use it for appropriate illustration or expression, clearly distinguished from real observations. Verify information-bearing diagrams and typeset critical labels in a controllable layer. A factual chart, screenshot or person must not be presented as real evidence when invented. Information graphics follow `figures.md`.
3. **Icon craft has numbers.** 24px canvas, ~20px live area, 2px stroke, one stroke weight across the set; respect optical sizes (a 24px icon scaled to 16px loses its counters). Fill state is never the only selection signal.
4. **Icons don't work alone.** Visible labels, not hover-only; if no icon comes to mind in 5 seconds, use text. The glyph is not the target — it sits inside the standard hit area.
5. **Artifacts travel: design the link-card surface.** One social-preview image at 1200×630 designed as a poster read small — one message, title ≥60px on the canvas, safe margins; favicon as a single glyph drawn for 16px, checked against light and dark tabs.

## Right-to-left & Hebrew

1. **Direction is markup, not alignment.** `<html dir="rtl" lang="he">` plus logical CSS properties (`margin-inline-start`, `text-align: start`, `inset-inline-*`) mirror the layout from one attribute. `text-align: right` is not RTL — punctuation placement and inline ordering stay broken. Logical properties cost nothing in LTR, so emit them always.
2. **Fix mixed-direction text by isolation, never by reordering characters.** An English run at the end of a Hebrew sentence steals the trailing punctuation; fix with `dir` on the element, `<bdi>` or `dir="auto"` for injected strings. Never hand-swap brackets — they mirror themselves.
3. **Logical properties don't fix:** shadow x-offsets, `translateX`, gradient directions, `background-position`, SVG path data. These need explicit `[dir="rtl"]` overrides.
4. **Icon mirroring is a two-list rule.** Flip: back/forward arrows, undo/redo, anything meaning forward-in-flow, text-block icons, progress bars. Never flip: media playback and scrubbers, clocks, checkmarks, numbers, logos, the search magnifier, slashes. Temporal flips; physical doesn't. Hebrew keeps the Latin question mark.
5. **Hebrew typography inverts Latin habits.** No italics — bold is the emphasis convention, and synthesized oblique reads as a rendering error; no all-caps (no case exists); pair by matching Hebrew letter-height to the Latin x-height; keep line-height at the Latin ~1.5. Stacks: Heebo, Rubik, Assistant, Noto Sans Hebrew — a Latin-only stack silently drops Hebrew to Arial.
6. **Charts: categorical axes mirror; numeric and time axes stay left-to-right.** Mirror chrome (titles, legends); never mirror with `scaleX(-1)`, which flips the glyphs.
7. **Format by locale API, not by hand:** `Intl.DateTimeFormat('he-IL')`, `Intl.NumberFormat('he-IL')` — the API also sidesteps the mixed-direction bugs hand-formatted slashes create.
8. **Size containers for expansion.** Short strings can double or triple in translation; language-average contraction does not bound an individual string. Test actual Hebrew, English and other supported text. Never fix a button or tab width to its English content.

## Touch & mobile

1. **Accuracy peaks at screen center; edges and corners degrade** — so corner targets get *bigger* (~64px), not merely avoided. Targets 44–48px with ≥8px gaps; never a small destructive control in a corner.
2. **Hover may duplicate, never solely carry.** Hover-only tooltips, hover-revealed actions, and CSS dropdowns are unreachable on touch. Gate hover embellishments behind `@media (hover: hover) and (pointer: fine)`; every gesture-revealed action gets a visible tap path.
3. **`100vh` lies on mobile** — it measures the largest viewport, so full-height elements overflow behind the browser chrome. Use `min-height: 100svh` (or `dvh` for app panes).
4. **Bottom placement earns its keep:** primary navigation visible at the bottom beats hidden hamburger menus on discovery; bottom sheets dismissible by scrim and handle.
5. **The attribute layer is the mobile form UX:** `inputmode="numeric"`/`"decimal"` for the right keypad, `type="email"/"tel"/"url"`, correct `autocomplete` tokens — autofill beats any keyboard tuning by skipping typing entirely. Generated forms are visually complete and attribute-empty.
6. **The ~390px breakage list:** sidebars collapse to a single column (a sidebar at 390px is a bug); wide tables scroll in their own `overflow-x: auto` wrapper, never the body; stat-card grids 2-up max with numbers allowed to wrap; sticky headers minimized.
7. **Container queries are the artifact-correct responsive tool:** a component styled by its container behaves in a phone, a side panel, or a full window alike. Media queries for page layout, container queries for components. Test text enlargement and applicable reflow; a `clamp()` formula alone cannot establish either.
8. **Desktop-first is right for desk-bound genres** — dense dashboards and comparison tools get a desktop-first design with a named degradation plan for 390px.

## Color construction

1. **Build color roles, then inspect them.** OKLCH is useful for reasoning about lightness/chroma/hue. Equal L does not guarantee equal visual weight or contrast. Use a role-appropriate ladder rather than imposing one hue’s numeric ramp on every palette.
2. **Shape ramps to their purpose.** Chroma often peaks near the middle; hue drift is optional, and neutral ramps may have zero chroma. Inspect actual state and text roles.
3. **Check the output gamut.** Out-of-sRGB is not necessarily outside the destination display gamut. Browser mapping differs; provide required fallbacks and inspect the actual output.
4. **Verify rendered color.** HSL lightness is not perceptually uniform. OKLCH can help construct a palette, but the coordinate system does not prove its contrast or quality.
5. **Compose color in context.** Test surface, foreground, emphasis, identity, category and state roles together with actual type and imagery. Similarity can unify; contrast can distinguish. Adjust hue, lightness, chroma and area for the relationship; a seed position, hue offset or percentage recipe cannot establish quality.
6. **Semantics follow audience and domain.** Keep brand, categories and states distinguishable without a fixed hue-count ceiling. Important state also gets a meaningful noncolor channel; inspect supported themes and color-vision conditions. A cultural generalization is not evidence for a particular audience.
7. **Color-vision check:** simulate green-weak vision first (most common deficiency); with ≥3 data series use a colorblind-safe categorical palette; keep the confusion pairs (red↔green, green↔brown, blue↔purple, light green↔yellow, pink↔gray) apart or split them in lightness.

## Typeface selection

1. **Choose typographic voice in composition.** Use the subject and intended experience, then inspect actual specimens. Classification alone does not assign emotion. Coordinate face, width, weight, optical size, tracking, leading and space; expressive display and productive utility regions can coexist.
2. **Check the font itself.** Required scripts, glyphs, styles, licensing and readability matter. Price, category or institutional sponsorship does not establish fitness.
3. **Pairing:** a superfamily first (same bones, built-in contrast); else contrast of classification across one boundary; match x-heights optically; vary one axis dramatically, not several. Budget: one display role + one body role; a mono is a non-counting functional third for code and numeral columns.
4. **Test body text in context.** Inspect supported scripts, ambiguous glyphs, emphasis styles and actual reading size, including enlargement. A display or geometric classification alone does not establish failure.
5. **Load for the swap:** webfonts default to swapping in after first paint — provide a metric-matched local fallback (`size-adjust`, ascent/descent overrides) so the swap doesn't reflow. System stacks are the legitimate default for utilitarian tools; webfonts when the subject demands a voice.
6. **Verify `tabular-nums` support** in the actual font and rendered numeric columns; declaring the CSS feature does not establish support.

## Accessibility depth

Checks requiring meaning and interaction; automated coverage varies by tool, artifact and defect. An automated pass is not accessibility conformance.

1. **Headings are the navigation system.** Most screen-reader users navigate by headings: one `h1`, no skipped levels, headings that narrate the page when read as a bare list. Landmarks cost one tag each — add them, never instead of headings.
2. **Native first.** `<button>`, `<a href>`, `<details>`, `<dialog>`, `<label>`, native inputs; `role`/`aria-*` only where no native element exists. Use ARIA where it supplies needed semantics; an association with errors does not prove causation.
3. **The modal focus contract:** open → focus moves in (to the least-destructive action when confirming something irreversible); Tab wraps inside; Escape closes; close → focus returns to the invoker. Native `<dialog>.showModal()` supplies the trap and Escape free.
4. **Test announcements.** A stable empty polite/status region populated later is a compatibility default. Initially populated or injected alerts can receive special handling. Choose urgency and verify the actual browser/screen-reader behavior; preserve meaningful updates through rerenders.
5. **Alternative text preserves meaning and function.** Identify simple images succinctly; complex graphics may need descriptions of relationships, values, uncertainty or state. Use `figures.md` for equivalent information. Decorative images can have empty alternatives; hide a chart only when the needed equivalent is actually available.
6. **Icon buttons name the action** — "Copy link", not "Chain"; pressed-state toggles use a stable label with `aria-pressed`; an action button may instead change Mute to Unmute without pressed-state semantics; expansion uses `aria-expanded` where appropriate.
7. **Recent floor items models miss:** focus never fully obscured by sticky chrome (`scroll-padding-top` sized to the header); every drag interaction gets a single-pointer alternative; never block paste in auth fields; target-size requirements with their exceptions, as specified in `floors.md`.
8. **The manual checks that matter, ranked:** keyboard-only walk with the mouse unplugged; headings-only read; 200% zoom and 320px reflow; alt and accessible-name *quality*; color-only-meaning sweep under grayscale; focus order after dynamic inserts. Run these as a generation-time self-audit — an automated scan passing is not accessibility.

## Style derivation

1. **Develop the subject-specific idea.** References can inform composition, material and rhythm as well as palette. Judge the realized direction against its purpose; a familiar technique or required identity is not a defect.
2. **Fashion observations are dated.** Treat `calibration.md` as historical calibration, not a current prevalence measurement. Refresh from observed output when needed; the calendar alone does not establish a new trend.
3. **A generation process is its own ubiquity engine.** Whatever it defaults to, it commoditizes — the strongest reason to derive style from the subject rather than shipping a house look.
