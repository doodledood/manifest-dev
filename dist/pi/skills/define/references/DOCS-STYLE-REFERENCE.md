# Documentation Style Reference

Mechanics for the **documentation register** — specs, proposals, reports, formal documentation,
technical design documents, READMEs, and reference material. Verification lookup data for gate
evaluators.

**Register scope.** Every rule in this file binds documentation-register prose only. Human-voiced
prose — marketing copy, social posts, narrative, creative writing, and blog posts — is governed
by `WRITING-REFERENCE.md` instead, whose rules on rhythm, tonal texture, and deliberate
imperfection do not apply here and are not defects when absent here. Rules that hold in both
registers live in `PROSE-FLOOR-REFERENCE.md` and are not repeated in this file.

**Precedence.** A project's own style sheet or `AUTHOR_VOICE.md` outranks this reference; the
`review-writing` skill applies that rule and is its one home.

**Not for `/define` interviews** — this file is lookup data for gate evaluation. The task files
(`tasks/DOCUMENT.md`, `tasks/TECH_DESIGN.md`) carry the compressed gate text.

---

## Severity anchor

Documentation-register findings are graded on what the prose costs a reader, not on how
AI-generated it sounds. The AI-detection scale used in the human-voice register does not apply.

| Severity | Bar |
|----------|-----|
| **CRITICAL** | The prose misleads or blocks the reader: a procedure whose steps cannot be followed in the order given, a modal verb stating the wrong obligation (`may` where the action is required), a code reference or placeholder that would not work if copied, an instruction whose condition arrives after the action it governs, or a missing accessibility affordance that denies the content to a reader entirely. |
| **HIGH** | A violation of a rule the major style guides agree on, which a professional editor would flag: title-case headings in a sentence-case document, first person addressing the reader, passive voice hiding who acts, undefined jargon or an unexpanded acronym, vague link text, non-inclusive terminology. |
| **MEDIUM** | Local inconsistency or a rule broken without cost to comprehension: mixed date formats, an inconsistent serial comma, a number spelled where the rule wants a numeral, an unnecessary parenthetical. |
| **LOW** | Preference-level observations. Informational only. |

Grade by consequence, not by rule count: ten MEDIUM inconsistencies do not aggregate into a HIGH.

---

## Voice and tone

- Write conversationally, in a friendly and respectful register, without being frivolous. Aim for a knowledgeable colleague explaining something, not a pedantic authority and not entertainment.
- Don't use "please" in instructions. Write "To view the document, click **View**."
- Don't call a task "simple", "easy", "quick", or tell the reader to "just" do something. What is simple for the author may not be for the reader, and the word adds nothing when the step is genuinely easy.
- Keep jokes, pop-culture references, and wordplay out. They date, they distract, and they don't translate.
- Don't use figurative language or metaphor where a plain statement works, and don't attribute human qualities to software or hardware: a system *detects* a device rather than *seeing* it; an object *specifies* a value rather than *telling* something.
- Don't pre-announce unreleased features or plans.

## Person, mood, and tense

- Address the reader as **you**. Don't use "we", "our", or "us" to mean the reader; first person is acceptable only for the authoring organization, with an unambiguous antecedent.
- Reserve **user** for the end user of the software the reader is building. The reader is "you", not "the user".
- Write procedure steps in the imperative: "Click **Submit**", not "You should click Submit".
- Use present tense for behavior, including a result that follows an action: "Send the query. The server returns an acknowledgment." Use "will" only when one event genuinely occurs later than another.

Active voice is a floor rule; see `PROSE-FLOOR-REFERENCE.md`. It bites hardest in procedures,
where the reader is the actor and passive voice hides that from them.

## Sentence and paragraph construction

- Put the condition, circumstance, or goal before the instruction, so a reader can skip what doesn't apply: "To delete the document, click **Delete**" — not "Click Delete to delete the document."
- Keep sentences under about 26 words. Long multi-clause sentences are the single most common comprehension and translation failure in documentation.
- Prefer subject-verb-object order, with subject and verb near the start.
- Use the **same term for the same thing** every time. Elegant variation — swapping in a synonym to avoid repetition — is a defect in this register: a reader cannot tell whether a new word means a new thing.
- Place "only" immediately before what it modifies. Avoid stacking more than two nouns as modifiers of a third.
- Keep optional helper words ("that", "which", "then") where they prevent ambiguity, and replace a pronoun with its noun wherever the antecedent could be misread.

