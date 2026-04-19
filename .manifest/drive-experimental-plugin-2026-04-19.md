# Definition: Experimental Tick-Driven Manifest Runner (`manifest-dev-experimental`)

## 1. Intent & Context

- **Goal:** Build a new experimental plugin `manifest-dev-experimental` that ships a tick-based, cron-driven driver (`/drive` + `/drive-tick`) which takes a manifest (or a PR in babysit mode) from its current state to a terminal state (all verify passes for local mode, or merge-ready for github mode) via repeated stateless ticks. Replaces `/do`'s monolithic fix-verify-loop-hook pattern with cross-tick convergence. Coexists with existing `manifest-dev` skills (nothing deprecated in v0).

- **Mental Model:**
  - **Tick** = one fresh Claude session woken by `/loop` cron. Reads full state (manifest, execution log, git, PR if github), decides one wide action pass (bootstrap / implement / verify / fix / tend PR), commits + pushes if changes, exits. Stateless between ticks — all state lives in manifest + log + git + PR.
  - **Wide tick** = one tick does everything pending. Implementation may take the whole tick (30+ min). Lock file (`/tmp/drive-lock-{run-id}`) with 30-min stale TTL blocks overlap; cron fires that hit the lock exit silently.
  - **Cross-tick convergence** = no internal fix-verify-loop-limit inside a tick. "Keep trying until it sticks" is expressed as "tick → tick → tick." No flow-control hooks because the loop is the flow-control mechanism. No auto-escalation on no-progress — loop runs indefinitely in continuing-states until a terminal state is reached or the user stops it.
  - **Two adapter axes inside the skill: platforms + sinks.** Trigger is external (cron via `/loop` for v0; webhooks/events could invoke `/drive-tick` directly in the future, possibly from outside Claude Code).
  - **Platforms** = how state is read/written. `none` (local branch only, no PR) or `github` (bootstraps PR, tends comments/CI, merges). Each platform owns its own bootstrap, state-read contract, inbox handling, write-outputs, and terminal-state definitions. Adapter files at `skills/drive/references/platforms/{none,github}.md`.
  - **Sinks** = where escalations/status go. `local` (writes to run log file) for v0. Slack/Discord/email deferred.
  - **Wrapper + tick split** = `/drive` parses args, validates mode, bootstraps state, kicks off `/loop`. `/drive-tick` is the per-iteration brain — trigger-agnostic, idempotent, lock-guarded.
  - **Modes** = `manifest` (manifest file provided → verify-driven) or `babysit` (no manifest → tends PR based on conversation + PR comments). Babysit + platform=none is rejected at `/drive` — degenerate combo (no manifest, no PR, no input).
  - **Full duplication of tend-pr-tick** = `platforms/github.md` inlines tend-pr-tick's comment classification (bot/human, actionable/FP/uncertain), CI triage (pre-existing/infrastructure/code-caused), PR description sync, thread-resolution rules, and terminal states. Direct copy — no cross-plugin delegation. Accept manual sync burden.
  - **No plugin-specific hooks.** Flow control is the loop. Safety against irreversible actions is documented as recommended Claude Code permission settings in the plugin README — not enforced by hooks. V0 also ships no correctness-during-work hooks — verify is the sole gate.
  - **Cross-plugin skill invocations** = `/drive-tick` calls `manifest-dev:verify` (verification) and `manifest-dev:define --amend --from-do` (mid-tick manifest amendments for scope changes). These are Skill-tool calls, same pattern as existing `/tend-pr-tick`.

- **Mode:** thorough
- **Interview:** thorough
- **Medium:** local

## 2. Approach

- **Architecture:**

  ```
  claude-plugins/manifest-dev-experimental/
  ├── .claude-plugin/plugin.json
  ├── README.md
  └── skills/
      ├── drive/
      │   ├── SKILL.md                              # wrapper: parse, validate, bootstrap, /loop kickoff
      │   └── references/
      │       ├── ADAPTER_CONTRACT.md               # interface shape all adapters follow
      │       ├── platforms/
      │       │   ├── none.md                       # local-only adapter
      │       │   ├── github.md                     # github adapter (tend-pr-tick duplication)
      │       │   └── data/
      │       │       ├── known-bots.md             # copied from manifest-dev
      │       │       └── classification-examples.md # copied from manifest-dev
      │       └── sinks/
      │           └── local.md                      # local-file escalation sink
      └── drive-tick/
          └── SKILL.md                              # per-iteration brain (lean; reads adapters)
  ```

  `/drive-tick` SKILL.md is lean (≤300 lines hard cap). Reads the resolved platform + sink adapter files, follows their contracts. Each adapter specifies a consistent interface: bootstrap, read-state, terminal-state check, inbox handling, write-outputs. Adding `gitlab.md` later = copy `github.md`, adjust API calls. Adding `slack.md` sink = copy `local.md`, adjust transport.

  Trigger is external — `/drive` wrapper kicks off `/loop` for v0 cron. Future triggers may invoke `/drive-tick` directly without a wrapper. `/drive-tick` is trigger-agnostic: it just does one pass when called.

  **Adapter data shape**: adapters return a **markdown-formatted state report** with fixed section headings (`## Git State`, `## Inbox`, `## Terminal Check`, `## CI/Checks`, `## PR State` for platforms; `## Escalation Target` for sinks). Tick consumes the report directly — no structured-data passing. Platforms omit sections that don't apply (e.g., `none` has no `## Inbox`).

- **Execution Order:**
  - D1 (scaffold) → D4 adapter contract first → D2 (/drive wrapper) + D3 (/drive-tick brain) in parallel → D4 adapter implementations → D5 (docs + marketplace)
  - Rationale: contract must lock before skills and adapter implementations can proceed in parallel.

