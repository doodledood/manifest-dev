---
name: adr
description: 'Synthesize Architecture Decision Records from session transcripts. Extracts decisions via multi-agent pipeline and writes MADR files to a specified directory. Use after completing a /define or /do session to capture architectural decisions as durable records.'
user-invocable: true
---

# /adr - Architecture Decision Record Synthesis

## Goal

Extract ADR-worthy decisions from a completed manifest workflow session and write individual MADR files. Operates as post-processing — runs AFTER the manifest workflow completes, not during it.

## Input

`$ARGUMENTS` = `<manifest-path> <output-dir> --session <transcript-path>`

All three are required:
- **manifest-path**: Path to the manifest file (primary structured input)
- **output-dir**: Directory where ADR files will be written (created if needed)
- **--session \<path\>**: Path to the session transcript JSONL file (primary raw input — `/define` outputs this path at completion)

If any required argument is missing: error and halt with usage:
```
Usage: /adr <manifest-path> <output-dir> --session <transcript-path>

Example: /adr /tmp/manifest-1234.md docs/adr/ --session ~/.claude/projects/.../session.jsonl
```

Optional:
- Execution log path(s) from `/do` runs — supplementary input for implementation decisions. Pass as additional positional arguments after output-dir.

## Pipeline

### Phase 1: Parallel Extraction

Spawn three extraction agents in parallel, each analyzing the session transcript through a different decision lens:

1. **Architecture Lens** — Identify technology choices, component structure decisions, integration approaches, and pattern selections. Look for: "we should use X", "the architecture is Y", structural decisions with alternatives discussed.

2. **Trade-off Lens** — Identify tensions where competing concerns were weighed. Look for: "A vs B", preference statements with reasoning, rejected approaches with "because", T-* items from the manifest's Approach section that trace back to transcript deliberation.

3. **Scope & Constraints Lens** — Identify deliberate inclusions/exclusions that shape system boundaries, key constraint decisions where alternatives existed. Look for: "out of scope", "we need to include", "the constraint is", INV-G* items from the manifest that arose from deliberation (not just mechanical quality gates).

Each extraction agent receives:
- The full session transcript (primary source)
- The manifest file (structured reference)
- Any execution logs (supplementary)

Each agent outputs a list of candidate decisions with:
- **Title**: Short decision name
- **Context**: Why the decision was needed (from transcript)
- **Decision**: What was chosen
- **Alternatives**: What else was considered and why not
- **Consequences**: Positive and negative impacts
- **Evidence**: Quotes or references from the transcript

### Phase 2: Synthesis & Gatekeeper

A synthesis agent receives all candidates from Phase 1 and:

1. **Deduplicates** — Merge candidates that describe the same decision from different lenses. Prefer the version with richer context and alternatives.

2. **Applies ADR-worthiness criteria** — Read `references/ADR_FORMAT.md` in this skill's directory. Apply the decision test to each candidate: *"Would a new team member joining in 6 months benefit from knowing WHY this was decided this way?"* Remove candidates that fail.

3. **Writes ADR files** — For each surviving candidate, generate a MADR file at `<output-dir>/YYYYMMDD-kebab-title.md` using the template from `references/ADR_FORMAT.md`. Create the output directory if it doesn't exist. Use today's date for the YYYYMMDD prefix.

## Graceful Degradation

If the session transcript at `--session <path>` is unreadable or missing:
- **Warn the user**: "Session transcript not found at <path>. Proceeding with manifest and logs only — ADRs will be less detailed (no deliberation context)."
- **Proceed with manifest + logs**: Skip Phase 1 parallel extraction. Instead, extract decisions directly from the manifest's Approach section (Architecture, Trade-offs, Risk Areas) and any execution logs. Apply the same worthiness criteria.
- **Note in each ADR**: Add to the Source section: "Note: Synthesized from manifest only. Session transcript was unavailable — deliberation context may be incomplete."

If no ADR-worthy decisions are found after synthesis:
- Output: "No ADR-worthy decisions identified. The session may not have involved architectural decisions, or all decisions were mechanical/obvious."

## Error Handling

- **Missing manifest**: Error and halt — the manifest is required.
- **Empty/very short transcript** (< 10 messages): Warn "Session transcript is very short — ADR extraction may produce limited results." Proceed normally.
- **Output directory not writable**: Error and halt with clear message.

## Output

On completion, output:
```
ADRs written to: <output-dir>/

| # | Title | File |
|---|-------|------|
| 1 | [title] | YYYYMMDD-kebab-title.md |
| 2 | [title] | YYYYMMDD-kebab-title.md |

Total: N ADR(s) from M candidate decisions.
```

## Known Limitations

- **Multi-define sessions**: If the session transcript contains multiple `/define` runs, `/adr` processes the full transcript. ADRs may reflect decisions from any run in the session. Review output for relevance to your specific task.
- **Session transcript format**: Assumes the Claude Code session transcript JSONL format (`~/.claude/projects/<dir>/<id>.jsonl`) is stable. If the format changes, extraction agents may need updating.
- **Discovery/execution logs are supplementary**: Logs are attention aids for the model, not structured data stores. The skill does not assume or require any particular log structure — it reads them as free-form text for additional context.
