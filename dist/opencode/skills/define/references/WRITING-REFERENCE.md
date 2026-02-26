# Writing Quality Reference

Reference material for writing quality verification. Use as context when verifying writing task deliverables.

**Purpose**: Verification fallback for users without the writing plugin (writing-reviewer agent). Pass this file as context to a general-purpose verifier when writing-reviewer is unavailable.

**Not for /define interviews** — this file contains lookup tables and detailed rules. The task file (`tasks/WRITING.md`) has compressed summaries for interview probing. Do not load this file during `/define`.

---

## Vocabulary Kill-List

Statistically flagged as AI-generated across peer-reviewed studies of millions of documents. Never use:

**Nouns**: delve, tapestry, landscape, realm, testament, journey, insight, resilience, ecosystem, milestone, prowess, utilization

**Verbs**: embark, endeavor, leverage, harness, navigate (metaphorical), unlock, foster, catalyze, bolster, underscore, showcase, elucidate, encompass, unveil, embrace, enhance, illuminate, resonate, transcend

**Adjectives**: seamless, robust, groundbreaking, transformative, pivotal, vibrant, compelling, crucial, invaluable, holistic, multifaceted, meticulous, commendable, intricate, comprehensive, profound, nuanced, innovative

**Adverbs**: seamlessly, meticulously, notably, profoundly, predominantly, subsequently, thereby, ultimately, significantly, particularly, additionally

**Phrases**: "ever-evolving landscape," "in today's fast-paced world," "as we navigate the complexities," "It isn't just X, it's Y," "it's important to note," "it's worth noting that," "without further ado," "in conclusion," "at the heart of"

**Hedging phrases**: "it could be argued," "this might suggest," "may potentially," "what could be considered"

**Verb substitution**: AI systematically replaces simple verbs ("is," "are") with elaborate alternatives ("serves as a," "features," "offers"). Over 10% decrease in simple verb usage in AI text.

**False intensifiers**: "genuinely," "truly," "actually" (when used to simulate conviction)

## Anti-Patterns

### Structural

| Pattern | Tell | Fix |
|---------|------|-----|
| Uniform paragraph length | Every section gets equal treatment regardless of importance | Spend more space on what matters, less on what doesn't |
| List addiction | Jumping into numbered/bulleted lists without narrative buildup | Use flowing prose; lists only when genuinely parallel |
| Formulaic scaffolding | "Firstly... Secondly... Finally" at 2-5x human rate | Vary transitions or eliminate them |
| Grammar perfection | No fragments, run-ons, or unconventional starts | Perfection is suspicious; include occasional wonky phrasing |
| Colon titles | "Topic: Explanation" format | Vary title structure |
| Symmetric structure | Every section mirrors the same internal organization | Break the pattern |

### Rhetorical

| Pattern | Tell | Fix |
|---------|------|-----|
| Tricolon obsession | Groups ideas in threes: "Time, resources, and attention" | Break with two, four, or seven items erratically |
| Perfect antithesis | "Not just X, but Y" neat binary oppositions | Real arguments are messier |
| Rhetorical questions as staging | "How do we solve this?" with pre-composed answer | Ask genuine questions or just state the point |
| Excessive hedging | "may potentially offer what could be considered significant benefits" | Strip to: "this works" |
| Compulsive signposting | "It's worth noting," "It's important to remember" | Trust the reader |
| Opinion-avoidant framing | "commonly described as," "many find," "generally considered" | State the view directly |

### Tonal

| Pattern | Tell | Fix |
|---------|------|-----|
| Uniform register | Same tone throughout; no tonal shifts | Shift between formal and colloquial; reveal personality |
| Relentless positivity | Everything framed positively; nothing weak or bad | Call things weak, inadequate, or bad when they are |
| Equal professional distance | All subjects treated with same measured tone | Nerd out about what you care about; show impatience with boring parts |
| Risk aversion | No confusing sentences, sharp observations, or controversial assertions | Take risks; write surprising, opinionated content |
| Emotional overreach without depth | Exclamation marks, enthusiastic phrasing that feels oddly impersonal; polished yet hollow, like a greeting card for someone you've never met | Replace emotional proxies with actual emotional content grounded in specifics |

## Punctuation & Formatting Rules

- **Em-dashes and en-dashes**: One of the most reliable AI tells. ChatGPT uses 8 per 573 words; Deepseek 9 per 555 words. Ban entirely; use commas, periods, parentheses, or colons instead.
- **Emojis**: AI overuses emojis as emotional proxies. Never add unless explicitly requested.
- **Semicolons**: AI rarely uses them. Including some adds human texture.
- **Contractions**: AI avoids them. Use freely in conversational prose.
- **Oxford commas**: AI applies them consistently. Break the pattern occasionally.
- **Casual language markers**: Inject informal connectors ("So," "Anyway," "By the way," "if I recall correctly," "I've found that," "in my experience") for disproportionate impact on human feel.

