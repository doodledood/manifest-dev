# Definition: Make understand-done model-invocable + /auto context inference

## 1. Intent & Context
- **Goal:** Enable the model to end /understand sessions when conversation naturally concludes, and let /auto infer tasks from conversation context instead of hard-erroring on missing arguments.
- **Mental Model:** understand-done is a signal that the understanding session is over. Currently only users can send it. /auto currently requires explicit args but should behave like /define (infer from context).
- **Mode:** thorough
- **Interview:** autonomous
- **Medium:** local

## 3. Global Invariants (The Constitution)

- [INV-G1] No behavioral divergence from stated intent across all changed files | Verify: change-intent-reviewer
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Review the diff for behavioral divergence from stated intent: making understand-done model-invocable, updating understand skill's Ending section, and updating /auto to infer task from context. Changed files: claude-plugins/manifest-dev/skills/understand-done/SKILL.md, claude-plugins/manifest-dev/skills/understand/SKILL.md, claude-plugins/manifest-dev/skills/auto/SKILL.md, claude-plugins/manifest-dev/.claude-plugin/plugin.json"
  ```

- [INV-G2] No MEDIUM+ prompt quality issues introduced by the changes | Verify: prompt-reviewer
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review these prompt files for quality issues: claude-plugins/manifest-dev/skills/understand-done/SKILL.md, claude-plugins/manifest-dev/skills/understand/SKILL.md, claude-plugins/manifest-dev/skills/auto/SKILL.md"
  ```

- [INV-G3] Hook transcript parsing detects model-invoked understand-done identically to user-invoked | Verify: codebase check
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read claude-plugins/manifest-dev/hooks/hook_utils.py and verify that parse_understand_flow() detects understand-done completion via tool use records (was_skill_invoked), not via user message parsing. This means model-invoked and user-invoked understand-done are detected identically. PASS if the function uses tool use records. FAIL if it parses user message text to detect understand-done."
  ```

## 4. Process Guidance (Non-Verifiable)

- [PG-1] High-signal changes only — each change addresses a real friction point, no change for the sake of change (auto)
- [PG-2] Right-sized changes — don't overcorrect. The understand-done change is permissive (allow model invocation), not prescriptive (force model to invoke).

## 5. Known Assumptions

- [ASM-1] Local .claude/skills/ copies are plain files (not symlinks) that need manual sync | Default: update both plugin source and local copies | Impact if wrong: local copies would auto-update via symlink, making D1/D2/D3 local copy ACs unnecessary

## 6. Deliverables (The Work)

### Deliverable 1: Make understand-done model-invocable
*Plugin source: claude-plugins/manifest-dev/skills/understand-done/SKILL.md*

**Acceptance Criteria:**
- [AC-1.1] `disable-model-invocation: true` is removed from understand-done/SKILL.md frontmatter | Verify: file check
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read claude-plugins/manifest-dev/skills/understand-done/SKILL.md. PASS if 'disable-model-invocation' does not appear anywhere in the file. FAIL if it's still present."
  ```

- [AC-1.2] Local copy at .claude/skills/understand-done/SKILL.md matches plugin source | Verify: diff
  ```yaml
  verify:
    method: bash
    command: "diff /home/user/manifest-dev/claude-plugins/manifest-dev/skills/understand-done/SKILL.md /home/user/manifest-dev/.claude/skills/understand-done/SKILL.md"
  ```

### Deliverable 2: Update understand skill's Ending section
*Plugin source: claude-plugins/manifest-dev/skills/understand/SKILL.md*

**Acceptance Criteria:**
- [AC-2.1] Ending section allows model to invoke /understand-done when conversation has naturally concluded | Verify: content check
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read claude-plugins/manifest-dev/skills/understand/SKILL.md. Find the '## Ending' section. PASS if it allows or instructs the model to invoke /understand-done (or the understand-done skill) when the conversation naturally concludes. FAIL if it still says 'Never invoke it yourself' or equivalent prohibition."
  ```

- [AC-2.2] Ending section preserves user primacy — user can always end the session, model invocation is for natural conclusions not premature termination | Verify: content check
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read claude-plugins/manifest-dev/skills/understand/SKILL.md. Find the '## Ending' section. PASS if the section still preserves user primacy (user decides when understanding is sufficient, model flags gaps before ending). FAIL if the model is given unconstrained authority to end sessions."
  ```

- [AC-2.3] Local copy at .claude/skills/understand/SKILL.md matches plugin source | Verify: diff
  ```yaml
  verify:
    method: bash
    command: "diff /home/user/manifest-dev/claude-plugins/manifest-dev/skills/understand/SKILL.md /home/user/manifest-dev/.claude/skills/understand/SKILL.md"
  ```

### Deliverable 3: Update /auto to infer task from context
*Plugin source: claude-plugins/manifest-dev/skills/auto/SKILL.md*

**Acceptance Criteria:**
- [AC-3.1] /auto no longer hard-errors when no arguments are provided | Verify: content check
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read claude-plugins/manifest-dev/skills/auto/SKILL.md. PASS if the 'no arguments' case does NOT halt with an error. It should infer the task from conversation context instead. FAIL if it still contains 'error and halt' or equivalent for the no-arguments case."
  ```

- [AC-3.2] /auto with no args passes conversation context to /define (via $TASK_DESCRIPTION or equivalent) | Verify: content check
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read claude-plugins/manifest-dev/skills/auto/SKILL.md. PASS if the no-arguments flow instructs the model to infer the task from conversation context and pass it to /define. FAIL if there's no mechanism for context-based task inference."
  ```

- [AC-3.3] When both arguments and conversation context are absent, /auto still errors with a clear message | Verify: content check
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read claude-plugins/manifest-dev/skills/auto/SKILL.md. PASS if there is explicit handling for the case where no arguments are provided AND no conversation context exists (e.g., fresh session with just '/auto') — it should error with a usage message. FAIL if the no-context edge case is not handled."
  ```

- [AC-3.4] /auto's description field mentions context inference capability | Verify: content check
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read claude-plugins/manifest-dev/skills/auto/SKILL.md. Check the 'description' field in the YAML frontmatter. PASS if it mentions inferring task from conversation context or working without explicit arguments. FAIL if the description only mentions requiring a task description."
  ```

- [AC-3.5] Local copy at .claude/skills/auto/SKILL.md matches plugin source | Verify: diff
  ```yaml
  verify:
    method: bash
    command: "diff /home/user/manifest-dev/claude-plugins/manifest-dev/skills/auto/SKILL.md /home/user/manifest-dev/.claude/skills/auto/SKILL.md"
  ```

### Deliverable 4: Version bump
*Plugin source: claude-plugins/manifest-dev/.claude-plugin/plugin.json*

**Acceptance Criteria:**
- [AC-4.1] Plugin version bumped (minor) from 0.80.0 | Verify: version check
  ```yaml
  verify:
    method: bash
    command: "grep '\"version\"' /home/user/manifest-dev/claude-plugins/manifest-dev/.claude-plugin/plugin.json | grep -v '0.80.0'"
  ```
