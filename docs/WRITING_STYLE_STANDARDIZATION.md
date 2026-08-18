# Writing-style standardization — investigation read

**Status**: Implemented. This document records the investigation that produced the design — an examination of the [Google developer documentation style guide](https://developers.google.com/style) against the repo's existing writing references. The design it recommends now ships: `PROSE_FLOOR.md` carries the shared floor, `WRITING.md` and `DOCUMENT.md` are the two register overlays, `DOCS-STYLE-REFERENCE.md` and `PROSE-FLOOR-REFERENCE.md` are new evaluator references, and the `review-writing` skill applies the same standards outside a manifest run. The problem statement below describes the state before that change.

**Date**: 2026-08-18. Google guide state as fetched that day (last upstream update July 7, 2026).

## The problem

The repo carries two bodies of writing guidance with different jobs:

- **Anti-AI-tell corpus** (`define/references/WRITING-REFERENCE.md`, plus the reviewer-side `review-code/references/prose-value.md`): judges whether prose reads as authentically human-voiced — kill-list vocabulary, statistical variation, craft, tonal texture.
- **Document-structure gates** (`define/tasks/DOCUMENT.md`, `TECH_DESIGN.md`): demand uniform terminology and style but have no mechanics standard behind them — nothing on headings, lists, punctuation, numbers, dates, link text, code-in-text, placeholders, UI verbs, accessibility, inclusive language, or global-audience phrasing.

Because `WRITING.md` is the base for all prose task types, the anti-tell rules bind register-blind, and they conflict with documentation-style norms — including the repo's own DOCUMENT consistency gate — whenever the deliverable is a formal document.

## The conflict inventory

Verified conflicts between the anti-tell corpus and the documentation-style consensus (Google, corroborated by the Microsoft Writing Style Guide on every axis below):

| # | Axis | Documentation consensus | Anti-tell corpus |
|---|------|--------------------------|------------------|
| 1 | Em dashes | Standard device for breaks; no space before or after; en dash unused | "Ban entirely" (density is an AI tell) |
| 2 | Serial comma | Required, always | "Break the pattern occasionally" |
| 3 | Semicolons | "If possible, avoid" | "Including some adds human texture" |
| 4 | Terminology | Exact same term for the same thing everywhere; no elegant variation | Vocabulary diversity rewarded as a human signal |
| 5 | Sentence length | Short (under ~26 words), consistently | Deliberate burstiness, long sentences for nuance |
| 6 | Humor / personality | Discouraged in docs | Absence is an AI tell |
| 7 | Deliberate imperfection | Consistency and correctness | "Include occasional wonky phrasing" |

Equally load-bearing: the two corpora **agree** on a large floor — no puffery or buzzwords (robust, seamless, leverage), no filler ("in order to", "it's worth noting"), no hedging, active voice, contractions welcome, straight quotes, plain words, front-load the point, don't open successive sentences identically, specifics over generic abstraction. The conflicts are register conflicts, not a contradiction between the corpora's purposes.

## The read

**Standardize by register partition plus a precedence residue, delivered as a distilled local reference in the existing gate-lookup slot.** Confidence: high on the structure, medium on file-level placement details.

1. **Two registers, one floor.** Documentation register (DOCUMENT, TECH_DESIGN, repo-resident docs reviewed by prose-value) is governed by a distilled documentation-style standard derived from Google's guide. Human-voice register (BLOG and the expressive genres in the WRITING base — articles, marketing, social, creative) is governed by the existing anti-tell corpus. The agreement floor above, plus accessibility and inclusive-language rules, binds in both registers.
2. **Contested rules live only in a register layer, never in the base.** The base `WRITING.md` gate set keeps the floor (kill-list, puffery, filler, accuracy, audience fit); the statistical-variation gate moves to the human-voice layer. This dissolves the repo's internal DOCUMENT-vs-WRITING conflict at authoring time rather than asking each gate evaluator to adjudicate it — necessary because per-gate verifier executions may load only one reference and cannot resolve cross-file precedence themselves.
3. **A new distilled reference, not a link and not a mirror.** `define/references/` gains a documentation-style reference distilled from the Google guide (verifiers can't rely on network access; the full guide and its ~587-entry word list are too large and update continuously). The file carries the CC BY 4.0 attribution notice ("modifications based on work created and shared by Google…") and a link to the canonical guide as the fallback tier.
4. **Precedence chain, mirroring the Google guide's own:** a project's own style sheet or `AUTHOR_VOICE.md` first, then the register standard, then external fallbacks (the online Google guide; Merriam-Webster first-listed spellings). `prose-value.md` already defers to a present style guide, so the reviewer side needs at most a pointer.
5. **One outright repair, not a scoping:** the anti-tell rule "Oxford commas: break the pattern occasionally" is contradicted by every major authority in every register (Chicago requires the serial comma; AP omits it consistently; no authority endorses varying it within a document). Deliberate punctuation inconsistency is an editor-visible defect bought for marginal detector evasion. Replace with: pick one convention and hold it; get burstiness from rhythm and vocabulary, not punctuation correctness. The neighboring imperfection rules (fragments, rhythm breaks) survive in the human-voice register as legitimate craft, reworded as intentional devices rather than "errors".
6. **Docs-register gates need their own severity anchor.** The existing scale (CRITICAL = immediately identifiable as AI) doesn't fit mechanics violations. Docs mechanics: CRITICAL = misleads or blocks the reader (wrong can/may/must, broken procedure order); HIGH = consensus-rule violation an editor would flag; MEDIUM = local inconsistency.

### What the distilled documentation standard covers (from the research)

Voice and tone (conversational, never frivolous; no "please" in instructions; no "simply/easy/just/quickly"; humor and figurative language out; no anthropomorphism). Person and tense (second person "you", never "we"; "user" reserved for the reader's software's users; imperative procedures; present tense, "will" only for genuinely later events; active voice with three narrow passive exceptions). Punctuation (serial comma; unspaced em dashes; no en dashes; semicolons avoided; straight quotes; exclamation points out of concept/reference docs; parentheses not for important information). Capitalization and structure (sentence case for headings, titles, table headers, list items; no heading periods; task headings in bare imperative; numbered lists only for sequences; parallel list items; condition before instruction; sentences under ~26 words; front-loaded paragraphs). Numbers, dates, units (spell zero–nine; numerals 10+; all ordinals spelled; "January 19, 2017" or ISO 8601; nonbreaking space number–unit; exact byte units). Links ("For more information, see…"; descriptive link text, never "click here" or bare URLs). Word choices (since→because, once→after, via→through/by using, "in order to"→to, "allows you to"→"lets you", can/may/must semantics, timeless-docs vocabulary — no "currently/now/new/soon" unless release-anchored). Code and UI (code-font inventory; never inflect code elements; UPPER_SNAKE placeholders without MY_/YOUR_; click/select/choose/press/tap verb system; bold UI names; menu paths with >). Register-independent floors: inclusive language (allowlist/denylist-style domain-precise replacements, singular they, no ableist terms, diverse example names) and accessibility (alt text, no directional "above/below", no merged table cells, don't rely on color alone).

## Evidence ledger (summary)

- Google guide pages fetched 2026-08-18, per-rule provenance retained in the investigation log: `/style` (precedence, "guidelines, not rules"), `/style/highlights`, `/style/tone`, `/style/accessibility`, `/style/inclusive-documentation`, `/style/translation`, `/style/timeless-documentation`, `/style/voice`, `/style/person`, `/style/contractions`, `/style/commas`, `/style/dashes`, `/style/semicolons`, `/style/quotation-marks`, `/style/exclamation-points`, `/style/hyphens`, `/style/capitalization`, `/style/headings`, `/style/lists`, `/style/procedures`, `/style/tables`, `/style/text-formatting`, `/style/numbers`, `/style/dates-times`, `/style/units-of-measure`, `/style/link-text`, `/style/cross-references`, `/style/code-samples`, `/style/code-in-text`, `/style/code-syntax`, `/style/placeholders`, `/style/ui-elements`, `/style/word-list`, `/style/whats-new`, plus grammar pages (abbreviations, articles, anthropomorphism, clause-order, jargon, possessives, prepositions, pronouns, tense, sentence-structure, spelling). Load-bearing quotes (serial comma, em dash, precedence) re-verified through direct fetches as a second path.
- Repo files: `define/tasks/WRITING.md`, `BLOG.md`, `DOCUMENT.md`, `TECH_DESIGN.md`, `define/references/WRITING-REFERENCE.md`, `review-code/references/prose-value.md`, `define/SKILL.md` (task index and reference-file semantics).
- Cross-guide context: Microsoft Writing Style Guide agreement on the conflict axes; Chicago/AP serial-comma positions; GitLab's empirical guide selection; criticism that Google's rules lack cited research grounding (Bob Watson, 2017).
- License: developers.google.com content is CC BY 4.0 (verified at Google's site-policies page), permitting a distilled derivative with attribution.
- An independent re-derivation from the evidence alone (conclusion withheld) converged on the same partition-plus-precedence structure and the same losing rivals, and contributed the severity-anchor point and the licensing check.

## Alternatives weighed and set aside

- **Do nothing**: leaves DOCUMENT/TECH_DESIGN consistency gates with no evaluable standard and keeps seven live conflicts, including one internal to the repo.
- **Adopt Google wholesale**: kills the anti-tell corpus in the registers where it does its work; Google itself scopes its guide to developer docs and disclaims broader registers.
- **Anti-tell corpus everywhere**: defies an industry consensus (two independent major guides) for documentation mechanics and leaves the mechanics gap standing.
- **Precedence order only, no partition**: pushes conflict resolution to evaluation time, which isolated per-gate verifiers cannot perform.
- **Link to the guide instead of distilling**: verifiers have no guaranteed network; the guide changes under the gate's feet.
- **Full local mirror**: unmaintainable (~587 word-list entries, continuous upstream updates).

## Known assumptions

- **ASM-1**: "All the refs" means the Google guide plus this repo's existing writing references. The upstream "writing plugin v1.3.0" noted as WRITING.md's source is not in this repo; its content is treated as already absorbed. Impact if wrong: a source corpus is missing from the reconciliation, and edits here may diverge from an upstream that still syncs.
- **ASM-2**: The deliverable's home is the define reference layer plus task-file wiring, not a new standalone skill or plugin. A new skill would duplicate the delivery vehicles that already exist (gates and review dimensions). Impact if wrong: packaging changes; the content stands.
- **ASM-3**: The existing gate-threshold shape and severity vocabulary stay, extended by the docs-register severity anchor above.
- **ASM-4**: How much of Google's inventory to distill is a curation call; the section list above is the recommended cut line, erring toward rules a text deliverable in this ecosystem can actually violate.

## What would overturn this read

- Evidence that the project wants AI-tell pressure (variation machinery specifically, beyond the kill-list floor) kept on formal documents — that would soften the partition into scoped gates rather than relocation.
- The upstream writing plugin turning out to be live and synced, which would move the reconciliation there instead of here.
- Empirical evaluation (the direction GitLab took) showing the anti-tell rules do not measurably affect reader trust or editor acceptance — that would thin the human-voice layer toward "one documentation guide plus a small anti-slop annex," since the docs-register consensus is convergence between vendors, not controlled validation.
- A decision to make the workflows register-agnostic by dropping formal-document task types entirely, which would remove the docs register this design exists to serve.
