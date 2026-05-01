# Definition: Progressive-disclosure refactor of /define skill

## 1. Intent & Context

- **Goal:** Tighten `claude-plugins/manifest-dev/skills/define/SKILL.md` so it dispatches to reference files instead of summarizing them. Multi-repo content, the conditional branches inside Pre-flight, and the redundant Delegation Map move out. Main file holds only universal happy-path guidance.
- **Mental Model:** SKILL.md is `main()`; references are imported modules. A reader of SKILL.md should not load context for flagged or conditional behavior unless its trigger fires. The user's framing: "It's like code, you know."
- **Mode:** thorough
- **Interview:** autonomous (switched mid-run; remaining decisions auto-resolved)
- **Medium:** local

## 2. Approach

- **Architecture:**
  - SKILL.md becomes a thin dispatcher. Three categories of content:
    - **Universal happy-path** stays inline (Goal, Prerequisites, Input, Pre-flight detection trigger, Branch-Diff Seeding trigger, Domain Guidance, Principles, Coverage Goals, Disciplines, Convergence, Approach Section guidance, Manifest Schema (single-repo only), ID Scheme, Verification Loop, Summary, Medium Routing, Complete).
    - **Triggered routes** are one-liners: `if <trigger>, see references/X.md`. No body, no summary.
    - **Multi-repo and Session-Default Detection content** moves to references — these are the conditional/flagged paths.
  - References absorb the moved content as canonical homes:
    - `references/MULTI_REPO.md` gains a "Manifest schema additions" section enumerating `Repos:`, `Branch:`, `repo:` fields with the documentation moved from SKILL.md.
    - `references/AMENDMENT_MODE.md` gains a canonical "Session-Default Detection" section (the branches Related/Truly unrelated/Unreadable + announcement formats).
  - `deferred-auto` stays a verify method enum value in SKILL.md's schema (it's a general user-triggered mechanism, used for single-repo and multi-repo) with a single short inline description; cross-repo-specific semantics (prefix injection, /escalate routing, --deferred semantics) stay in MULTI_REPO.md §e.

- **Execution Order:**
  - D1 (move multi-repo schema delta into MULTI_REPO.md) → D2 (trim SKILL.md schema) → D3 (collapse Multi-Repo Scope section in SKILL.md) → D4 (move Pre-flight branches to AMENDMENT_MODE.md as Session-Default Detection) → D5 (replace Pre-flight branches in SKILL.md with route) → D6 (remove Delegation Map) → D7 (version bump) → D8 (verify behavioral preservation via reviewer agents).
  - Rationale: write the destinations before pruning the sources. Prevents content disappearing if a step is interrupted.

- **Risk Areas:**
  - [R-1] Behavioral regression on the happy path (single-repo, fresh /define, no flags). | Detect: change-intent-reviewer compares old vs new SKILL.md flow.
  - [R-2] External cross-references break. `done/SKILL.md`, `CANVAS_MODE.md`, `AMENDMENT_MODE.md` mention "Session-Default Amendment". | Detect: bash sweep across all referenced files.
  - [R-3] Duplication-in-place — content lands in references AND stays in SKILL.md. | Detect: bash grep ensures specific moved-strings absent from SKILL.md.
  - [R-4] MULTI_REPO.md / AMENDMENT_MODE.md become dumping grounds. | Detect: prompt-reviewer reads both for coherence.
  - [R-5] AMENDMENT_MODE.md's existing `### 3. Session-Default` subsection contradicts or duplicates the new Session-Default Detection section. | Detect: criteria-checker reads both.
  - [R-6] Some `references/*.md` route in the new SKILL.md points at a section that doesn't exist (typo, rename). | Detect: bash sweep over every route.

- **Trade-offs:**
  - [T-1] Brevity in SKILL.md vs discoverability of conditional flows → Prefer brevity. Each route names its trigger explicitly.
  - [T-2] Aggressive renaming for cleanliness vs preserved external references → Prefer preserved references. Section renames serve cross-reference stability, not aesthetics.
  - [T-3] Single-repo deferred-auto fully documented in SKILL.md vs concise schema → Concise schema with one-line description; behavior detail in MULTI_REPO.md §e.

## 3. Global Invariants

