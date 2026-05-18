# Definition: Verifier FAIL Hints Are Directives — Implementation

## 1. Intent & Context

- **Goal:** Implement ADR `docs/adr/20260518-verifier-fail-hints-are-directives.md` — convert `github-pr-lifecycle` FAIL output from prose suggestions to per-gate directive lines, add a literal-execution discipline rule to `/do`, move wait-cadence policy into the agent (variable per-gate with cycle cap), and extend steering to parse wait-cadence overrides. Land on existing branch `feature/verifier-fail-hints-directives` alongside the ADR as a local commit; the user pushes and opens the PR manually when ready. PR-lifecycle dog-fooding deferred to that push.
- **Mental Model:** The current contract has the inspector emit prose hints and `/do` consume them with judgment. Three observed wrong inventions (Stop / `/loop` misuse / busy-wait) demonstrate that judgment fails reliably on suggestion-shaped hints. The fix removes the judgment: hints become directives the caller executes literally. The agent gains responsibility for wait-cadence policy because it has the GitHub-state visibility to pick gate-appropriate intervals; `/do` gains a discipline rule that names the three failure modes and forbids them. Cycle counting reuses the existing `prior-retrigger-context` mechanism — semantically extended, not replaced. Steering customization stays in the existing judgment-parsed surface.

## 2. Approach

- **Architecture:** Two files in scope: `claude-plugins/manifest-dev/agents/github-pr-lifecycle.md` (new FAIL format, wait-cadence policy section, cycle counter semantics, steering example) and `claude-plugins/manifest-dev/skills/do/SKILL.md` (one-paragraph discipline rule about literal directive execution). Plus plugin metadata: version bump 1.1.0 → 1.2.0; README updates if a behavior summary references the FAIL format; `dist/` regeneration via `/sync-tools` so Gemini/OpenCode/Codex distributions stay in sync.
- **Execution Order:**
  - D1 (agent + skill edits) → D2 (plugin housekeeping: version, README, dist sync) → D4 (drop phantom "budget" framing from /do SKILL.md — follow-up cleanup that surfaced during INV-G2 review).
  - Rationale: substantive edits must land before housekeeping so version-bump + README reflect the actual change; sync-tools reads source files so it runs after edits; D4 came last because it was prompted by review feedback on D1's discipline rule paragraph (same paragraph in /do SKILL.md). Push + PR are out of band; the user lands commits manually.
- **Risk Areas:**
  - [R-1] Backward compatibility of the agent's FAIL format with `/do`'s existing parsing path. | Detect: read the existing `/do` SKILL.md description of how FAIL bodies are consumed; verify the new format is a superset of the old (per-gate `Breakdown:` survives; directives replace prose hints inside that structure). If `/do` parses by section header, the new format works for both old and new behavior.
  - [R-3] Cycle-counter semantic extension to `prior-retrigger-context`. | Detect: read the existing input description and verify the extension fits without breaking the CI-retrigger counting semantics (per-gate counting was already implicit; the change names it explicitly).
- **Trade-offs:**
  - [T-1] Inspector encapsulation vs caller-mechanic coupling — naming `bash sleep` in the agent couples the inspector to one specific caller's mechanism. Prefer the coupling because the alternative (prose hints + caller judgment) has been observed to fail in three different ways; coupling cost is real but bounded to one caller today.
  - [T-2] Single-source-of-truth vs multi-CLI sync work — every plugin edit requires regenerating `dist/` via `/sync-tools`. Prefer the friction because the alternative (skipping sync) would silently drift Gemini/OpenCode/Codex distributions away from the canonical Claude Code plugin.

## 3. Global Invariants

- [INV-G1] (PROMPTING quality gate) Intent analysis: the implemented change matches the ADR's stated intent across both modified files.
  ```yaml
  verify:
    agent: change-intent-reviewer
    prompt: |
      Review the diff on branch feature/verifier-fail-hints-directives against the ADR at docs/adr/20260518-verifier-fail-hints-are-directives.md.
      The ADR's Decision section specifies six changes: (1) per-gate directive lines in github-pr-lifecycle FAIL output, (2) /do discipline rule about literal execution, (3) wait-cadence policy in agent with variable per-gate duration, (4) cycle counter via prior-retrigger-context input, (5) steering "Wait cadence:" overlay, (6) multi-gate failure handling (just list multiple directives).
      Verify each of the six landed in the diff. Threshold: no LOW+ severity divergences from intent. Return PASS or FAIL with a directive per the new format (`- <gate>: FAIL — <directive>`).
  ```
