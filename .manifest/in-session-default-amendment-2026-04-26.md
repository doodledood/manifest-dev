# Definition: In-Session Default Amendment for /define

## 1. Intent & Context
- **Goal:** When `/define` is invoked again in the same session and a prior manifest exists, default to amending that manifest. Only fall back to a fresh manifest when the new task is *truly* unrelated (rare). Outcome: one manifest per change set, so follow-up tasks (bug fixes, feature extensions, polish on the same surface) inherit and respect the prior INVs/ACs/PGs — preventing silent regression of earlier constraints.
- **Mental Model:** The manifest is the change-set's constitution. Today, every `/define` starts from scratch — so a bug-fix or follow-up tweak runs without the original task's invariants in scope, and can quietly undo decisions the user already made. Defaulting to amendment carries the constitution forward. The agent does the relatedness judgment using prior manifest's Goal + Deliverables vs. the new task description, with a strong bias to amend (relatedness is the default; only clear domain mismatch → fresh).
- **Mode:** thorough
- **Interview:** thorough
- **Medium:** local

## 2. Approach
*Initial direction. SKILL.md-only change; instructions, no hook, no util, no flag.*

- **Architecture:**
  - Add a new standalone **"Session-Default Amendment"** section to `claude-plugins/manifest-dev/skills/define/SKILL.md`, positioned immediately AFTER the "Input" section and BEFORE the existing "Amendment Mode" section (so the explicit `--amend` flag check still happens first and short-circuits the session check; new section sits between Input and Amendment Mode).
  - The section instructs the agent to: (a) at the start of every `/define`, scan its own conversation context for prior `/define` completion outputs of the form `Manifest complete: /tmp/manifest-{timestamp}.md`; (b) if found and `--amend` was not explicitly passed, read the most recent prior manifest and compare its Goal + Deliverables against the new task description; (c) bias strongly toward "related" — only fresh when domain/surface is clearly different; (d) when amending, announce one line to the user with an explicit invitation to redirect; (e) when the prior manifest file no longer exists or cannot be read, fall back to fresh with a brief note.
  - Update `references/AMENDMENT_MODE.md` to add a third trigger context: **"Session-Default"** — same behavior as Standalone, but the trigger is `/define`'s in-session detection rather than an explicit `--amend` flag.
  - Bump plugin version (minor — new feature) and update root + plugin READMEs with a one-line mention.
  - `/auto` requires no changes — it invokes `/define` via Skill tool, so the new SKILL.md instructions execute inside the `/auto` flow automatically.

- **Execution Order:**
  - D1 (SKILL.md instructions) → D2 (AMENDMENT_MODE.md context update) → D3 (version bump + README sync)
  - Rationale: D1 is the load-bearing change. D2 documents the new trigger so amendment-mode behavior reads coherently. D3 is housekeeping per CLAUDE.md sync checklist.

- **Risk Areas:**
  - [R-1] Conversation compaction may evict the prior `Manifest complete: ...` line, causing /define to miss the amendment target | Detect: post-compaction /define behavior — agent treats the session as fresh. Acceptable per ASM-2; user can re-amend with explicit `--amend <path>`.
  - [R-2] Agent misjudges "related" and amends an unrelated manifest | Detect: user redirects after the announcement. Mitigation: announcement always offers the opt-out path.
  - [R-3] Prior manifest file deleted/moved from /tmp/ between invocations | Detect: amendment read fails. Mitigation: AC-1.6 requires graceful fallback to fresh with note.
  - [R-4] Agent biases too aggressively toward "fresh" because the new task description doesn't lexically match the prior one — losing the regression-prevention benefit the user wants | Detect: change-intent-reviewer cross-checks the section's wording for "amend by default; fresh only when domain is clearly different". Mitigation: encode the bias explicitly in SKILL.md prose (INV-G7).

- **Trade-offs:**
  - [T-1] User surprise vs. friction → Prefer brief one-line announcement over silent or confirmation-gated, because users need a redirect lever without per-invocation prompts.
  - [T-2] Determinism (hook/flag) vs. simplicity (instructions only) → Prefer simplicity per user direction; agent already has its conversation context and can reason about it.
  - [T-3] Strong amend-bias (regression prevention) vs. precise relatedness judgment → Prefer strong amend-bias; "truly unrelated" is the only reason to start fresh, per user.

