# Definition: Default durable artifacts to ~/.manifest-dev/ instead of /tmp

## 1. Intent & Context
- **Goal:** Move the three *durable* manifest-dev artifacts (Manifest, handoff doc, figure-out/-team `--log`) out of `/tmp` into a typed tree under `~/.manifest-dev/` so they survive OS temp cleanup during multi-day work. Update downstream docs that teach the old `/tmp` path. Leave genuinely single-run ephemeral artifacts in `/tmp`.
- **Mental Model:** Root cause of the user's pain — losing manifests mid-feature — is that macOS purges `/tmp` files unaccessed for ~3 days (Linux `systemd-tmpfiles` / tmpfs do the same on a longer clock). Only artifacts that must outlive a multi-day gap need a durable home; everything consumed within a single run/session correctly stays in `/tmp`. These are **prompt edits** to skill markdown — calibration matters: state the location + brief WHY + one fallback clause, trust the agent to `mkdir -p` and expand `~`.
- **Repos:** doodledood/manifest-dev (branch `claude/manifest-artifact-location-kHv7i`)

## 2. Approach
- **Architecture:** Edit each owning skill's path line in `claude-plugins/`. `define/SKILL.md` is the canonical manifest-location source; `CANVAS_MODE.md` and `MULTI_REPO.md` already defer to it ("same dir as the manifest" / "whatever /define chose") so they auto-follow with no edit. `BABYSIT_MODE.md` has its own concrete path line, so it must be aligned explicitly.
- **Execution Order:**
  - D1 (move durable paths) → D2 (update downstream docs) → D3 (housekeeping: versions, READMEs, lint) → D4 (land: commit, push, PR)
  - Rationale: behavior edits first, docs reflect them, housekeeping verifies the whole, then ship.
- **Trade-offs:**
  - [T-1] Targeted scope (3 durable artifacts) vs the original "everything" ask → Prefer targeted because only durable artifacts hit the cleanup window; moving ephemera clutters `$HOME` with no benefit (user reversed to this after root-cause discussion).
  - [T-2] Brief WHY clause in each prompt line vs minimal terseness → Prefer including a short WHY so the executing agent doesn't "optimize" back to `/tmp`; it closes a real behavioral gap.

## 3. Global Invariants

- [INV-G1] Out-of-scope ephemeral artifacts are NOT changed: walk-pr canvas (`walk-pr/references/CANVAS_MODE.md`), reviewer-agent findings logs (`agents/change-intent-reviewer.md`, `contracts-reviewer.md`, `code-bugs-reviewer.md`, `type-safety-reviewer.md`), repo-local dev-skill logs (`.claude/skills/sync-tools`, `harden-task-file`, `learn-from-session`), externally-synced prompt skills (`auto-optimize-prompt`, `compress-prompt`, `optimize-prompt-token-efficiency`, `review-prompt`), and the define `CANVAS_MODE.md` (auto-follows the manifest dir). These still reference `/tmp` / temp paths as before.
  ```yaml
  verify:
    prompt: "In repo doodledood/manifest-dev on branch claude/manifest-artifact-location-kHv7i, run `git diff main --name-only`. PASS only if NONE of these files appear in the diff: claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md, claude-plugins/manifest-dev/agents/change-intent-reviewer.md, claude-plugins/manifest-dev/agents/contracts-reviewer.md, claude-plugins/manifest-dev/agents/code-bugs-reviewer.md, claude-plugins/manifest-dev/agents/type-safety-reviewer.md, claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md, and nothing under .claude/skills/sync-tools, .claude/skills/harden-task-file, .claude/skills/learn-from-session, .claude/skills/auto-optimize-prompt, .claude/skills/compress-prompt, .claude/skills/optimize-prompt-token-efficiency, .claude/skills/review-prompt. Also confirm these files still contain their original /tmp or temp references (grep them). FAIL listing any out-of-scope file that was modified."
    phase: 2
  ```