- [INV-G2] (PROMPTING quality gate) Prompt quality on modified agent and skill files: no MEDIUM+ issues.
  ```yaml
  verify:
    agent: prompt-reviewer
    prompt: |
      Review the modified files on branch feature/verifier-fail-hints-directives:
      - claude-plugins/manifest-dev/agents/github-pr-lifecycle.md
      - claude-plugins/manifest-dev/skills/do/SKILL.md
      Apply prompt-engineering principles. Threshold: no MEDIUM+ issues across either file. Focus on: clarity of the directive vocabulary, no conflicting rules (the new discipline rule must not contradict existing /do guidance), structure (critical rules surfaced), information density (no padded prose in the discipline rule), invocation fit (the agent's new format must match what /do consumes).
  ```

## 4. Process Guidance

- [PG-1] (PROMPTING default) High-signal changes only — every edit must address the ADR. Don't restructure adjacent text in the agent or skill files; don't tighten unrelated prose; don't refactor sections that weren't explicitly named in the ADR. The ADR is the scope contract.
- [PG-2] (PROMPTING default) Calibrate emotional tone — the new discipline rule in `/do` and the wait-cadence section in the agent both stay in trusted-advisor register. No urgency language. No "MUST NEVER" caps-bombs. The forbidden-substitution list (Stop / `/loop` / `ScheduleWakeup` / busy-wait) is descriptive ("do not substitute"), not threatening.
- [PG-3] Edit claude-plugins/, not symlink resolutions — per CLAUDE.md, `.claude/` and `.agents/skills/` are symlinks. Always edit the `claude-plugins/manifest-dev/` source; the symlinks resolve automatically.
- [PG-4] After source edits, run `/sync-tools` before final verification — `dist/{gemini,opencode,codex}/` and `.gemini/`, `.opencode/` distributions must reflect the new agent and skill behavior. Stale dist content is a real (silent) regression for non-Claude-Code consumers.

## 5. Known Assumptions

- [ASM-1] Plugin version bump scope: minor (1.1.0 → 1.2.0). | Default: minor, per CLAUDE.md's rule "new features, new skills/agents" — this adds new behavior (directive vocabulary, cycle counter semantics, wait-cadence policy) without breaking existing API. | Impact if wrong: if interpreted as patch (1.1.1), downstream consumers may miss a meaningful behavior change; if interpreted as major (2.0.0), version-pinning consumers see a breaking-change signal that doesn't match reality.
- [ASM-2] README updates: minimal — only update if a section explicitly describes github-pr-lifecycle's FAIL format or /do's hint-consumption discipline. | Default: scan repo-root README, claude-plugins/README.md, and claude-plugins/manifest-dev/README.md for these references; edit only if present. | Impact if wrong: stale README content describing the old prose-hint format silently misleads future readers; over-edit risks scope creep beyond the ADR.
- [ASM-3] No tests required for these markdown-only changes. | Default: per CLAUDE.md, hook tests (`tests/hooks/`) cover Python hook behavior; no test suite exists for agent or skill markdown content. Manual review via change-intent-reviewer and prompt-reviewer is the verification path. | Impact if wrong: if a tests/ regression catches structural breakage (e.g., markdown frontmatter parsing), it would surface in CI on the PR; that's the safety net.
- [ASM-4] (auto) sync-tools regenerates only manifest-dev plugin content (per its scope), so dist updates are bounded. | Default: trust sync-tools' scope rules; review its output for unexpected file deletions. | Impact if wrong: dist drift on other plugins would be a sync-tools bug, not this work's responsibility.

## 6. Deliverables

### Deliverable 1: github-pr-lifecycle agent + /do skill updated per ADR

Edit `claude-plugins/manifest-dev/agents/github-pr-lifecycle.md` and `claude-plugins/manifest-dev/skills/do/SKILL.md` to implement the ADR's six specified changes. Both files are the canonical source; the `.claude/` and `.agents/skills/` symlinks resolve automatically.

**Acceptance Criteria:**

- [AC-1.1] github-pr-lifecycle FAIL output specifies per-gate directive lines.
  ```yaml
  verify:
    agent: general-purpose
    prompt: |
      Read claude-plugins/manifest-dev/agents/github-pr-lifecycle.md.
      Verify the FAIL output section specifies per-gate directive lines of the form `- <gate>: FAIL — <directive>` where <directive> is a literal command (e.g., `bash sleep 600; reinvoke`, `retrigger <check-name>`, `escalate`). Prose context belongs in the Reason and Breakdown structure, not inside directive lines.
      Return PASS if the spec change is present and the example FAIL body in the file reflects the new format. Return FAIL with a directive (`- spec update: FAIL — edit the FAIL Output section per ADR section 1`) if not.
  ```