- **Risk Areas:**
  - [R-1] `platforms/github.md` diverges from `manifest-dev:tend-pr-tick` over time | Detect: periodic manual diff; version bumps of manifest-dev trigger review.
  - [R-2] `/loop` fails silently | Detect: user observes no log updates; plugin README documents `/loop`'s behavioral contract as a dependency.
  - [R-3] Amendment oscillation in manifest mode | Detect: log tracks amendment count; inherit /do R-7 (escalate as Proposed Amendment after 3 auto-amendments without new external input).
  - [R-4] Lock TTL mismatch or crash → stale lock clears → next tick sees partial state | Detect: execution log authoritative for "what was attempted last." Mitigated by enforcing `--interval ≥ lock-TTL (30m)` at invocation.
  - [R-9] Runaway cost — loop spins indefinitely across many ticks, accumulating token spend without user observing | Detect: tick-count budget cap (default 100 ticks, configurable via `--max-ticks`); on cap exceed, tick writes BUDGET EXHAUSTED escalation via sink and ends loop.
  - [R-5] Cross-plugin skill calls break if manifest-dev evolves | Detect: skill invocation errors surface; README documents min manifest-dev version.
  - [R-6] Safety rails absent | Detect: relies on documented permission settings; reconsider for v1 after observed incidents.
  - [R-7] User pushes commits between ticks | Detect: tick reads fresh state; verify catches regressions; normal flow fixes. Not breaking.
  - [R-8] Lock TOCTOU — two ticks see stale lock simultaneously | Detect: tick re-verifies lock by reading back PID/timestamp after creation; mismatch → exit silently. Accept rare duplicate work as v0 limit.

- **Trade-offs:**
  - [T-1] Full duplication vs cross-plugin call → Full (self-contained; user rejected delegation)
  - [T-2] Safety-rail hooks vs permission settings → Permission settings (v0 experimental)
  - [T-3] Pluggable trigger adapter vs external-only → External-only
  - [T-4] Internal fix-verify loop vs cross-tick convergence → Cross-tick
  - [T-5] Always-wide vs narrow tick → Always-wide
  - [T-6] Ship both platforms in v0 vs one → Both
  - [T-7] Babysit+none reject vs allow → Reject
  - [T-8] Terminal-state logic in tick vs adapter → In adapter
  - [T-9] Auto-escalate on no-progress vs run forever → Run forever
  - [T-10] Correctness-during-work hooks vs none → None
  - [T-11] Interval/TTL decoupled vs coupled → Coupled (enforce `--interval ≥ 30m` at invocation; prevents parallel ticks when wide tick exceeds default interval)
  - [T-12] Tick budget cap vs unbounded → Capped (default 100 ticks; prevents silent cost runaway; user may raise/lower via `--max-ticks`)

## 3. Global Invariants

- [INV-G1] All SKILL.md files in new plugin pass prompt-reviewer at no-MEDIUM+. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review the prompts in claude-plugins/manifest-dev-experimental/skills/ (SKILL.md files) and all reference files under skills/drive/references/. Report issues of severity MEDIUM+. Focus on clarity, no conflicts, structure, information density, no anti-patterns, invocation fit, complexity fit, memento pattern (multi-phase), description-as-trigger, edge case coverage, model-prompt fit, guardrail calibration, output calibration, emotional tone."
  ```

- [INV-G2] Intent matches design — change-intent-reviewer confirms implementation matches stated intent at no-LOW+. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Review claude-plugins/manifest-dev-experimental/ against the manifest intent: tick-based cron-driven driver with pluggable platform + sink adapters, cross-tick convergence, wide ticks, lock-guarded concurrency, no flow-control hooks. Confirm skills + adapters achieve this intent. Report LOW+ issues."
  ```

- [INV-G3] Every AC maps to concrete implementation (requirements traceability). | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "For every AC in the manifest under review (resolve from $MANIFEST_PATH or the most recent `.manifest/*experimental*.md` if variable is unset), locate the corresponding implementation in claude-plugins/manifest-dev-experimental/. Report AC with no implementation (MEDIUM+) or divergence (MEDIUM+)."
  ```

- [INV-G4] Behavior completeness — all specified modes and edge cases are handled. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Review claude-plugins/manifest-dev-experimental/ and confirm: (1) manifest+none, (2) manifest+github, (3) babysit+github, (4) babysit+none REJECTED with clear error, (5) current-branch=base → new branch with meaningful slug, (6) current-branch!=base → use existing, (7) babysit+github with no open PR → error, (8) lock held → silent skip, (9) stale lock clears, (10) terminal states per platform adapter, (11) no-progress continues indefinitely (no auto-escalation). Report MEDIUM+ gaps."
  ```

- [INV-G5] Error experience — errors produce specific, actionable messages. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "For every error condition in drive/SKILL.md and drive-tick/SKILL.md (invalid mode combo, missing git remote, base detection fail, no PR in babysit, missing /loop, invalid platform/sink, out-of-range interval), confirm the error message is specific and actionable. Report silent failures or generic errors as MEDIUM+."
  ```

- [INV-G6] Skill folder architecture — each skill is a directory with SKILL.md; references under the skill dir. | Verify:
  ```yaml
  verify:
    method: bash
    command: "test -d claude-plugins/manifest-dev-experimental/skills/drive && test -f claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md && test -d claude-plugins/manifest-dev-experimental/skills/drive-tick && test -f claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md && test -d claude-plugins/manifest-dev-experimental/skills/drive/references/platforms && test -d claude-plugins/manifest-dev-experimental/skills/drive/references/sinks"
  ```

- [INV-G7] Progressive disclosure — SKILL.md files are lean; adapter logic lives in reference files. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md. Confirm it does NOT inline: tend-pr-tick's full classification rules, CI triage, PR description sync, branch creation, or terminal-state lists. Those must be in skills/drive/references/platforms/*.md. Tick references adapters via '../drive/references/platforms/<platform>.md'. Report MEDIUM+ violations."
  ```

