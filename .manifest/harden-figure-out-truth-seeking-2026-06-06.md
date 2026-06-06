# Definition: Harden figure-out's truth-seeking process (general-case, anti-bloat)

## 1. Intent & Context
- **Goal:** Make the figure-out skill converge on truth more reliably across ALL uses — general investigations, coding investigations (root-cause and design), and research-style investigations — by weaving a small amount of process rigor into its SKILL.md spine, with a strict replace-before-add / no-bloat discipline. Mode-general (helps interactive and `--autonomous`).
- **Mental Model:** figure-out buys *process trust* (the unraveling was rigorous), not *artifact trust* (which is define→do's job via independent verifiers). The fix is inline awareness in the spine, not new machinery. Two ADRs settle the direction: `docs/adr/20260606-figure-out-process-trust-vs-define-do-artifact-trust.md` and `docs/adr/20260606-harden-figure-out-truth-seeking-inline-defer-independent-pass.md`. The whole change is realistically ~one replaced line + one added line + an optional tight conditional clause. Symlink: `.claude/skills/figure-out` → `claude-plugins/manifest-dev/skills/figure-out` (edit the claude-plugins copy).

## 2. Approach
- **Architecture:** Surgical edits to `claude-plugins/manifest-dev/skills/figure-out/SKILL.md` only (no new files). Then repo housekeeping (version, lint, README check).
- **Execution Order:**
  - D1 (spine edits) → D2 (housekeeping)
  - Rationale: housekeeping/verification depends on the content being final.
- **Risk Areas:**
  - [R-1] Redundancy with existing spine lines (inversion, multi-angle, up-front enumeration already present) | Detect: prompt-reviewer flags unintentional redundancy; manual diff of spine.
  - [R-2] Source-rigor clause bloats the spine | Detect: if it can't be said in ~2 lines gated on external sources, drop it (belongs in deep-research).
  - [R-3] Live-rival-set line collides with BUG.md "one symptom, several causes" | Detect: read both, confirm distinct angles.
- **Trade-offs:**
  - [T-1] Coverage vs leanness → Prefer leanness: drop any line that doesn't pass "would the model miss this by default?" Better to under-add than bloat.
  - [T-2] Catching the never-considered cause completely vs simplicity → Prefer simplicity now: inline rigor raises probability; the independent unanchored pass is deferred (ADR-logged).

## 3. Global Invariants

- [INV-G1] Prompt quality / anti-bloat gate: the modified figure-out SKILL.md passes prompt-review with no MEDIUM+ issues — specifically no unintentional redundancy, no bloat, every changed/added line earns its place.
  ```yaml
  verify:
    prompt: "Review claude-plugins/manifest-dev/skills/figure-out/SKILL.md against prompt-engineering gap-calibration principles, focusing on the changes in this branch (git diff against origin/main or the branch base). FAIL (MEDIUM+) if any added/changed line restates what the spine already says (the spine already covers: 'walk every branch', belief register with evidence-for/against and 'what would change the read', 'verify before asserting; confirm negative findings via a second independent path', holding positions under pushback), or if the change adds a checklist/new section, or if any line would be done by a capable model by default. The net spine growth should be ~one line (one replace + one add + at most a tight conditional clause). Report PASS only if every surviving change closes a real gap and holds at the edges (general across coding/research/general investigations)."
    agent: prompt-reviewer
    phase: 2
  ```
- [INV-G2] Change intent: the edits actually achieve the stated intent (better truth-seeking for all cases) without behavioral divergence or scope creep.
  ```yaml
  verify:
    prompt: "Adversarially verify that the figure-out SKILL.md changes in this branch achieve their stated intent: (1) make the rival/hypothesis set live (regenerate, not just re-weight, when evidence opens/forecloses a region; commit when evidence stops moving the set); (2) add outside-view/reference-class awareness; (3) optionally add a tight conditional external-source-rigor clause. FAIL at LOW+ if any intended behavior is missing, if phrasing is coding-only (must read general — causes for diagnosis AND candidate designs for a decision), or if the commit clause fails to act as a convergence terminator. Cite specific lines."
    agent: change-intent-reviewer
    phase: 2
  ```
- [INV-G3] Scope discipline: none of the explicitly-deferred items are built. No new task/probe files; no `--autonomous`-only machinery; no independent verification/unanchored pass; no non-convergence→/define router; no verifier fan-out in figure-out.
  ```yaml
  verify:
    prompt: "Inspect the full branch diff (git diff against the branch base). PASS only if the figure-out changes are confined to SKILL.md spine prose edits (plus repo housekeeping: plugin.json version, READMEs if needed). FAIL if the diff adds any new file under skills/figure-out/, adds --autonomous-only logic, adds an independent/unanchored verification pass, adds a non-convergence→/define router, or adds verifier fan-out to figure-out. These were explicitly deferred."
    agent: general-purpose
    phase: 2
  ```

## 4. Process Guidance
- [PG-1] Edit the `claude-plugins/manifest-dev/skills/figure-out/SKILL.md` copy (the `.claude/` path is a symlink to it).
- [PG-2] Replace before add: prefer sharpening existing prose over appending new lines.
- [PG-3] No PR-lifecycle steps in this task (commit + push + open PR only; no babysitting).
- [PG-4] High-signal only: if a candidate line is borderline, drop it rather than hedge it in.

## 5. Known Assumptions
- [ASM-1] (auto) Version bump is **minor** (2.3.0 → 2.4.0) — a skill-behavior improvement, not just a typo fix. | Impact if wrong: trivial; could be patch instead.
- [ASM-2] (auto) The source-rigor clause is **kept** as a tight conditional line (not dropped), since it closes a real gap figure-out has today. | Impact if wrong: if it can't be said tightly, INV-G1 will force dropping it — acceptable.
- [ASM-3] (auto) No README component-list change is needed (no new component added); only verify. | Impact if wrong: a README edit gets added.

## 6. Deliverables

### Deliverable 1: figure-out spine rigor edits

**Acceptance Criteria:**
- [AC-1.1] The belief-register paragraph's "Do not stop at the first coherent explanation…" line is REPLACED by a single "live rival set" formulation: rivals are live not fixed up front; regenerate rivals (don't only re-weight) when a finding opens/forecloses a region; commit only once new evidence stops moving the set. Phrasing is investigation-general (rivals = causes for a diagnosis AND candidate designs for a decision).
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md. PASS if the old line 'Do not stop at the first coherent explanation; keep pressing plausible alternatives until remaining unknowns would not materially change the read.' is gone and replaced by a live-rival-set formulation that: (a) says the rival set is not fixed up front, (b) says to regenerate rivals when evidence opens/forecloses a region rather than only re-weighting, (c) includes a commit/stop clause tied to evidence no longer moving the set, and (d) reads general (not coding-only). FAIL otherwise. Quote the new line."
    agent: general-purpose
  ```
- [AC-1.2] Exactly one new line adds outside-view / reference-class awareness (what does this CLASS of problem usually turn out to be — base rates — to surface branches the inside view skipped).
  ```yaml
  verify:
    prompt: "Read the figure-out SKILL.md. PASS if exactly one new line/clause adds outside-view / reference-class awareness (base rate of the problem class), and it is not a restatement of an existing spine line. FAIL if absent, or if more than one line was added for it, or if it duplicates existing content. Quote it."
    agent: general-purpose
  ```
- [AC-1.3] External-source-rigor awareness is present as a TIGHT conditional clause (~≤2 lines), gated on the investigation leaning on external/published sources, composing with the existing 'confirm negative findings via a second independent path' — OR it was deliberately dropped with a reason. It must not be unconditional spine weight.
  ```yaml
  verify:
    prompt: "Read the figure-out SKILL.md. PASS if external-source-rigor awareness (external sources can be unreliable: fabricated/circular/AI-polluted) is either (a) present as a tight conditional clause of ~2 lines or fewer, explicitly gated on leaning on external/published sources, OR (b) absent. FAIL only if it is present but unconditional, longer than ~2 lines, or a standalone new section that bloats the spine. Quote the relevant text or state it is absent."
    agent: general-purpose
  ```
- [AC-1.4] The new live-rival-set line does not duplicate or collide with `skills/figure-out/tasks/BUG.md`'s "one symptom, several causes" probe; coding/RCA coverage holds.
  ```yaml
  verify:
    prompt: "Compare the new live-rival-set line in figure-out SKILL.md with the 'One symptom, several causes' probe in claude-plugins/manifest-dev/skills/figure-out/tasks/BUG.md. PASS if they are distinct angles (BUG.md = could the symptom have multiple simultaneous causes; spine line = regenerate the rival set as evidence shifts the space) and the spine line clearly applies to a coding root-cause investigation. FAIL if they are redundant restatements."
    agent: general-purpose
  ```

### Deliverable 2: Repo housekeeping

**Acceptance Criteria:**
- [AC-2.1] `claude-plugins/manifest-dev/.claude-plugin/plugin.json` version is bumped from 2.3.0 (minor → 2.4.0 per ASM-1).
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/.claude-plugin/plugin.json. PASS if version is greater than 2.3.0 (expected 2.4.0). FAIL otherwise."
    agent: general-purpose
  ```