## 3. Global Invariants

- [INV-G1] change-intent-reviewer reports no LOW-or-higher findings on the SKILL.md + AMENDMENT_MODE.md changes
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    model: inherit
    prompt: "Review the changes to claude-plugins/manifest-dev/skills/define/SKILL.md and claude-plugins/manifest-dev/skills/define/references/AMENDMENT_MODE.md against this stated intent: when /define is invoked in a session that already has a prior manifest, default to amending that manifest (strong bias to amend; only start fresh when the new task is clearly unrelated to the prior manifest's Goal + Deliverables). Explicit --amend flag must continue to work as before. /do --from-do amendment path must remain unaffected. /auto must inherit the new default automatically because it invokes /define via Skill tool. Verify the prompt actually achieves these behaviors. Report LOW/MEDIUM/HIGH findings."
  ```

- [INV-G2] prompt-reviewer reports no MEDIUM-or-higher findings on the SKILL.md changes
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review the new Session-Default Amendment section in claude-plugins/manifest-dev/skills/define/SKILL.md and any modified text in references/AMENDMENT_MODE.md. Check clarity, structure, anti-patterns (no prescribing HOW the model should scan its context, no arbitrary limits, no weak language), invocation fit (the section runs at the start of /define), composition with existing SKILL.md sections (Input parsing, Amendment Mode, Existing Manifest Feedback). Report MEDIUM/HIGH findings."
  ```

- [INV-G3] Explicit `--amend <path>` behavior is preserved end-to-end (standalone and `--from-do` paths unaffected)
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "In claude-plugins/manifest-dev/skills/define/SKILL.md, verify the Input section still parses --amend (and --from-do) exactly as before, and that the new Session-Default Amendment section explicitly short-circuits when --amend is already present in arguments. PASS if both are true; FAIL otherwise."
  ```

- [INV-G4] When no prior manifest exists in the session context, /define behavior is unchanged from current
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "In claude-plugins/manifest-dev/skills/define/SKILL.md's new Session-Default Amendment section, verify that the section explicitly states the no-prior-manifest case is treated as a fresh /define (current behavior preserved). PASS if explicit; FAIL if ambiguous or missing."
  ```

- [INV-G5] Hardlink integrity preserved between `claude-plugins/manifest-dev/skills/define/` files and their `.claude/skills/define/` counterparts (covers SKILL.md and references/AMENDMENT_MODE.md — both confirmed hardlinked)
  ```yaml
  verify:
    method: bash
    command: "for f in skills/define/SKILL.md skills/define/references/AMENDMENT_MODE.md; do a=\"claude-plugins/manifest-dev/$f\"; b=\".claude/$f\"; ai=$(stat -c %i \"$a\"); bi=$(stat -c %i \"$b\"); if [ \"$ai\" != \"$bi\" ]; then echo \"FAIL hardlink: $f\"; exit 1; fi; done; echo OK"
  ```

