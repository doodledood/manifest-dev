# Craft domains

Per-domain craft guidance. Numerical examples and style choices are defaults; validate their fit to the task, medium and existing system. Applicable functional/access requirements live in `floors.md`; unfamiliar media and delivery in `experience.md`.

## Composition & layout

1. **Every gap is a grouping claim.** Grouping reads *relative* distances: within-group spacing at least one rhythm step smaller than between-group. Check each gap by asking "what does this distance say is related?" — the caught defects are a label equidistant between two fields, a heading floating between sections, a caption ambiguous between two images, toolbar icon+text pairs spaced so the pairs dissolve.
2. **Whitespace first, box as escalation.** Group by spacing; add a border or background region only where spacing cannot disambiguate (dense dashboards). A drawn boundary is the strongest grouping signal — which is why boxes multiply clutter when used as the first move.
3. **Make hierarchy inspectable.** Name the intended reading order and check the actual render. Blur and first-impression checks can reveal competing emphasis; they cannot prove a user’s fixation order.
4. **Make the entry useful and continuation discoverable.** Put orientation and the next relevant step where the person needs them. Do not infer that a clean viewport edge always stops scrolling or that every artifact needs its primary action in the first screenful.
5. **A grid is an alignment minimizer.** One base spacing unit, few alignment edges, structure matched to task: columns for reading, modules for browsing and comparison.
6. **Optical beats mathematical inside components; the layout spine stays mathematical.** Nudge asymmetric glyphs toward their visual center (a play triangle sits slightly right of geometric center); when a centered element looks wrong, believe the look. This never licenses breaking the layout-level alignment spine.
7. **Macro whitespace is a register lever, not a virtue.** Generous space reads premium and calm; packed space reads utilitarian and urgent. Set it by what the subject world should signal, not by habit.
8. **Repeated things are one object.** Siblings share edges, baselines, and internal spacing; the container's height comes from its content, never a fixed value that clips; inspect awkward grouping, clipping and overflow against the intended layout and content.
9. **Keep styling understandable.** Resolve unintended competing rules at their source. Intentional cascade, responsive overrides and accessibility overrides are not defects merely because they share a property.

## Motion

1. **An animation is a response time.** Micro-feedback 70–150ms, small change 150–250ms, standard transition 250–350ms, large or expressive 400–500ms, nothing longer without a named reason. Use these UI timings as starting points; media pacing and spatial motion require their own context. Encode durations as tokens (100/200/300ms).
2. **Three easing roles.** Standard for on-screen moves `cubic-bezier(0.2, 0, 0, 1)`; decelerate into entrances; accelerate out of exits; choose easing for the intended motion; constant speed can be appropriate. Exits run faster than entrances; user-triggered dismissals near-instant.
3. **Common motion jobs.** Feedback (≤150ms — its *absence* is the defect); orientation (a transition that states the spatial relationship); attention (one event, then still — never looping); delight (once, at the peak moment). Anything else is decoration.
4. **Micro-interaction timing:** pressed feedback 0ms; hover-in ~100–150ms ease-out; hover-out equal or faster; focus changes instant. Design the trigger, the rules, the feedback, *and* what happens on repeat — generated output ships the first two and forgets the rest.
5. **Mechanics.** Prefer `transform` and `opacity` for efficient UI effects where suitable; measure other properties; never `transition: all`; animation never blocks input — interactive from the first frame; reduced motion preserves feedback through an immediate update or a suitable reduced effect.
6. **The generated signature to avoid:** everything too slow and too springy, staggered fade-up-on-scroll on every section, no enter/exit asymmetry, hero animation present while button-press feedback is missing. Productive motion everywhere; expressive motion at most at the one or two moments the artifact exists for.

## Emotion & delight