- [AC-1.2] /do SKILL.md has an explicit discipline rule: execute verifier directives literally; do not substitute Stop / /loop / ScheduleWakeup / busy-wait.
  ```yaml
  verify:
    agent: general-purpose
    prompt: |
      Read claude-plugins/manifest-dev/skills/do/SKILL.md.
      Verify the SKILL.md contains a rule instructing the executor to: (a) execute verifier directive lines literally; (b) not substitute Stop, /loop, ScheduleWakeup, or busy-wait — those bypass the polling contract. The four forbidden substitutions must be named explicitly so the model recognizes the temptations.
      Return PASS if the rule is present with the four named substitutions. Return FAIL with a directive if missing or incomplete.
  ```

- [AC-1.3] Wait-cadence policy in agent: variable per-cycle duration by gate (CI ≈ 300s, review ≈ 600s, bot ≈ 120s), agent-owned cycle cap per gate, at cap the directive switches to `escalate`.
  ```yaml
  verify:
    agent: general-purpose
    prompt: |
      Read claude-plugins/manifest-dev/agents/github-pr-lifecycle.md.
      Verify the agent file specifies wait-cadence policy with: (a) variable per-cycle durations by what's being waited on, with example values for CI, review, and bot scanners; (b) per-gate cycle cap (e.g., 6 cycles ≈ 1 hour for reviewers); (c) at-cap behavior: directive switches to `escalate`.
      Return PASS if all three are present. Return FAIL with a directive naming the missing piece.
  ```

- [AC-1.4] Cycle counter threading via existing prior-retrigger-context input, with semantics extended to count wait cycles per gate.
  ```yaml
  verify:
    agent: general-purpose
    prompt: |
      Read claude-plugins/manifest-dev/agents/github-pr-lifecycle.md.
      Verify the agent's input specification for prior-retrigger-context names that the same mechanism counts wait cycles per gate (in addition to CI retriggers). The extension should be a semantic note, not a new input field.
      Return PASS if the extension is documented. Return FAIL with a directive if the prior-retrigger-context section was untouched or doesn't mention wait cycles.
  ```

- [AC-1.5] Steering customization includes a "Wait cadence:" example block (parsed with judgment, no schema change).
  ```yaml
  verify:
    agent: general-purpose
    prompt: |
      Read claude-plugins/manifest-dev/agents/github-pr-lifecycle.md.
      Verify the steering section (or its examples) shows a "Wait cadence:" block format that users can paste into AC verify.prompt to override per-cycle duration and cycle cap per gate. The parse rule must still be "judgment, no schema" — no new YAML schema for steering.
      Return PASS if the example is present and the no-schema constraint preserved. Return FAIL with a directive if missing.
  ```

- [AC-1.6] Multi-gate failure handling: just list multiple directive lines, no priority or sequencing logic in agent or /do.
  ```yaml
  verify:
    agent: general-purpose
    prompt: |
      Read claude-plugins/manifest-dev/agents/github-pr-lifecycle.md and claude-plugins/manifest-dev/skills/do/SKILL.md.
      Verify both files reflect the multi-gate-failure handling: the agent emits multiple directive lines (one per failing gate), and /do executes them without inventing priority or sequencing logic.
      Return PASS if both are aligned. Return FAIL with a directive identifying the misalignment.
  ```

### Deliverable 2: Plugin housekeeping (version, README, dist sync)

Bump plugin version, update READMEs only if they explicitly reference FAIL-format or hint-consumption discipline, and regenerate `dist/` via `/sync-tools`.

**Acceptance Criteria:**

- [AC-2.1] Plugin version bumped to 1.2.0 in `claude-plugins/manifest-dev/.claude-plugin/plugin.json`.
  ```yaml
  verify:
    agent: general-purpose
    prompt: |
      Read claude-plugins/manifest-dev/.claude-plugin/plugin.json and parse the version field.
      Return PASS if version equals "1.2.0". Return FAIL with a directive (`- version: FAIL — bump version field from <observed> to 1.2.0`) if not.
  ```

- [AC-2.2] READMEs scanned for references to old FAIL-prose format or hint-consumption discipline; updated where they exist, otherwise untouched.
  ```yaml
  verify:
    agent: general-purpose
    prompt: |
      Search README.md, claude-plugins/README.md, claude-plugins/manifest-dev/README.md for references to: "natural-language hint", "prose hint", "FAIL with a hint", or descriptions of /do's hint-consumption behavior.
      If any such references exist, verify they describe the new directive format (per-gate `FAIL — <directive>` lines, /do executes literally). If none exist, the READMEs need no edit — return PASS.
      Return FAIL with a directive identifying any stale prose-hint references found and the file they live in.
  ```