- [INV-G8] Description-as-trigger — descriptions follow What+When+Triggers. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review the description field in drive/SKILL.md and drive-tick/SKILL.md frontmatter. Confirm each follows What+When+Triggers, is a trigger specification not a summary, and fits within 1024 chars. Report MEDIUM+ issues."
  ```

- [INV-G9] Gotchas sections — each SKILL.md contains a Gotchas section with concrete, actionable observed/anticipated failure modes. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "For each SKILL.md in claude-plugins/manifest-dev-experimental/skills/, verify a Gotchas section with concrete entries (e.g., bot comments repeat after push, rebase destroys review context, empty diff terminal, lock stale semantics, /loop reliability, amendment oscillation, lock TOCTOU). Report missing or theoretical-only gotchas as MEDIUM+."
  ```

- [INV-G10] Marketplace registered. | Verify:
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; m = json.load(open('.claude-plugin/marketplace.json')); names = [p['name'] for p in m['plugins']]; assert 'manifest-dev-experimental' in names, f'manifest-dev-experimental not in marketplace: {names}'; entry = [p for p in m['plugins'] if p['name']=='manifest-dev-experimental'][0]; assert entry['source'] == './claude-plugins/manifest-dev-experimental', f'wrong source: {entry}'\""
  ```

- [INV-G11] Plugin.json valid. | Verify:
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; p = json.load(open('claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json')); assert p['name'] == 'manifest-dev-experimental'; assert 'version' in p; assert 'description' in p\""
  ```

- [INV-G12] No plugin-specific hooks declared. | Verify:
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; p = json.load(open('claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json')); assert 'hooks' not in p or p.get('hooks') in ({}, None), f'plugin declares hooks: {p.get(\\\"hooks\\\")}'\""
  ```

- [INV-G13] Existing manifest-dev and manifest-dev-tools plugins untouched except README cross-refs. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Run `git diff --name-only <base>...HEAD` and list files in claude-plugins/manifest-dev/ and claude-plugins/manifest-dev-tools/. Confirm only README.md files modified (cross-referencing new plugin). Any skill/agent/hook change is MEDIUM+ violation unless justified."
  ```

- [INV-G14] CLAUDE.md adherence (kebab-case, frontmatter, version bump, README sync). | Verify:
  ```yaml
  verify:
    method: subagent
    agent: context-file-adherence-reviewer
    prompt: "Review claude-plugins/manifest-dev-experimental/ and README edits against /home/user/manifest-dev/CLAUDE.md. Confirm kebab-case naming, skill frontmatter, plugin.json patterns, README sync checklist. Report MEDIUM+ violations."
  ```