1. **Basics are floor, delighters are ceiling.** A delight moment cannot compensate for a broken basic; evaluate expressive quality separately while preserving the basic requirements.
2. **Design endings; remove the worst moment first.** The last screen of every flow — success, receipt, error recovery — gets deliberate design; the single worst moment gets removed before any high point is added. A signature peak is permitted spice, never funded by degrading the baseline.
3. **Make expression understandable.** Preserve orientation while realizing a distinctive idea. Complexity and novelty have no universal numeric optimum; judge the actual audience, artifact and task.
4. **Celebration attaches to the user's own achievement only** — never to a spend or engagement event; scaled to the feat; with an off switch for repetition; `prefers-reduced-motion` respected. Check repeated use for interruption, fatigue and unwanted pressure.
5. **Interruptive personality needs precision and memory:** a high-precision trigger, memory of dismissal (never re-offer what was dismissed), no mascot face on an annoyance. Whimsy shrinks with audience size, stakes, and exposure frequency; tone goes matter-of-fact at failure moments.
6. **Place personality at moments of real emotional stakes** — anxiety at Send, relief at completion — where they serve the purpose. A familiar delight pattern is neither proof of quality nor an automatic defect; inspect its effect in context.

## Imagery & icons

1. **An image earns its place by answering a reader question.** Real-subject imagery draws attention; decorative stock is skipped. Default hero for reports, tools, and explainers is typographic or data-led. Illustration lives in empty states, errors, and onboarding — one spot, not one per section.
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
5. **Seed-to-palette:** fix the seed as the mid-ramp chroma peak; run the ladder through it; tint the neutrals with the seed hue at C 0.003–0.05 so the page reads as one temperature; pick the accent to contrast the *tinted neutral*, roughly 90–180° away.
6. **Semantic color is convention, not universal — and always double-encoded.** Green-success/red-danger is Western; several East Asian financial contexts run red = up. Ceiling: four semantic hues plus one brand hue; separate semantics in lightness so they survive grayscale; state always gets a second channel (icon, label, position) — red/green alone self-collides for ~8% of male users.
7. **Color-vision check:** simulate green-weak vision first (most common deficiency); with ≥3 data series use a colorblind-safe categorical palette; keep the confusion pairs (red↔green, green↔brown, blue↔purple, light green↔yellow, pink↔gray) apart or split them in lightness.

## Typeface selection

1. **Derive the face from the subject, not the reflex.** Sans = technical/restrained (grotesque institutional, humanist warm, geometric precise-cold); serif = established or warm authority; slab = sturdy confidence; mono = code, evidence, raw data; display = thematic atmosphere. Procedure: name the subject's era, material, and register → map to a class → pick a face inside the class that clears the quality bar.
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
5. **Alt text: content and function, succinctly.** Decorative → `alt=""` (present, empty); no "image of". Charts: "[chart type] of [data type] where [takeaway]", plus the reliable fallback — `aria-hidden` on the SVG, visible takeaway text, the data as an HTML table.
6. **Icon buttons name the action** — "Copy link", not "Chain"; pressed-state toggles use a stable label with `aria-pressed`; an action button may instead change Mute to Unmute without pressed-state semantics; expansion uses `aria-expanded` where appropriate.
7. **Recent floor items models miss:** focus never fully obscured by sticky chrome (`scroll-padding-top` sized to the header); every drag interaction gets a single-pointer alternative; never block paste in auth fields; target-size requirements with their exceptions, as specified in `floors.md`.
8. **The manual checks that matter, ranked:** keyboard-only walk with the mouse unplugged; headings-only read; 200% zoom and 320px reflow; alt and accessible-name *quality*; color-only-meaning sweep under grayscale; focus order after dynamic inserts. Run these as a generation-time self-audit — an automated scan passing is not accessibility.

## Style derivation

1. **Derive from the durable bases; quote ornament languages only when the subject earns them.** Languages built on a functional claim persist (grid discipline, editorial and print craft, terminal aesthetics within their own world); languages built on a surface treatment cycle in and out of fashion; languages that fight perception die on the defect; languages an OS institutionalizes stop being distinctive.
2. **Fashion observations are dated.** Treat `calibration.md` as historical calibration, not a current prevalence measurement. Refresh from observed output when needed; the calendar alone does not establish a new trend.
3. **A generation process is its own ubiquity engine.** Whatever it defaults to, it commoditizes — the strongest reason to derive style from the subject rather than shipping a house look.