- [INV-G2] Each moved-artifact path line follows prompt-engineering calibration: states the new `~/.manifest-dev/<subdir>/` location, a brief WHY (durability / survives temp cleanup), and exactly one fallback clause to a writable temp path when home isn't writable; expresses cross-platform via `~` = `$HOME` / `%USERPROFILE%` WITHOUT spelling out verbose per-platform branches or step-by-step mkdir instructions.
  ```yaml
  verify:
    prompt: "Read these four locations after the change: claude-plugins/manifest-dev/skills/define/SKILL.md (manifest path line), claude-plugins/manifest-dev/skills/define/references/BABYSIT_MODE.md (Output section), claude-plugins/manifest-dev-tools/skills/handoff/SKILL.md (Output line), and claude-plugins/manifest-dev/skills/figure-out/references/LOG.md + claude-plugins/manifest-dev/skills/figure-out-team/references/LOG.md (the `--log` with no path bullet). For EACH: PASS only if it (a) names the correct ~/.manifest-dev/ subdir (manifests/ for the two manifest lines, handoffs/ for handoff, logs/ for both --log bullets), (b) gives a short reason it's durable / survives temp cleanup, (c) has a single fallback to a writable temp path when home isn't writable, and (d) is concise — no multi-sentence platform branching, no enumerated mkdir steps. These are prompt instructions for an LLM agent, so trust-the-model brevity is the bar. FAIL any line that is verbose/over-specified or missing one of a-d, quoting the line."
    phase: 2
  ```
- [INV-G3] Lint, format, and typecheck pass clean.
  ```yaml
  verify:
    prompt: "From repo root run: ruff check claude-plugins/ && black --check claude-plugins/ && mypy . PASS only if all three exit 0 (no errors). If black would reformat or ruff/mypy report errors, FAIL with the offending output. If mypy reports a config/no-files condition that also occurs on the base branch (pre-existing), note it and PASS for the diff under review."
    phase: 3
  ```

## 4. Process Guidance
- [PG-1] Edit only the `claude-plugins/` copies (`.claude/` resolves through symlinks to the same files per CLAUDE.md). Do not create new files except the directories the runtime creates at execution; this change is text-only in tracked skills/docs.

## 5. Known Assumptions
- [ASM-1] Version bump severity = minor (manifest-dev 2.1.0→2.2.0, manifest-dev-tools 0.16.2→0.17.0). Default: minor. Impact if wrong: a patch bump would also be defensible (behavioral default change, not a new feature); trivial to adjust.
- [ASM-2] `~/.manifest-dev/manifests/` and repo-committed `.manifest/` coexist — the home dir is the in-flight working location; `.manifest/` archival (manual post-session `cp`) is unchanged except its source path. Impact if wrong: none functional; archival still works.

## 6. Deliverables

### Deliverable 1: Durable artifacts default to ~/.manifest-dev/ typed subdirs

**Acceptance Criteria:**
- [AC-1.1] The canonical manifest-location line in `claude-plugins/manifest-dev/skills/define/SKILL.md` defaults to `~/.manifest-dev/manifests/manifest-{ts}.md` (no longer `/tmp` as the primary), with a temp fallback.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/define/SKILL.md. PASS only if the Manifest-encoding sentence now names ~/.manifest-dev/manifests/manifest-{ts}.md as the primary write location and lists /tmp (or $TMPDIR/%TEMP%) only as a fallback when home isn't writable. FAIL if /tmp is still the primary/preferred path. Quote the line."
    phase: 1
  ```
- [AC-1.2] The babysit/lifecycle manifest Output line in `claude-plugins/manifest-dev/skills/define/references/BABYSIT_MODE.md` writes to the same `~/.manifest-dev/manifests/` location (not `$TMPDIR/manifest-{ts}.md`).
  ```yaml
  verify:
    prompt: "Read the ## Output section of claude-plugins/manifest-dev/skills/define/references/BABYSIT_MODE.md. PASS only if it directs the manifest to ~/.manifest-dev/manifests/ (matching /define's durable location) with a temp fallback, and no longer presents $TMPDIR/manifest-{ts}.md as the primary example. Quote the line."
    phase: 1
  ```
- [AC-1.3] The handoff Output line in `claude-plugins/manifest-dev-tools/skills/handoff/SKILL.md` defaults to `~/.manifest-dev/handoffs/handoff-{timestamp}.md` with a temp fallback.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev-tools/skills/handoff/SKILL.md. PASS only if the Output line now writes handoffs to ~/.manifest-dev/handoffs/handoff-{timestamp}.md (with a temp fallback) instead of /tmp/handoff-{timestamp}.md, and the UTC timestamp format + pure-rewrite-on-prior-handoff behavior are preserved. Quote the line."
    phase: 1
  ```