- [AC-2.3] dist/ regenerated via `/sync-tools` — Gemini, OpenCode, Codex outputs reflect the new agent + skill content.
  ```yaml
  verify:
    agent: general-purpose
    prompt: |
      Verify dist/gemini/, dist/opencode/, and dist/codex/ contain the updated github-pr-lifecycle agent and /do skill content. Compare key sections:
      - dist/gemini/agents/github-pr-lifecycle.md should contain the new FAIL directive format
      - dist/opencode/agents/github-pr-lifecycle.md should contain the same
      - dist/codex/agents/github-pr-lifecycle.toml should contain the same (TOML-converted)
      - dist/{gemini,opencode,codex}/skills/do/SKILL.md should contain the new discipline rule
      Also verify .gemini/ and .opencode/ root-level distributions if they exist.
      Return PASS if all are in sync. Return FAIL with a directive (`- dist sync: FAIL — run /sync-tools`) if any file lags.
  ```

### Deliverable 4: Drop phantom "budget" framing from /do SKILL.md

The /do SKILL.md previously used a "Budget + routing" header with prose referring to "the budget" and "burn the budget" — but no budget value or counter is defined anywhere in /do. The phrasing was pre-existing prose (predates this ADR) that surfaced for cleanup during INV-G2 review feedback on D1. Replace "Budget + routing" with "Iteration + routing" and reword the paragraph so the actual rule reads cleanly: code-change fix attempts iterate to pass-or-unrecoverable; other retry shapes (waiting, retriggering, replying with or without resolving, mechanical syncs) aren't fix attempts. The semantic distinction the old text was drawing is preserved verbatim in meaning — only the phantom "budget" word and "burn the budget" phrasing are gone. Resync `dist/{gemini,opencode,codex}/skills/do/SKILL.md` after the edit.

**Acceptance Criteria:**

- [AC-4.1] The word "budget" no longer appears in `claude-plugins/manifest-dev/skills/do/SKILL.md`.
  ```yaml
  verify:
    agent: general-purpose
    prompt: |
      Search claude-plugins/manifest-dev/skills/do/SKILL.md for the substring "budget" (case-insensitive).
      Return PASS if zero matches. Return FAIL with a directive (`- /do cleanup: FAIL — remove the remaining occurrence(s) of "budget" from /do SKILL.md`) if any match exists, naming the line numbers.
  ```

- [AC-4.2] The iteration semantics survive verbatim in meaning — code-change fix attempts iterate to pass-or-unrecoverable, and other retry shapes (waiting, retriggering, replying with or without resolving, mechanical syncs) are explicitly named as not-fix-attempts.
  ```yaml
  verify:
    agent: general-purpose
    prompt: |
      Read claude-plugins/manifest-dev/skills/do/SKILL.md.
      Verify the rewritten paragraph (which replaced the old "Budget + routing" section) preserves both clauses:
      (a) Code-change fix attempts iterate until they pass or hit genuinely unrecoverable → `/escalate`.
      (b) Other retry shapes (waiting, retriggering, replying with or without resolving, mechanical syncs) are explicitly distinguished — they aren't fix attempts and don't trigger the iterate-until-stuck handling.
      Return PASS if both clauses are present in the new paragraph. Return FAIL with a directive (`- /do semantics: FAIL — restore missing clause: <which one>`) if either is missing.
  ```

- [AC-4.3] `dist/{gemini,opencode,codex}/skills/do/SKILL.md` byte-match source after the edit (sync-tools coverage for this single-file change).
  ```yaml
  verify:
    agent: general-purpose
    prompt: |
      For each of:
      - dist/gemini/skills/do/SKILL.md
      - dist/opencode/skills/do/SKILL.md
      - dist/codex/skills/do/SKILL.md
      Compare against claude-plugins/manifest-dev/skills/do/SKILL.md.
      Return PASS if all three are byte-identical to source. Return FAIL with a directive (`- dist sync: FAIL — re-sync /do SKILL.md to <which CLI dist>`) naming the lagging file(s).
  ```

## Source

- ADR: `docs/adr/20260518-verifier-fail-hints-are-directives.md`
- Session: `~/.claude/projects/-Users-aviram-kofman-Documents-Projects-manifest-dev/8c3870c7-ab4c-4ca2-8125-59b813b55130.jsonl`
- Branch: `feature/verifier-fail-hints-directives`
