# Blind landing review

Independent fresh-context review; labels were hidden until this verdict was returned. This is the review response with local evidence paths normalized; its wording and findings are preserved. The operator separately ran the checker with working Chromium; see the main report for combined coverage.

**A:** baseline-repeat | **B:** candidate | **C:** baseline | **D:** intermediate

## Verdict

**C narrowly preferred, then A, B, D — moderate confidence.** C offers the best balance of expressive identity, readable example, visible terms and compact interaction. A is close; B trades stronger upfront explanation for a longer, smaller-text encounter. D has a concrete feedback defect.

**Genre/use context:** product-concept landing page for a studio lead deciding whether Relay addresses handoff needs and trying a reversible local example.

I rendered and exercised every variant in isolated `judge-landing-*` sessions at **1440×900, 390×844 and 320×844**. Each completed repeated acknowledgement/undo loops using keyboard and pointer, including reduced-motion operation. No files were changed.

### A — Strong, coherent; close second

**Findings:** No MEDIUM-or-higher defect observed in the exercised scope.

**Observed:** The cobalt surround, yellow entry action and paper receipt distinguish the product story from the working example. At desktop size, all four sample facts, acknowledgement and sender feedback fit together. Acknowledging changes the receipt to **“Received by you”**, with a green check; undo restores the waiting state. Focus remains on the control.

At 390px, the demo anchor leaves the receipt at the viewport’s bottom: the status is visible, but its explanatory detail falls below it. At 320px, seeing the receipt requires another downward scroll. Once positioned there, acknowledgement and recovery remain together; this is not a repeated-loop blocker.

Pricing is absent from the initial hero but reachable through a working, plainly named link. The price, trial and concept limitation are grouped clearly.

**Design judgment:** The receipt treatment makes the handoff/confirmation relationship tangible without adding much explanatory machinery. It has stronger visual presence than B while keeping the sheet readable. Compared with C, it spends more vertical space on instructions and delays the commercial terms.

**Evidence:** `../samples/baseline-repeat-landing.html`; `../screenshots/review-landing/A-desktop.png`, `../screenshots/review-landing/A-mobile-received.png` and `../screenshots/review-landing/A-desktop-pricing-final.png` under the same `../screenshots/review-landing/` prefix.

### B — Clear explanation, quieter identity, higher reading cost

**Findings:** No MEDIUM-or-higher defect observed in the exercised scope.

**Observed:** B’s introductory paragraph explicitly includes both the shared page **and acknowledgement**, while the action note distinguishes receipt from completed work. Its folded sheet, green mount and highlighted Thursday form a consistent stationery treatment. The receipt turns lime and shows **“Acknowledged by the production designer”**; the control becomes an outlined undo action. Both reverse correctly.

The desktop sheet uses smaller project text than A/C, and the complete demo disclosure extends beyond the initial viewport. On mobile, nested mount/sheet padding reduces the available reading width. The additional three-part explanation lengthens the journey to pricing, although the navigation link bypasses it.

**Design judgment:** B is the clearest verbal introduction, and its visual restraint is not a defect. Its disadvantage is cumulative: smaller utility text, more enclosing layers and an additional section explaining much of what the example already demonstrates. The darker pricing panel supplies a strong ending, but C/A reach that ending more economically.

**Evidence:** `../samples/candidate-landing.html`; `../screenshots/review-landing/B-desktop.png`, `../screenshots/review-landing/B-mobile-received.png`, `../screenshots/review-landing/B-desktop-pricing-final.png`.

### C — Best overall balance

**Findings:** No MEDIUM-or-higher defect observed in the exercised scope.

**Observed:** At 1440px, the opening view contains the offer, complete sample, action, waiting receipt and **$12/workspace/month, 14-day trial, no-card, concept-only** terms. At 390px, following “Try a handoff” frames the project context, action, disclosure and complete receipt together. The larger sample text remains readable without the nested framing used by B/D.

Acknowledgement immediately produces **“Received by the production designer”**, a checkmark and an outlined undo button. Undo correctly restores all three. Keyboard focus is visible and retained.