- [INV-G15] V0 explicitly ships no correctness-during-work hooks — verify is sole gate; users migrating from /do must be informed in README. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/README.md. Confirm a section or note states v0 ships NO correctness-during-work hooks (the PreToolUse/PostToolUse hooks present in manifest-dev plugin.json for /do), and that users are informed this differs from /do. Report MEDIUM+ if absent."
  ```

## 4. Process Guidance

- [PG-1] Skill type — `/drive`, `/drive-tick` are Business Process skills (autonomous workflow drivers).
- [PG-2] Progressive disclosure — keep `/drive-tick` SKILL.md lean; platform/sink logic in reference files; tick delegates via "Load ../drive/references/platforms/<platform>.md and follow its contract."
- [PG-3] Empty input behavior — /drive with no args errors actionably; /drive-tick missing required args errors with usage.
- [PG-4] Memento pattern — execution log `/tmp/drive-log-{run-id}.md` is cross-tick memento. Every tick APPENDS an entry (timestamp, detected state, action taken, outcome, next expected state). Next tick reads full log before deciding.
- [PG-5] Calibrate emotional tone — SKILL.md and adapter prompts use calm, direct, trusted-advisor voice. Failure is normalized ("tick N detected X; tick N+1 will retry").
- [PG-6] Document load-bearing dependencies in README: `/loop`, `manifest-dev:verify`, `manifest-dev:define --amend`, GitHub MCP, git CLI, `/tmp` persistence.
- [PG-7] /drive does NOT replace /do, /tend-pr, /tend-pr-tick, /auto in v0 — coexists. Document in README.
- [PG-8] Rollback = uninstall manifest-dev-experimental. Transient `/tmp` artifacts are not cleanup concerns.
- [PG-9] Full duplication of tend-pr-tick logic in platforms/github.md — copy body, adapt headings to adapter contract; retain all classification, CI triage, PR desc sync, thread rules, gotchas verbatim.
- [PG-10] Recommended Claude Code permissions documented in README (force-push, push to base, rm outside project, gh pr merge). Not a runtime gate.
- [PG-11] Version starts at `0.1.0` (pre-1.0 experimental).
- [PG-12] No state files beyond the log. No JSON state blobs, no side channels. Log is the only memento.
- [PG-13] No auto-escalation on no-progress — loop runs indefinitely in continuing-states. User stops by talking to Claude or terminal states fire.
- [PG-14] Every tick — including lock-held skip and terminal exit — appends a status entry to the log. User distinguishes "working" from "hung" via log recency.

## 5. Known Assumptions

- [ASM-1] Lock TTL = 30 minutes, matching tend-pr-tick. | Impact: if real ticks exceed 30 min, two can parallelize. Amend TTL higher if observed.
- [ASM-2] Execution log `/tmp/drive-log-{run-id}.md`, lock `/tmp/drive-lock-{run-id}`. | Impact: /tmp persistence across ticks assumed (matches tend-pr-tick's pattern).
- [ASM-3] Run ID = `gh-{repo-owner}-{repo-name}-{pr-number}` (github mode) or `local-{timestamp}-{4-char-random}` (none mode). Repo qualification prevents cross-repo PR-number collisions in shared /tmp; random suffix prevents same-second collisions in none mode. | Impact: mild filename length; avoids silent log corruption.
- [ASM-4] Generated branch name = `claude/<slug-from-manifest-title>-<short-hash>`. Babysit mode always uses existing branch so this doesn't apply there. | Impact: branch collision retries with new hash.
- [ASM-5] Amendment loop guard — inherit /do R-7 pattern: after 3 self-amendments without external input between them, escalate via sink. | Impact: occasional escalation; user reviews log.
- [ASM-6] Log format = same shape as /do execution log (timestamp headers, per-action entries). | Impact: readability only.
- [ASM-7] manifest-dev-experimental README declares minimum-supported manifest-dev version. Users install manifest-dev first. | Impact: cross-skill calls error visibly if missing.
- [ASM-8] `/loop` available and schedules sessions reliably. /drive pre-flights via ToolSearch; errors if missing. | Impact: /drive errors before bootstrap side-effects.
- [ASM-9] Bootstrap errors bubble via /drive wrapper before /loop starts. | Impact: no ambiguous "loop started but nothing happened" state.
- [ASM-10] plugin.json fields: name, version, description, keywords, author/homepage/repository/license optional. Matches manifest-dev's shape. | Impact: plugin registration; verified by INV-G11.
- [ASM-11] `/drive` is user-invocable; `/drive-tick` is user-invocable too (for manual debug, matches /tend-pr-tick). | Impact: manual debug preserved.
- [ASM-12] PR comments are sole async input channel in v0. No terminal input, no /tell, no inbox file. User interruption via talking to Claude at session level. | Impact: no mid-flight feedback in manifest+none mode. Accepted v0 limit.

## 6. Deliverables

### Deliverable 1: Plugin scaffold and marketplace registration

Create the new plugin directory with valid plugin.json and register in repo-root marketplace.

**Acceptance Criteria:**

- [AC-1.1] Directory `claude-plugins/manifest-dev-experimental/` exists with `.claude-plugin/plugin.json`, `README.md`, and `skills/` subdirectory. | Verify:
  ```yaml
  verify:
    method: bash
    command: "test -d claude-plugins/manifest-dev-experimental/.claude-plugin && test -f claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json && test -f claude-plugins/manifest-dev-experimental/README.md && test -d claude-plugins/manifest-dev-experimental/skills"
  ```

- [AC-1.2] plugin.json contains: name=manifest-dev-experimental, version=0.1.0, description present, keywords ⊇ {drive, tick, loop, autonomous, experimental}; no hooks section. | Verify:
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; p = json.load(open('claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json')); assert p['name']=='manifest-dev-experimental'; assert p['version']=='0.1.0'; assert p.get('description'); kw=set(p.get('keywords',[])); req={'drive','tick','loop','autonomous','experimental'}; assert req.issubset(kw), f'missing: {req-kw}'; assert 'hooks' not in p or not p['hooks']\""
  ```

- [AC-1.3] Repo-root `.claude-plugin/marketplace.json` lists the new plugin with correct source path. | Verify:
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; m = json.load(open('.claude-plugin/marketplace.json')); entry = [p for p in m['plugins'] if p['name']=='manifest-dev-experimental']; assert entry, 'manifest-dev-experimental missing'; assert entry[0]['source']=='./claude-plugins/manifest-dev-experimental'\""
  ```

- [AC-1.4] Root `README.md` and `claude-plugins/README.md` list the new plugin. | Verify:
  ```yaml
  verify:
    method: bash
    command: "grep -q 'manifest-dev-experimental' README.md && grep -q 'manifest-dev-experimental' claude-plugins/README.md"
  ```

### Deliverable 2: `/drive` wrapper skill

User-invocable wrapper that parses arguments, validates mode, pre-flights `/loop`, bootstraps state (branch, empty commit, PR if github), kicks off `/loop`.

**Acceptance Criteria:**

- [AC-2.1] File `skills/drive/SKILL.md` exists with valid frontmatter (`name: drive`, `description:` following What+When+Triggers, `user-invocable: true`). | Verify:
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md && head -20 claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md | grep -q '^name: drive$' && head -20 claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md | grep -q '^user-invocable: true$'"
  ```

- [AC-2.2] Input parsing documented — accepts: optional `<manifest-path>` (absent = babysit), `--platform none|github` (default none), `--sink local` (default local), `--base <branch>` (override auto-detection), `--interval <duration>` (default 30m), `--max-ticks <N>` (default 100). Invalid platform or sink values error actionably. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md. Confirm the Input section documents: manifest-path (optional), --platform (none|github, default none), --sink (local, default local), --base (optional, auto-detect default), --interval (default 30m), --max-ticks (default 100). Confirm error messages for invalid combinations are specific and actionable. Report MEDIUM+ gaps."
  ```

- [AC-2.3] Mode validation — rejects `babysit + platform=none` with error "babysit mode requires --platform github". | Verify:
  ```yaml
  verify:
    method: bash
    command: "grep -q 'babysit' claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md && grep -q 'requires --platform github' claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md"
  ```

- [AC-2.4] Bootstrap per platform — github: resolve base via `git symbolic-ref refs/remotes/origin/HEAD` (fallback main); if current=base, create new branch `claude/<manifest-slug>-<short-hash>`; else use current; empty commit; push; open PR via GitHub MCP if absent. none: same branch logic, commit only, no push/PR. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md. Confirm bootstrap is documented per platform: github creates branch if needed, empty commit, push, PR; none creates branch if needed, commit only. Confirm base detection uses git symbolic-ref with main fallback. Confirm current vs base branch logic. Report MEDIUM+ gaps."
  ```

