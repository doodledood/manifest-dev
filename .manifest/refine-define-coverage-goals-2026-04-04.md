# Definition: Refine /define — Procedural Protocols to Principle-Based Coverage Goals

## 1. Intent & Context
- **Goal:** Rewrite /define's protocol sections from procedural steps (causing rigid sequential execution) to coverage goals (states of sufficient understanding that build on any existing context). Make /define adaptive — it probes gaps, not territory already covered.
- **Mental Model:** Protocols are lenses for finding gaps in understanding, not steps to execute. Domain grounding, pre-mortem, etc. describe what must be true (coverage states), not what to do (procedures). Understanding from any source — conversation, research, prior sessions — counts equally toward coverage.
- **Interview:** thorough
- **Medium:** local

## 2. Approach

- **Architecture:** Reframe each protocol section as a coverage goal: "What must be true" + "What to assess" + "Convergence test". Add context inheritance to the discovery log. Update interview modes and manifest-verifier to reference coverage states instead of protocol execution.

- **Execution Order:**
  - D1 (SKILL.md) → D2 (Interview modes) → D3 (Manifest-verifier) → D4 (Auto + version)
  - Rationale: SKILL.md is the source of truth; interview modes reference it; verifier audits against it; auto is trivial alignment.

- **Risk Areas:**
  - [R-1] Model declares coverage met without actual understanding | Detect: manifest-verifier flags generic scenarios; convergence tests are falsifiable
  - [R-2] Rewrite loses analytical substance (failure dimensions, dispositions) | Detect: prompt-reviewer checks completeness; change-intent-reviewer catches behavioral divergence

- **Trade-offs:**
  - [T-1] Thoroughness vs Adaptiveness → Prefer adaptiveness because the current procedural approach is the documented problem, but guard against under-probing via convergence tests + self-check constraint
  - [T-2] Brevity vs Explicit guidance → Prefer brevity (lean sections) because shorter text reduces context rot risk and the analytical substance (failure dimensions table, dispositions) is preserved inline

## 3. Global Invariants (The Constitution)

- [INV-G1] All changes pass change-intent-reviewer with no LOW or above issues
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Review the diff for behavioral divergence from stated intent: rewriting /define's protocol sections from procedural steps to coverage goals while preserving analytical substance."
  ```

- [INV-G2] All changed prompt files pass prompt-reviewer with no MEDIUM or above issues
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review the following changed files for prompt quality issues: claude-plugins/manifest-dev/skills/define/SKILL.md, claude-plugins/manifest-dev/skills/define/references/interview-modes/thorough.md, claude-plugins/manifest-dev/skills/define/references/interview-modes/minimal.md, claude-plugins/manifest-dev/skills/define/references/interview-modes/autonomous.md, claude-plugins/manifest-dev/agents/manifest-verifier.md"
  ```

- [INV-G3] No procedural protocol framing remains in rewritten sections — no "The exercise:", no "Protocol" in section headers, no sequential execution instructions
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check these files for residual procedural framing: claude-plugins/manifest-dev/skills/define/SKILL.md, claude-plugins/manifest-dev/skills/define/references/interview-modes/thorough.md, claude-plugins/manifest-dev/skills/define/references/interview-modes/minimal.md, claude-plugins/manifest-dev/skills/define/references/interview-modes/autonomous.md. FAIL if any of these patterns appear: (1) 'The exercise:' framing in coverage goal sections, (2) '## ... Protocol' as section headers (should be '## Coverage Goal: ...'), (3) 'Protocols are sequential' or fixed protocol execution order, (4) 'Run all protocols' language. PASS if all procedural framing has been replaced with coverage-goal framing."
  ```

- [INV-G4] Analytical substance preserved — failure dimensions table, scenario disposition rules, backcasting questions, and adversarial patterns all present in rewritten SKILL.md
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/SKILL.md for preserved analytical content. FAIL if any of these are missing: (1) Failure dimensions table with Technical/Integration/Stakeholder/Timing/Edge cases/Dependencies rows, (2) Scenario disposition rules (encoded as criterion, out of scope, mitigated by approach), (3) Backcasting focus areas (infrastructure/tooling, user behavior, stability), (4) Adversarial self-review patterns (scope creep, deferred edge cases, temporary solutions, process shortcuts). PASS if all are present."
  ```

