# Definition: Collapse /drive into /do via verifier-hint protocol

## 1. Intent & Context

- **Goal:** Remove `/drive` and `/drive-tick` as separate skills; absorb their responsibilities into `/do` via a free-form rich-hint protocol returned by verifiers. The manifest becomes the contract for "done" including PR-lifecycle gates (CI green, threads addressed, PR mergeable, etc.). Terminal is *mergeable*, not *merged* — /do drives the PR to a clean, ready-to-merge state and stops; the actual merge button is left to a human or GitHub auto-merge. A new `github-pr-lifecycle` agent owns the canonical lifecycle checks (mergeable composite, thread classification, retrigger-cap, hint emission); a paired `tasks/PR_LIFECYCLE.md` task file is the /define-time guide that templates an AC invoking the agent. A new `/define --babysit <pr-url>` mode synthesizes a lifecycle-only manifest from an existing PR. `/auto` keeps `--platform` pass-through and gains `--babysit` for one-command PR tending on repos that don't use manifest-dev. No /drive feature is silently lost — every responsibility maps to a new home (agent prompt, AC template, /do dispatch, or explicit drop with rationale).
- **Mental Model:**
  - *Verifier FAIL bodies are just FAIL messages* — criteria-checker returns PASS or FAIL with actionable detail; /do reads with LLM judgment and acts. No "hint protocol" layer — a FAIL message has always been free-form text and /do has always been an LLM. The agent never references /define or any workflow concept; /do owns workflow routing (e.g., recognizing an out-of-scope finding and routing it through Self-Amendment).
  - *Action-aware fix-cap* — execution-modes per-phase fix-cap only increments on **code-change fix attempts**. Other retry shapes (waits for CI, retriggers of transient failures, replies on threads, pushes of sync updates, scope-amendment cycles) don't burn the fix budget — they're not fix attempts. Per-AC `verify.timeout:` provides the wall-clock cap for criteria that legitimately wait (e.g., 30m CI-poll, 1d approval-wait).
  - *Lifecycle as a single agent-invoking AC* — `PR_LIFECYCLE.md` composes onto `CODING.md` when `--platform github` (auto-detected from git remote). It templates ONE AC: `method: subagent, agent: github-pr-lifecycle, prompt: <PR URL + branch + optional steering>`. The agent owns the canonical gate set (PR exists, CI green, threads addressed, PR description in sync, PR mergeable composite) as internal implementation detail — not five separate templated verifier prompts. Centralizing into the agent means one read of GitHub state, holistic cross-signal reasoning (e.g., "CI green but branch behind → push-update before claiming clean"), and a single reviewable prompt file. **The agent is steerable through the AC's verify.prompt** — users layer per-PR nuances (custom labels, named approvers, known-flaky CI jobs) without forking the agent. Multi-repo: PR_LIFECYCLE.md auto-templates the AC per-repo when manifest declares `Repos:`. Mergeable composite is read via `gh pr view --json mergeable,mergeStateStatus,reviewDecision` — GitHub's own composite, single source of truth. Platform-specific agent by design: GitLab/Bitbucket would each get their own (`gitlab-pr-lifecycle`, etc.); /define picks by `--platform`.
  - *Babysit mode* — `/define --babysit <pr-url>` reads PR title/body/state, templates lifecycle-only ACs from `PR_LIFECYCLE.md`, writes manifest. Default interview style: autonomous (templated ACs need minimal probing). Precedent: existing Branch-Diff Seeding does the same shape with branch diffs.
  - *Manifest IS the scheduler* — /drive's tick loop existed to solve "when do I check again?". The new answer: when the manifest's longest-timeout AC says to. Terminal is encoded as an AC ("PR mergeable" — GitHub's own composite state covering CI green + required approvals + no conflicts + threads resolved + branch up-to-date), not an external check. /do drives the PR *to a mergeable state* and stops; it does not press the merge button (that stays human, or GitHub auto-merge). Late-arriving activity (comments, CI re-runs, force-push) is handled by the next verify cycle inside /do's running session. Per-AC `verify.timeout:` + verifier-hint sleep dispatch IS the polling primitive. Trade-off: session-held — terminal close stops progress (see Risk R-3, accepted).
  - *Self-bootstrapping caveat* — this manifest implements PR_LIFECYCLE; it cannot compose what it builds. PR lifecycle for this PR is managed manually by the user (see ASM-1).
- **Mode:** thorough
- **Interview:** thorough
- **Medium:** local

## 2. Approach

*Initial direction. Plans break on reality — adjust freely when reality diverges; log adjustments.*

- **Architecture:**
  Build the new abstractions before removing the old, in this dependency order:
  1. *New artifacts first.* `agents/github-pr-lifecycle.md` (the agent) + `tasks/PR_LIFECYCLE.md` (the /define-time AC template + composition rule) + `references/BABYSIT_MODE.md` (the synthesis spec) — pure additions, no consumer change yet.
  2. *Entry points.* `/define --babysit <pr-url>` flag, platform auto-detection from git remote, manifest schema gains `verify.timeout:` field.
  3. *Runtime mechanics.* `/verify` documents the rich-hint return shape; `criteria-checker` agent's output format admits a free-form hint body; `/do` adds hint dispatch (sleep / fix / retrigger / reply / push / amend) with action-aware budget; execution-mode files clarify which actions increment fix-cap. The github-pr-lifecycle agent is the canonical hint producer for lifecycle ACs; non-lifecycle ACs continue to emit hints directly from their own verifier prompts (same vocabulary).
  4. *Update callers.* `/auto` drops `--drive`, `--interval`, `--max-ticks`, `--sink`, `--base`; keeps `--platform` pass-through; gains `--babysit <pr-url>` (forwards to `/define --babysit`, then `/do`).
  5. *Remove old.* Delete `skills/drive/` and `skills/drive-tick/` directories with all reference subtrees.
  6. *Sweep + redistribute.* Plugin metadata (plugin.json, marketplace.json), READMEs at three levels, then run sync-tools to regenerate dist/ for Gemini/OpenCode/Codex.

  Rationale: avoids broken intermediate state. New ACs become available before /do dispatch lands (verifiers degrade gracefully on FAIL — /do already escalates), and old skill removal happens only after callers (/auto) and metadata reference the new model.

- **Execution Order:**
  - D1 → D2 → D3 → D4 → D5 → D6 → D7
  - Rationale: dependencies above. D7 (sync-tools) is always last per repo convention.

- **Risk Areas:**
  - [R-1] *Hint-parser misclassification.* Free-form hint text relies on /do's LLM judgment to extract action + parameters; ambiguous phrasing could dispatch the wrong action. | Detect: prompt-reviewer flags ambiguity in verifier prompts; explicit hint vocabulary listed in /do SKILL.md is checked by intent reviewer.
  - [R-2] *Verifier prompt complexity.* Lifecycle verifiers embed classification logic (bot/human, in-scope/out-of-scope, retriggerable/genuine-failure, retrigger-cap tracking via log read). Risk of bloat or contradiction. | Detect: prompt-reviewer no MEDIUM+ on the new prompts; intent reviewer confirms each classification rule earns its place.
  - [R-3] *Session-held trade-off.* /do running for hours/days on lifecycle waits requires the session to stay alive; closing the terminal stops progress. Approval-wait is the dominant long-poll (mergeable can't flip until a human approves). Same trade-off as /drive's inline-fallback. | Detect: PR_LIFECYCLE.md Gotchas section names this explicitly with the approval-wait long-poll case spelled out; user acknowledges via manifest review.
  - [R-4] *Stale references after removal.* /drive mentions linger in READMEs, plugin.json keywords/description, marketplace.json, cross-skill references in other SKILL.md files. | Detect: INV-G7 grep-based gate (see below).
  - [R-5] *Self-bootstrap pitfall.* This manifest builds PR_LIFECYCLE; can't compose it. Lifecycle for this PR is manual. | Detect: ASM-1 logs the limitation.

- **Trade-offs:**
  - [T-1] Free-form hint text vs structured contract → Prefer free-form because /do is an LLM that reads English; structured schema is overhead without benefit. Risk: misclassification — mitigated by consistent action vocabulary in verifier and /do prompts.
  - [T-2] Branch lock for parallel /do vs no lock → Prefer no lock because lifecycle /do runs are long but single-user workflows; parallel invocations are user error and surface naturally as git push conflicts. Documented in /do Gotchas.
  - [T-3] Gate ownership: agent vs templated verifier prompts → Agent. The canonical gate set lives inside `github-pr-lifecycle`'s prompt as implementation detail (mergeable composite GitHub-computed, threads, CI, PR description sync, PR-exists pre-flight). PR_LIFECYCLE.md templates ONE agent-invoking AC, not five separate verifier prompts. Win: cross-signal holistic reasoning (e.g., "CI green but branch behind → push-update before claiming clean"), one PR-state read per check, one prompt file to iterate, simpler customization (user overlays via the AC's verify.prompt). Cost: less verify-report granularity (one ❌ "pr-lifecycle (CI failed)" instead of multiple ❌). Mitigation: agent emits a breakdown in its FAIL body. User custom gates beyond the canonical set still use direct verifier hints in user-added ACs (added via /define --amend).
  - [T-4] Platform-specific agent vs generic pr-lifecycle agent → Platform-specific (`github-pr-lifecycle`, future `gitlab-pr-lifecycle`/`bitbucket-pr-lifecycle`). Each platform's API surface is different enough that a single agent branching on platform is more complex than separate agents. /define picks by `--platform`.

## 3. Global Invariants

- [INV-G1] change-intent-reviewer reports no LOW or higher findings across all changed prompt files (skill, agent, reference, task files).
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    model: inherit
    prompt: "Review the changes on this branch for intent fidelity. Threshold: no LOW or higher findings. Focus on whether the verifier-hint protocol, /do action dispatch, action-aware budget, PR_LIFECYCLE templates, BABYSIT_MODE, and /auto --babysit pass-through match the documented intent in /tmp/define-discovery-20260512-053955.md."
  ```

- [INV-G2] prompt-reviewer reports no MEDIUM or higher findings on all newly authored or substantially modified prompts (SKILL.md files, criteria-checker.md, **github-pr-lifecycle.md (NEW agent)**, PR_LIFECYCLE.md, BABYSIT_MODE.md, execution-mode files).
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review newly authored or substantially modified prompts in this branch against prompt-engineering principles. Threshold: no MEDIUM or higher findings. Files in scope: claude-plugins/manifest-dev/agents/github-pr-lifecycle.md, claude-plugins/manifest-dev/skills/define/tasks/PR_LIFECYCLE.md, claude-plugins/manifest-dev/skills/define/references/BABYSIT_MODE.md, claude-plugins/manifest-dev/skills/define/SKILL.md, claude-plugins/manifest-dev/skills/do/SKILL.md, claude-plugins/manifest-dev/skills/verify/SKILL.md, claude-plugins/manifest-dev/skills/auto/SKILL.md, claude-plugins/manifest-dev/skills/do/references/execution-modes/*.md, claude-plugins/manifest-dev/agents/criteria-checker.md."
  ```

- [INV-G3] No `/drive`, `/drive-tick`, `drive-log-`, `drive-lock-`, `drive-tick:` references in any surviving file (markdown, json, python).
  ```yaml
  verify:
    method: bash
    command: "OUT=$(grep -rEn '/drive|/drive-tick|drive-log-|drive-lock-|drive-tick:' --include='*.md' --include='*.json' --include='*.py' /home/user/manifest-dev 2>/dev/null | grep -v -E '^(/home/user/manifest-dev/(\\.manifest|dist|node_modules))' | grep -v -E '/tmp/' | head -50); [ -z \"$OUT\" ] || { echo \"$OUT\"; false; }"
  ```

- [INV-G4] Plugin keywords and description in `claude-plugins/manifest-dev/.claude-plugin/plugin.json` do not mention drive, drive-tick, tick, or loop. Version is bumped from `0.107.0`.
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; p=json.load(open('/home/user/manifest-dev/claude-plugins/manifest-dev/.claude-plugin/plugin.json')); bad=[k for k in p.get('keywords',[]) if k in ('drive','drive-tick','tick','loop')]; desc_bad=any(s in p.get('description','').lower() for s in ('drive','drive-tick','/drive','/loop')); ver_ok=p.get('version','')!='0.107.0'; assert not bad, f'forbidden keywords: {bad}'; assert not desc_bad, 'description mentions drive/loop'; assert ver_ok, 'version not bumped'; print('plugin.json clean')\""
  ```

- [INV-G5] Existing non-lifecycle manifests (no action-labeled hints, no `verify.timeout:`) run through new `/do` without behavioral change. Action-aware budget is no-op when no action-labeled hints exist; per-phase fix-cap behaves identically to the pre-change contract.
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    model: inherit
    prompt: "Audit claude-plugins/manifest-dev/skills/do/SKILL.md and the three execution-mode files (claude-plugins/manifest-dev/skills/do/references/execution-modes/{thorough,balanced,efficient}.md) for backwards compatibility: verify that a manifest containing only standard ACs (no PR_LIFECYCLE gates, no action-labeled hint vocabulary in verifier prompts) executes identically to pre-change behavior. Specifically: (1) per-phase fix-verify cap behavior is unchanged when verifiers return FAIL without action labels, (2) /do's fix dispatch defaults to code-fix when no action label is detected in the hint body, (3) no new mandatory schema fields break old manifest parsing. Report any LOW+ findings as failures."
  ```

- [INV-G6] sync-tools has been run after all skill/agent/reference changes — the `dist/` directory reflects the current state of claude-plugins/manifest-dev/.
  ```yaml
  verify:
    method: bash
    phase: 2
    command: "test -d /home/user/manifest-dev/dist && find /home/user/manifest-dev/dist -newer /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/tasks/PR_LIFECYCLE.md 2>/dev/null | head -1 | grep -q . && echo 'dist is newer than PR_LIFECYCLE.md (sync-tools ran after changes)'"
  ```

- [INV-G7] No `/drive`, `/drive-tick`, `drive-log-`, `drive-lock-` references in the `dist/` directory after sync-tools regeneration.
  ```yaml
  verify:
    method: bash
    phase: 2
    command: "OUT=$(grep -rEn '/drive|/drive-tick|drive-log-|drive-lock-' /home/user/manifest-dev/dist 2>/dev/null | head -20); [ -z \"$OUT\" ] || { echo \"$OUT\"; false; }"
  ```

- [INV-G8] /do never invokes `gh pr merge` (or any merge-button action) and the github-pr-lifecycle agent never emits a `merge-pr` action label. The terminal is "PR mergeable", not "PR merged" — pressing the button is out of scope for both. Enforced by grep across all surviving plugin markdown/json/python files, case-insensitively, with a documented allowlist for canonical prohibition prose. The canonical prohibition phrasing — to keep allowlist tight — is `never invokes` / `never emits` / `does not call` / `out of scope` / `NOT a supported action`; writers must use these verbatim when documenting the prohibition.
  ```yaml
  verify:
    method: bash
    command: "OUT=$(grep -riEn 'gh pr merge|merge-pr|pr_merge|merge_pr_action' /home/user/manifest-dev/claude-plugins/manifest-dev/ --include='*.md' --include='*.json' --include='*.py' 2>/dev/null | grep -viE '(test_|\\.test\\.|never (invokes|emits|calls) (gh pr merge|merge-pr)|(does|do) not (call|invoke|emit) (gh pr merge|merge-pr)|out of scope|not a supported action|never a member|excluded from|prohibited from|forbidden)' | head -20); [ -z \"$OUT\" ] || { echo \"$OUT\"; false; }"
  ```

## 4. Process Guidance

- [PG-1] High-signal changes only — every modification addresses a documented requirement or known failure mode. No incidental refactors, no scope creep beyond declared deliverables.
- [PG-2] Calibrate emotional tone in all authored prompts — low arousal, no urgency language, no "MUST/ALWAYS/NEVER" on judgment calls; reserve absolutes for true invariants.
- [PG-3] Empty-input behavior is explicit for `/define --babysit` and `/auto --babysit` — both flags require a PR URL argument; missing → halt with an actionable usage message.
- [PG-4] Establish behavior contract before removal — for every /drive feature listed in the feature parity mapping (see discovery log), confirm the new home is present and operational before deleting the corresponding /drive code.
- [PG-5] Identify and migrate consumers — the only in-repo caller of /drive is /auto via `--drive`. After /auto's update lands, the /drive removal is safe.
- [PG-6] Out of scope: refactoring /verify's pass-logging contract, /do's memento pattern, /define's interview-mode files. Only touch what the deliverables require.
- [PG-8] Document session-held trade-off — PR_LIFECYCLE.md Gotchas section names the long-session implication clearly so users understand the workflow cost.

## 5. Known Assumptions

- [ASM-1] This manifest does NOT compose PR_LIFECYCLE.md (the feature being built) — chicken-and-egg. PR lifecycle for this PR (open, CI, merge) is managed manually by the user. | Default: treat lifecycle for this PR as out of /do scope; user reviews and merges manually. | Impact if wrong: dogfooding gap; first real user of PR_LIFECYCLE is a subsequent change.
- [ASM-2] Plugin version bump: 0.107.0 → 0.108.0 (minor — pre-1.0 plugin per repo convention; new features outweigh internal-skill removal). | Default: 0.108.0. | Impact if wrong: version semantics misread by consumers; correct via patch bump.
- [ASM-3] (Forward-looking — affects downstream consumers, not this manifest's verification.) When users compose PR_LIFECYCLE.md into future manifests, gh CLI and/or GitHub MCP tools must be available in the /do session for criteria-checker lifecycle verifiers (already true under /drive). | Default: assume availability; PR_LIFECYCLE.md Gotchas section names this prerequisite. | Impact if wrong: lifecycle ACs fail with "tool unavailable" at downstream consumer time; this manifest's verification is unaffected (ASM-1 keeps this PR's lifecycle manual).
- [ASM-4] sync-tools (the skill) is invocable via the Skill tool; running it regenerates `dist/` per repo convention. | Default: invoke `sync-tools` skill in D7. | Impact if wrong: dist/ stale; manual regeneration step required.

## 6. Deliverables

### Deliverable 1: github-pr-lifecycle agent + PR_LIFECYCLE.md task file

The agent owns lifecycle checking (mergeable composite, thread classification, retrigger-cap, hint emission). The task file is the /define-time guide that templates an AC invoking the agent. Paired because they define one concept together — agent is the runtime, task file is the /define-time onboarding.

**Acceptance Criteria:**

- [AC-1.1] `claude-plugins/manifest-dev/agents/github-pr-lifecycle.md` exists with valid frontmatter (name, description suitable for caller matching, tools list including Bash + Read with no Write/Edit since the agent is read-only). Body documents: purpose, expected invocation inputs (PR URL, branch, optional steering input), inspection goals (mergeable composite, CI status, review threads, PR description), output format (PASS or FAIL with a rich hint body in natural English), retrigger-cap logic at agent-neutral level (default cap 3, overridable via steering, escalate after cap), thread classification goals (bot vs human, in-scope vs out-of-scope), and explicit hard prohibitions: agent NEVER invokes `gh pr merge` or any merge-button action, terminal is "mergeable" not "merged"; agent NEVER references workflow-routing concepts (`/do`, `/verify`, `/define`, manifest amendment, Self-Amendment, AMENDMENT_MODE, etc.) — the agent reports findings, the caller owns dispatch decisions. Hints are free-form English; bracketed shorthand labels are optional and not required by any contract.
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev/agents/github-pr-lifecycle.md for prompt-engineering correctness and structural completeness. Verify: (1) frontmatter — name = github-pr-lifecycle, description semantically supports matching the agent for PR/lifecycle/mergeable concepts AND signals that the agent is steerable through the caller's invoking prompt, tools list includes Bash and Read and explicitly excludes Write/Edit (read-only inspection); (2) body documents invocation inputs (PR URL, branch, optional steering input) — agent-neutral framing; (3) the agent names the kinds of state it must reach to evaluate the canonical gates WITHOUT prescribing specific gh commands, JSON field lists, or API recipes — trust the model on capability; (4) the agent documents WHAT each gate verifies (the goal), NOT step-by-step procedure; (5) output format is PASS or FAIL with a free-form natural-English hint body — the agent may use bracketed shorthand labels (`[sleep]`, `[fix-code]`, etc.) as OPTIONAL clarity helpers but is NOT required to enumerate a closed vocabulary; (6) retrigger-cap logic documented agent-neutrally — prior counts from any context the caller provides; default cap 3, escalate after cap; (7) thread classification documented as goals (distinguish bot/human, classify intent, identify in-scope/out-of-scope) — NOT rigid procedure; (8) hard prohibitions explicit — agent NEVER invokes `gh pr merge` or any merge-button action; terminal is mergeable not merged; (9) **steerability** documented as first-class — invoking prompt is read additively on baseline; empty → baseline; narrower-wins on conflict; word 'steerable' or obvious equivalent appears; (10) **portability — agent is workflow-agnostic**. Banned tokens in the body (case-insensitive grep): `/do`, `/verify`, `/define`, `/escalate`, `/done`, `--scope`, `--amend`, `verify.prompt`, `AC's`, `the invoking AC`, `INV-G`, `manifest amendment`, `Self-Amendment`, `AMENDMENT_MODE`, `execution log`, `memento`, `PR_LIFECYCLE`, `task file`, `deliverable`, `verify-loop`. Generic English `manifest` (as plan/scope/contract) is allowed; multi-PR composition described agent-neutrally; (11) **prompt-engineering hygiene** — WHAT/WHY not HOW; trust capability; no prescriptive HOW recipes, no capability instructions, no arbitrary numbers without justification, no rigid checklists. Decision rules are fine; rigid procedures are not. ABSOLUTES (MUST/NEVER) reserved for true invariants: hard prohibitions (merge button, force-push, secret exposure), workflow decoupling, output-shape, steerability additive-overlay. Other content stays goal-shaped. Threshold: no MEDIUM+ findings."
  ```

- [AC-1.1b] Agent frontmatter `tools` list deterministically asserted — includes Bash and Read, excludes Write/Edit. Token-level membership (not substring). Handles all three YAML serializations the repo uses: bare CSV (`tools: A, B, C` — the repo convention; see criteria-checker.md / manifest-verifier.md / prompt-reviewer.md), inline array (`tools: [A, B, C]`), and YAML list (`tools:\n  - A\n  - B`). Belt-and-suspenders alongside AC-1.1's prompt-reviewer judgment — Write/Edit on a read-only inspection agent is a real safety boundary.
  ```yaml
  verify:
    method: bash
    command: |
      python3 - <<'PYEOF'
      import re
      t = open('/home/user/manifest-dev/claude-plugins/manifest-dev/agents/github-pr-lifecycle.md').read()
      m = re.search(r'^---\n(.*?)\n---', t, re.DOTALL)
      assert m, 'no frontmatter'
      fm = m.group(1)
      v = re.search(r'^tools:\s*(.*?)(?=^[a-zA-Z_][a-zA-Z0-9_-]*:|\Z)', fm + '\n', re.DOTALL | re.MULTILINE)
      assert v, f'no tools key in frontmatter:\n{fm}'
      raw = v.group(1).strip()
      if raw.startswith('['):
          tools = [x.strip().strip("'\"") for x in raw.strip('[]').split(',') if x.strip()]
      elif re.search(r'(^|\n)\s*-\s', raw):
          tools = [ln.strip().lstrip('-').strip().strip("'\"") for ln in raw.split('\n') if ln.strip().startswith('-')]
      else:
          tools = [x.strip().strip("'\"") for x in raw.split(',') if x.strip()]
      assert 'Bash' in tools, f'Bash missing from tools: {tools}'
      assert 'Read' in tools, f'Read missing from tools: {tools}'
      assert 'Write' not in tools, f'Write must NOT be in tools (agent is read-only): {tools}'
      assert 'Edit' not in tools, f'Edit must NOT be in tools (agent is read-only): {tools}'
      print(f'tools list OK: {tools}')
      PYEOF
  ```

- [AC-1.2] `claude-plugins/manifest-dev/skills/define/tasks/PR_LIFECYCLE.md` exists and follows task-file structure per /define SKILL.md "Task file content types": Quality Gates (the single agent-invoking AC template + customization examples), Defaults (timeout values, retrigger cap reference), Gotchas (session-held, security defaults, externally-closed PR handling), Risks/Scenarios/Trade-offs. The file does NOT contain inline verifier-prompt strings for the canonical gates (that logic lives in the agent); it documents the AC template that wraps the agent invocation. Platform→agent-name mapping convention documented (`{platform}-pr-lifecycle`) so future variants don't require dual edits.
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev/skills/define/tasks/PR_LIFECYCLE.md. Verify: (1) Quality Gates section presents ONE AC template — a verify block with method: subagent, agent: github-pr-lifecycle, model: inherit, and a templated prompt field that /define populates with PR URL, branch, and any user customization (additional gates, named approvers, known-flaky CI, etc.); (2) the file does NOT inline verifier-prompt strings for CI/threads/mergeable/etc. (those checks are the agent's internal logic, not the task file's concern); (3) Defaults section names timeout values (e.g., 30m CI-poll, 1d approval-wait) and the default retrigger cap (3) — cross-references where the agent applies them; (4) Gotchas section names session-held trade-off, security defaults preserved from /drive (no force-push, no secrets in replies, untrusted-inbox handling), AND externally-closed PR handling (someone else merged/closed the PR mid-session); (5) follows 'probing fuel, not execution instructions' pattern; (6) multi-repo composition rule documented (auto-template AC per-repo when Repos: declared); (7) **steering examples** show how a user steers the agent through the AC's verify.prompt (e.g., 'Required label: qa-approved', 'Reviewer @alice required', 'CI job foo is known-flaky'); the task file frames customization as steering the agent, not amending the task file itself; (8) platform→agent-name convention is documented as `{platform}-pr-lifecycle` (current value: github-pr-lifecycle) so future GitLab/Bitbucket additions don't require editing the task file at two sites. Threshold: no MEDIUM+ findings."
  ```

- [AC-1.2b] PR_LIFECYCLE.md's templated AC literally names `github-pr-lifecycle` as the agent (deterministic check alongside AC-1.2's prompt-reviewer judgment).
  ```yaml
  verify:
    method: bash
    command: "grep -qE '^\\s*agent:\\s*github-pr-lifecycle\\s*$' /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/tasks/PR_LIFECYCLE.md && echo 'PR_LIFECYCLE.md templates agent: github-pr-lifecycle'"
  ```

- [AC-1.3] /define SKILL.md Domain Guidance table includes a row for PR_LIFECYCLE with appropriate Indicators ("PR / lifecycle / shipping / merge / CI gates"), and a Composition paragraph documents that PR_LIFECYCLE composes onto CODING.md when `--platform github` is set (auto-detected from git remote unless `--platform none`). The paragraph or table entry also names the agent (`github-pr-lifecycle`) as the runtime that PR_LIFECYCLE's templated AC invokes — making the wire explicit.
  ```yaml
  verify:
    method: codebase
    prompt: "In claude-plugins/manifest-dev/skills/define/SKILL.md: verify the Domain Guidance table contains a row referencing tasks/PR_LIFECYCLE.md with appropriate indicators (PR / lifecycle / shipping / merge / CI). Verify the Composition paragraph (or a new paragraph) explicitly documents: (1) PR_LIFECYCLE composes onto CODING.md when --platform github resolves (auto-detected from git remote unless --platform none is passed); (2) PR_LIFECYCLE.md templates an AC that invokes the github-pr-lifecycle agent — the agent is named explicitly so a /define reader knows which agent the templated AC binds to."
  ```

- [AC-1.4] github-pr-lifecycle agent file is hardlinked into `.claude/agents/` per the repo's "local development" convention from CLAUDE.md, so /define can reach it without plugin install. Hardlink integrity checked via inode equality + canonical file non-empty (a copy or two empty files would pass a naive diff check).
  ```yaml
  verify:
    method: bash
    command: "test -e /home/user/manifest-dev/.claude/agents/github-pr-lifecycle.md && test -s /home/user/manifest-dev/claude-plugins/manifest-dev/agents/github-pr-lifecycle.md && test \"$(stat -c %i /home/user/manifest-dev/.claude/agents/github-pr-lifecycle.md)\" = \"$(stat -c %i /home/user/manifest-dev/claude-plugins/manifest-dev/agents/github-pr-lifecycle.md)\" && echo 'agent hardlinked (inode match) and non-empty'"
  ```

- [AC-1.5] Gate enumeration is encapsulated to the agent file. All plugin markdown — task files (`tasks/CODING.md`, `tasks/FEATURE.md`, `tasks/PR_LIFECYCLE.md`, other task files), SKILL.md files (define / do / verify / auto), reference files (`references/BABYSIT_MODE.md`, `references/AMENDMENT_MODE.md`, `references/CANVAS_MODE.md`, `references/execution-modes/*.md`), agent files (criteria-checker, change-intent-reviewer, manifest-verifier — all surviving agents), and the three README levels (root, `claude-plugins/README.md`, `claude-plugins/manifest-dev/README.md`) — must NOT enumerate the canonical gates as a normative list. **Exempt:** the github-pr-lifecycle.md agent file (it owns the gate definitions) and this manifest file (definition-time, not consumer-facing). **Threshold:** any list (numbered, bulleted, or comma-separated) of 3+ canonical gates in normative position counts as leakage. Casual 1-2 item mentions in passing prose are fine.
  ```yaml
  verify:
    method: codebase
    prompt: "Scan ALL surviving plugin markdown under /home/user/manifest-dev/claude-plugins/manifest-dev/ (task files in skills/define/tasks/, reference files in skills/*/references/, SKILL.md files, all agent files except github-pr-lifecycle.md) AND the three READMEs (/home/user/manifest-dev/README.md, /home/user/manifest-dev/claude-plugins/README.md, /home/user/manifest-dev/claude-plugins/manifest-dev/README.md) for normative enumerations of the canonical lifecycle gates. EXEMPT (do not scan): /home/user/manifest-dev/claude-plugins/manifest-dev/agents/github-pr-lifecycle.md (the agent owns the gate definitions). LEAKAGE = any list (numbered, bulleted, or comma-separated) of 3+ canonical gates (PR exists / CI green / threads addressed / PR description in sync / PR mergeable) in normative position (contract statement, requirement, definition). OK: 'covers the lifecycle gates including CI and threads' (1-2 mentions in prose). OK: 'PR_LIFECYCLE templates an AC that invokes the agent for lifecycle checking' (no gate enumeration). NOT OK: 'the gates are: CI green, threads, description, mergeability' (4-item normative list). NOT OK: a bulleted list with 3+ gates each on its own line in normative context. Fail with file:line citations if found. Particularly high-risk leakage sites: tasks/CODING.md (PR_LIFECYCLE composes onto it), tasks/FEATURE.md (overlaps with PR work), and the three READMEs (authors describing the new model may want to enumerate)."
  ```

### Deliverable 2: /define --babysit + BABYSIT_MODE.md + platform auto-detection

Synthesis path for an existing PR (no manifest required), platform-aware composition, schema additions.

**Acceptance Criteria:**

- [AC-2.1] `claude-plugins/manifest-dev/skills/define/references/BABYSIT_MODE.md` exists and specifies: PR URL parsing (gh URL format), pre-flight (gh availability, PR accessible, repo matches origin), Intent seeding from PR title/body, AC templating sources PR_LIFECYCLE.md (which produces the agent-invoking AC), default interview style is autonomous (rationale: the lifecycle AC is one templated invocation), how the user adds custom ACs via re-invoking `/define --amend` after.
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev/skills/define/references/BABYSIT_MODE.md for prompt quality. Verify it specifies: (1) PR URL parsing convention, (2) pre-flight checks (gh CLI / GitHub MCP availability, PR accessible, repo matches), (3) Intent seeding from PR title/body, (4) AC templating sources PR_LIFECYCLE.md which produces the github-pr-lifecycle agent-invoking AC (single AC, not a 5-gate list), (5) default interview style is autonomous with rationale, (6) post-babysit custom AC path (/define --amend) for adding user-specific gates beyond the agent's canonical set. Threshold: no MEDIUM+ findings. Compare structure against AMENDMENT_MODE.md and CANVAS_MODE.md for parallel pattern alignment."
  ```

- [AC-2.2] /define SKILL.md flags table contains `--babysit <pr-url>` and `--platform` entries with documented behavior: `--babysit` triggers babysit mode (Pre-flight routes accordingly), `--platform` accepts `github` | `none` and defaults to auto-detection from git remote (github remote → github; no recognized remote → none). Missing argument errors are actionable (e.g., "`--babysit` requires a PR URL").
  ```yaml
  verify:
    method: codebase
    prompt: "In claude-plugins/manifest-dev/skills/define/SKILL.md flags table: verify two new rows exist for --babysit <pr-url> and --platform <github|none>. Verify documented behavior: --babysit routes to babysit mode (per BABYSIT_MODE.md); --platform defaults to auto-detection from git remote (github remote → github; otherwise none). Verify Input section halts with actionable error when --babysit is passed without a URL or with an inaccessible URL."
  ```

- [AC-2.3] /define Pre-flight section recognizes `--babysit` as a third mode alongside fresh/amend, and routes to BABYSIT_MODE.md when set. Babysit + amend together → halt with a clear error.
  ```yaml
  verify:
    method: codebase
    prompt: "In claude-plugins/manifest-dev/skills/define/SKILL.md Pre-flight section: verify --babysit is recognized as a third mode beside fresh and amend. Verify routing to references/BABYSIT_MODE.md when --babysit is set. Verify a clear error when --babysit and --amend are passed together (conflicting modes)."
  ```

- [AC-2.4] Manifest schema in /define SKILL.md documents a per-AC `verify.timeout:` field (optional, shorthand duration string e.g. `30s`, `5m`, `6h`, `1d`). Existing verify blocks without `timeout` behave unchanged.
  ```yaml
  verify:
    method: codebase
    prompt: "In claude-plugins/manifest-dev/skills/define/SKILL.md Manifest Schema section: verify the verify block YAML example documents an optional `timeout:` field with type and example values (`timeout: 30s`, `timeout: 5m`, `timeout: 6h`, `timeout: 1d`). Verify a note that the field is optional and absent means no wall-clock cap (legacy behavior preserved)."
  ```

- [AC-2.5] Parser/consumer behavior for `verify.timeout:` is documented in /do SKILL.md: valid shorthand parses to seconds; absent → unbounded (legacy); malformed → halt with actionable error naming the offending AC and value.
  ```yaml
  verify:
    method: codebase
    prompt: "In claude-plugins/manifest-dev/skills/do/SKILL.md: verify a paragraph documents verify.timeout parser behavior — accepted shorthand (s/m/h/d suffix), absent means no cap (legacy compat), malformed → halt with error that names which AC and which value. Cross-references to AC-2.4's schema entry."
  ```

- [AC-2.6] BABYSIT_MODE.md documents error paths for non-canonical PR URLs and unsuitable PR states:
  - wrong-platform URL when `--platform github` is set (or auto-detected) → halt with actionable error;
  - PR closed or merged at synthesis time → halt with clear message (synthesizing a manifest for a terminal PR is user error);
  - PR from a fork → babysit targets the upstream repo where the PR lives, not the fork.
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "In claude-plugins/manifest-dev/skills/define/references/BABYSIT_MODE.md: verify three error-path / convention paragraphs exist — (1) wrong-platform URL when --platform is set → halt with actionable error; (2) PR already closed or merged at synthesis time → halt with clear message; (3) fork PR convention — babysit targets the upstream repo where the PR lives. Each must have phrasing concrete enough that the implementing skill can act on it (not vague advice). Threshold: no MEDIUM+ findings."
  ```

### Deliverable 3: Verifier rich-hint protocol + /do hint dispatcher + action-aware budget

Runtime mechanics — the core abstraction that replaces /drive's tick-driven action layer.

**Acceptance Criteria:**

- [AC-3.2] `claude-plugins/manifest-dev/agents/criteria-checker.md` documents its standard Output Format — PASS/FAIL with Status, Evidence, and (on FAIL) actionable detail in plain English. No separate "rich-hint convention" layer; a FAIL message is itself the hint. Hard rule preserved: outputs must not suggest pressing the merge button or invoking `gh pr merge` (INV-G8 enforces).
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev/agents/criteria-checker.md for prompt quality (no MEDIUM+). Verify the Output Format section documents the standard PASS/FAIL output (Status, Evidence, and on FAIL an actionable fix hint field) in natural English. Verify there is NO separate 'rich-hint convention' subsection or closed vocabulary block — the standard Output Format alone is sufficient; an extra layer documenting 'FAIL bodies may include hints' would be redundant (a FAIL message IS the hint). Flag MEDIUM if such a redundant section is present. Hard rule preserved: outputs must not suggest pressing the merge button or invoking `gh pr merge`. **Light-touch portability** still applies: opening role statement remains generic ('verify a SINGLE criterion. Read-only.') and does not hard-couple to manifest-dev's workflow."
  ```

- [AC-3.3] /do SKILL.md documents three things about verifier hint handling: (a) FAIL bodies may include free-form natural-English hint text; /do parses with LLM judgment — no closed vocabulary, no required schema, no rigid dispatch table; (b) **action-aware fix-cap** — only code-change fix attempts increment the per-phase fix-verify counter; other retry shapes (waits for CI, retriggers of transient failures, replies on threads, pushes of sync updates, scope-amendment cycles) are not fix attempts and don't burn the budget; (c) explicit prohibition: `merge-pr` is not a supported action; /do does NOT invoke `gh pr merge` under any path. Mid-Execution Amendment section notes that scope-amend hints route through Self-Amendment, same as user-message-triggered amendments.
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev/skills/do/SKILL.md for verifier-hint handling. Verify: (1) the file documents that FAIL bodies may include free-form natural-English hint text; /do parses with LLM judgment — NO required vocabulary, NO dispatch mapping table, NO rigid parsing rules. Optional bracketed shorthand labels may be mentioned as convention but not as contract; (2) **action-aware fix-cap** rule is documented — only code-change fix attempts increment the per-phase fix-verify counter; other retry shapes (waits, retriggers, replies, pushes, scope-amendments) don't burn the budget; (3) merge-button prohibition explicit — `merge-pr` is not a supported action, /do does NOT invoke `gh pr merge`; (4) Mid-Execution Amendment section notes scope-amend hints route through Self-Amendment. Threshold: no MEDIUM+ findings. If the file still contains a closed-vocabulary section, a dispatch-mapping table, or parsing rules for specific labels, flag MEDIUM — these are over-engineered relative to LLM-judgment dispatch."
  ```

- [AC-3.4] Execution-mode files (`thorough.md`, `balanced.md`, `efficient.md`) document action-aware fix-cap semantics: only **code-change fix attempts** increment the per-phase fix-verify counter. Other retry shapes (re-verifications after waits, CI retriggers, thread replies, sync pushes, scope-amendment cycles) are not fix attempts and don't burn the budget. Per-AC `verify.timeout:` is the wall-clock cap that prevents runaway on criteria that legitimately wait. The rule is stated as a principle, not enumerated as a closed list of action labels.
  ```yaml
  verify:
    method: codebase
    prompt: "In claude-plugins/manifest-dev/skills/do/references/execution-modes/{thorough,balanced,efficient}.md: verify each file's Fix-Verify Loops (or equivalent) section states the principle that only code-change fix attempts count toward the cap; other retry shapes (waits, retriggers, replies, pushes, scope-amendments) don't burn budget. The rule is stated as a principle — enumerating specific action labels is NOT required (and over-enumeration is a soft anti-signal: prefer principle over closed list). Verify a cross-reference to per-AC verify.timeout: for criteria that legitimately wait. `amend-manifest` must NOT appear as a hint label anywhere."
  ```

- [AC-3.5] Backwards compat — /do behavior on non-lifecycle manifests (no action-labeled hints, no verify.timeout: fields) is unchanged. Verifier hints without recognizable action labels default to code-fix interpretation (preserves the legacy fail→fix→reverify cycle).
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    model: inherit
    prompt: "Verify backwards compat for non-lifecycle manifests in the updated /do SKILL.md and execution-mode files. Default dispatch when no action label is present must be code-fix; per-phase counter must increment as before. Confirm no new mandatory fields break old manifest parsing. Threshold: no LOW+ findings."
  ```

### Deliverable 4: /auto trim + --babysit pass-through

/auto becomes a thin chain: /define → /do with optional --platform and --babysit pass-through.

**Acceptance Criteria:**

- [AC-4.1] /auto SKILL.md drops `--drive`, `--interval`, `--max-ticks`, `--sink`, `--base` flags entirely. Mentions of /drive in the description, Flow, Failure Handling, and Multi-Repo sections are removed.
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '\\-\\-drive|\\-\\-interval|\\-\\-max-ticks|\\-\\-sink|\\-\\-base|/drive|drive-tick' /home/user/manifest-dev/claude-plugins/manifest-dev/skills/auto/SKILL.md"
  ```

- [AC-4.2] /auto SKILL.md keeps `--platform` flag and passes it to /define. Default platform inference (auto-detect from git remote) lives in /define; /auto just forwards the flag value.
  ```yaml
  verify:
    method: codebase
    prompt: "In claude-plugins/manifest-dev/skills/auto/SKILL.md: verify --platform <github|none> is documented and passed through to /define. Verify there is no platform inference logic in /auto itself (lives in /define per spec)."
  ```

- [AC-4.3] /auto SKILL.md gains `--babysit <pr-url>` flag. When set, /auto invokes `/define --babysit <pr-url>` (autonomous interview), then `/do <manifest-path>` on the resulting lifecycle-only manifest. Documented use case: tend a PR in a repo that doesn't use manifest-dev.
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev/skills/auto/SKILL.md for the --babysit flag. Verify: (1) flag is documented in Input section, (2) Flow section describes the chain — /define --babysit <pr-url> then /do <manifest>, (3) use case is documented (tend a PR in a repo without manifest-dev), (4) missing URL halts with actionable error, (5) --babysit + free-form task description combo is handled (error or precedence rule documented). Threshold: no MEDIUM+ findings."
  ```

- [AC-4.4] /auto --babysit infers `--platform` from the PR URL host when not explicitly passed (github.com → github), not from the local git remote. Rationale: the use case is repos that may not be locally cloned. Encoded as documented behavior in /auto SKILL.md flags + Pre-flight sections.
  ```yaml
  verify:
    method: codebase
    prompt: "In claude-plugins/manifest-dev/skills/auto/SKILL.md: verify --auto --babysit's platform-inference rule is documented — when --platform is not explicitly passed and --babysit is set, platform is derived from the PR URL host (github.com → github). Verify this is distinct from /define's git-remote-based inference (which is the right default when no babysit URL is provided). If both --platform and --babysit are passed and disagree with the URL host, halt with a clear error."
  ```

- [AC-4.5] /auto trigger description in frontmatter is updated to drop drive-specific triggers ("pr lifecycle", "review", etc., to the extent they reference drive). Add babysit-related triggers naturally.
  ```yaml
  verify:
    method: codebase
    prompt: "In claude-plugins/manifest-dev/skills/auto/SKILL.md frontmatter description: verify drive-specific phrasing is removed (no mention of 'PR review lifecycle automation', 'cron-driven', etc.). Verify babysit use case (tend an existing PR) is naturally reflected in description triggers."
  ```

### Deliverable 5: Remove /drive and /drive-tick

Delete the skill directories with all reference subtrees. Verify nothing breaks.

**Acceptance Criteria:**

- [AC-5.1] Directories `claude-plugins/manifest-dev/skills/drive/` and `claude-plugins/manifest-dev/skills/drive-tick/` no longer exist.
  ```yaml
  verify:
    method: bash
    command: "test ! -d /home/user/manifest-dev/claude-plugins/manifest-dev/skills/drive && test ! -d /home/user/manifest-dev/claude-plugins/manifest-dev/skills/drive-tick"
  ```

- [AC-5.2] The hardlinked/symlinked counterparts under `.claude/skills/drive/`, `.claude/skills/drive-tick/`, `.agents/skills/drive/`, `.agents/skills/drive-tick/` are also removed (if any existed). CLAUDE.md's hardlink note still applies to surviving skills.
  ```yaml
  verify:
    method: bash
    command: "test ! -e /home/user/manifest-dev/.claude/skills/drive && test ! -e /home/user/manifest-dev/.claude/skills/drive-tick && test ! -e /home/user/manifest-dev/.agents/skills/drive && test ! -e /home/user/manifest-dev/.agents/skills/drive-tick"
  ```

- [AC-5.3] No other skill or agent in the manifest-dev plugin still references /drive or /drive-tick (cross-skill mentions cleaned up).
  ```yaml
  verify:
    method: bash
    command: "OUT=$(grep -rEn '/drive|/drive-tick|drive-log-|drive-lock-|drive-tick:' /home/user/manifest-dev/claude-plugins/manifest-dev/ 2>/dev/null | head -20); [ -z \"$OUT\" ] || { echo \"$OUT\"; false; }"
  ```

### Deliverable 6: Plugin metadata + READMEs sweep

Reflect the new model in user-facing docs and plugin descriptors.

**Acceptance Criteria:**

- [AC-6.1] `claude-plugins/manifest-dev/.claude-plugin/plugin.json` version bumped from 0.107.0 to 0.108.0; description rewritten to omit /drive and reflect the new model; keywords list drops `drive`, `drive-tick`, `tick`, `loop` and adds entries reflecting the new capabilities (e.g., `pr-lifecycle`, `babysit`).
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; p=json.load(open('/home/user/manifest-dev/claude-plugins/manifest-dev/.claude-plugin/plugin.json')); v=p.get('version',''); kw=p.get('keywords',[]); desc=p.get('description','').lower(); assert v=='0.108.0', f'version should be 0.108.0, got {v}'; bad=[k for k in kw if k in ('drive','drive-tick','tick','loop')]; assert not bad, f'forbidden keywords still present: {bad}'; assert not any(s in desc for s in ('drive','/loop','cron','tick')), 'description still references drive/loop/cron/tick'; assert any(k in kw for k in ('pr-lifecycle','babysit','lifecycle')), f'new keywords missing from {kw}'; print('OK')\""
  ```

- [AC-6.2] Root `README.md` reflects the new model — /drive and /drive-tick removed from Available Plugins / Skills listings; new capabilities (PR lifecycle ACs, babysit mode) mentioned where appropriate.
  ```yaml
  verify:
    method: subagent
    agent: docs-reviewer
    model: inherit
    prompt: "Audit /home/user/manifest-dev/README.md against the change set on this branch. Verify: (1) /drive and /drive-tick are not listed in any skill/component listing, (2) the new model (lifecycle ACs via PR_LIFECYCLE, --babysit mode, /auto --babysit) is mentioned where the prior README mentioned /drive, (3) no broken links or stale references remain. Threshold: no MEDIUM+ findings."
  ```

- [AC-6.3] `claude-plugins/README.md` and `claude-plugins/manifest-dev/README.md` reflect the new model — no /drive or /drive-tick references; lifecycle/babysit capabilities reflected.
  ```yaml
  verify:
    method: subagent
    agent: docs-reviewer
    model: inherit
    prompt: "Audit claude-plugins/README.md and claude-plugins/manifest-dev/README.md against the change set. Verify no /drive or /drive-tick references in skill listings/tables, and that PR_LIFECYCLE / babysit capabilities are reflected. Threshold: no MEDIUM+ findings."
  ```

- [AC-6.4] If `.claude-plugin/marketplace.json` references /drive, /drive-tick, or drive-keyworded copy in plugin metadata, those references are cleaned.
  ```yaml
  verify:
    method: bash
    command: "! grep -nEi 'drive|drive-tick|/loop' /home/user/manifest-dev/.claude-plugin/marketplace.json 2>/dev/null"
  ```

### Deliverable 7: sync-tools regeneration

Regenerate multi-CLI distribution packages so dist/ reflects the current plugin state.

**Acceptance Criteria:**

- [AC-7.1] sync-tools skill has been invoked after all prior deliverables landed; resulting `dist/` directory contains updated Gemini CLI / OpenCode / Codex CLI artifacts.
  ```yaml
  verify:
    method: bash
    phase: 2
    command: "test -d /home/user/manifest-dev/dist && find /home/user/manifest-dev/dist -name '*.md' -newer /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/tasks/PR_LIFECYCLE.md 2>/dev/null | head -3 | grep -q . && echo 'dist refreshed after task file changes'"
  ```

- [AC-7.2] `dist/` contains no references to /drive, /drive-tick, drive-log-, drive-lock- after regeneration (sync-tools should not propagate stale content; this verifies the regeneration captured the deletion).
  ```yaml
  verify:
    method: bash
    phase: 2
    command: "OUT=$(grep -rEn '/drive|/drive-tick|drive-log-|drive-lock-' /home/user/manifest-dev/dist 2>/dev/null | head -20); [ -z \"$OUT\" ] || { echo \"$OUT\"; false; }"
  ```

- [AC-7.3] sync-tools regeneration did not surface errors — every plugin component (skill, agent, hook) listed under claude-plugins/manifest-dev/ has corresponding dist artifacts for each target CLI (Gemini, OpenCode, Codex), per repo convention.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: inherit
    prompt: "Inspect /home/user/manifest-dev/dist/ structure. Verify the three target distributions (Gemini CLI, OpenCode, Codex CLI per the sync-tools skill description) are present, and that the count of skill/agent artifacts per distribution matches the count of source skills/agents under /home/user/manifest-dev/claude-plugins/manifest-dev/skills/ and /home/user/manifest-dev/claude-plugins/manifest-dev/agents/. Report discrepancies (missing, orphaned, mis-converted) as findings. Threshold: zero discrepancies."
  ```

## 7. Amendments

### Amendment 1 (post-/done, from /do) — Decouple agent from /define; rename `amend-manifest` → `out-of-scope`

**Trigger**: User feedback after /done — "Agent shouldn't know about define keep it one way. It does its job and reports. Also make sure the agent prompt went through the prompt reviewer."

**Rationale**: The agent's emitted action label `amend-manifest` named /define's workflow surface, coupling the agent's vocabulary to /do's dispatch decisions. Per separation-of-concerns: the agent reports findings; /do owns workflow routing. Renaming to `out-of-scope` re-frames the agent's vocabulary as *findings* (situation descriptions) rather than *actions* (workflow steps). /do internally maps `out-of-scope` → Self-Amendment / `/define --amend` in dispatch — same end-state, clean responsibility boundary.

**Changes**:
- **PG-7** (closed action set): `amend-manifest` → `out-of-scope`. Added note that vocabulary names findings, not workflow actions. Explicit ban: `amend-manifest` is NOT a member (sibling of the existing `merge-pr` ban).
- **§1 Mental Model** verifier-hint protocol bullet: updated example list; added decoupling sentence.
- **AC-1.1** (agent file authoring):
  - Updated emittable-vocabulary clause: `out-of-scope` replaces `amend-manifest`; `amend-manifest` and `merge-pr` both explicitly banned.
  - Added clause (11) — **workflow decoupling**: agent body must NOT reference `/define`, `/define --amend`, manifest amendment, Self-Amendment, AMENDMENT_MODE, or any workflow-routing concept. Agent prompt-reviewer must verify the word `/define` (and `manifest amendment` phrasing) does not appear in the agent body.
- **AC-3.2** (criteria-checker rich-hint convention): vocabulary updated; explicit `amend-manifest` ban noted.
- **AC-3.3** (/do Hint Dispatch): vocabulary updated. New clause (7) — explicit decoupling note that the agent emits findings, /do owns mapping findings to workflow (specifically: `out-of-scope` → Self-Amendment is /do's internal mapping, not the agent's concern). Mid-Execution Amendment routing reworded: `out-of-scope` hints route through Self-Amendment.
- **AC-3.4** (execution-mode action-aware fix-cap): non-counting actions list updated to include `out-of-scope` and explicitly state `amend-manifest` must NOT appear.

**Unchanged**: INV-G8 (no `gh pr merge` / `merge-pr`) is unrelated to amend-manifest rename and stays as-is.

**/do scope hint**: D1 (agent + task file) and D3 (criteria-checker, /do dispatch, execution-modes) are the affected deliverables. D5/D6/D7 unaffected. Recommend `--scope D1,D3` for the re-execution.

### Amendment 2 (post-/done, from /do) — Broaden agent portability requirement

**Trigger**: User feedback after Amendment 1 — "Agents shouldn't know they are even a part of define do loop. Like reviewers can be used outside of this repo."

**Rationale**: Amendment 1 banned `/define` and manifest-amendment terms from the agent, but the agent body still leaked many other manifest-dev workflow concepts: `the invoking AC's verify.prompt:`, `execution log (memento)`, `/do's session`, `PR_LIFECYCLE.md auto-templates`, etc. A user pasting `github-pr-lifecycle.md` into a non-manifest-dev repo wouldn't have AC schemas, /do session lifecycle, execution logs, or PR_LIFECYCLE.md task files — but they would have a GitHub PR. Like `prompt-reviewer` or `code-bugs-reviewer` can be used by anyone with prompts or code, this agent should be invocable by anyone with a PR URL and a steering prompt.

**Changes**:

- **AC-1.1 clause (11)** broadened. Banned tokens in agent body extended from `/define` / manifest-amendment to include `/do`, `/verify`, `/escalate`, `/done`, `--scope`, `--amend`, `verify.prompt`, `AC's`, `the invoking AC`, `INV-G`, `manifest amendment`, `Self-Amendment`, `AMENDMENT_MODE`, `execution log`, `memento`, `PR_LIFECYCLE`, `task file`, `deliverable`, `verify-loop`. Generic English use of "manifest" (as plan/scope/contract) remains allowed when the surrounding phrase reads as a finding regardless of which workflow the caller uses.
- **AC-1.1 clauses (2), (7), (10), Multi-PR** re-described agent-neutrally: invocation inputs are "the caller's invoking prompt"; retrigger-cap context is "any context made available to this invocation (log path / env var / steering counter)"; steerability frame uses "the invoking prompt" / "the caller's prompt"; multi-PR section says "agent handles one PR per invocation; multi-PR composition is the caller's responsibility" — no naming of PR_LIFECYCLE.md or the manifest workflow.
- **AC-3.2** light-touch addition: criteria-checker's opening role statement should be generic enough to support callers other than /verify (e.g., "verify a SINGLE criterion. Read-only"). Workflow-internal terms may appear in Input/Type-Specific Guidance sections (caller passes that data) but not as load-bearing assumptions in the role statement.

**Unchanged**: /do SKILL.md, /verify SKILL.md, PR_LIFECYCLE.md, BABYSIT_MODE.md, execution-mode files — these are workflow files and may reference manifest-dev's workflow freely. The decoupling requirement targets agent files (github-pr-lifecycle primarily; criteria-checker secondarily) where reusability outside this repo is the goal.

**/do scope hint**: D1 (agent body rewrite) and D3 (criteria-checker opening clarification). D2, D4, D5, D6, D7 unaffected. Recommend `--scope D1,D3`.

### Amendment 3 (post-/done, from /do) — Soften AC-1.1 prescription; require prompt-engineering principles

**Trigger**: User feedback after Amendment 2 — "Agent prompt is too prescriptive for example using gh tool. Rework the prompt with prompt template and prompt engineering skill and rerun."

**Rationale**: AC-1.1 clauses (3), (4), (7), (8) prescribed HOW (specific `gh pr view --json` field lists, exact procedural steps for state inspection, retrigger-count source format, classification procedures). Per the prompt-engineering skill (and PROMPTING.md anti-patterns: "Prescribing HOW" / "Capability instructions"), agent prompts should state goals + constraints and trust the model to pick the right tools / API calls / field names. The agent already knows how to use `gh` — it should not need a recipe.

**Changes**:

- **AC-1.1 clause (3)** softened: "the agent names the kinds of state it must reach to evaluate the canonical gates WITHOUT prescribing specific gh CLI commands, JSON field lists, or API surface details — trust the model to know the GitHub API." Removed the literal `gh pr view --json mergeable,mergeStateStatus,reviewDecision,statusCheckRollup,reviewThreads` enumeration from the AC.
- **AC-1.1 clause (4)** softened: "documents WHAT each canonical gate verifies (the goal) — NOT exact procedural steps."
- **AC-1.1 clause (7)** softened: retrigger-count context source no longer prescribes specific source formats — "any context made available to this invocation" agent-neutrally.
- **AC-1.1 clause (8)** softened: thread classification as goals, not rigid procedure.
- **AC-1.1 new clause (12)**: **Prompt-engineering hygiene**. Explicitly enforces the prompt-engineering principles: no prescriptive HOW, no capability instructions, no arbitrary numbers, no rigid checklists. ABSOLUTES (MUST/NEVER) reserved for true invariants (closed vocabulary, hard prohibitions, workflow decoupling, steerability). Suggests invoking prompt-engineering / review-prompt skill if uncertain.

**Unchanged**: Clauses (1), (2), (5), (6), (9), (10), (11), and PG-7 / AC-3.2 / AC-3.3 / AC-3.4 — these encode invariants (vocabulary, prohibitions, portability) which are appropriately prescriptive. criteria-checker is already goal-shaped — no change needed.

**/do scope hint**: D1 (rewrite the agent body via prompt-engineering skill to satisfy clause 12 + the softened clauses). D3, D2, D4, D5, D6, D7 unaffected. Recommend `--scope D1`.

### Amendment 4 (post-/done, from /do) — Strip the verifier-hint protocol layer; trust LLM capability

**Trigger**: User question — "Do we really need that hint protocol? Isn't that already baked in less formally?" Answer after honest reflection: mostly no. The closed action vocabulary, the dispatch mapping table, and the parsing convention enumerate things /do (an LLM) does naturally from free-form English. Only two pieces are genuinely new mechanism: (a) `verify.timeout:` schema/parser, (b) action-aware fix-cap. The rest was over-engineered protocol dressed up as mechanism. User direction: "Keep it simple we need to trust llm capability more as prompt engineering skill says."

**Rationale**: per prompt-engineering principles — WHAT and WHY, not HOW; trust capability. The protocol layer was capability-instructing /do on how to parse hints and which actions to dispatch — both already implicit in /do being an LLM that reads English.

**Changes**:

- **§1 Mental Model**:
  - "Verifier-hint protocol" bullet rewritten — verifier hints are natural English, no closed vocabulary, no required schema, no parsing rules; bracketed labels are optional shorthand for clarity.
  - "Action-aware budget" bullet reframed — only code-change fix attempts count toward the per-phase counter; other retry shapes don't (stated as principle, not enumerated by label).
- **PG-7** softened — vocabulary is convention not contract; merge-button prohibition preserved.
- **AC-1.1** description softened — agent emits PASS/FAIL with rich-hint body in natural English; the strict "vocabulary explicitly lists ..." requirement is dropped; bracketed shorthand is optional. Hard prohibitions (merge button, force-push, secret exposure) and workflow decoupling (banned tokens) remain.
- **AC-1.1 verifier prompt** trimmed — 11 clauses down to 11 (reorganized): drop the closed-vocabulary check (was clause 6); drop steerability invariant double-language; keep portability banned-token grep; keep prompt-engineering hygiene clause as final check.
- **AC-3.2** simplified — criteria-checker rich-hint convention is documented in natural English; no vocabulary list required; merge-button ban preserved.
- **AC-3.3** simplified — /do SKILL.md documents (a) LLM-judgment parsing of free-form hints, (b) action-aware fix-cap rule, (c) merge-button prohibition. No closed vocabulary, no dispatch table, no parsing rules. AC verifier prompt flags MEDIUM if these over-engineered artifacts remain in /do SKILL.md.
- **AC-3.4** simplified — execution-modes state the action-aware fix-cap principle; enumerating specific action labels is not required (and over-enumeration is a soft anti-signal).

**Unchanged (load-bearing, kept):**
- INV-G8 (no `gh pr merge` / `merge-pr` in plugin) — real safety boundary.
- `verify.timeout:` schema (AC-2.4) + parser semantics (AC-2.5) — genuinely new mechanism.
- Action-aware fix-cap (the rule, not the enumeration) — addresses real failure mode (lifecycle waits exhausting fix budget).
- Agent hard prohibitions, steerability, workflow decoupling — all invariants, all preserved.
- INV-G3, INV-G4, INV-G5, INV-G6, INV-G7 — unchanged.
- D2 (BABYSIT_MODE.md + /define schema), D4 (/auto), D5 (drive removal), D6 (plugin metadata + READMEs), D7 (sync-tools) — unchanged.

**/do scope hint**: D1 (agent body — drop closed-vocabulary section + action-mapping table; keep hard prohibitions and steerability) and D3 (criteria-checker — drop closed-vocabulary; /do SKILL.md — drop dispatch table and parsing rules, keep action-aware fix-cap principle and merge-button prohibition; execution-modes — simplify to principle, not enumeration). Other deliverables unaffected. Recommend `--scope D1,D3`.

### Amendment 5 (post-/done, from /do) — Drop the "rich hint" documentation layer; a FAIL message IS the hint

**Trigger**: User — "Rich hint section is redundant. Trust the agent knows what to return and caller is smart…" After Amendment 4 already stripped the closed vocabulary, dispatch table, and parsing rules, what remains is documentation of "the verifier may return hint text in FAIL bodies" — which is just what FAIL messages have always been. The standard PASS/FAIL output format already has a fix-hint field; a separate "rich hint convention" section repeats this without adding mechanism. Trust the agent to write useful failure messages; trust the caller to read them.

**Rationale**: per prompt-engineering principles — don't document what the model does anyway. /verify already says "Pass through file:line, expected vs actual, fix hints" in its Actionable feedback principle. criteria-checker's Output Format already names a Fix hint field. github-pr-lifecycle's FAIL output example already shows `Hint: <natural-language detail>`. Three separate "rich hint" sections are the same idea three times — documentation, not mechanism.

**Changes**:

- **§1 Mental Model** "Verifier hints" bullet — compressed to: "Verifier FAIL bodies are just FAIL messages. criteria-checker returns PASS or FAIL with actionable detail; /do reads with LLM judgment and acts. No 'hint protocol' layer — a FAIL message has always been free-form text and /do has always been an LLM."
- **AC-3.1** (/verify rich-hint passthrough documentation) — dropped entirely. /verify's existing Actionable-feedback principle already covers passthrough; a separate section is redundant.
- **AC-3.2** (criteria-checker rich-hint convention) — softened to: criteria-checker documents its standard Output Format (Status, Evidence, Fix hint on FAIL). Drop "rich-hint convention" framing. AC verifier prompt flags MEDIUM if a separate "rich-hint convention" subsection is still present alongside the standard Output Format.
- **PG-7** (verifier hints are natural English) — dropped entirely. This was documenting what /do does anyway as an LLM. INV-G8 (merge-button prohibition) carries the only load-bearing invariant from PG-7.

**Unchanged (load-bearing, kept):**
- INV-G8 (no `gh pr merge` / `merge-pr` in plugin) — real safety boundary. INV-G8 body adjusted to drop PG-7 cross-reference (writers use the canonical phrasing directly).
- `verify.timeout:` schema (AC-2.4) + parser semantics (AC-2.5) — genuinely new mechanism.
- Action-aware fix-cap (AC-3.3, AC-3.4, AC-3.5) — addresses real failure mode (lifecycle waits exhausting fix budget). AC-3.3 / AC-3.4 unchanged; their action-aware-fix-cap language was the real content.
- Agent hard prohibitions, steerability, workflow decoupling — all invariants, all preserved.
- D2, D4, D5, D6, D7 — unchanged.

**/do scope hint**: D1 + D3 only.
- D1 (agent): drop the "### Hint body" subsection from `claude-plugins/manifest-dev/agents/github-pr-lifecycle.md` — the FAIL output format example with `Hint: <natural-language detail>` already conveys it.
- D3 (verify SKILL + criteria-checker): delete "## Rich Hint Passthrough" section from `claude-plugins/manifest-dev/skills/verify/SKILL.md`; delete "### Rich-hint convention (FAIL bodies)" subsection from `claude-plugins/manifest-dev/agents/criteria-checker.md` (keep the standard PASS/FAIL Output Format).
- /do SKILL.md and execution-modes unchanged in this amendment (Amendment 4 already simplified them).

Recommend `--scope D1,D3`.