## Punctuation

- **Serial comma**: required. "Locations are divided into zones, regions, and multi-regions."
- **Em dash**: correct for a break in the flow of a sentence—like this—with no space before or after. (The human-voice register restricts em dashes for a different reason; that restriction does not apply here.)
- **En dash**: don't use. Use a hyphen, or the word "to".
- **Semicolon**: avoid where a period or comma will serve. Acceptable to join two closely related independent clauses, and to separate list items that contain their own commas.
- **Exclamation point**: don't use in conceptual or reference documentation. Acceptable in a tutorial to mark a genuine milestone, and in code or literal output where the syntax requires it.
- **Quotation marks**: commas and periods go inside the closing quotation mark, except where the quoted material is a literal string or code, where exactness governs. Double quotes are the default; use single quotes only for code that uses them and for a quote nested inside another. Don't put quotation marks around anything in code font. (Straight rather than curly is a floor rule.)
- **Parentheses**: don't put important information inside them — readers skip parentheticals. Prefer a comma, a dash, or a separate sentence. Don't write "file(s)".
- **Ellipsis**: don't use in prose. In quoted material, use it only for omissions inside a sentence.
- **Slash**: avoid outside code and file paths. Write "or" rather than "and/or".
- **Hyphen**: hyphenate compound modifiers before a noun ("well-designed system"), not after a verb ("the system is well designed"), and never with an -ly adverb ("publicly available service"). Always hyphenate after "self-" and "cross-". Use a hyphen for ranges ("5-10 minutes"), and spell out the range after "from" ("from 5 to 10 minutes").
- **Period**: one space between sentences. No period at the end of a heading.
- **Possessive**: don't form a possessive from a product name, feature name, or code element; attach it to a following ordinary noun or rephrase with "of".

## Capitalization and headings

- Use **sentence case** everywhere: headings, page titles, table headers, table cells, list items, captions, and glossary definitions. Capitalize only the first word, the first word after a colon, and proper nouns.
- Don't end a heading with a period. Don't put links or code items in a heading, and don't number headings to indicate sequence.
- One top-level heading per document; don't skip heading levels, and don't pick a level for its visual weight.
- Write task headings as a bare imperative ("Create an instance"), and conceptual headings as noun phrases ("Migration to the new API"). Avoid opening a heading with an -ing verb.
- Avoid unnecessary capitalization in body text. Don't capitalize a common noun to signal that it matters.
- Keep articles in headings: "Create a VM instance", not "Create VM instance".

## Lists and procedures

- Numbered list when the sequence matters; bulleted list when it doesn't; description list for term-and-definition pairs.
- Introduce every list with a complete sentence, ending in a colon when the list follows immediately.
- Keep list items parallel in structure. Capitalize the first word. End items with a period unless the item is a single word, a fragment with no verb, entirely code, or entirely link text — and be consistent within a list.
- Don't write a one-item list.
- One action per procedure step, with the step's first sentence carrying an imperative verb. State where the action happens before the action itself, and state the result in the same step rather than as a step of its own.
- Prefix an optional step or section with "Optional:".
- Don't repeat a procedure documented elsewhere; link to it.
- Don't use directional language — "above", "below", "the box on the right". Use "preceding", "following", or the name of the thing.

## Numbers, dates, and units

- Spell out zero through nine; use numerals for 10 and above. Use numerals throughout a sentence that mixes both.
- Always use numerals for versions, measurements, prices, percentages, and step or chapter numbers.
- Spell out a number that starts a sentence, and spell out all ordinals ("first", "twelfth" — never "1st").
- Percentages take a numeral and the symbol, no space: "40%".
- Use a leading zero on decimals below one. Use commas as thousands separators from four digits up.
- Write dates as "January 19, 2017", or ISO 8601 (`2017-01-19`) where a numeric form is needed. A month with a year takes no comma. Don't use slash dates.
- Use the 12-hour clock with capitalized AM/PM. Avoid seasons; use months or quarters.
- Put a nonbreaking space between a number and its unit (64 GB), except for currency, percent, and degrees. Match binary and decimal byte units to what is actually measured — don't write GB where GiB is meant.