- [INV-G1] Every directive in SKILL.md that asks the agent to *load* a file under `references/` (or `tasks/`, or another skill's references) is gated by an explicit triggering condition stated at the route — flag value, detection result, mode resolution, domain match, or runtime check. Universal happy-path inline content is exempt; this rule applies to file-loading directives only. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/SKILL.md. For every directive that tells the agent to read a file (anything matching `references/*.md`, `tasks/*.md`, `../do/references/*.md`, `references/messaging/*.md`, `references/interview-modes/*.md`), confirm the directive is gated by an explicit triggering condition stated at the route (a flag value, detection result, mode resolution, domain match, or a runtime check). The flag table itself counts as a trigger surface — entries there are gated by the flag's presence. PASS if every file-loading directive is gated. FAIL if any directive loads a reference unconditionally on every /define run, with the offending lines cited."
  ```

- [INV-G2] SKILL.md contains no summary-of-reference content. No section paraphrases or restates content that exists in a reference file under `references/`. The single allowed mention is the one-line route. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/SKILL.md and every file under /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/references/. For each reference file, identify whether SKILL.md contains content that paraphrases, summarizes, or restates material from that reference. The only acceptable mention is a one-line route stating the trigger and pointing at the file. Cite specific overlapping content if any is found. PASS if no overlap beyond one-line routes. FAIL otherwise."
  ```

- [INV-G3] Multi-repo manifest schema fields (`Repos:` in Intent, `Branch:` in Intent, `**Repo:**` on deliverables) and the cross-repo deferred-auto semantics (cross-repo prefix injection, `/escalate` routing for "Deferred-Auto Pending", `/verify --deferred` flag interactions) live in MULTI_REPO.md, not SKILL.md. | Verify:
  ```yaml
  verify:
    method: bash
    command: "set -e; F=/home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/SKILL.md; ! grep -E '^\\s*-\\s+\\*\\*Repos:\\*\\*' \"$F\" && ! grep -E '^\\s*-\\s+\\*\\*Branch:\\*\\*' \"$F\" && ! grep -E '^\\*\\*Repo:\\*\\*' \"$F\" && ! grep -F 'See Multi-Repo Scope above' \"$F\" && ! grep -F 'cross-repo prefix injection' \"$F\" && ! grep -F 'Available repos:' \"$F\" && ! grep -F 'deliverable-scope-independent' \"$F\""
  ```

- [INV-G4] Every `references/<file>.md` route mentioned in the new SKILL.md resolves to a real file, and the canonical "Session-Default Detection" section exists in `AMENDMENT_MODE.md`. External cross-references in `done/SKILL.md`, `CANVAS_MODE.md`, and `AMENDMENT_MODE.md` itself still mention "Session-Default" so they grep-resolve. | Verify:
  ```yaml
  verify:
    method: bash
    command: "set -e; D=/home/user/manifest-dev/claude-plugins/manifest-dev/skills/define; F=$D/SKILL.md; AM=$D/references/AMENDMENT_MODE.md; grep -F 'Session-Default Detection' \"$AM\" >/dev/null; grep -oE 'references/[A-Za-z_/-]+\\.md|tasks/[A-Za-z_/-]+\\.md' \"$F\" | sort -u | while read p; do test -f \"$D/$p\" || { echo \"missing route target: $p\"; exit 1; }; done; for f in /home/user/manifest-dev/claude-plugins/manifest-dev/skills/done/SKILL.md $D/references/CANVAS_MODE.md $D/references/AMENDMENT_MODE.md; do grep -F 'Session-Default' \"$f\" >/dev/null || { echo \"reference missing in $f\"; exit 1; }; done"
  ```

- [INV-G5] /define behavior is unchanged for the happy path (single-repo, fresh /define, no flags). Every step from the prior SKILL.md is reachable and produces equivalent outcome. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Compare /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/SKILL.md against the same file at origin/main (use `git -C /home/user/manifest-dev show origin/main:claude-plugins/manifest-dev/skills/define/SKILL.md`). Stated intent: SKILL.md becomes a dispatcher; references absorb conditional/flagged content. Verify the happy-path /define run (single-repo, fresh, no flags) is unchanged in observable behavior — every step in the old flow (input parsing, pre-flight detection, branch-diff seeding evaluation, domain guidance, interview, manifest write, verification loop, summary, complete) is still reachable in the new SKILL.md. Flag any silently dropped step. Severity LOW or above blocks. Read both files end-to-end."
  ```

- [INV-G6] Files under `claude-plugins/manifest-dev/skills/define/` are the edit source; `.claude/skills/define/` is hardlinked per CLAUDE.md and propagates. | Verify:
  ```yaml
  verify:
    method: bash
    command: "set -e; for f in SKILL.md references/MULTI_REPO.md references/AMENDMENT_MODE.md; do ino_a=$(stat -c '%i' \"/home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/$f\"); ino_b=$(stat -c '%i' \"/home/user/manifest-dev/.claude/skills/define/$f\" 2>/dev/null || echo missing); [ \"$ino_a\" = \"$ino_b\" ] || { echo \"$f hardlink broken: $ino_a vs $ino_b\"; exit 1; }; done"
  ```

- [INV-G7] (PROMPTING — folder architecture) `define` skill is a directory with SKILL.md + companions. | Verify:
  ```yaml
  verify:
    method: bash
    command: "set -e; D=/home/user/manifest-dev/claude-plugins/manifest-dev/skills/define; [ -d \"$D\" ] && [ -f \"$D/SKILL.md\" ] && [ -d \"$D/references\" ] && [ -d \"$D/tasks\" ]"
  ```

- [INV-G8] (PROMPTING quality gate) Intent analysis — change-intent-reviewer flags no LOW+ on the diff. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Review the diff on the current branch (git -C /home/user/manifest-dev diff origin/main..HEAD -- claude-plugins/manifest-dev/skills/define/ claude-plugins/manifest-dev/.claude-plugin/plugin.json). Stated intent: progressive-disclosure refactor of the /define skill. SKILL.md becomes a dispatcher; multi-repo schema delta moves to MULTI_REPO.md; Session-Default Detection branches move to AMENDMENT_MODE.md; Delegation Map removed; deferred-auto remains a general schema method with cross-repo specifics in MULTI_REPO.md. Adversarially attack the diff for behavioral divergence between intent and result. Report findings by severity. PASS only if no LOW or higher issue."
  ```

- [INV-G9] (PROMPTING quality gate) Prompt quality — prompt-reviewer flags no MEDIUM+ on the modified prompt files. The prompt-reviewer applies the full PROMPTING.md gate set as its umbrella check (clarity, no conflicts, structure, information density, no anti-patterns, invocation fit, domain context, complexity fit, edge case coverage, model-prompt fit, guardrail calibration, output calibration, emotional tone, progressive disclosure). | Verify:
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review the prompt files modified by this refactor: /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/SKILL.md, /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/references/MULTI_REPO.md, /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/references/AMENDMENT_MODE.md. Apply prompt-engineering principles end-to-end. PASS only if no MEDIUM or higher issue."
  ```

## 4. Process Guidance

- [PG-1] High-signal changes only. Every line removed from SKILL.md or moved to a reference must address one of: (a) duplication of reference content, (b) flag-/condition-gated behavior with no inline trigger justifying inline residence, or (c) redundant meta-summary. Don't over-extract; don't restructure beyond what the manifest specifies.
- [PG-2] Edit `claude-plugins/manifest-dev/skills/define/` files directly; the `.claude/skills/define/` hardlink propagates per CLAUDE.md.
- [PG-3] Calibrate emotional tone in moved/added prose. Direct, calm, "trusted advisor" register; no urgency, no praise, no pressure framing. (PROMPTING.md default.)
- [PG-4] When moving a block of content, write the destination first, then prune the source. Avoid the failure mode where a step is interrupted and the content vanishes.
- [PG-5] Plugin-version semantic: this refactor is a minor bump (0.96.3 → 0.97.0). Structural changes to skill files but no observable-behavior changes.

## 5. Known Assumptions

- [ASM-1] Single-repo `deferred-auto` is rare enough that a one-line description in SKILL.md's verify-method enum suffices, with cross-repo behavior detail in MULTI_REPO.md §e. Impact if wrong: users with single-repo deferred-auto cases need to read MULTI_REPO.md for behavior — mild friction, no breakage.
- [ASM-2] Plugin version bump is minor: `0.96.3` → `0.97.0`. Refactor with structural moves but no observable-behavior changes. Impact if wrong: semver expectations drift; correctable in follow-up.
- [ASM-3] No README updates needed (no components added, removed, or renamed; this is internal restructure of an existing skill). Impact if wrong: README sections drift slightly; correctable.
- [ASM-4] `Branch-Diff Seeding` (~10 lines) and `Approach Section` (~17 lines) stay inline despite containing conditional logic, because the trigger evaluation happens on every /define run and the bodies are small. INV-G1 applies to file-loading directives, not all conditional logic. Impact if wrong: SKILL.md retains some conditional content; can be moved later.
- [ASM-5] PROMPTING quality gates "Gotchas section" and "Description as trigger" are skipped for this refactor: current SKILL.md has no Gotchas section and adding one is out of scope per user direction; description is unchanged. Impact if wrong: skipped gates miss issues; user reviews manifest.
- [ASM-6] The deferred-auto enum description in SKILL.md's schema uses the form "user-triggered; runs only via /verify --deferred" (or semantically equivalent — same contract referenced by `done/SKILL.md:33`). Impact if wrong: downstream consumers parsing the enum see different wording; semantic equivalence is the contract.
- [ASM-7] The Multi-Repo Scope section in SKILL.md becomes a single sentence of the form: "If the task spans multiple repositories, see `references/MULTI_REPO.md`." (or semantically equivalent). The trigger phrasing names the multi-repo signal directly. Impact if wrong: route reads less clear; correctable.

## 6. Deliverables

### Deliverable 1: SKILL.md — Multi-Repo Scope reduced to one-line trigger

**Acceptance Criteria:**

- [AC-1.1] The `## Multi-Repo Scope` section in SKILL.md exists as a heading followed by a single short paragraph (≤ 3 lines of prose, blank lines excluded) stating the trigger and routing to `references/MULTI_REPO.md`. No schema fields, no deferred-auto explanation, no detection mechanics, no examples. | Verify:
  ```yaml
  verify:
    method: bash
    command: "set -e; F=/home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/SKILL.md; python3 -c \"import re,sys; t=open('$F').read(); m=re.search(r'^## Multi-Repo Scope\\n(.*?)(?=^## )', t, re.M|re.S); assert m, 'section missing'; body=m.group(1); lines=[ln for ln in body.splitlines() if ln.strip()]; assert len(lines) <= 3, f'expected <=3 prose lines, got {len(lines)}: {lines}'; assert 'MULTI_REPO.md' in body, 'route target missing'; assert 'multiple' in body.lower() or 'multi-repo' in body.lower() or 'repos' in body.lower(), 'trigger condition missing'\""
  ```

### Deliverable 2: SKILL.md — Manifest schema is single-repo-only

**Acceptance Criteria:**

- [AC-2.1] The Manifest Schema section's Intent template no longer contains `Repos:` or `Branch:` fields. The Deliverable template no longer contains a `**Repo:**` field. No "*See Multi-Repo Scope above*" pointer notes. | Verify:
  ```yaml
  verify:
    method: bash
    command: "set -e; F=/home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/SKILL.md; ! grep -E '^- \\*\\*Repos:\\*\\*' \"$F\" && ! grep -E '^- \\*\\*Branch:\\*\\*' \"$F\" && ! grep -E '^\\*\\*Repo:\\*\\*' \"$F\" && ! grep -F 'See Multi-Repo Scope above' \"$F\""
  ```

- [AC-2.2] `deferred-auto` remains listed as a verify method enum value in the schema, with a single inline description (one short sentence or fragment) characterizing it as user-triggered and run via `/verify --deferred`. No paragraphs about cross-repo behavior, prefix injection, or escalation in SKILL.md. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/SKILL.md. Locate the Manifest Schema section. Confirm: (a) `deferred-auto` appears as one of the values in the verify method enum; (b) there is a single inline description (one short sentence or fragment) characterizing it as user-triggered / runs via `/verify --deferred`; (c) no paragraph-length explanation of cross-repo behavior, no mention of prefix injection, no `/escalate` routing details, no `--deferred` flag-interaction tables. PASS only if all three hold."
  ```

### Deliverable 3: MULTI_REPO.md — hosts the multi-repo schema delta

**Acceptance Criteria:**

- [AC-3.1] MULTI_REPO.md contains a clearly identified section that documents the multi-repo-only schema fields: `Repos:` in Intent, `Branch:` in Intent, `**Repo:**` on deliverables. The documentation moved from SKILL.md (semantics, optionality, format) is present here. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/references/MULTI_REPO.md. Confirm a section documents the multi-repo manifest schema fields `Repos:`, `Branch:`, and `**Repo:**` (on deliverables) — including their position in the manifest, format/syntax, optionality, and semantics. The content moved from SKILL.md must be present in MULTI_REPO.md. PASS only if all three fields are documented."
  ```

- [AC-3.2] MULTI_REPO.md §e (or its successor section) remains the canonical home for cross-repo `deferred-auto` behavior: cross-repo prefix injection, `/escalate` "Deferred-Auto Pending" routing, `/verify --deferred` flag interactions. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/references/MULTI_REPO.md. Confirm a section explains: (a) cross-repo prefix injection (`Available repos: ...`) prepended to verifier prompts; (b) routing to `/escalate` with type 'Deferred-Auto Pending' instead of `/done` while uncovered; (c) the `/verify --deferred` flag's behavior including its interactions with `--scope` and `--final`. PASS only if all three are explained."
  ```

### Deliverable 4: SKILL.md — Pre-flight is detection trigger + route only

**Acceptance Criteria:**

- [AC-4.1] The Pre-flight section in SKILL.md keeps: detection signals (in-session completion line, conversation reference), the skip rule for explicit `--amend`, and a one-line route to AMENDMENT_MODE.md's Session-Default Detection. The "Prior Manifest Found" subsection (Related/Truly unrelated/Unreadable branches and announcement formats) is removed from SKILL.md. | Verify:
  ```yaml
  verify:
    method: bash
    command: "set -e; F=/home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/SKILL.md; ! grep -F 'Related (default)' \"$F\" && ! grep -F 'Truly unrelated' \"$F\" && ! grep -F 'Detected prior manifest in session' \"$F\" && ! grep -F 'Prior manifest unreadable' \"$F\" && grep -F 'Session-Default Detection' \"$F\" >/dev/null"
  ```

### Deliverable 5: AMENDMENT_MODE.md — hosts Session-Default Detection canonically

**Acceptance Criteria:**

- [AC-5.1] AMENDMENT_MODE.md contains a section whose heading includes the exact phrase "Session-Default Detection" (so external grep-references resolve). The section contains the branches Related → amend; Truly unrelated → fresh; Prior manifest unreadable → fresh, plus the announcement formats moved from SKILL.md. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/references/AMENDMENT_MODE.md. Confirm: (a) a heading contains the exact phrase 'Session-Default Detection'; (b) the section under that heading documents three branches — 'Related (default)' (amend, with announcement format), 'Truly unrelated' (fresh, with announcement format), and 'Prior manifest unreadable' (fresh, with announcement format); (c) the announcement strings moved from SKILL.md are present (e.g., 'Detected prior manifest in session', 'Found prior manifest', and the unreadable fallback). PASS only if all three hold."
  ```

- [AC-5.2] All external mentions of "Session-Default" still appear in `done/SKILL.md`, `CANVAS_MODE.md`, and `AMENDMENT_MODE.md` itself. (Mentions are not deleted; they continue to point at a section that now canonically lives in AMENDMENT_MODE.md.) | Verify:
  ```yaml
  verify:
    method: bash
    command: "set -e; for f in /home/user/manifest-dev/claude-plugins/manifest-dev/skills/done/SKILL.md /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/references/AMENDMENT_MODE.md; do grep -F 'Session-Default' \"$f\" >/dev/null || { echo \"reference missing in $f\"; exit 1; }; done"
  ```

- [AC-5.3] AMENDMENT_MODE.md's existing `### 3. Session-Default` subsection (under "Three Contexts") is reconciled with the new Session-Default Detection section. They do not duplicate detection logic; the existing subsection refers to the detection section rather than restating it; no contradictions exist between them. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/references/AMENDMENT_MODE.md. Two related sections should exist after the refactor: (a) 'Session-Default Detection' (the detection trigger + branches Related/Truly unrelated/Unreadable + announcement formats); (b) the existing '### 3. Session-Default' subsection under 'Three Contexts' (which describes how amendment behavior runs once detection has decided to amend). Confirm: the two sections do not duplicate the detection logic; the '### 3. Session-Default' subsection now refers to the detection section rather than restating it; no contradictions exist between them. PASS only if both hold."
  ```

### Deliverable 6: SKILL.md — Delegation Map removed

**Acceptance Criteria:**

- [AC-6.1] SKILL.md no longer contains a "Delegation Map" section, heading, or table. | Verify:
  ```yaml
  verify:
    method: bash
    command: "F=/home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/SKILL.md; ! grep -F 'Delegation Map' \"$F\""
  ```

### Deliverable 7: Plugin version bumped

**Acceptance Criteria:**

- [AC-7.1] `claude-plugins/manifest-dev/.claude-plugin/plugin.json` version is `0.97.0` (minor bump from `0.96.3`). | Verify:
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; v=json.load(open('/home/user/manifest-dev/claude-plugins/manifest-dev/.claude-plugin/plugin.json'))['version']; assert v == '0.97.0', f'expected 0.97.0 got {v}'\""
  ```

### Deliverable 8: Behavioral preservation verified

**Acceptance Criteria:**

- [AC-8.1] The happy-path /define flow (single-repo, fresh, no flags) reaches every step it does today: input parsing, pre-flight detection check, branch-diff seeding evaluation, domain guidance lookup, principles + coverage goals + disciplines applied, interview, manifest write, verification loop, summary for approval, complete. No step is silently skipped after the refactor. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Read /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/SKILL.md (current). Read the same file at origin/main via `git -C /home/user/manifest-dev show origin/main:claude-plugins/manifest-dev/skills/define/SKILL.md`. Walk the happy-path /define flow (single-repo, fresh /define, no flags) on both versions. Confirm every step in the old flow is reachable in the new SKILL.md. Specifically check: input parsing, pre-flight detection check, branch-diff seeding trigger evaluation, domain guidance lookup, principles + coverage goals + disciplines, interview, manifest schema (now single-repo only), verification loop dispatch, summary for approval, complete. Flag any silently dropped step. PASS only if every step is preserved."
  ```

- [AC-8.2] The multi-repo path is functionally equivalent post-refactor. A reader who follows SKILL.md's one-line multi-repo trigger and reads MULTI_REPO.md gets the same schema (`Repos:`, `Branch:`, `repo:`), the same `deferred-auto` cross-repo semantics (prefix injection, /escalate routing, --deferred flag), and the same end-state manifest as before. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Compare two reading paths for a multi-repo /define run. (1) Old: read /home/user/manifest-dev/claude-plugins/manifest-dev/skills/define/SKILL.md at origin/main (`git -C /home/user/manifest-dev show origin/main:claude-plugins/manifest-dev/skills/define/SKILL.md`) plus MULTI_REPO.md at origin/main. (2) New: read the current SKILL.md plus the current MULTI_REPO.md. Confirm both reading paths yield the same outcome for a multi-repo task: same manifest schema (Repos:, Branch:, repo: fields), same deferred-auto cross-repo behavior contract (prefix injection, /escalate 'Deferred-Auto Pending' routing, --deferred flag interactions including --scope and --final). Flag anything that differs in the runtime contract. PASS only if behaviorally equivalent."
  ```

### Deliverable 9: Measurable progressive-disclosure outcome

**Acceptance Criteria:**

- [AC-9.1] SKILL.md is materially shorter than at origin/main: at least 30 lines removed net (the Multi-Repo Scope section plus Pre-flight branches plus Delegation Map plus schema multi-repo additions all leave SKILL.md). | Verify:
  ```yaml
  verify:
    method: bash
    command: "set -e; cd /home/user/manifest-dev; OLD=$(git show origin/main:claude-plugins/manifest-dev/skills/define/SKILL.md | wc -l); NEW=$(wc -l < claude-plugins/manifest-dev/skills/define/SKILL.md); test $((OLD - NEW)) -ge 30 || { echo \"net removal $((OLD - NEW)) < 30 (old=$OLD new=$NEW)\"; exit 1; }"
  ```

- [AC-9.2] Combined size of MULTI_REPO.md + AMENDMENT_MODE.md grows by less than the size SKILL.md shrank by 1.5× (i.e., references absorb moved content with little overhead, not duplicate it). | Verify:
  ```yaml
  verify:
    method: bash
    command: "set -e; cd /home/user/manifest-dev; B=claude-plugins/manifest-dev/skills/define; OLD_S=$(git show origin/main:$B/SKILL.md | wc -l); NEW_S=$(wc -l < $B/SKILL.md); OLD_M=$(git show origin/main:$B/references/MULTI_REPO.md | wc -l); NEW_M=$(wc -l < $B/references/MULTI_REPO.md); OLD_A=$(git show origin/main:$B/references/AMENDMENT_MODE.md | wc -l); NEW_A=$(wc -l < $B/references/AMENDMENT_MODE.md); SHRANK=$((OLD_S - NEW_S)); GREW=$((NEW_M + NEW_A - OLD_M - OLD_A)); test $GREW -le $((SHRANK * 3 / 2)) || { echo \"references grew $GREW vs SKILL.md shrank $SHRANK (1.5x cap = $((SHRANK * 3 / 2)))\"; exit 1; }"
  ```
