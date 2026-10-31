---
kind: skill
covers: claude-plugins/manifest-dev/skills/review-writing
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# review-writing

Reviews prose against the project's writing standards in the register it detects — documentation or human-voiced writing — and reports graded findings with the fix.

## How a user reaches it

- `/review-writing [file or pasted text] [register=docs|voice]`. An explicit register wins; otherwise it infers one and says so. The docs register covers specs, READMEs and reports; the voice register covers posts, articles and marketing copy.
- Phrases its description matches: "does this read as AI-written", "review this before publishing".
- define's writing and document gates.
- The project's style sheet, `AUTHOR_VOICE.md` and the user's stated rules outrank the shipped references.

## Scenarios

### review
Run: `scripts/drive-skill.sh review-writing verification/prompts/review-writing-review.md`
Proves: a report naming the register it used and findings with severity and a fix. The draft is unchanged.
Check: read

### user-rule-critical
Run: `scripts/drive-skill.sh review-writing verification/prompts/review-writing-user-rule-critical.md`
Proves: a team rule whose result is a CRITICAL (softening a required step to "may") — the CRITICAL is still reported, naming the rule.
Check: read

### user-rule
Run: `scripts/drive-skill.sh review-writing verification/prompts/review-writing-user-rule.md`
Proves: with two team rules the references contradict (Title Case headings, "utilize") and a draft following them, neither raises a finding, and the report says which rules it applied.
Check: read

## Gotchas

- A wrong register gives a wrong review; name it when the text is mixed.
- Whether prose earns its place in a code change is review-code's `prose-value`, not this.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set. No behavior case measures it.
- Not yet driven: the description phrases, define's writing gates, the voice register.
