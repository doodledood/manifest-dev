# Definition: Add /check-in fallback scheduler to drive plugin

## 1. Intent & Context

- **Goal:** Add a `/check-in` skill to the `manifest-dev-experimental` (drive) plugin that serves as an automatic fallback when `/loop` is not available in the environment. Behaviour: sleep for the configured interval, invoke the tick command, detect terminal markers, and re-loop until terminal — effectively a blocking, session-local substitute for `/loop`'s background cron.
- **Mental Model:**
  - `/loop` is an external, cron-like scheduler that fires `/drive-tick` on an interval without blocking. It is required by `/drive` today and `/drive` errors out in pre-flight when it is missing. Today's invocation is verbatim (drive/SKILL.md line 107): `Invoke the /loop skill with: "<interval> /drive-tick --run-id <run-id> --mode <mode> --platform <platform> --sink <sink> --log <log-path> --max-ticks <N> [--manifest <manifest-path>] [--pr <pr-number>]"`.
  - `/check-in` is a **blocking, same-session substitute**. Interface: `<interval> <log-path> <command>` — one extra positional arg (`<log-path>`) compared to `/loop` because `/check-in` reads terminal state from the **log file**, not from the Skill-tool response. Drive-tick writes its `## Tick N — …` markers to the log file per its Output Protocol (verbatim strings verified in §3 INV-G8); the Skill-tool response is not the contract channel. After each invocation `/check-in` reads the log file, finds the most recent `## Tick N — …` header, and classifies: `Terminal:` / `Error:` / `BUDGET EXHAUSTED` → exit; `Continuing` / `Skipped (lock held)` → re-loop; anything else or no entry at all → fail-loud exit.
  - `/drive` pre-flight learns a tri-branch: `/loop` available → use it (preferred, preserves existing semantics); only `/check-in` available → fall back (warn user that the session will block); neither available → error with actionable message.
  - `/drive-tick` itself is **unchanged** — it already writes the markers `/check-in` reads from the log. The scheduler swap is invisible to the tick.
- **Mode:** thorough
- **Interview:** autonomous
- **Medium:** local

## 2. Approach

