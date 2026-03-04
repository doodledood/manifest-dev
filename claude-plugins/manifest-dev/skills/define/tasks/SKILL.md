# SKILL Task Guidance

Creating or improving Claude Code skills or agent skills. Composes with PROMPTING.md.

## Quality Gates

- **Progressive disclosure** — Skill body under 500 lines; reference files organized in references/ with clear loading pointers from SKILL.md; no single-file context overload | Verify: line count + directory structure check
- **Instruction transparency** — All rigid directives (MUST/NEVER/ALWAYS) accompanied by reasoning explaining why the constraint matters. LLMs generalize better from understanding than from rigid rules without context | Verify: scan for rigid directives, check each has adjacent explanation

## Context to Discover

Beyond PROMPTING.md's general context probes, surface these before defining a skill:

| Context Type | What to Surface | Probe |
|--------------|-----------------|-------|
| **Existing skills** | Similar skills already available, duplication risk | What skills exist in this area? Would this overlap? |
| **Target platform** | Claude Code, Claude.ai, Cowork — affects available capabilities | Where will this skill run? Subagents available? Browser? |
| **Audience expertise** | Developer, non-technical, mixed — affects communication style within the skill | Who will invoke this skill? What jargon is safe? |
| **Tool requirements** | MCPs, scripts, file access, subagents the skill needs | What tools must be available? Any external dependencies? |
| **Invocation mode** | Auto-invoked, user-invoked (/slash), programmatic (skill-from-skill) | How will this skill be triggered? Multiple modes? |

## Compressed Domain Awareness

*Key skill-creation practices not covered by PROMPTING.md. Informs probing; no resolution needed.*

**Three-level loading** — Skills load in layers: Level 1 = name + description (~100 words, always in context); Level 2 = SKILL.md body (loaded when triggered, keep under 500 lines); Level 3 = bundled resources in references/, scripts/, assets/ (loaded on demand, unlimited). Design for progressive disclosure — what's always needed goes in body, detailed reference data in Level 3.

**Description testing** — Descriptions drive auto-invocation and models tend to undertrigger. Test descriptions against realistic user phrasings (concrete like "my boss sent me this xlsx" not abstract like "format data"). Mix should-trigger and should-not-trigger queries to find the right sensitivity.

**Bundled resources** — When test runs independently produce similar helper scripts or reference lookups, bundle them into scripts/ or references/. Reduces reinvention per invocation and improves reliability.

**Feedback generalization** — Skills run many times across diverse prompts. Improvements should generalize from patterns across test cases, not encode fiddly fixes for specific examples that overfit the test set.

## Risks

- **Context overload** — skill tries to load everything into SKILL.md body instead of using layered references; probe: can content be split into body + references/?
- **Script reinvention** — every invocation independently writes the same helper scripts; probe: are there deterministic/repetitive operations that should be bundled in scripts/?
- **Platform mismatch** — skill depends on capabilities unavailable on target platform (subagents, browser, CLI tools); probe: what platform features does this require?

## Scenario Prompts

- **Undertriggering** — skill exists but Claude never invokes it because description is too narrow, too generic, or uses wrong vocabulary; probe: tested description against realistic user phrasings?
- **Overtriggering** — skill fires for irrelevant queries, polluting unrelated workflows; probe: what near-miss queries should NOT trigger this skill?
- **Author-bias** — skill works for creator's test cases but fails on diverse real-user phrasings and contexts; probe: tested with prompts outside the author's mental model?
- **Skill collision** — multiple skills compete for the same query, causing unpredictable invocation; probe: how does this skill differentiate from adjacent skills in the description?

## Trade-offs

- Generic coverage vs specialized precision
- Pushy description (risk overtrigger) vs conservative description (risk undertrigger)
- All-in-body vs layered references (simplicity vs context efficiency)
- Bundled scripts vs inline generation (reliability and speed vs flexibility)
- Autonomous /do execution vs skill-creator human-in-the-loop (workflow integration vs systematic eval quality)

## Process Guidance Candidates

*PG candidates — presented as batch during interview, user selects which apply.*

- **Use skill-creator for complex skills** — The skill-creator skill provides systematic eval-driven development (test cases, baseline comparison, grading, iteration). NOTE: skill-creator is non-autonomous by design — requires human interaction for eval reviews and feedback cycles, breaking /do's autonomous execution flow. Best suited for complex skills where quality justifies the overhead; may be overkill for simple skills.

## Defaults

*Domain best practices for this task type.*

- **Eval-driven iteration** — Test skill against realistic prompts with baseline comparison (with-skill vs without-skill); iterate based on observed results rather than assumptions about what will work
- **Keep prompt lean** — Remove instructions not pulling their weight; read execution transcripts to identify unproductive patterns the skill causes
