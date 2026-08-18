# Prose Floor Reference

The rules that hold for **every** prose deliverable, in either register. Verification lookup data
for gate evaluators.

**Register scope.** Nothing in this file is register-specific — that is what qualifies it for the
floor. Documentation-register mechanics live in `DOCS-STYLE-REFERENCE.md`; human-voice register
rules on rhythm, texture, and craft live in `WRITING-REFERENCE.md`. Neither set is repeated here,
and a rule in this file is never contradicted by either.

**Precedence.** A project's own style sheet or `AUTHOR_VOICE.md` outranks this reference; the
`review-writing` skill applies that rule and is its one home.

**Not for `/define` interviews** — lookup data for gate evaluation. The task file
(`tasks/PROSE_FLOOR.md`) carries the compressed gate text.

---

## Vocabulary kill-list

Statistically flagged as AI-generated across peer-reviewed studies of millions of documents.
Never use when *writing*. When *reviewing* existing prose, judge by density and clustering rather
than single instances.

**Nouns**: delve, tapestry, landscape, realm, testament, journey, insight, resilience, ecosystem, milestone, prowess, utilization

**Verbs**: embark, endeavor, leverage, harness, navigate (metaphorical), unlock, foster, catalyze, bolster, underscore, showcase, elucidate, encompass, unveil, embrace, enhance, illuminate, resonate, transcend

**Adjectives**: seamless, robust, groundbreaking, transformative, pivotal, vibrant, compelling, crucial, invaluable, holistic, multifaceted, meticulous, commendable, intricate, comprehensive, profound, nuanced, innovative

**Adverbs**: seamlessly, meticulously, notably, profoundly, predominantly, subsequently, thereby, ultimately, significantly, particularly, additionally, moreover, furthermore

**Phrases**: "ever-evolving landscape," "in today's fast-paced world," "as we navigate the complexities," "It isn't just X, it's Y," "it's important to note," "it's worth noting that," "without further ado," "in conclusion," "at the heart of"

**Puffery / promotional drift**: "breathtaking," "stunning," "must-see," "must-visit," "iconic," "world-class," "rich cultural tapestry," "hidden gem." AI drifts toward advertisement-like writing even when prompted for a neutral or encyclopedic register — watch for this puffery vocabulary as the canary.

**Hedging phrases**: "it could be argued," "this might suggest," "may potentially," "what could be considered"

**Verb substitution**: AI systematically replaces simple verbs ("is," "are") with elaborate alternatives ("serves as a," "features," "offers"). Over 10% decrease in simple verb usage in AI text.

**False intensifiers**: "genuinely," "truly," "actually" (when used to simulate conviction)

**Era-tracked vocabulary**: AI vocabulary shifts over time. "Delve" peaked 2023–early 2024 then declined as model training data caught up to public awareness; "align with," "fostering," and "showcasing" rose with later models. Treat the kill-list as a living snapshot, not a fixed law — fresh anti-AI corpora keep moving.

## Filler, hedging, and signposting

| Pattern | Tell | Fix |
|---------|------|-----|
| Compulsive signposting | "It's worth noting," "It's important to remember" | Trust the reader; state the point |
| Excessive hedging | "may potentially offer what could be considered significant benefits" | Strip to: "this works" |
| Opinion-avoidant framing | "commonly described as," "many find," "generally considered" | State the view directly |
| Wind-up and wind-down | "In this section, we will…", "In conclusion, we have shown…" | Delete; start with the content and stop at the end |
| Padding phrases | "in order to," "at this point in time," "the fact that" | "to," "now," "that" |

## Register-neutral AI rhetorical patterns

These read as machine-written in any register, so they fail on a documentation deliverable and a
narrative one alike.