- **Architecture:**
  - New skill directory: `claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md`. No references/, no assets/ — single-file skill for v0 simplicity (PROMPTING default: match architecture to skill type; this is a thin Business Process orchestrator).
  - `/check-in` internal flow (loop inside one Skill invocation):
    1. Parse `<interval> <log-path> <command>`; validate interval range (`15m`–`24h`); error on malformed input with the same wording `/drive` uses.
    2. Convert interval to seconds.
    3. Loop:
       - Sleep the interval. Compute chunk count upfront: `chunks = ceil(interval_seconds / 540)` (where 540s = 9 minutes, leaving headroom under the Bash tool's 600s cap). Issue `chunks - 1` sequential `sleep 540` calls plus one final `sleep <remainder>` where `remainder = interval_seconds - (chunks - 1) * 540` (always in `1..540` — ceil guarantees non-zero, avoiding 9-minute shortfalls on exact-multiple-of-540 intervals that naive `% 540` would produce). No in-loop arithmetic — counter is known at entry. Cumulative semantics (sum of chunks), not wall-clock-target.
       - Invoke the `<command>` verbatim via the Skill tool — `<command>` is passed unparsed; no shell expansion, no re-quoting.
       - If the Skill-tool invocation itself fails (tool error, timeout, crash): fail-loud, exit with an explanatory message. Do NOT retry.
       - Read the log file at `<log-path>`. Find the last `## Tick N — …` or `## BUDGET EXHAUSTED` header.
       - Classify: `Terminal:` / `Error:` / `BUDGET EXHAUSTED` → exit; `Continuing` / `Skipped (lock held)` → re-loop; anything else or no header found → fail-loud exit (unexpected drive-tick output).
  - `/drive` edits (same file `claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md`):
    - §Pre-flight: replace the single `/loop` availability check with a tri-branch check.
    - §/loop Kickoff → rename to §Scheduler Kickoff; parameterise invocation on chosen scheduler name.
    - Run summary: add the scheduler-used line.
    - §Gotchas: add a line describing the session-blocking nature of `/check-in` fallback.
  - README edits: `claude-plugins/manifest-dev-experimental/README.md` (What it ships, Dependencies, Gotchas). Plugin version bump in `plugin.json` (0.4.0 → 0.5.0, add `check-in` / `fallback` keywords).

- **Execution Order:**
  - D1 (`/check-in` skill) → D2 (`/drive` integration) → D3 (README + plugin.json updates).
  - Rationale: the skill must exist before `/drive` can reference it in pre-flight; README reflects the final state once both are in place.

- **Risk Areas:**
  - [R-1] Infinite loop if drive-tick's marker format changes | Detect: /check-in reads responses that contain none of the recognized markers → it halts and reports (fail-loud), instead of silently looping.
  - [R-2] Bash tool's long-sleep restriction (single-call cap ~10m, "long leading sleep" blocked) | Detect: upfront chunk-count formula (AC-1.6) ensures each sleep call is ≤540s, well under the 600s cap. End-to-end integration test (invoking a stubbed drive-tick over a full 15m sleep) is explicitly scoped out for v0 — cost/time disproportionate to the bounded risk of a well-specified chunk formula. If the formula itself is wrong, INV-G1 (prompt-reviewer) should catch it; if chunking still fails at runtime, the Bash call times out with an explicit error rather than silently hanging.
  - [R-3] Pre-flight regression — existing `/drive` behaviour when `/loop` IS available must be byte-identical | Detect: INV-G4 compares pre/post on the "/loop available" branch.
  - [R-4] Session-end fragility — closing the Claude session kills /check-in mid-sleep (unlike /loop which delegates to host cron) | Detect: documented in gotchas; no automated detection. Acknowledged as intrinsic to fallback mode.

- **Trade-offs:**
  - [T-1] Interface fidelity to /loop vs. bespoke interface → Prefer fidelity. /drive builds the invocation string once; swap skill name only.
  - [T-2] Blocking session vs. backgrounded → Prefer blocking. Honest about fallback's weaker guarantees; user who wants cron installs /loop.
  - [T-3] Auto-fallback vs. user-selectable flag → Prefer auto. User asked for automatic fallback explicitly.
  - [T-4] Fail-loud on unknown marker vs. keep looping → Prefer fail-loud. Silent infinite loops waste tokens; halt and surface.

## 3. Global Invariants

- [INV-G1] `/check-in` SKILL.md passes the `prompt-reviewer` agent with no MEDIUM-or-higher findings. This subsumes PROMPTING.md quality gates: Clarity, No conflicts, Structure, Information density, No anti-patterns, Invocation fit, Domain context, Complexity fit, Edge case coverage, Model-prompt fit, Guardrail calibration, Output calibration, Emotional tone — all covered by prompt-reviewer's default rubric. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md against prompt-engineering principles. Report issues with severity. Pass = no MEDIUM+ issues."
  ```

- [INV-G2] The full change set (check-in SKILL.md + drive/SKILL.md edits + README + plugin.json) passes the `change-intent-reviewer` agent with no LOW-or-higher intent mismatches. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Review the git diff on branch claude/add-checkin-fallback-*. Intent: add a /check-in skill to manifest-dev-experimental that serves as an automatic fallback scheduler when /loop is unavailable. /check-in sleeps the configured interval, invokes the command, detects drive-tick terminal markers, and either exits or re-loops. /drive pre-flight learns a tri-branch; /loop path must be byte-identical to today when /loop is available. Pass = no LOW+ findings."
  ```

- [INV-G3] `/check-in`'s description field follows the What + When + Triggers pattern (PROMPTING.md skill gate: "Description as trigger"). | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md frontmatter. Verify the description field is: (a) a trigger specification not a human-readable summary, (b) explains WHAT the skill does, WHEN to invoke, and includes trigger terms. Pass = all three present; Fail = any missing."
  ```

- [INV-G4] `/drive`'s behaviour when `/loop` IS available remains byte-equivalent to today. The tri-branch pre-flight only DIVERGES from today when /loop is unavailable. | Verify: codebase.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md §Pre-flight and §Scheduler Kickoff (was §/loop Kickoff). Confirm: (1) when /loop is available and /check-in is also available, /drive uses /loop; (2) the invocation string for /loop is identical in structure to today's; (3) the run summary's scheduler line is additive (doesn't alter existing fields). Fail if any /loop-path behaviour changed."
  ```

- [INV-G5] `/check-in`'s prompt is ≤450 instruction words of SKILL.md body (excluding frontmatter and section headers), keeping context-rot surface minimal for long-running loops. Threshold set realistically given AC-1.1 through AC-1.10 require specific content (arg spec, chunk formula, five verbatim marker anchors, fail-loud semantics for four distinct failure modes, last-seen-header tracking, first-iteration grace, gotchas). 150 was the original threshold set autonomously during /define; self-amended during /do after discovering the lower bound required more prose than 150 words permit. | Verify: bash.
  ```yaml
  verify:
    method: bash
    command: "awk '/^---$/{f=!f;next} !f && !/^#/ && NF{print}' claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md | wc -w | awk '{if($1<=450){print \"pass: \"$1\" words\"}else{print \"fail: \"$1\" words (>450)\"; exit 1}}'"
  ```

- [INV-G6] No changes to `claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md`. The tick is scheduler-agnostic. | Verify: bash.
  ```yaml
  verify:
    method: bash
    command: "git diff --name-only $(git merge-base HEAD origin/main 2>/dev/null || git rev-list --max-parents=0 HEAD | tail -1) HEAD -- claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md | wc -l | awk '{if($1==0){print \"pass\"}else{print \"fail: drive-tick/SKILL.md was modified\"; exit 1}}'"
  ```

- [INV-G7] `manifest-dev-experimental/.claude-plugin/plugin.json` version bumped to 0.5.0 (minor, new feature) per CLAUDE.md versioning rules. | Verify: bash.
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; v = json.load(open('claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json'))['version']; assert v == '0.5.0', f'version is {v}, expected 0.5.0'; print('pass: 0.5.0')\""
  ```

- [INV-G8] `/check-in`'s terminal-marker anchors match drive-tick's Output Protocol verbatim — including the em-dash `—` (U+2014), not the hyphen `-`. The five anchor strings are: `## Tick N — Terminal:`, `## Tick N — Continuing`, `## Tick N — Skipped (lock held)`, `## Tick N — Error:`, `## BUDGET EXHAUSTED`. | Verify: bash.
  ```yaml
  verify:
    method: bash
    command: "f=claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md; for s in 'Tick N — Terminal:' 'Tick N — Continuing' 'Tick N — Skipped (lock held)' 'Tick N — Error:' 'BUDGET EXHAUSTED'; do grep -qF \"$s\" \"$f\" || { echo \"fail: missing '$s'\"; exit 1; }; done; echo pass"
  ```

- [INV-G9] `/check-in` reads terminal state from the **log file** (parses the last `## Tick N — …` header from the file at `<log-path>`). It does NOT rely on parsing the Skill-tool response text for these markers — drive-tick's Output Protocol writes them to the log, not to its response. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md. Confirm it describes reading the log file at <log-path> to detect terminal state — NOT scanning the Skill-tool response for '## Tick N' markers. Pass only if the body explicitly says the log file is the detection source and the Skill-tool response is NOT."
  ```

- [INV-G10] `/check-in` treats a failed Skill-tool invocation (tool error, timeout, crash — distinct from drive-tick completing and writing an `Error:` log entry) as fail-loud: stop looping, surface the error, exit. No retry, no silent continuation. | Verify: bash.
  ```yaml
  verify:
    method: bash
    command: "grep -E -q 'Skill[- ]tool.*(fail|error|crash)' claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md && grep -E -q '(No retry|do not retry|without retry|fail-loud)' claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md && echo pass || (echo fail; exit 1)"
  ```

## 4. Process Guidance

- [PG-1] Skill type: Business Process + Scaffolding (thin orchestrator). Architecture: single SKILL.md file, no references/, no assets/, no scripts/. (PROMPTING.md default: match architecture to skill type.)

- [PG-2] No externalised memento. `/check-in`'s cross-iteration state is minimal — the original args PLUS the last-seen `## Tick N — …` signature (required by AC-1.10) PLUS a counter of consecutive header-less iterations (required by AC-1.9). All three live in the model's working context for the one Skill-tool invocation; no state file, no JSON blob, no scratchpad on disk. drive-tick owns cross-tick memento.

- [PG-3] Emotional tone: trusted-advisor, low-arousal. Match `/drive` and `/drive-tick`'s tone. No urgency language, no praise, no "finally you can ..." framing.

- [PG-4] High-signal changes only. Touch only the files the task requires:
  - Add: `claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md`.
  - Edit: `claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md` (pre-flight, kickoff, run summary, gotchas).
  - Edit: `claude-plugins/manifest-dev-experimental/README.md` (What it ships, Dependencies, Gotchas).
  - Edit: `claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json` (version, keywords, description one-liner).
  - Do NOT edit drive-tick, adapter contracts, platform/sink files, or any other plugin.

- [PG-5] Write content incrementally per CLAUDE.md "Output Style". Use an initial Write for the first section, then Edit-append subsequent sections. Applies to SKILL.md if it grows beyond a single logical block.

- [PG-6] Kebab-case naming per CLAUDE.md convention. Skill name is `check-in` (hyphen, not underscore, not camelCase).

- [PG-7] Do NOT mirror `/check-in` into `.claude/skills/`. The drive plugin is not hardlinked there today (verified via `stat` — only `manifest-dev` skills are). Adding `/check-in` there would diverge from the repo's symlink convention.

## 5. Known Assumptions

- [ASM-1] **Confirmed from source.** Interface shape: `/check-in` takes `<interval> <log-path> <command>` — one extra positional arg compared to `/loop`'s `<interval> <command>`. `/loop`'s exact invocation today was read verbatim from drive/SKILL.md line 107 and quoted in §1 Mental Model. The extra `<log-path>` is necessary because drive-tick writes terminal markers to the log file, not to its Skill-tool response (verified in INV-G9). Impact if wrong: would only change if `/loop`'s real implementation turns out to differ from what drive/SKILL.md documents — outside this repo's control.

- [ASM-2] Behaviour shape: self-contained loop (/check-in owns the re-invocation), NOT "drive-tick calls /check-in at end of tick." Chosen so drive-tick is unchanged and scheduler choice is entirely /drive's concern. Impact if wrong: if the user intended the drive-tick-invokes-scheduler pattern, /check-in becomes a single sleep+invoke call and drive-tick grows scheduler awareness. Reversal is mechanical.

- [ASM-3] No user-specific config persisted for /check-in. All state comes from /drive via invocation args. Impact if wrong: if the user wanted session-persistent preferences (e.g., default interval), those would be added later — easy additive change.

- [ASM-4] No memento / externalised state. Impact if wrong: would need a log file; currently unnecessary because each iteration's state is re-derivable from args.

- [ASM-5] `/loop` is preferred when both /loop and /check-in are available. Rationale: preserves today's background-cron semantics; /check-in blocks the session. Impact if wrong: user who actively wants /check-in's blocking determinism would need a future `--scheduler` flag (deferred, additive).

- [ASM-6] Interval range for /check-in mirrors /drive: 15m–24h. Rationale: consistency, and /drive is the only caller in v0. Impact if wrong: if a user invokes /check-in directly with a sub-15m interval, they get an error they could perceive as arbitrary — but /drive is the documented caller, so this is acceptable.

- [ASM-7] **Confirmed from source.** Terminal-marker set read verbatim from drive-tick/SKILL.md §Output Protocol (lines 222, 228, 234, 242) and §Budget Check (line 52). Terminal: `## Tick N — Terminal:`, `## Tick N — Error:`, `## BUDGET EXHAUSTED`. Non-terminal: `## Tick N — Continuing`, `## Tick N — Skipped (lock held)`. All use em-dash `—` (U+2014), not hyphen. Pinned by INV-G8 in `/check-in` SKILL.md; protected from drive-tick drift by INV-G6 (no drive-tick edits). If drive-tick's markers drift in a FUTURE change, `/check-in` fails-loud on unrecognized headers (per INV-G9/G10 and AC-1.5) — not silent loop.

- [ASM-8] `<command>` is passed verbatim to the Skill tool — no shell expansion, no re-quoting, no re-parsing. `/check-in` treats `<command>` as an opaque string after interval and log-path extraction. Impact if wrong: if a real `<command>` contains shell metacharacters that need escaping, the Skill-tool invocation may misfire. Mitigation: drive-tick's arg format is known and controlled (flag-based, space-separated — no shell metacharacters).

- [ASM-9] Chunked-sleep uses **cumulative-sleep** semantics (sum of per-chunk durations), not wall-clock target. If chunks accumulate drift (e.g., 540s calls taking 541s), total sleep is slightly longer than requested. Impact if wrong: <1% drift over a 15m interval; interval is already documented as a floor not a precise cadence. Negligible.

- [ASM-10] Session compaction mid-loop is out of scope for v0. If Claude Code auto-compacts context during `/check-in`'s loop, the next iteration resumes with compacted history; `/check-in`'s per-iteration state is minimal (interval, log-path, command — all re-derived from args at skill entry, not from accumulated context), so compaction should not break the loop. Not explicitly protected — future regression risk. Impact if wrong: compaction corrupts state → `/check-in` exits loudly on the next unrecognized outcome. Acceptable v0 behavior.

- [ASM-11] "drive plugin" in the user's request maps to `manifest-dev-experimental` — the plugin that ships `/drive` and `/drive-tick`. Inferred from repo exploration (`/drive` lives at `claude-plugins/manifest-dev-experimental/skills/drive/`); there is no standalone plugin named `drive`. Impact if wrong: would need to relocate `/check-in` to the correct plugin directory — mechanical, but edits to drive/SKILL.md would follow the `/drive` file wherever it lives.

## 6. Deliverables

### Deliverable 1: /check-in skill

Scope: `claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md` (new file). Single-file skill. Frontmatter includes `name`, `description` (What + When + Triggers), `user-invocable: true` (consistent with /drive and /drive-tick).

**Acceptance Criteria:**

- [AC-1.1] File exists at `claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md` with valid YAML frontmatter. | Verify: bash.
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md && python3 -c \"import re,sys; t=open('claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md').read(); m=re.match(r'^---\\n(.*?)\\n---\\n', t, re.S); assert m, 'no frontmatter'; import yaml; d=yaml.safe_load(m.group(1)); assert d.get('name')=='check-in'; assert d.get('user-invocable') is True; assert isinstance(d.get('description'),str) and len(d['description'])>0; print('pass')\""
  ```

- [AC-1.2] Skill documents the sleep + invoke + read-log + classify flow in SKILL.md body. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md. Verify the body describes all five steps: (1) parse interval + log-path + command, (2) sleep the interval (with chunked-sleep for >9 minute intervals), (3) invoke the command via the Skill tool, (4) read the log file at <log-path> and locate the LAST `## Tick N — …` or `## BUDGET EXHAUSTED` header, (5) classify per INV-G8's five anchors and either exit (Terminal / Error / BUDGET) or re-loop (Continuing / Skipped). Pass = all five present and unambiguous; step (4) reads the log file (NOT the Skill-tool response)."
  ```

- [AC-1.3] Skill documents the terminal-marker list consistent with drive-tick/SKILL.md §Output Protocol: `## Tick N — Terminal:`, `## Tick N — Error:`, `## BUDGET EXHAUSTED` are terminal; `## Tick N — Continuing` and `## Tick N — Skipped (lock held)` are non-terminal. | Verify: bash.
  ```yaml
  verify:
    method: bash
    command: "grep -q 'Tick N — Terminal' claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md && grep -q 'Tick N — Error' claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md && grep -q 'BUDGET EXHAUSTED' claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md && grep -q 'Continuing' claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md && echo pass"
  ```

- [AC-1.4] Skill defines empty-input and malformed-interval behaviour: errors with usage message, does not sleep or invoke anything. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md. Verify the skill: (a) errors with a 'Usage: /check-in <interval> <command>' message when called with no args, (b) errors on intervals outside 15m–24h with a matching-wording message, (c) never sleeps or invokes the command before args are validated. Pass = all three present."
  ```

- [AC-1.5] Skill documents fail-loud behaviour on unrecognized log-file markers — `/check-in` halts and reports rather than looping when the log's most recent `## Tick N — …` header (or lack thereof) doesn't match any of the five anchors from INV-G8. Verified semantically (not regex-prescriptive) by subagent. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md. Confirm: when the log file contains no `## Tick N — …` header at all, OR contains a header that matches none of the five known anchors (Terminal:, Continuing, Skipped (lock held), Error:, BUDGET EXHAUSTED), the skill STOPS the loop and surfaces an error. Pass only if fail-loud is explicit and silent-continue is ruled out."
  ```

- [AC-1.6] Skill documents the chunked-sleep pattern with an **upfront** chunk-count formula (`ceil(interval_seconds / 540)`), not an in-loop decrementing counter. This avoids arithmetic-during-loop drift, which LLMs are prone to. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md. Confirm chunked-sleep specification: (1) computes chunk count UPFRONT via `ceil(interval_seconds / 540)` (or equivalent wording making the 540s cap and ceil-division explicit), (2) issues that many sequential `sleep 540` calls plus a final remainder chunk, (3) does NOT use an in-loop cumulative-elapsed counter that the model maintains across chunks. Pass = upfront formula is specified."
  ```

- [AC-1.7] Skill documents Skill-tool-failure handling: if the Skill tool invocation itself errors (distinct from drive-tick completing and writing `Error:` to the log), `/check-in` stops the loop, surfaces the failure, and does NOT retry. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md. Confirm it distinguishes (a) drive-tick completing normally and writing a log entry (including `Error:`), from (b) the Skill tool invocation itself failing (tool error, timeout, crash). For case (b), verify the skill halts the loop, surfaces the failure, and does not retry. Pass = distinction is explicit and no-retry is stated."
  ```

- [AC-1.8] Skill documents parsing of the three-positional-arg spec `<interval> <log-path> <command>`. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md. Confirm the arg spec is `<interval> <log-path> <command>` — three positional args — and the skill uses <log-path> to locate the log file it reads for terminal-state detection. Pass only if the arg shape is unambiguous."
  ```

- [AC-1.9] Skill documents first-iteration and log-absence behaviour: if the log file is missing or contains no `## Tick N — …` header on a given iteration (i.e., drive-tick was invoked but appended nothing, or the file was not yet created), treat as `Continuing` for up to ONE consecutive iteration (handles first-tick initialization races), then fail-loud. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md. Confirm first-iteration / log-absence handling: (a) missing or header-less log on the FIRST iteration counts as Continuing (allow one grace iteration for initialization race), (b) TWO CONSECUTIVE iterations without a new `## Tick N — …` header triggers fail-loud exit with an explanatory message, (c) this is explicitly stated — not implicit. Pass = all three."
  ```

- [AC-1.10] Skill documents per-iteration 'last-seen header' tracking to distinguish new headers from stale ones. `/check-in` remembers the last header index/signature it classified and requires a STRICTLY NEWER entry before re-classifying. Prevents misreading an old `Terminal:` header from a prior crashed run. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/check-in/SKILL.md. Confirm the skill describes how it distinguishes a newly-written `## Tick N — …` header from one that was already present before the current iteration's invocation. Acceptable mechanisms: tracking the last-seen tick number, tracking the file size / byte offset before invocation and reading only new content after, or reading only the log tail after the invocation timestamp. Pass = an explicit distinguishing mechanism is described."
  ```

### Deliverable 2: /drive integration

Scope: `claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md`. Edits to §Pre-flight, §/loop Kickoff (renamed to §Scheduler Kickoff), the run-summary print, and §Gotchas. No structural restructuring — minimal surgical edits.

**Acceptance Criteria:**

- [AC-2.1] §Pre-flight's first dependency check replaces the single `/loop available` bullet with a tri-branch: both available → use /loop; only /check-in → use /check-in with blocking-session warning; neither → error naming both providers. | Verify: bash.
  ```yaml
  verify:
    method: bash
    command: "awk '/## Pre-flight/,/## Base Branch Resolution/' claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md | grep -E -q '/check-in' && awk '/## Pre-flight/,/## Base Branch Resolution/' claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md | grep -E -q 'neither|both unavailable|not found' && echo pass || (echo fail; exit 1)"
  ```

- [AC-2.2] Error message when neither scheduler is available names both skills and suggests installation paths — does not silently fall through. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Pre-flight in claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md. Confirm: when both /loop AND /check-in are unavailable, the error message (a) names /loop, (b) names /check-in, (c) is actionable (tells user what to do). Pass only if all three are present."
  ```

- [AC-2.3] §Scheduler Kickoff (renamed from §/loop Kickoff) documents two scheduler-specific invocation blocks: the `/loop` invocation is byte-equivalent to today (INV-G4); the `/check-in` invocation differs by one additional positional arg (`<log-path>`) up front, which is REQUIRED by INV-G9 (log-file-as-contract). The drive-tick arg string passed to both schedulers is identical. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Scheduler Kickoff (renamed from §/loop Kickoff) in claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md. Confirm: (1) the section is renamed to 'Scheduler Kickoff'; (2) a /loop invocation block exists and is byte-identical to what drive used today (<interval> then the /drive-tick args); (3) a /check-in invocation block exists with <log-path> as the second positional arg BEFORE the /drive-tick command, consistent with /check-in's need to read the log file per INV-G9; (4) the /drive-tick args string is identical between the two blocks. Pass = all four."
  ```

- [AC-2.4] Run summary printed at end of §Scheduler Kickoff includes an explicit scheduler field naming which was chosen (a labelled line such as `scheduler: /loop` or `scheduler: /check-in`, not merely a mention). Existing summary fields (run-id, mode, platform, sink, interval, budget, branch, PR number, log path, `tail -f` hint) unchanged. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Scheduler Kickoff (or §/loop Kickoff if unrenamed) in claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md. Confirm the run-summary print specification: (1) includes an explicit scheduler-name field labelled clearly enough that a reader can tell it's the chosen scheduler (e.g., `scheduler:` prefix, or a sentence like 'scheduler used: X'), not merely a passing mention; (2) all of these original fields remain and are unchanged in meaning: run-id, mode, platform, sink, interval, budget, branch, PR number (github), log path, tail-f hint. Pass = both."
  ```

- [AC-2.5] §Gotchas includes a new line flagging the session-blocking nature of /check-in fallback (session close → scheduler dies immediately, unlike /loop cron). | Verify: bash.
  ```yaml
  verify:
    method: bash
    command: "awk '/## Gotchas/,0' claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md | grep -E -q '/check-in.*(block|session|fallback)' && echo pass || (echo fail; exit 1)"
  ```

- [AC-2.6] Drive's §Pre-flight explicitly orders /loop preferred, /check-in fallback, neither → error — with /loop named first in prose (not a coin-flip or alphabetical order). | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Pre-flight in claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md. Confirm the scheduler-selection ordering is explicit and stated as: /loop is preferred when available; /check-in is used only when /loop is unavailable; neither → error. The order must not be ambiguous or reversible from the text. Pass = ordering is stated explicitly."
  ```

### Deliverable 3: README + plugin metadata

Scope: `claude-plugins/manifest-dev-experimental/README.md` and `claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json`.

**Acceptance Criteria:**

- [AC-3.1] README's "What it ships" section mentions `/check-in` with a one-sentence summary of its fallback role. | Verify: bash.
  ```yaml
  verify:
    method: bash
    command: "awk '/## What it ships/,/## Mode matrix/' claude-plugins/manifest-dev-experimental/README.md | grep -E -q '/check-in' && echo pass || (echo fail; exit 1)"
  ```

- [AC-3.2] README's "Dependencies checked before bootstrap" section updated: the `/loop skill` bullet expanded to "`/loop` OR `/check-in`" with a note that `/loop` is preferred. | Verify: bash.
  ```yaml
  verify:
    method: bash
    command: "awk '/## Dependencies/,/## Recommended/' claude-plugins/manifest-dev-experimental/README.md | grep -E -q '/check-in' && echo pass || (echo fail; exit 1)"
  ```

- [AC-3.3] README's "Gotchas" section includes a bullet that (a) names `/check-in`, (b) describes blocking-session semantics (session close ends the loop immediately, no background cron), (c) contrasts with `/loop`'s fire-and-forget behaviour. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read the Gotchas section of claude-plugins/manifest-dev-experimental/README.md. Confirm a bullet exists that (a) names /check-in, (b) describes session-blocking / session-end-kills-loop semantics, (c) contrasts with /loop's cron/background behaviour. All three must be present. Pass = all three."
  ```

- [AC-3.4] plugin.json version bumped to `0.5.0`; keywords array includes both `check-in` and `fallback`. | Verify: bash.
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; d=json.load(open('claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json')); assert d['version']=='0.5.0', d['version']; kw=d.get('keywords',[]); assert 'check-in' in kw and 'fallback' in kw, kw; print('pass')\""
  ```

- [AC-3.5] plugin.json description mentions `/check-in` fallback in a single clause (keeps the one-liner under ~240 chars). | Verify: bash.
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; d=json.load(open('claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json')); desc=d['description']; assert 'check-in' in desc, 'no check-in in desc'; assert len(desc)<=280, f'desc too long: {len(desc)}'; print('pass:',len(desc),'chars')\""
  ```

- [AC-3.6] No other README in the repo is stale because of this change. | Verify: subagent.
  ```yaml
  verify:
    method: subagent
    agent: docs-reviewer
    prompt: "Audit README.md at repo root and claude-plugins/README.md for mentions of /drive, /loop, or the experimental plugin's dependencies. The change in this PR adds a /check-in fallback to the experimental plugin. Report any stale references that contradict the new state — 'dependencies: /loop only' phrasing, missing /check-in mentions where drive's scheduler list is enumerated, etc. Pass = either no drift or no dependency enumerations exist in those files."
  ```