- [INV-G5] Manifest schema, encoding rules (INV/AC/PG/ASM), verification loop, summary for approval, interview mode decision authority, and amendment protocol are unchanged
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/SKILL.md. Verify these sections are UNCHANGED from the original: 'The Manifest Schema' (the markdown template), 'ID Scheme' table, 'Amendment Protocol', 'Verification Loop', 'Summary for Approval', 'What the Manifest Needs', 'Approach Section (Complex Tasks)'. Also verify interview mode files still have distinct Decision Authority sections (thorough=user decides all, minimal=user decides scope/constraints, autonomous=agent decides all). FAIL if any of these sections were modified. PASS if all are preserved."
  ```

## 4. Process Guidance (Non-Verifiable)

- [PG-1] Each coverage goal section follows lean structure: "What must be true" → "What to assess" (bullet list) → "Convergence test". No exploration instructions, no log templates, no "exercise" framing.
- [PG-2] When rewriting, change framing of existing content — don't add new analytical content or remove existing analytical substance. The volume of text should decrease, not increase.
- [PG-3] Use the plan at `/root/.claude/plans/twinkly-munching-blanket.md` as the primary reference for specific before/after examples and section-level guidance.

## 5. Known Assumptions

- [ASM-1] Lean coverage goal sections (~15-20 lines each) provide sufficient guidance for the model | Default: lean is enough, convergence tests catch gaps | Impact if wrong: model may under-probe; fixable by expanding sections in a follow-up
- [ASM-2] The manifest-verifier's existing coverage audit logic is sufficient to catch under-probing | Default: verifier catches it | Impact if wrong: manifests lose quality; fixable by strengthening verifier criteria
- [ASM-3] No other files beyond the 6 identified reference protocol names or depend on protocol execution order | Default: exploration confirmed this | Impact if wrong: broken references; easily caught by grep

## 6. Deliverables (The Work)

### Deliverable 1: Rewrite SKILL.md Protocol Sections and Supporting Infrastructure
*Core skill file — all protocol-related sections transformed*

**Acceptance Criteria:**

- [AC-1.1] Five protocol sections rewritten as coverage goals with new headers: "Coverage Goal: Domain Understanding", "Coverage Goal: Reference Class Awareness", "Coverage Goal: Failure Mode Coverage", "Coverage Goal: Positive Dependency Coverage", "Coverage Goal: Process Self-Audit"
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/SKILL.md for five sections with headers matching '## Coverage Goal: Domain Understanding', '## Coverage Goal: Reference Class Awareness', '## Coverage Goal: Failure Mode Coverage', '## Coverage Goal: Positive Dependency Coverage', '## Coverage Goal: Process Self-Audit'. Each must contain: (1) a 'What must be true' statement, (2) a 'What to assess' or analytical content section, (3) a 'Convergence test' statement. FAIL if any section is missing or lacks these elements. PASS if all five are present with required elements."
  ```

- [AC-1.2] Each coverage goal section includes "any source counts" language — understanding from conversation, research, prior sessions, arguments all qualify
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check the five 'Coverage Goal' sections in claude-plugins/manifest-dev/skills/define/SKILL.md. Each must acknowledge that understanding from any source (conversation context, prior research, arguments, task files, etc.) counts toward meeting the coverage goal. FAIL if any section implies the only way to achieve coverage is through fresh exploration/execution. PASS if all five acknowledge multiple sources of understanding."
  ```

- [AC-1.3] Interview Flow section references coverage goals as states, not protocols as steps
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check the '## Interview Flow' section in claude-plugins/manifest-dev/skills/define/SKILL.md. It must: (1) name the five coverage goals, (2) describe them as states of sufficient understanding, not steps to execute, (3) state that existing context counts toward coverage, (4) state the interview probes gaps. FAIL if it still lists 'protocols' as sequential steps. PASS if it describes coverage goals as states."
  ```

- [AC-1.4] Complexity Triage table reframed from "which protocols to run" to "what coverage depth is needed"
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check the Complexity Triage table in claude-plugins/manifest-dev/skills/define/SKILL.md. The table column should reference coverage depth, not protocol names. Simple row should NOT say 'Domain Grounding + quick Pre-Mortem' but should describe the coverage depth needed. FAIL if table still maps complexity to protocol names. PASS if it maps to coverage depth."
  ```

- [AC-1.5] Discovery log section includes context inheritance mechanism — "Seed from existing context" with Context Assessment template
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/SKILL.md for a context inheritance mechanism in the discovery log section. Must include: (1) instruction to assess existing understanding before probing, (2) mechanism to log items resolved from context as '- [x] RESOLVED (from context)', (3) statement that the interview begins at the gaps. FAIL if discovery log always starts blank. PASS if context seeding is described."
  ```

- [AC-1.6] Convergence checklist references coverage goal names and states, with "items resolved from any source count equally"
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check the convergence requirements in claude-plugins/manifest-dev/skills/define/SKILL.md (in the 'Stop when converged' constraint). Must: (1) reference coverage goal names or state descriptions, not protocol names, (2) include 'items resolved from any source count equally' or equivalent, (3) test understanding completeness not activity completeness. FAIL if convergence still references 'domain grounded' and 'pre-mortem scenarios logged' as protocol execution checks. PASS if it references coverage states."
  ```

- [AC-1.7] Explicit self-check constraint present: "Before marking a coverage goal as met from context, verify you can produce concrete evidence — name specific patterns, scenarios, or findings. Vague confidence doesn't count."
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/SKILL.md for an explicit self-check constraint about coverage goals. Must contain instruction that before marking a coverage goal as met from context, the model must verify it can produce concrete evidence (specific patterns, scenarios, findings). Vague or general confidence should not count. FAIL if no such self-check exists. PASS if present."
  ```

