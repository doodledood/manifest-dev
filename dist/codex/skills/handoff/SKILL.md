---
name: handoff
description: 'Produce a self-contained context payload that lets a fresh agent continue without re-deriving what this session established. Use for cross-boundary transfer such as switching tools, starting a clean session, or handing off to another agent, and for DIY sub-agent flows where a focused side-session returns context to the parent.'
argument-hint: '<what the next session is for>'
user-invocable: true
---

Produce a self-contained context payload that lets a fresh agent continue this work without re-deriving or re-learning what this session already established. The argument is what the next session is for — use it to shape what's captured and what's left out.

Capture what's hard-won — anything the new session would have to re-do otherwise. For each item that travels, carry the grounding with it, so the receiver inherits the working state rather than just the conclusion. *Examples (illustrative, not required):* a settled decision travels with the alternatives considered and why this won; a verified fact travels with how it was verified (file:line, command output, doc URL); an open thread travels with what would close it. If a particular handoff isn't structured around decisions, facts, or threads, capture whatever the goal requires — with its grounding.

Reference other artifacts (PRDs, manifests in `.manifest/`, ADRs, issues, PRs, commits, diffs) by path or URL — don't restate their content.

Shape is the agent's call. Section names, headings, prose-vs-lists, ordering — driven by the intent, not a template.

Output to a writable scratch path: `/tmp/handoff-{timestamp}.md` when `/tmp` is writable; otherwise the host temp directory (`$TMPDIR` / `%TEMP%`). `{timestamp}` is `YYYYMMDD-HHMMSS` in UTC. If the argument is a path to a prior handoff, read it first and write a fresh doc reflecting the current state — pure rewrite, not append.