- [INV-G6] SKILL.md text expresses a strong bias toward amending (relatedness is the default; only "clearly different domain/surface" triggers fresh)
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "In claude-plugins/manifest-dev/skills/define/SKILL.md's new Session-Default Amendment section, verify the relatedness rule is biased toward AMEND: amendment is the default; fresh requires clear evidence the new task targets a different domain or surface from the prior manifest's Goal + Deliverables. The wording must NOT read as a 50/50 judgment call. PASS if biased toward amend; FAIL if neutral or biased toward fresh."
  ```

## 4. Process Guidance

- [PG-1] High-signal changes only — modify only the sections that implement the new default. Do not refactor surrounding sections of SKILL.md or AMENDMENT_MODE.md.
- [PG-2] Calibrate emotional tone — the user-facing announcement should be calm and matter-of-fact ("Detected... Defaulting... Tell me if..."). No urgency, no apologetic hedging.
- [PG-3] When editing SKILL.md or AMENDMENT_MODE.md, edit the `claude-plugins/manifest-dev/skills/define/...` canonical copy. The hardlink propagates to `.claude/skills/define/...`.
- [PG-4] Discovery log lifecycle is unchanged — every /define invocation (fresh OR session-default amendment) creates its own `/tmp/define-discovery-{timestamp}.md`. Logs are not appended across invocations; the manifest itself is what carries forward.

## 5. Known Assumptions

- [ASM-1] "Most recent manifest" = the last `Manifest complete: /tmp/manifest-...md` line emitted in the transcript (transcript order, not path-timestamp order — handles the case where the user manually amended an older manifest mid-session) | Default: last-emitted-in-transcript | Impact if wrong: user redirects via the announcement opt-out, or invokes `/define --amend <other-path>` explicitly.
- [ASM-2] Conversation compaction may evict the prior `Manifest complete: ...` line; in that case /define falls back to fresh | Default: accept | Impact if wrong: user invokes `/define --amend <path>` explicitly to recover.
- [ASM-3] No explicit opt-out flag — verbal redirect after the announcement is the only override path | Default: agreed by user | Impact if wrong: a future change can add `--new` without breaking anything.
- [ASM-4] Standalone `/define --amend` writes to a new `/tmp/manifest-{timestamp}.md` (or in-place — current behavior unchanged either way). The session-default path inherits whatever standalone amend currently does.

## 6. Deliverables

### Deliverable 1: Session-Default Amendment section in SKILL.md
File: `claude-plugins/manifest-dev/skills/define/SKILL.md`

**Acceptance Criteria:**

- [AC-1.1] A new standalone section titled "Session-Default Amendment" exists in SKILL.md, positioned after the existing "Input" section and before the existing "Amendment Mode" section. It is a separate section, not merged into Amendment Mode.
  ```yaml
  verify:
    method: bash
    command: "python3 -c 'import re; t=open(\"claude-plugins/manifest-dev/skills/define/SKILL.md\").read(); pos={m.group(1): m.start() for m in re.finditer(r\"^## (.+)$\", t, re.M)}; assert \"Session-Default Amendment\" in pos, \"missing heading\"; assert \"Input\" in pos and \"Amendment Mode\" in pos, \"missing reference headings\"; assert pos[\"Input\"] < pos[\"Session-Default Amendment\"] < pos[\"Amendment Mode\"], \"wrong order\"; print(\"OK\")'"
  ```

- [AC-1.2] The new section instructs the agent to scan its own conversation context for prior `/define` completion outputs (lines matching `Manifest complete: /tmp/manifest-...md`) at the start of every invocation, BEFORE entering the interview. When multiple prior outputs exist, the most recent in transcript order wins.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "In the Session-Default Amendment section of claude-plugins/manifest-dev/skills/define/SKILL.md, verify the agent is told to: (1) check conversation context for prior /define manifest paths, (2) do this check at the start of every invocation BEFORE the interview, (3) when multiple priors exist pick the most recent in transcript order. PASS if all three are explicit; FAIL otherwise."
  ```

- [AC-1.3] The section instructs the agent to read the most recent prior manifest's Goal + Deliverables and compare against the new task description, with a strong bias toward amendment (only "truly unrelated / clearly different domain or surface" → fresh).
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "In the Session-Default Amendment section of claude-plugins/manifest-dev/skills/define/SKILL.md, verify the relatedness check uses the prior manifest's Goal AND Deliverables as the comparison basis (not just title), and the wording biases strongly toward amend ('truly unrelated' / 'clearly different domain' style language). PASS if both; FAIL otherwise."
  ```

- [AC-1.4] When a prior manifest is found and the relatedness check passes, /define proceeds as if invoked with `--amend <prior-path>` (delegates to the existing AMENDMENT_MODE.md flow) and explicitly cross-references the new "Session-Default" trigger context in AMENDMENT_MODE.md.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "In the Session-Default Amendment section of claude-plugins/manifest-dev/skills/define/SKILL.md, verify that (1) on a positive relatedness match the agent reuses the existing --amend flow rather than reimplementing amendment logic, and (2) the section explicitly cross-references references/AMENDMENT_MODE.md (by name or path) for the actual amendment behavior. PASS if both; FAIL otherwise."
  ```