- [AC-1.8] "Resolve all Resolvable" constraint retains "all" but adds context-inheritance caveat — items already resolved in context are logged as resolved, not re-probed
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check the 'Resolve all Resolvable task file structures' constraint in claude-plugins/manifest-dev/skills/define/SKILL.md. Must: (1) still require engagement with all resolvable items (no silent drops), (2) add caveat that items already resolved in conversation context are logged as resolved, not re-probed. FAIL if 'all' obligation removed OR if no context-inheritance caveat added. PASS if both present."
  ```

- [AC-1.9] Checkpoint trigger updated — "after resolving a cluster of related questions" without "before transitioning to a new topic area"
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check the 'Confirm understanding periodically' constraint in claude-plugins/manifest-dev/skills/define/SKILL.md. Must trigger checkpoints 'after resolving a cluster of related questions' but should NOT reference 'before transitioning to a new topic area' or protocol transitions. FAIL if protocol-transition trigger remains. PASS if only cluster-based trigger."
  ```

- [AC-1.10] Principle #4 "Complete" updated with coverage-goal language and "context from any source counts"
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check Principle #4 'Complete' in claude-plugins/manifest-dev/skills/define/SKILL.md. Must state that these are coverage goals not sequential steps, and that context from any source counts toward them. FAIL if still reads as listing protocols to execute. PASS if framed as coverage goals."
  ```

### Deliverable 2: Update Interview Mode Files
*Align flow descriptions with coverage-goal framing*

**Acceptance Criteria:**

- [AC-2.1] thorough.md Interview Flow section replaces "Protocols are sequential" with adaptive, gap-driven flow
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/references/interview-modes/thorough.md Interview Flow section. Must NOT contain 'Protocols are sequential' or 'Domain Grounding → Outside View → Pre-Mortem → Backcasting → Adversarial Self-Review' as an execution order. Must describe adaptive flow that builds on existing context and probes gaps. FAIL if sequential protocol order remains. PASS if adaptive."
  ```

- [AC-2.2] minimal.md Interview Flow updated — no reference to "same order as thorough mode"
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/references/interview-modes/minimal.md. Must NOT reference 'same order as thorough mode' or 'Protocols run in the same order'. Must reference coverage goals, not protocol execution. FAIL if protocol order reference remains. PASS if aligned with coverage-goal framing."
  ```

- [AC-2.3] autonomous.md Interview Flow updated — no "Run all protocols internally"
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/references/interview-modes/autonomous.md. Must NOT contain 'Run all protocols internally'. Must reference coverage goals, not protocol execution. FAIL if protocol language remains. PASS if aligned."
  ```

- [AC-2.4] All three interview modes preserve their distinct decision authority (thorough=user decides all, minimal=user decides scope/constraints, autonomous=agent decides all)
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check all three interview mode files in claude-plugins/manifest-dev/skills/define/references/interview-modes/. Verify Decision Authority sections are unchanged: thorough.md must say user decides everything, minimal.md must say user decides scope/constraints/high-impact, autonomous.md must say agent decides everything. FAIL if any Decision Authority section was modified. PASS if all preserved."
  ```

### Deliverable 3: Update Manifest-Verifier
*Audit coverage states, not protocol execution*

**Acceptance Criteria:**

- [AC-3.1] Backcasting section renamed and checks territory coverage, not protocol execution — "positive dependencies not examined (from any source)" instead of "no backcasting exercise in log"
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/agents/manifest-verifier.md backcasting/positive-dependency section. Must NOT contain 'no backcasting exercise' or check for protocol-named log sections. Must check whether positive dependencies were examined from any source. FAIL if still checks for protocol execution. PASS if checks coverage state."
  ```

- [AC-3.2] Adversarial self-review section renamed and checks process risk coverage, not protocol execution — "process risks not examined" instead of "no adversarial self-review in log"
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/agents/manifest-verifier.md adversarial/process-audit section. Must NOT contain 'no adversarial self-review in log' or check for protocol-named log sections. Must check whether process risks were examined. FAIL if still checks for protocol execution. PASS if checks coverage state."
  ```

- [AC-3.3] Pre-mortem section header updated for consistency (if needed)
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/agents/manifest-verifier.md for consistency in section naming. Sections that previously referenced protocol names should now reference coverage concepts. The pre-mortem section can keep 'scenario resolution' or shift to 'failure mode coverage'. PASS if naming is internally consistent across all audit sections."
  ```

### Deliverable 4: Trivial Alignment + Version Bump

**Acceptance Criteria:**

- [AC-4.1] auto/SKILL.md line 11: "all protocols" changed to "all coverage goals"
  ```yaml
  verify:
    method: bash
    command: "grep -c 'all coverage goals' claude-plugins/manifest-dev/skills/auto/SKILL.md && ! grep -q 'all protocols' claude-plugins/manifest-dev/skills/auto/SKILL.md && echo PASS || echo FAIL"
  ```

- [AC-4.2] Plugin version bumped (minor) in plugin.json
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/.claude-plugin/plugin.json. The version should have its minor component incremented compared to the current version. Use git diff to verify the version was bumped. FAIL if version unchanged. PASS if minor version incremented."
  ```