At 320px, the receipt moves below the initial demo viewport, as it does in A/B; scrolling exposes it without horizontal overflow or losing the recovery control.

**Design judgment:** The coral field, large editorial headline and contrasting dark/cream handoff sheet give C a deliberate studio-facing identity. Its strongest advantage is not the color alone: the same sheet carries the explanation, interaction and result without extra panels. The quieter lower section provides a useful change of pace.

Its trade-off is that acknowledgement’s purpose is explained less explicitly in the opening prose than in B. The visible demo and lower explanation carry that relationship instead.

**Evidence:** `../samples/baseline-landing.html`; `../screenshots/review-landing/C-desktop.png`, `../screenshots/review-landing/C-mobile-demo.png`, `../screenshots/review-landing/C-mobile-received.png`.

### D — Strong visual hierarchy; incorrect icon feedback

**MEDIUM — state feedback:** After acknowledgement, the receipt says **“Received”** but still displays the **waiting clock**. The button says **“Undo acknowledgement”** but retains its acknowledgement checkmark. This repeats on desktop/mobile and with reduced motion. Text and recovery work, so the loop is not blocked, but two visual signals contradict the new state.

**Cause confirmed after rendering:** `../samples/intermediate-landing.html:927–930` assigns `.hidden` properties to SVG elements without changing their `hidden` attributes. In the acknowledged state, the browser reported the waiting SVG as `display: block` and the received SVG as `display: none`.

**Concrete fix:** Toggle the SVGs’ actual `hidden` attributes, or control their visibility through the existing state attribute; then retest both directions. No redesign is needed.

**Design judgment:** D has an assertive headline and the most prominent receipt status. Its blue mounting frame clearly identifies the interactive region, and the price appears upfront. Against C, the heavy heading and saturated frame compete more strongly for attention; nested padding also makes the narrow example less economical. Conversely, its anchor placement keeps the receipt visible particularly well at 320px. These are trade-offs, not additional graded defects.

**Evidence:** `../screenshots/review-landing/D-received.png`, `../screenshots/review-landing/D-mobile-received.png`, `../screenshots/review-landing/D-reduced-received.png`; source lines above.

## Shared behavior, motion and truthfulness

- **Content/terms:** All four contain the required Harbor identity facts and correct fictional offer. All distinguish the concept/local demo from a live signup. I found no invented customers, testimonials, integrations or measured benefits.
- **Local behavior:** All worked with network access disabled. Reloading an acknowledged example restored waiting state. Resource timing showed no fetched resources; no forms or browser errors were observed.
- **Keyboard:** Skip links, demo entry, Tab-to-acknowledge, Enter activation and Space undo worked. Focus indicators were visible. Some initial off-screen automation clicks required scrolling the target into view; I did not treat those tooling misses as artifact defects.
- **Motion:** A/C navigate and update receipt state immediately. B/D use smooth anchor travel and brief receipt-color transitions; sampled text changed immediately rather than waiting for animation. Reduced motion removed travel/transitions while preserving state and recovery. No variant needs additional motion to meet this brief.
- **Reflow/readability:** No horizontal overflow was found at 320px. Narrow screens introduce vertical scrolling, not inaccessible content. A bounded computed-color check found no text-contrast candidates on supported opaque backgrounds; B’s highlighted gradient text was outside that check.

## Rulers and limits

**No ranking or severity difference is attributable only to the old versus new ruler.** Both support the D finding. The old ruler’s more explicit token/spacing prescriptions could produce source-level candidates for B/D, but I found no corresponding rendered grouping defect worth grading. The newer whole-encounter emphasis supports examining the complete journey; it is not itself evidence that any label is better.

The supplied current checker reported zero findings but skipped rendered checks because Playwright was unavailable; the browser work above supplied independent rendered evidence.

**Unverified:** screen-reader announcements, physical-phone touch ergonomics, 200% text resizing, forced-colors behavior and browsers beyond the tested Chromium host. This is not full accessibility certification or evidence of human comprehension, preference, conversion or general efficacy.