## Links and cross-references

- Use short, descriptive link text that makes sense out of context. Never "click here", "this document", or a bare URL as link text.
- When linking to a page or section by name, match the link text to its title.
- Standard phrasing: "For more information, see …". Use "see", not "on" or "at".
- Put punctuation outside the link, and don't put quotation marks around link text.
- Be selective: prefer a brief in-place explanation over a link for a definition or a short step. Don't link twice to the same destination on one page, and don't force a link to open in a new tab.

## Word choice

- **because**, not "since", when stating cause. **after**, not "once", when stating sequence.
- **can** for ability or an optional action; **may** for permission or policy; **must** for a requirement. Avoid "should" — say what happens if the reader does otherwise.
- Don't use "via" — use "through", "by using", or "with".
- "in order to" → "to". "allows you to" → "lets you". "utilize" → "use", except when referring to resource utilization. "leverage" → "use", "build on", or "take advantage of".
- Don't use "i.e." or "e.g." — write "that is" and "for example". Avoid "etc." and "and so on".
- Don't use "and/or" outside space-constrained contexts like a table cell.
- Don't abbreviate with slashes ("w/", "c/o") or substitute symbols for words ("10x" → "10 times", "&" → "and" outside official names).
- Expand an acronym on first use, then use the acronym. Don't use periods in acronyms. If the first mention falls in a heading, expand it in the following paragraph instead.
- Write around jargon where plain language exists. Where a term must appear, define it briefly on first use or link to a definition.

## Timeless documentation

- Don't write "currently", "now", "at this time", "presently", "soon", "eventually", "new", "newer", "latest", or "does not yet". Documentation describes the product as it is; these words are either implied or will go stale.
- Where a change genuinely needs anchoring, anchor it to a release or date: "The January 2026 release adds …".
- Describe how the product works now — not how it has changed, and not how it might change.
- Exception: release notes, changelogs, and blog posts, where the point *is* the change over time.

## Code and interface references

- Use code font for: filenames, paths, and extensions; class, method, function, and enum names; environment variables; command names and their output; HTTP verbs, status codes, and content types; data types, constants, and keywords; placeholders; ports and IP addresses; query parameters; and text the reader types into a field.
- Use ordinary font for product and service names, and for URLs the reader visits in a browser.
- Don't inflect a code element to make it plural or possessive. Add a noun and inflect that: "the `POST` request", "the `ADDRESS` constant's value".
- Don't put quotation marks or angle brackets around a code element, and don't put a code item in a heading.
- Write placeholders in uppercase with underscores (`API_NAME`), without possessive prefixes (`MY_`, `YOUR_`). Introduce a single one with "Replace `PLACEHOLDER` with …", and several with "Replace the following:".
- Introduce a code sample with a complete sentence, ending in a colon when the sample follows immediately. Indicate omitted code with a comment in the language's own syntax, not bare dots.
- In command syntax, put optional arguments in square brackets, mutually exclusive choices in braces separated by pipes, and repeated arguments after three dots. Keep a copyable command free of brackets, braces, and ellipses. Wrap at 80 characters.
- Interface verbs: **click** (never "click on") for a mouse target; **select** and **clear** for checkboxes; **choose** for a menu option; **enter** or **type** for text input; **press** for keys; **tap** for touch. Bold the names of interface elements, and write a menu path as bold items separated by angle brackets.
- Name files in lowercase with hyphens between words. Refer to a file type by its formal name — "a PNG file", not "a .png file".

## Accessibility and inclusive language

Both floors bind every register, so they live in `PROSE-FLOOR-REFERENCE.md` and are evaluated
from there. Two documentation-specific applications of the accessibility floor are stated in this
file where they arise: table structure under **Lists and procedures** and link text under
**Links and cross-references**.

---

## Attribution

Portions of this reference are modifications based on work created and shared by Google and used
according to terms described in the [Creative Commons 4.0 Attribution License](https://creativecommons.org/licenses/by/4.0/).
The source is the [Google developer documentation style guide](https://developers.google.com/style),
distilled here for offline gate evaluation; consult it directly for questions this reference
doesn't cover.
