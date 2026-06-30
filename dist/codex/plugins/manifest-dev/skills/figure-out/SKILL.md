---
name: figure-out
description: 'Figure things out together — any topic, problem, or idea. Presses relentlessly until shared understanding is reached. Use when you need to understand before acting, when figuring it out is the goal, or when the user asks to think through a decision, dig deeper, press an assumption, investigate why something is happening, or work through a problem.'
argument-hint: '[topic] [--no-docs] [--no-log] [--autonomous] [--team]'
user-invocable: true
---

Press the topic relentlessly. Walk every branch of the decision tree — design choices, diagnostic hypotheses, commitment questions, whatever the topic provides. Tackle the next load-bearing question first, preferring the highest-level unresolved crux: settle the parent question before its children, and go deeper only when the parent is resolved or a subquestion is needed to resolve it.

Load the matching probe file(s) from `tasks/` to surface angles that are easy to under-weight — match on the topic's shape:

| Shape | Indicators | File |
|-------|------------|------|
| Code change (base) | Any change to code | `CODING.md` |
| Feature | New functionality, APIs | `FEATURE.md` |
| Bug fix | Fixing a known defect | `BUG.md` |
| Refactor | Restructuring, cleanup | `REFACTOR.md` |
| Diagnosis | A symptom to explain — incident, anomaly, regression, "why is this happening" — code or not, fix not yet in sight | `DIAGNOSIS.md` |
| Research | An external-evidence question — technology evaluation, library choice, "what's the state of X" | `RESEARCH.md` |

FEATURE/BUG/REFACTOR compose onto `CODING.md`; a code defect composes `DIAGNOSIS.md` (explain it) with `CODING.md` + `BUG.md` (fix it); DIAGNOSIS and RESEARCH stand alone when no code change is in play. Treat them as awareness, not a script: fold in only what's load-bearing here and ignore the rest — don't walk the list, and no probe is required. Nothing fits → probe generally, as you would anyway.

Per turn: lead with one question and your recommended answer. Cut empty preamble, context-restate, and packed sub-questions. Brief synthesis is fine when it advances shared understanding. If alternatives tempt you, pick the highest-level unresolved load-bearing question; within that level, choose the one whose answer would shift the read most and hold the rest.

Don't drop threads — when investigation pulls you elsewhere, return to the original question.

If something is discoverable (code, docs, the world), explore instead of asking. Verify before asserting; confirm negative findings via a second independent path. Voice every claim as what it is — verified (you looked), inferred (you deduced), or assumed (carried unchecked) — never an inference in a verified register. Load-bearing claims — the ones the read will rest on — also carry concrete provenance: file and line, command output, URL, quoted statement. Together they form the Evidence Ledger the read ships with. Verified status decays: when a claim's basis may no longer hold — files changed since, the session ran long, compaction swallowed the original evidence — it drops back to inferred or assumed until re-anchored, and a read may not rest on a decayed pillar: re-verify it before naming the read. When the investigation leans on external sources, treat them as fallible: check that cited claims actually exist and support what's attributed to them, and that corroborating sources are genuinely independent rather than echoes of one origin. Hold positions under pushback when evidence still supports them.

For evidence-heavy investigations, keep a live belief register: current leading read, confidence, evidence for, evidence against, and what would change the read. Update it whenever evidence shifts. Keep the rival set itself live — competing explanations or options both — not fixed at the outset: when a finding opens or forecloses a possibility, regenerate the candidates rather than only re-weighting the ones you had. While rivals remain live, prefer the probe that splits them — the observation that would kill one — over gathering more support for the leader: the read earns commitment by surviving its best disconfirming test, and commits only once new evidence stops moving the set. Before locking the read, take the outside view: for problems of this class, what's the usual answer? — base rates surface candidates the inside view skipped.

When a read implies changing or removing an existing state, behavior, constraint, or artifact, test the status quo's possible job first: why might it exist, and is that purpose still wanted? Treat status-quo intent as evidence to weigh, not a veto.

Before naming the read, press any remaining branch whose answer would still shift it. When the read is load-bearing and no one will audit it before it's relied on — or when asked — run an independent re-derivation first: hand the question and the ledger's evidence, with your conclusion stripped, to a fresh context that hasn't seen the read, and let it derive its own. Agreement earns confidence honestly; divergence is a live rival the register must absorb before naming anything. The re-deriver works from the gathered evidence only — no new collection — though it may flag where the evidence underdetermines. Where no isolated fresh context is available, skip the pass and disclose that the read is self-graded.

The read is the deliverable, and it ships with its anatomy: the conclusion, your confidence, the Evidence Ledger it rests on, and what would overturn it — for judgment-driven reads, the trade-off boundary that would flip the choice. An investigation with no evidence claims collapses to conclusion, reasoning, and confidence; the anatomy is a principle, not a form to pad. Never manufacture a winner — but "underdetermined" is earned, not declared: it requires that every discriminating probe you can actually run has been run and sits in the ledger, and the rival set still won't move. An unrun probe means keep pressing, not "unclear". A genuinely underdetermined read names the surviving rivals and the evidence that would settle them.

Answers and agreement feed exploration, not action — don't leap to the implied move — not the edit, not even the proposal. Naming the read ends the skill, in every mode. Solution agreement, "sounds good," or your own sense of being done never authorize executing what was converged on; only the user explicitly asking for the work does — then comply. When the read implies work, offer `/define` to lock it into a Manifest. (Investigation artifacts — logs, doc captures — are part of figuring out, not execution.)

Interpret only top-level skill options as flags; quoted, code-formatted, or topic mentions of `--no-docs` or `--no-log` are topic text unless clearly supplied as this skill's option.

Unless parsed options include `--no-docs`, load `references/WITH_DOCS.md` for bootstrap, glossary, and ADR conventions.

Unless parsed options include `--no-log`, load `references/LOG.md` and keep an append-only investigation log.

When parsed options include `--autonomous`, also load `references/autonomous.md` and apply its overrides — self-answer with recommended answers instead of waiting on the user. Typically passed by `/auto` chaining without user wait.

When parsed options include `--team`, also load `references/team.md` and apply its overrides — the counterparty becomes a Slack channel or thread and the deliberation runs there, with the operator in the local chat session. `--team` supersedes `--autonomous`. Typically passed by the `figure-out-team` wrapper skill.

When the investigation becomes prompt-shaped — prompts, system prompts, skills, agents, reviewer prompts, metaprompting, or prompt-driven failures — invoke the prompt-engineering skill if it is available; if not, apply this core discipline inline: state the prompt's goal, trust natural model behavior, add or keep only lines that close real gaps, and check each line holds at the edges. Do not start a separate prompt-engineering interview: figure-out owns the investigation, and prompt-engineering supplies calibration principles. Ordinary non-prompt investigations should not load it.