- [AC-1.4] The `--log` (no path) default in BOTH `claude-plugins/manifest-dev/skills/figure-out/references/LOG.md` and `claude-plugins/manifest-dev/skills/figure-out-team/references/LOG.md` is `~/.manifest-dev/logs/figure-out-log-{timestamp}.md` with a temp fallback; the explicit-`--log <path>` and parent-dir-safety bullets are unchanged.
  ```yaml
  verify:
    prompt: "Read both claude-plugins/manifest-dev/skills/figure-out/references/LOG.md and claude-plugins/manifest-dev/skills/figure-out-team/references/LOG.md. PASS only if, in each, the `--log` with no path bullet now defaults to ~/.manifest-dev/logs/figure-out-log-{timestamp}.md (temp as fallback) and the subsequent bullets about `--log <path>` and creating parent dirs only for explicit paths are byte-for-byte unchanged. FAIL with the diff if either file's other bullets changed or the two files diverge in the new default. Quote both new bullets."
    phase: 1
  ```

### Deliverable 2: Downstream docs stop teaching the /tmp manifest path

**Acceptance Criteria:**
- [AC-2.1] The two `/do` quick-start examples in `claude-plugins/manifest-dev/README.md` use `~/.manifest-dev/manifests/manifest-<timestamp>.md`.
  ```yaml
  verify:
    prompt: "Read the Quick Start block of claude-plugins/manifest-dev/README.md. PASS only if both the `/goal /do ...` and `/do ...` example lines reference ~/.manifest-dev/manifests/manifest-<timestamp>.md and neither references /tmp/manifest-<timestamp>.md. Quote both lines."
    phase: 1
  ```
- [AC-2.2] The `/adr` example in `claude-plugins/manifest-dev-tools/skills/adr/SKILL.md` uses the new manifest path.
  ```yaml
  verify:
    prompt: "Read the Example line in claude-plugins/manifest-dev-tools/skills/adr/SKILL.md (the `/adr <manifest> <adr-dir> <session>` example). PASS only if the manifest argument now points under ~/.manifest-dev/manifests/ instead of /tmp/manifest-1234.md. Quote the line."
    phase: 1
  ```
- [AC-2.3] The CLAUDE.md "Manifest Archival" section's `cp` source path and surrounding prose reference `~/.manifest-dev/manifests/` instead of `/tmp/`.
  ```yaml
  verify:
    prompt: "Read the ## Manifest Archival section of CLAUDE.md. PASS only if BOTH the prose ('copy the final manifest from ...') and the `cp` command source path reference ~/.manifest-dev/manifests/ rather than /tmp/. The destination (.manifest/) must remain unchanged. Quote the prose sentence and the cp line."
    phase: 1
  ```

### Deliverable 3: Housekeeping (versions, README sync, lint)

**Acceptance Criteria:**
- [AC-3.1] Both plugin versions are bumped: manifest-dev 2.1.0→2.2.0, manifest-dev-tools 0.16.2→0.17.0.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/.claude-plugin/plugin.json and claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json. PASS only if version is 2.2.0 and 0.17.0 respectively. FAIL with the actual values otherwise."
    phase: 1
  ```
- [AC-3.2] README sync checklist honored: no README or CLAUDE.md describes a component or path the change contradicts; if a moved path is documented anywhere else in root README.md / claude-plugins/README.md, it's consistent. (No new/removed/renamed components here, so component tables need no change.)
  ```yaml
  verify:
    prompt: "Grep the repo (README.md, claude-plugins/README.md, claude-plugins/*/README.md, CLAUDE.md, and all SKILL.md/reference .md under claude-plugins/manifest-dev and manifest-dev-tools) for remaining occurrences of '/tmp/manifest', '/tmp/handoff', and '/tmp/figure-out-log'. PASS only if every remaining occurrence is either (a) an explicitly-out-of-scope ephemeral context, or (b) a deliberate fallback mention within a moved-artifact line. FAIL listing any stale primary reference to the old /tmp path that should have moved. Also confirm no component table rows needed editing (no skills/agents added/removed/renamed)."
    phase: 2
  ```

## Approach note for /do
Phase 1 = make edits + verify each file. Phase 2 = cross-cutting consistency (no stray /tmp primaries, out-of-scope untouched, calibration). Phase 3 = lint/format/typecheck. After all PASS: commit on `claude/manifest-artifact-location-kHv7i`, push with `-u origin`, open a ready-for-review PR.