| Pattern | Tell | Fix |
|---------|------|-----|
| Perfect antithesis | "Not just X, but Y" as a default construction | State the point; real distinctions are messier |
| Tricolon padding | Three near-synonyms where one works — "clear, concise, and easy to understand" | Cut to the one that carries meaning |
| Hedge-and-pivot transition | "While X is true, it's important to note that Y" as a default connector | Cut the setup; state Y |
| Contrast-and-correct opener | "While many think X, in fact Y" where no one actually thinks X | Open with the claim itself |
| Stacked conjunctions | "Moreover," "Furthermore," "Additionally" opening successive paragraphs | Let the sentences carry the logic |
| Repeated sentence openers | Three or more consecutive sentences starting the same way ("You can…", "This is…") | Vary or combine |
| Rhetorical question staging | "How do we solve this?" followed by the pre-composed answer | Ask a real question or state the point |

## Mechanics floor

- **Active voice** by default; make clear who or what performs the action. Passive is acceptable where the object is genuinely the subject of interest, where naming the actor would misassign blame, or where the actor is irrelevant.
- **Plain words** over elaborate ones: "use" over "utilize", "about" over "with respect to". Take the short familiar word.
- **Front-load.** The first sentence of a paragraph carries its point.
- **Contractions** are welcome in both registers. Their absence reads as stiff, not as formal.
- **Straight quotation marks and apostrophes** (`"` `'`), not curly. Word processors auto-curl; check the output rather than the input.
- **Emoji**: never add unless explicitly requested.
- **Boldface**: only where genuine emphasis serves the reader. Don't bold a term every time it appears, and don't bold a label that the following sentence then restates.
- **No sycophantic or assistant-voice fragments**: "Certainly!", "Great question!", "As an AI", "I should note". These are paste artifacts and always fail.

## Accessibility floor

Binds any prose deliverable published as a document or page, in either register.

- Every image carries alt text; a decorative image carries an empty alt attribute. Don't put information only in an image, and don't use images of text or code.
- Don't rely on color, size, or position alone to carry meaning — pair it with a text label.
- Don't use directional language to locate content ("the box on the right", "see above"). Name the thing, or use "preceding" and "following".
- Use real heading elements in order, with no skipped levels and no empty headings.
- Don't merge table cells. Give tables real header cells, and introduce each table with a complete sentence.
- Write link text that is meaningful out of context, and warn the reader when a link does something unexpected, such as starting a download.
- Expand acronyms on first use and don't write double negatives.
- Minimize all-caps and camel case in prose — screen readers may spell them out letter by letter.

## Inclusive-language floor

Binds every prose deliverable in either register.

- Don't use "whitelist", "blacklist", "master/slave", or "sanity check". Use terms precise to the domain: allowlist and denylist, primary and replica, controller and worker, a quick check or coherence check. Where a code identifier forces the term, name it once as the literal identifier and use the preferred term thereafter.
- Use singular "they" as the general pronoun. Don't use a gendered pronoun unless referring to a specific person of known gender, and never "he/she" or "(s)he".
- Avoid ableist words used figuratively — "crazy", "insane", "blind to", "cripple", "dumb". Say "placeholder", not "dummy".
- Use person-first phrasing for disability by default ("people with disabilities"), and don't describe non-disabled people as "normal".
- Prefer "person-hours" to "man-hours", "humanity" to "mankind", "staffed" to "manned".
- Use diverse names, genders, ages, and locations in examples, and avoid references that assume one country's culture.

## Editing passes

Applies in both registers; the register references add their own passes on top.

1. **Word level** — remove kill-list vocabulary on sight. Strip adjectives that carry no information: "robust system" becomes "handles 10k requests per second without data loss".
2. **Sentence level** — read the first few words of consecutive sentences; where three or more share a pattern, cut or combine.
3. **Structural** — remove meta-commentary and recap conclusions. Merge overlapping sections.
4. **Content** — check that every claim is supported and every specific is still specific.
5. **Read it aloud** — stumbling marks where the prose needs work. This is the single most effective check in either register.