- [AC-2.2] Lint/format/typecheck pass: `ruff check claude-plugins/ && black --check claude-plugins/ && mypy` (no Python source changed, so this should be clean).
  ```yaml
  verify:
    prompt: "Run: ruff check claude-plugins/ ; black --check claude-plugins/ ; mypy . (from repo root /home/user/manifest-dev). PASS if all succeed with no errors. FAIL with the error output otherwise. BLOCKED if a tool is not installed."
    agent: general-purpose
  ```
- [AC-2.3] README sync verified: confirm no component-list README change is required (no new component added), or apply the change if one is. ADR README index includes the two new 2026-06-06 ADRs.
  ```yaml
  verify:
    prompt: "Verify README sync. (1) Confirm no new skill/agent/component was added (the change is spine prose only), so root README.md, claude-plugins/README.md, and claude-plugins/manifest-dev/README.md need no component-list edits — PASS if they don't reference a now-stale component count for figure-out. (2) Confirm docs/adr/README.md lists both 20260606-* ADRs. FAIL if the ADR index is missing either, or if a README genuinely needed an edit that is absent."
    agent: general-purpose
  ```

## Summary for Approval

**The plan:** Make figure-out better at actually reaching the truth — for any kind of investigation (debugging, design decisions, research, or general thinking) — by adding a small amount of rigor directly into its main instructions, while keeping the skill lean.

**What changes:** Three light touches to figure-out's SKILL.md. (1) Replace the current "don't stop at the first explanation" line with a sharper idea: keep your list of candidate explanations *alive* — when something you learn opens up a possibility that wasn't on the table before, generate the new candidates instead of just re-ranking the old ones, and only settle once new evidence stops shifting the picture. (2) Add one line nudging it to ask "what does this *kind* of problem usually turn out to be?" (base rates), which surfaces causes it might otherwise skip. (3) If (and only if) an investigation is leaning on outside/web sources, a short note that those sources can be wrong or fake. Then routine housekeeping: bump the plugin version, run lint/format/typecheck, check the READMEs.

**Guardrails:** Strict no-bloat — net growth is about one line; nothing that just repeats what figure-out already says; no new files or modes. A bunch of things we discussed are deliberately left for later (an independent "second opinion" pass in autonomous mode, an auto-handoff to /define when things won't converge) and the manifest checks they were NOT built.

**How it's verified:** A prompt-quality reviewer checks for redundancy/bloat, a change-intent reviewer checks the edits do what they claim and read general (not coding-only), and a scope check confirms none of the deferred pieces snuck in. Plus concrete checks on each line, the version bump, lint, and the ADR index.