## Craft Fundamentals

Seven areas where human writers create unbridgeable distance from AI output (structural limitations of statistical text generation):

1. **Showing vs telling** — AI defaults to summarizing emotions ("serene and tranquil") rather than rendering specific sensory details. Probe: does the content show or tell?
2. **Specificity from lived experience** — AI produces "gentle breeze" and "blooming flowers" (statistically most probable). Probe: are descriptions generic or from actual observation?
3. **Strategic omission** — AI tends toward completeness and closure. Resonant writing lives in what's left unsaid. Probe: is everything spelled out, or does some meaning come from silence?
4. **Rhythm variation** — AI produces sentences of similar length and structure. Probe: do sentence lengths vary deliberately for effect?
5. **Deliberate rule-breaking** — AI won't choose the wrong word because it sounds better, or let a fragment hang. Probe: is there intentional imperfection?
6. **Humor** — Classified as an "AI-complete problem" (Google DeepMind study). Probe: does humor feel authentic or manufactured?
7. **Genuine insight** — AI provides summaries; humans provide analysis. Probe: does the content answer "so what?" with original thinking?

## Statistical Signatures

What detectors measure (understanding these helps write text that doesn't trigger them):

| Metric | Human | AI | Meaning |
|--------|-------|-----|---------|
| Perplexity (surprisal) | ~8.2 | ~4.2 | AI is ~50% more predictable |
| Burstiness (sentence variation) | 0.61 | 0.38 | AI has ~38% less variation |
| Token probability entropy | 4.56 | 3.11 | AI makes more uniform word choices (d=3.08) |
| Type-token ratio | 55.3 | 45.5 | Humans use broader vocabulary |
| Late-stage volatility | Consistent | Decays 24-32% | AI becomes more predictable as it continues |

Key implication: introduce genuine unpredictability through varied vocabulary, surprising sentence lengths, unexpected word choices, inconsistent structure. Target ~7th grade readability to push away from complex multi-clause sentences that signal AI.

## Model-Specific Signatures

| Model | Key Tells |
|-------|-----------|
| **ChatGPT** | Formal, clinical; heavy em-dashes (8/573 words); overuses "delve," "align," "noteworthy"; dry, robotic |
| **Gemini** | Conversational, explanatory; prefers simple language; no em-dash overuse |
| **Claude** | More natural and literary; minimal em-dashes (2/948 words); tonal flexibility; occasionally generates fiction unprompted |
| **Deepseek** | Heavy em-dashes (9/555 words); similar to ChatGPT structurally |

## Four-Layer Editing

Apply in order from surface to substance:

1. **Word-level** — Search-replace kill-list vocabulary on sight. Strip adjectives, restore only those carrying concrete information. "Robust system" becomes "handles 10k req/s without data loss."
2. **Sentence-level** — Read first few words of consecutive sentences; wherever three or more follow same pattern, cut or combine. Vary sentence length deliberately: short for punch, long for nuance.
3. **Structural** — Eliminate meta-commentary ("In this section, we will..."). Kill recap conclusions. Break pattern symmetry: demote repetitive subheadings, merge overlapping sections.
4. **Content** — Add lived experience: anecdotes, firsthand observations, specific failures. Ground in specifics. Inject honest opinion: state what you actually think.
5. **Final check** — Read aloud. Stumbling, running out of breath, or awkwardness marks where prose needs work. Cited as "the single most effective technique." Checklist: can you explain the argument order naturally? Are claims traceable? Does the tone match how you actually write? Would you be embarrassed if someone knew AI helped?

## Negative Space

AI text is identified as much by what's absent as what's present:

- **Lived experience** — specific personal anecdotes, not "generic specificity"
- **Sensory specificity** — unexpected observations, not statistically probable descriptions
- **Silence and subtext** — what's left unsaid, what characters don't say
- **Genuine messiness** — false starts, changed directions, productive digressions
- **A perspective** — a view that could not fit any other prompt

## Editorial Standards

What gets writing accepted vs rejected by human editors:

**Accepted**: Distinctive voice, subtext and layers, specificity grounded in real experience, emotional truth and vulnerability, intentional craft choices (including deliberate imperfection), surprise, the sense that the writer has something at stake.

**Rejected**: Uniform sentence length and structure, generic language that could apply to any topic, absence of subtext, over-smooth prose without personality, telling without showing, predictable patterns and stock phrases.

AI-generated submissions are identifiable because they are "bad in ways that no human has been bad before" (Neil Clarke, Clarkesworld). Even polished hybrid works display recognizable hallmarks.