- [AC-2.5] Babysit+github PR resolution — looks up current branch's open PR; errors "No open PR for current branch" if absent. Does not create a PR in babysit mode. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md. Confirm babysit+github: PR resolved from current branch's open PR, error on missing, does NOT create PR. Report MEDIUM+ gaps."
  ```

- [AC-2.6] Run ID generation — github: `gh-{repo-owner}-{repo-name}-{pr-number}`; none: `local-{timestamp}-{4-char-random}`. Lock `/tmp/drive-lock-{run-id}`, log `/tmp/drive-log-{run-id}.md`. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md. Confirm run-id formats: github = gh-<owner>-<repo>-<pr>, none = local-<timestamp>-<4-random>. Confirm lock and log paths use the run-id. Report MEDIUM+ gaps."
  ```

- [AC-2.7] /loop kickoff — after bootstrap and pre-flight, /drive invokes /loop with `<interval>` and `/drive-tick <args>`. Args include run-id, mode, platform, sink, manifest-path (if manifest mode), log-path, PR number (if github). | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md. Confirm the final action invokes /loop with interval and /drive-tick plus required args (run-id, mode, platform, sink, manifest-path, log-path, pr-number). Report MEDIUM+ gaps."
  ```

- [AC-2.8] Error paths — missing git remote (github), base detection failure with no --base (errors actionably, no silent fallback to master), no open PR (babysit+github), invalid platform/sink, /loop not available, out-of-range interval — each surfaces a specific error, not a silent no-op. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md. For each error condition (missing git remote, base detection fail, no PR in babysit+github, invalid platform/sink, /loop missing, interval out of range), confirm SKILL.md specifies an actionable error message. Confirm base detection failure does NOT silently fall back to master. Report MEDIUM+ silent or generic paths."
  ```

- [AC-2.9] /loop precondition check — pre-flight via ToolSearch for /loop skill BEFORE any bootstrap side-effects. If missing, error: "/loop skill not found — ensure manifest-dev or compatible loop provider is installed." No branch creation, commit, or push when /loop is unavailable. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md. Confirm a pre-flight /loop availability check BEFORE bootstrap. Confirm actionable error on missing /loop. Confirm no bootstrap proceeds without /loop. Report MEDIUM+ if bootstrap can proceed without /loop confirmed."
  ```

- [AC-2.10] --interval validated: 30m ≤ interval ≤ 24h inclusive (min matches lock TTL to prevent parallel ticks); errors actionably on out-of-range; defaults to 30m when omitted. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md. Confirm --interval validation: min 30m (matching lock TTL), max 24h, actionable error on out-of-range, default 30m. Confirm the invariant is documented: interval must be ≥ lock-TTL to prevent parallel ticks when a wide tick exceeds interval. Report MEDIUM+ if bounds missing or coupling undocumented."
  ```

- [AC-2.11] --max-ticks validated: positive integer, 1 ≤ max-ticks ≤ 10000; errors actionably on out-of-range; defaults to 100. Tick-count budget passed as arg to /drive-tick. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md. Confirm --max-ticks validation: positive int, default 100, error on invalid. Confirm max-ticks is passed to /drive-tick as an argument. Report MEDIUM+ if missing."
  ```

- [AC-2.12] Gotchas section — at minimum: /loop reliability outside /drive's control, base branch auto-detection failure modes, interval-must-be-≥-TTL coupling, same-second run-id collision mitigated by random suffix, cross-repo PR-number collision mitigated by repo qualification, max-tick budget stops runaway. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md. Confirm a Gotchas section with at least 5 concrete entries covering: /loop reliability, base auto-detect limits, interval-TTL coupling, run-id collision mitigations, tick budget. Report MEDIUM+ if absent or vague."
  ```

### Deliverable 3: `/drive-tick` brain skill

Per-iteration brain. Lean file (≤300 lines hard cap) that reads state, loads resolved adapter files, executes one wide action pass, exits. Trigger-agnostic (works whether invoked by /loop, manually, or external infra).

**Acceptance Criteria:**

- [AC-3.1] File `skills/drive-tick/SKILL.md` exists with valid frontmatter (`name: drive-tick`, `description:` following What+When+Triggers, `user-invocable: true`). | Verify:
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md && head -20 claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md | grep -q '^name: drive-tick$' && head -20 claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md | grep -q '^user-invocable: true$'"
  ```

- [AC-3.2] Input parsing — accepts positional/named args: run-id, mode (manifest|babysit), platform (none|github), sink (local), manifest-path (if mode=manifest), log-path, pr-number (if platform=github). Missing required args error with usage. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md. Confirm Input documents required args: run-id, mode, platform, sink, conditionally manifest-path (manifest mode) and pr-number (github platform), log-path. Confirm missing-args error is documented. Report MEDIUM+ gaps."
  ```

- [AC-3.3] Concurrency guard — lock file `/tmp/drive-lock-{run-id}`; skip if lock exists and < 30 min old; remove stale locks; create at start, remove at end (including terminal exit). After creating the lock, tick reads it back to verify ownership (PID or timestamp match) — mismatch means TOCTOU race; tick exits silently. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md. Confirm Concurrency Guard documents: lock path, 30-min staleness, skip-if-held, create-at-start, remove-at-end, remove-on-terminal, AND post-creation read-back verification for TOCTOU. Report MEDIUM+ gaps."
  ```

- [AC-3.4] Progressive disclosure — SKILL.md references adapters via `../drive/references/platforms/<platform>.md` and `../drive/references/sinks/<sink>.md`. Does NOT inline tend-pr-tick's classification rules, CI triage, PR description sync, bootstrap semantics, or terminal-state lists. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md. Confirm it does NOT inline tend-pr-tick's classification rules, CI triage, PR desc sync, bootstrap semantics, or platform-specific terminal states. Confirm references to '../drive/references/platforms/' and '../drive/references/sinks/'. Report MEDIUM+ violations of progressive disclosure."
  ```

