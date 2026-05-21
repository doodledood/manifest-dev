---
name: prompt-engineering
description: 'Create, update, slim, or review LLM prompts in the slim discipline — every word steers (behavior the model wouldn''t reach on its own) or scaffolds (preempts a failure the clean posture handles); cut scaffold. 1-3 paragraphs of essence in SKILL.md, contracts in references. Use when writing, slimming, reviewing, or diagnosing a prompt. Triggers: write a prompt, slim a prompt, edit a prompt, review a prompt, improve a prompt, diagnose prompt failure, fix failing prompt, system prompt, skill, agent.'
argument-hint: '<request>'
user-invocable: true
---

**User request**: $ARGUMENTS

Prompts are manifests: state the goal and the load-bearing constraints; trust the model to do everything else. Every word **steers** (behavior the model wouldn't reach on its own) or **scaffolds** (preempts a failure the clean posture handles); cut scaffold. The default is too few words — add specific lines back only when an observed failure justifies it. Aspirational shape: **1-3 short paragraphs** in SKILL.md; `references/*.md` for progressive disclosure — material loaded conditionally per branch, flag, or failure mode. If a reference would always be loaded, fold it back into SKILL.md. The model knows how to search, analyze, generate, format — don't restate. Decision rules over absolutes for judgment calls; no arbitrary numbers; low-arousal tone.

**Branch.** *Creating:* probe essence (one-sentence job, anti-defaults that need steering, exact contracts), then draft 1-3 paragraphs, contract data to references. *Updating / slimming:* find scaffolding per `references/review-checklist.md`, cut it; preserve every steer with the cut justified. *Reviewing:* for each line ask *"does this change behavior the model wouldn't produce without it?"* — flag the no's. *Diagnosing failure:* `references/metaprompting.md`. Discover context before drafting through targeted recommended-answer questions. Agents run isolated — declare every required tool in `tools:` frontmatter. For skills conventions, the canonical-template fallback, and the technique library, see `references/`.