- [AC-1.5] The agent announces the decision to the user before starting the interview, in the form: "Detected prior manifest in session: <path> (<title>). Defaulting to amendment mode. Tell me if this is unrelated work and I'll start fresh." Or substantively equivalent: includes manifest path, title, the word "amendment", and an explicit redirect invitation. Announcement is emitted regardless of interview mode (autonomous included) — preserves audit trail in transcript.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "In the Session-Default Amendment section of claude-plugins/manifest-dev/skills/define/SKILL.md, verify the announcement instruction includes: (a) the prior manifest path, (b) its title or a brief identifier, (c) explicit mention of amendment mode, (d) an opt-out invitation the user can act on verbally, (e) explicit statement that the announcement is emitted regardless of interview mode (including autonomous). PASS if all five; FAIL otherwise."
  ```

- [AC-1.6] Explicit `--amend` flag in arguments short-circuits the session check (the explicit flag wins). This preserves /do --from-do path (which always passes --amend).
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "In the Session-Default Amendment section of claude-plugins/manifest-dev/skills/define/SKILL.md, verify the section explicitly states that if --amend is already present in arguments, the session check is skipped. PASS if explicit; FAIL otherwise."
  ```

- [AC-1.7] When the prior manifest file no longer exists or cannot be read, /define falls back to fresh manifest creation with a brief one-line note to the user.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "In the Session-Default Amendment section of claude-plugins/manifest-dev/skills/define/SKILL.md, verify there is an explicit fallback rule for the case where the prior manifest path is no longer readable: fall back to fresh /define with a brief note to the user. PASS if explicit; FAIL otherwise."
  ```

- [AC-1.8] When the new task is determined to be truly unrelated, /define proceeds fresh and includes a one-line note explaining why (so the user can correct).
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "In the Session-Default Amendment section of claude-plugins/manifest-dev/skills/define/SKILL.md, verify that on a 'truly unrelated' determination the agent proceeds fresh AND tells the user why in one line so they can correct. PASS if both; FAIL otherwise."
  ```

- [AC-1.9] When no prior `Manifest complete: ...` line is present in the conversation context, the section explicitly states /define behavior is unchanged from current (fresh manifest, no announcement).
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "In the Session-Default Amendment section of claude-plugins/manifest-dev/skills/define/SKILL.md, verify the no-prior-manifest case is explicitly handled: the section says behavior is unchanged from a normal fresh /define and no announcement is emitted. PASS if explicit; FAIL otherwise."
  ```

### Deliverable 2: AMENDMENT_MODE.md notes the new trigger context
File: `claude-plugins/manifest-dev/skills/define/references/AMENDMENT_MODE.md`

**Acceptance Criteria:**

- [AC-2.1] AMENDMENT_MODE.md adds (or revises an existing section to add) a third trigger context: "Session-Default" — explains that /define may auto-promote to amendment mode based on session context (no explicit `--amend` flag), and behaves identically to the Standalone interactive path from that point on. Existing "Standalone" and "From /do (Autonomous Fast Path)" descriptions remain accurate.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "In claude-plugins/manifest-dev/skills/define/references/AMENDMENT_MODE.md, verify there is a third trigger context covering session-default amendment. It must (a) describe the trigger as /define's in-session detection of a prior related manifest, (b) state behavior is identical to the Standalone interactive path, (c) leave the existing Standalone and From /do descriptions intact and accurate. PASS if all three; FAIL otherwise."
  ```

### Deliverable 3: Plugin version bump + README sync
Files: `claude-plugins/manifest-dev/.claude-plugin/plugin.json`, `README.md` (root), `claude-plugins/manifest-dev/README.md`

**Acceptance Criteria:**

- [AC-3.1] `claude-plugins/manifest-dev/.claude-plugin/plugin.json` version bumped from 0.89.1 to 0.90.0 (minor — new feature).
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; v=json.load(open('claude-plugins/manifest-dev/.claude-plugin/plugin.json'))['version']; assert v == '0.90.0', f'expected 0.90.0, got {v}'; print('OK')\""
  ```

- [AC-3.2] Root `README.md` and `claude-plugins/manifest-dev/README.md` mention the new in-session default amendment behavior in the /define description (one line each, no detailed restatement). If the relevant README does not currently describe /define's per-invocation behavior at this level of detail, this AC is satisfied by adding a brief note where /define is described.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Check README.md (repo root) and claude-plugins/manifest-dev/README.md. For each, locate the section that describes the /define skill. PASS if at least one of the READMEs mentions the in-session default amendment behavior in one line; FAIL if neither mentions it. If the READMEs don't describe /define's behavior at this granularity at all, PASS (the change doesn't warrant new sections)."
  ```