- [AC-3.5] Hard-line cap — `/drive-tick` SKILL.md is ≤300 lines. | Verify:
  ```yaml
  verify:
    method: bash
    command: "test $(wc -l < claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md) -le 300"
  ```

- [AC-3.6] State reading — each tick reads full execution log, current git HEAD, manifest (manifest mode), and platform-specific state via the platform adapter's read-state contract. Memento discipline: read log BEFORE deciding any action. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md. Confirm State Reading documents reading full log FIRST, then git HEAD, manifest (manifest mode), platform-adapter state (github: PR/CI/comments, none: git only). Report MEDIUM+ gaps."
  ```

- [AC-3.7] Action decision tree — ordered checks: (1) terminal-state check via platform adapter → exit if terminal; (2) inbox/event handling per platform adapter; (3) implementation pass if manifest mode and incomplete; (4) verify if HEAD advanced since last verify or no prior verify; (5) fix if verify failed criteria logged; (6) tend-PR actions per platform adapter (github only); (7) else: schedule next tick. No auto-escalation on no-progress — continuing states schedule next tick indefinitely. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md. Confirm Action Decision Tree documents ordered checks: terminal, inbox, implementation, verify, fix, tend-pr, else schedule-next. Confirm no auto-escalation on no-progress. Report MEDIUM+ gaps."
  ```

