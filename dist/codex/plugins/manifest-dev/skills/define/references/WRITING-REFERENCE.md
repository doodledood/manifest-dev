# Human-Voice Writing Reference

Rules for the **human-voice register** — articles, marketing and social copy, newsletters,
narrative, creative writing, and blog posts. Verification lookup data for gate evaluators.

**Register scope.** Every rule in this file binds human-voiced prose only. Documentation-register
prose — specs, proposals, reports, formal and technical documentation — is governed by
`DOCS-STYLE-REFERENCE.md` instead, and the rules here on rhythm variation, tonal shifts, and
deliberate imperfection are **defects** in that register, not virtues: a specification is supposed
to read uniformly. Rules that hold in both registers live in `PROSE-FLOOR-REFERENCE.md` and are
not repeated here.

**Precedence.** A project's own style sheet or `AUTHOR_VOICE.md` outranks this reference; the
`review-writing` skill applies that rule and is its one home.

**Severity.** CRITICAL = immediately identifiable as AI-written. HIGH = experienced readers would
notice. MEDIUM/LOW = informational. (The documentation register grades on cost to the reader
instead; see that reference's own anchor.)

**Not for `/define` interviews** — lookup data for gate evaluation. The task file
(`tasks/WRITING.md`) carries the compressed gate text.

---

## Anti-patterns

### Structural

| Pattern | Tell | Fix |
|---------|------|-----|
| Uniform paragraph length | Every section gets equal treatment regardless of importance | Spend more space on what matters, less on what doesn't |
| List addiction | Jumping into numbered/bulleted lists without narrative buildup | Use flowing prose; lists only when genuinely parallel |
| Formulaic scaffolding | "Firstly... Secondly... Finally" at 2-5x human rate | Vary transitions or eliminate them |
| Grammar perfection | No fragments, no unconventional starts, nothing that breaks stride | Perfection reads as machine-made; an intentional fragment or a sentence that starts on a conjunction is craft here |
| Colon titles | "Topic: Explanation" format | Vary title structure |
| Symmetric structure | Every section mirrors the same internal organization | Break the pattern |

### Rhetorical

| Pattern | Tell | Fix |
|---------|------|-----|
| Tricolon obsession | Ideas habitually grouped in threes: "time, resources, and attention" | Break with two, four, or seven items erratically |

### Tonal

| Pattern | Tell | Fix |
|---------|------|-----|
| Uniform register | Same tone throughout; no tonal shifts | Shift between formal and colloquial; reveal personality |
| Relentless positivity | Everything framed positively; nothing weak or bad | Call things weak, inadequate, or bad when they are |
| Equal professional distance | All subjects treated with the same measured tone | Nerd out about what you care about; show impatience with the boring parts |
| Risk aversion | No sharp observations, no controversial assertions | Take risks; write surprising, opinionated content |
| Emotional overreach without depth | Exclamation marks and enthusiastic phrasing that feel oddly impersonal; polished yet hollow, like a greeting card for someone you've never met | Replace emotional proxies with actual emotional content grounded in specifics |
| Encyclopedic-yet-promotional drift | Even when prompted for a neutral register, AI drifts toward advertisement prose — travel-guide copy for places, marketing copy for products | Neutral doesn't mean polished-bland; it means specific, factual, and unlabored |

## Punctuation as a tell

These are register-specific readings of punctuation. The documentation register reads the same
marks differently and its reading governs there.

- **Em dashes and en dashes**: one of the most reliable AI tells in human-voiced prose. ChatGPT uses 8 per 573 words; Deepseek 9 per 555 words. Avoid them here; use commas, periods, parentheses, or colons instead. (In documentation the em dash is the correct mark for a sentence break and carries no such signal.)
- **Semicolons**: AI rarely uses them. A few add human texture in this register. (Documentation avoids them.)
- **Serial comma**: pick one convention and hold it for the whole piece. Varying it within a deliverable is an editor-visible defect that buys nothing — no major style authority endorses inconsistency, and rhythm should come from sentence construction and word choice, not from punctuation that changes rules mid-piece.
- **Heading capitalization**: match the surrounding document's style rather than defaulting to title case. (Documentation is always sentence case.)
- **Casual language markers**: informal connectors — "So," "Anyway," "By the way," "if I recall correctly," "I've found that," "in my experience" — have disproportionate impact on how human the prose reads.

## Craft fundamentals

Seven areas where human writers create distance from AI output — structural limitations of
statistical text generation, not stylistic preferences.

1. **Showing vs telling** — AI summarizes emotion ("serene and tranquil") rather than rendering specific sensory detail. Does the content show or tell?
2. **Specificity from lived experience** — AI produces "gentle breeze" and "blooming flowers" because they are statistically probable. Are the descriptions generic or observed?
3. **Strategic omission** — AI tends toward completeness and closure. Resonant writing lives in what's left unsaid. Is everything spelled out, or does some meaning come from silence?
4. **Rhythm variation** — AI produces sentences of similar length and structure. Do sentence lengths vary deliberately for effect: short for punch, long for nuance?
5. **Deliberate rule-breaking** — AI won't choose the wrong word because it sounds better, or let a fragment hang. Is there intentional imperfection?
6. **Humor** — classified as an "AI-complete problem". Does the humor feel authentic or manufactured?
7. **Genuine insight** — AI provides summaries; humans provide analysis. Does the content answer "so what?" with original thinking?

## Statistical signatures

What detectors measure. Understanding these helps write prose that doesn't trigger them.

| Metric | Human | AI | Meaning |
|--------|-------|-----|---------|
| Perplexity (surprisal) | ~8.2 | ~4.2 | AI is ~50% more predictable |
| Burstiness (sentence variation) | 0.61 | 0.38 | AI has ~38% less variation |
| Token probability entropy | 4.56 | 3.11 | AI makes more uniform word choices (d=3.08) |
| Type-token ratio | 55.3 | 45.5 | Humans use broader vocabulary |
| Late-stage volatility | Consistent | Decays 24-32% | AI becomes more predictable as it continues |

Introduce genuine unpredictability through varied vocabulary, surprising sentence lengths,
unexpected word choices, and inconsistent structure. Target roughly 7th-grade readability to push
away from the complex multi-clause sentences that signal AI.

Vocabulary diversity is a virtue **here** and a defect in documentation, where the same thing
must carry the same name every time.

## Model-specific signatures

| Model | Key Tells |
|-------|-----------|
| **ChatGPT** | Formal, clinical; heavy em-dashes (8/573 words); overuses "delve," "align," "noteworthy"; dry, robotic |
| **Gemini** | Conversational, explanatory; prefers simple language; no em-dash overuse |
| **Claude** | More natural and literary; minimal em-dashes (2/948 words); tonal flexibility; occasionally generates fiction unprompted |
| **Deepseek** | Heavy em-dashes (9/555 words); similar to ChatGPT structurally |

## Editing passes for this register

The floor's passes apply first. These come after.

1. **Rhythm** — vary sentence length deliberately. Where consecutive sentences share a length and shape, break one.
2. **Voice** — inject honest opinion. State what you actually think, and let the piece be wrong about something rather than safe about everything.
3. **Lived experience** — add anecdotes, firsthand observation, specific failures. Ground abstractions in something that happened.
4. **Final check** — read it aloud. Can you explain the argument order naturally? Does the tone match how you actually write? Would you be embarrassed if someone knew AI helped?

## Negative space

AI text is identified as much by what's absent as by what's present:

- **Lived experience** — specific personal anecdotes, not "generic specificity"
- **Sensory specificity** — unexpected observations, not statistically probable descriptions
- **Silence and subtext** — what's left unsaid
- **Genuine messiness** — false starts, changed directions, productive digressions
- **A perspective** — a view that could not fit any other prompt

## Editorial standards

**Accepted**: distinctive voice, subtext and layers, specificity grounded in real experience,
emotional truth, intentional craft choices including deliberate imperfection, surprise, the sense
that the writer has something at stake.

**Rejected**: uniform sentence length and structure, generic language that could apply to any
topic, absence of subtext, over-smooth prose without personality, telling without showing,
predictable patterns and stock phrases.

AI-generated submissions are identifiable because they are "bad in ways that no human has been bad
before" (Neil Clarke, Clarkesworld). Even polished hybrid works display recognizable hallmarks.