- [AC-3.8] Implementation pass shape — work performed INLINE (no Skill invocation of manifest-dev:do). Tick iterates deliverables in execution order, ACs within each deliverable, appends a log entry per AC attempt (shape matches /do's execution log). Entire pass within one tick session. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md. Confirm Implementation Pass specifies: (1) INLINE work, no Skill call to manifest-dev:do, (2) iterate deliverables in execution order, (3) iterate ACs within each deliverable, (4) per-AC log entry, (5) entire pass within one tick session. Report MEDIUM+ if delegation or per-AC logging are missing."
  ```

- [AC-3.9] Verify invocation — tick invokes `manifest-dev:verify` via Skill tool with manifest + log + mode. No phase hints, no scoping — inherits /verify's phase contract verbatim. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md. Confirm verify is invoked as Skill call with only manifest + log + mode. No phase hints or scoping. Report MEDIUM+ if verify logic is inlined or reimplemented or if the tick tries to constrain verify's inputs."
  ```

- [AC-3.10] Amendment invocation — mid-tick amendments use `manifest-dev:define --amend --from-do` via Skill tool. Loop guard: tracks self-amendment count without external input (new PR comment or user message) between them; after 3, escalate as Proposed Amendment via the sink. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md. Confirm: (1) amendments use manifest-dev:define --amend --from-do, (2) loop-guard counts self-amendments without external input, (3) escalation after N=3 routes through the sink. Report MEDIUM+ gaps."
  ```

- [AC-3.11] Crash recovery — on tick start (after lock acquisition), tick treats: (1) existing git HEAD as authoritative (no reset of uncommitted changes); (2) uncommitted working-tree changes as WIP from a crashed prior tick — commit them if consistent with last log entry, else log "UNCOMMITTED CHANGES FROM PRIOR TICK — review manually" and exit silently without further action; (3) last log entry as source of truth for what was attempted. Tick never force-resets or discards uncommitted work. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md. Confirm Crash Recovery documents: (1) HEAD authoritative, (2) uncommitted = WIP, commit if consistent with log else flag & exit, (3) log is source of truth, (4) NEVER force-reset. Report MEDIUM+ gaps."
  ```

- [AC-3.12] Output protocol — every tick ends with exactly one of: terminal-state (remove lock + end loop), continuing-state (remove lock + schedule next via /loop), skipped-lock-held (silent exit, NO scheduling). Each outcome appends a status entry to the log (timestamp, detected state summary, action taken or "skipped — lock held", next expected state or "terminal: <reason>"). User distinguishes "working" from "hung" via log recency. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md. Confirm Output Protocol specifies exactly three exit outcomes (terminal, continuing, skipped) AND requires a log entry on EVERY outcome. Confirm lock removal on terminal and continuing, and skipped exits silently without rescheduling. Report MEDIUM+ gaps."
  ```

- [AC-3.13] Tick-budget enforcement — tick accepts `max-ticks` arg. Before executing any action, tick counts prior tick entries in the execution log. If count ≥ max-ticks, tick appends "BUDGET EXHAUSTED — loop ending after {N} ticks" to the log, invokes the sink's escalate contract, removes the lock, and ends the loop (no further /loop scheduling). | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md. Confirm: (1) max-ticks arg accepted, (2) tick counts prior entries in log before any action, (3) on exceed: log BUDGET EXHAUSTED entry, escalate via sink, remove lock, end loop. Report MEDIUM+ gaps."
  ```

- [AC-3.14] Memento pattern — the tick's first action (after lock acquisition and before any state decision) is reading the full execution log top-to-bottom. SKILL.md calls this out explicitly as a standalone requirement — not buried in general state-reading guidance. Log IS the cross-tick state; no decision is made without reading it first. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md. Confirm a standalone Memento Pattern section states: (1) full log is read top-to-bottom at tick start, (2) no state decision precedes log read, (3) log is cross-tick state (not a JSON file, not a side channel). Report MEDIUM+ if buried or implicit only."
  ```

- [AC-3.15] Gotchas — at minimum: bot comments repeat after push (track by content not ID), lock TTL mismatch parallelizes ticks, TOCTOU on stale-lock acquisition (mitigated by read-back), user pushes between ticks → tick re-reads state, empty diff is terminal, rebase destroys review context, amendment oscillation guard, budget-exhaust terminal. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md. Confirm Gotchas section contains at least 5 concrete entries including the listed ones. Report MEDIUM+ if absent or generic."
  ```

### Deliverable 4: Adapter contract, platform adapters, sink adapter

Lock the adapter interface (ADAPTER_CONTRACT.md), then implement `platforms/none.md`, `platforms/github.md`, `sinks/local.md`, and copy the data files tend-pr-tick relies on.

**Acceptance Criteria:**

- [AC-4.1] Adapter contract file `skills/drive/references/ADAPTER_CONTRACT.md` exists and specifies the markdown-state-report interface: platform adapters return a report with section headings `## Git State`, `## Inbox`, `## Terminal Check`, `## CI/Checks`, `## PR State`; sinks use `## Escalation Target`. Platform required sections: `## Git State`, `## Terminal Check`. Optional: others (omitted when not applicable — e.g., `none` platform omits `## Inbox`, `## CI/Checks`, `## PR State`). Sink required: `## Escalation Target`. Includes example snippets for each. | Verify:
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev-experimental/skills/drive/references/ADAPTER_CONTRACT.md"
  ```

- [AC-4.2] ADAPTER_CONTRACT.md content is complete — specifies all listed section headings, required-vs-optional rules, and includes at least one example snippet for each of platform and sink. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/references/ADAPTER_CONTRACT.md. Confirm: markdown-state-report shape, platform section headings (Git State required, Terminal Check required, Inbox/CI-Checks/PR-State optional), sink section heading (Escalation Target required), example snippets for both adapter types, reference from drive-tick/SKILL.md. Report MEDIUM+ gaps."
  ```

- [AC-4.3] `platforms/none.md` exists. | Verify:
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/none.md"
  ```

- [AC-4.4] `platforms/none.md` content — bootstrap (resolve base, create branch if on base, empty commit, NO push, NO PR), read-state (git log + execution log + manifest only; `## Inbox`, `## CI/Checks`, `## PR State` omitted), terminal states (all-verify-pass → end loop with "manifest satisfied" status; escalation → end loop via sink), write-outputs (commit only, no push). Explicitly documents verify-pass → end-loop behavior. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/none.md. Confirm it covers bootstrap (base, branch-if-needed, commit, no push/PR), read-state (git+log+manifest; omits PR sections), terminal states (verify-pass = end loop, escalation), write-outputs (commit only). Confirm verify-pass → end-loop is explicit. Report MEDIUM+ gaps."
  ```

- [AC-4.5] `platforms/github.md` exists. | Verify:
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md"
  ```

- [AC-4.6] `platforms/github.md` is a full duplication of `manifest-dev:tend-pr-tick`'s behavior — classification (bot/human, actionable/FP/uncertain), CI triage (pre-existing/infrastructure/code-caused), PR description sync, thread resolution rules, merge readiness, stale thread escalation, gotchas — adapted to the adapter contract. Frontmatter, output-protocol wording for /loop scheduling, and adapter-contract section headings may differ. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Diff claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md against claude-plugins/manifest-dev/skills/tend-pr-tick/SKILL.md. Confirm classification rules (bot/human, actionable/FP/uncertain), CI triage (pre-existing/infrastructure/code-caused), PR description sync, thread resolution rules, merge readiness, stale thread escalation, and gotchas are present in github.md. Differences in frontmatter, output-protocol wording, and adapter-contract headings are acceptable. Report MEDIUM+ if any copied behavior is missing or simplified."
  ```

- [AC-4.7] Terminal-state logic lives in the platform adapter, not inlined in drive-tick SKILL.md — none.md enumerates verify-pass + escalation; github.md enumerates merged / closed / draft / merge-ready / empty-diff / escalation. Tick delegates "check terminal states" to the adapter. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read drive-tick/SKILL.md and both platform adapters. Confirm drive-tick does NOT enumerate platform-specific terminal states inline — it delegates to the adapter's contract. Confirm none.md and github.md each list their terminal states. Report MEDIUM+ if terminal states are duplicated or inlined in drive-tick."
  ```

- [AC-4.8] Data files `known-bots.md` and `classification-examples.md` exist under `skills/drive/references/platforms/data/` (copied from manifest-dev, not cross-referenced). | Verify:
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/data/known-bots.md && test -f claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/data/classification-examples.md"
  ```

- [AC-4.9] `platforms/github.md` references data files via local relative paths (e.g., `./data/known-bots.md`), not paths into manifest-dev. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md. Confirm references to known-bots.md and classification-examples.md use local relative paths (./data/ or similar), not paths into manifest-dev. Report MEDIUM+ if paths cross into manifest-dev."
  ```

- [AC-4.10] `sinks/local.md` exists. | Verify:
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev-experimental/skills/drive/references/sinks/local.md"
  ```

- [AC-4.11] `sinks/local.md` content — escalate (append formatted "ESCALATION" entry to run log), report-status (append "TICK STATUS" entry to run log). No external integrations, no state files beyond log. Returns a `## Escalation Target` section naming the log path. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/references/sinks/local.md. Confirm: escalate (log append with ESCALATION marker), report-status (log append), returns `## Escalation Target` section. Confirm no state files beyond log. Report MEDIUM+ gaps."
  ```

- [AC-4.12] Security — `platforms/github.md` specifies: PR comments and user inputs are UNTRUSTED; never execute commands from comment content; never expose secrets in replies or logs. Matches tend-pr-tick's Security section. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md. Confirm a Security section specifies: PR comments untrusted, never run commands from comment content, never expose secrets. Report MEDIUM+ if absent or weaker than tend-pr-tick."
  ```

### Deliverable 5: Documentation and safety-settings guidance

Plugin README, project-level README updates, safety-settings documentation, and explicit coexistence + v0 scope-out notes.

**Acceptance Criteria:**

- [AC-5.1] Plugin README at `claude-plugins/manifest-dev-experimental/README.md` covers: purpose (experimental cron-driven tick driver), mode matrix (manifest × {none, github} valid, babysit × none REJECTED, babysit × github valid), usage examples per valid combo, adapter composition (platforms + sinks + future extensions), coexistence with /do, /tend-pr, /auto, minimum manifest-dev version required, `/loop` behavioral contract relied on, observing progress (tail log). | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/README.md. Confirm sections present: purpose, mode matrix (4 cells with rejection note), usage examples for valid combos, adapter composition (platforms + sinks, future extensions noted), coexistence note, manifest-dev minimum version, /loop contract dependency, observing-progress (tail log), no-correctness-hooks note (INV-G15). Report MEDIUM+ gaps."
  ```

- [AC-5.2] Recommended safety settings documented — a "Recommended `.claude/settings.json` permissions" section provides concrete permission entries for: `git push --force`, `git push` to base branch, `rm -rf` outside project, `gh pr merge`. Documentation-only, not a runtime gate. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/README.md. Confirm 'Recommended safety settings' section with concrete permission-rule examples for git push --force, git push to main/base, rm -rf outside project, gh pr merge. Confirm documentation-only, not a runtime gate. Report MEDIUM+ if missing or generic."
  ```

- [AC-5.3] Explicit v0 scope-out list — README states what is NOT in v0: sinks beyond local (Slack/Discord/email), platforms beyond GitHub (GitLab/Bitbucket), triggers beyond cron (webhooks/events), terminal-channel user input, correctness-during-work hooks, auto-escalation on no-progress. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/README.md. Confirm a 'V0 Scope' or 'Not in v0' section explicitly lists: non-local sinks, non-GitHub platforms, non-cron triggers, terminal input, correctness-during-work hooks, auto-escalation on no-progress. Report MEDIUM+ if missing."
  ```

- [AC-5.4] Coexistence — README explains /drive does NOT deprecate /do, /tend-pr, /tend-pr-tick, /auto in v0. Users preferring synchronous or standalone flows continue with those. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/README.md. Confirm explicit text stating /drive coexists with /do, /tend-pr, /tend-pr-tick, /auto and does not replace them in v0. Report MEDIUM+ if absent."
  ```

- [AC-5.5] Repo-root `README.md` — "Available Plugins" section (or equivalent) and directory-structure block both list `manifest-dev-experimental` with a one-line description. Mention is substantive (not a stray token). | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read the repo-root README.md. Confirm `manifest-dev-experimental` appears in the 'Available Plugins' section (or equivalent plugin listing) with a one-line description AND in the directory-structure block (if present). A stray token reference is insufficient — it must be a substantive listing matching how `manifest-dev` and `manifest-dev-tools` are listed. Report MEDIUM+ if missing or superficial."
  ```

- [AC-5.6] `claude-plugins/README.md` — plugin table (or equivalent listing) includes `manifest-dev-experimental` row with one-line description and link to the plugin directory. Formatting matches how manifest-dev and manifest-dev-tools are listed. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/README.md. Confirm manifest-dev-experimental appears in the plugin table/listing with a one-line description and a link/path to ./manifest-dev-experimental. Confirm formatting parity with existing plugin rows. Report MEDIUM+ if missing or formatting differs significantly."
  ```

- [AC-5.7] `claude-plugins/manifest-dev/README.md` — updated with a brief "See also" or "Related" note cross-referencing `manifest-dev-experimental`, explaining the relationship (experimental cron-driven alternative to `/do` + `/tend-pr`; coexists, nothing deprecated). One or two sentences; does not modify any other content of manifest-dev's README. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev/README.md. Confirm a 'See also' or 'Related' note (one or two sentences) cross-references manifest-dev-experimental and briefly explains the relationship (experimental cron-driven alternative; coexists; nothing deprecated). Confirm no other content in manifest-dev's README is materially changed. Report MEDIUM+ if missing, over-expanded, or materially edits unrelated sections."
  ```

- [AC-5.8] Composition model — plugin README includes a section or table showing the two adapter axes (platforms, sinks) with v0 adapters listed and future additions described (copy-and-adjust pattern). | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/README.md. Confirm a Composition section shows the two axes (platforms, sinks), v0 adapters listed, future additions described with copy-and-adjust pattern. Report MEDIUM+ if absent or vague."
  ```

- [AC-5.9] Observing-progress section — plugin README tells users to `tail -f /tmp/drive-log-{run-id}.md` and sets expectations about console silence between ticks. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-experimental/README.md. Confirm an 'Observing progress' section documents `tail -f` the log file and sets expectations about console silence. Report MEDIUM+ if absent."
  ```

- [AC-5.10] Documentation accuracy — docs-reviewer confirms no MEDIUM+ inaccuracies or stale refs between any modified README (plugin, root, claude-plugins/, manifest-dev/) and actual SKILL.md / adapter file contents. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: docs-reviewer
    prompt: "Review claude-plugins/manifest-dev-experimental/README.md, repo-root README.md (sections referencing manifest-dev-experimental), claude-plugins/README.md, and claude-plugins/manifest-dev/README.md (cross-reference note) against actual SKILL.md and adapter files. Confirm every doc claim matches implementation. Flag inconsistencies as MEDIUM+."
  ```
