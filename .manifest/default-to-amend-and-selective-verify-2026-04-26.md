# Definition: Default-to-Amend Reflex + Full PR/Branch Manifest + Selective Verification

## 1. Intent & Context

- **Goal:** Make the manifest the canonical source of truth for a PR/branch, in three reinforcing ways:
  1. **Default-to-amend reflex** — any user feedback during `/do`, `/verify`, or after completion (same session) defaults to amending the manifest immediately, not handling inline. Pure questions remain inline.
  2. **Full PR/branch capture** — manifests are scoped to the full PR/branch lifetime: `/define` seeds from existing branch diff when commits exist ahead of base; amendments accumulate so the manifest describes the FULL PR state, not just the latest increment.
  3. **Selective verification** — fix-loop iterations run only the failing-criterion's deliverable's ACs + Global Invariants (selection driven by existing deliverable membership + `/do --scope` flag, no new schema field). Full verification runs once before `/done`. Mirrors test-suite economics: incremental fast feedback during work, full suite before merge.

- **Mental Model:**
  - **Manifest = canonical artifact for the PR/branch**, not per-task. One manifest, accumulated via amendments.
  - **Feedback flows through the manifest**, never around it. Amend → resume.
  - **Verification scales with N criteria**. Today every fix-loop iteration re-runs all criteria from Phase 1 — token cost is linear in N × loops. Selective verification breaks the multiplier: only the in-scope deliverables' ACs (driven by existing `/do --scope` and fix-loop's failing-deliverable inference) + globals during loop; full suite once at the end.
  - Existing primitives we leverage: `phase:` field (already gates execution), `--scope D2,D3` on `/do` (limits work), Self-Amendment escalation in `/escalate`, Session-Default Amendment in `/define`. The in-/do `prompt_submit_hook.py` already injects an amendment reminder during /do — left untouched (per user direction, no hook changes; skill-prompt strengthening is enough).
  - Existing gaps the change closes: /do's Mid-Execution Amendment uses hedged "clarifications and confirmations are NOT amendments" framing; /verify runs ALL criteria every cycle ignoring scope; /define doesn't inspect branch diff on fresh start; /done has no documented post-completion feedback handling; /escalate's Self-Amendment template doesn't reflect the default-to-amend strength.

- **Mode:** thorough
- **Interview:** thorough
- **Medium:** local

## 2. Approach

*Initial direction. Three reinforcing changes that share the manifest-as-source-of-truth thesis. Expect adjustment when reality diverges.*

- **Architecture:**
  - **Skill prompt layer only** — no hook changes. The in-/do `prompt_submit_hook.py` already fires during active /do; that's left unchanged. Post-/done feedback handling lives in `/done`'s skill prompt itself. Strengthening default-to-amend lives in `/do`, `/done`, `/escalate`, and `AMENDMENT_MODE.md` — not in injected reminders. (Per user: "Don't want to pollute the context after done unnecessarily for now.")
  - **Skill prompt layer changes** (`/do`, `/verify`, `/done`, `/escalate`, `/define`, `AMENDMENT_MODE.md`) — strengthen Mid-Execution Amendment, add post-/done feedback handling, document /verify-time feedback routing, add branch-diff seeding to /define, state cumulative-manifest rule in AMENDMENT_MODE.md, update /escalate's Self-Amendment template wording for consistency.
  - **Verification scaling** — leverage existing primitives, no new fields. `/verify` gains a "selective mode" that runs only the ACs of the deliverables `/do` is currently scoped to (via existing `--scope D2,D3` flag) plus all Global Invariants. ACs without enclosing scope = first /do pass on a fresh manifest = degenerates to full. After fix-loop iteration, /verify re-runs only the failing-criterion's deliverable + globals. Before `/done`, full suite runs unconditionally. Final gate auto-triggered to preserve the "/done means everything passed" contract. (Earlier draft proposed a new `scope:` field per-AC; per user pushback, dropped — deliverable membership + existing `--scope` is the right granularity.)
  - **Plugin metadata** — version bump (minor), README sync, sync-tools regeneration.

- **Execution Order:**
  - D1 (AMENDMENT_MODE + /define branch awareness — receiver primitives)
  - D2 (/do default-to-amend reframing)
  - D3 (/verify selective verification + full final gate)
  - D4 (/done + /escalate + /verify post-completion feedback routing)
  - D5 (/tend-pr-tick alignment crosslink)
  - D6 (plugin.json version + READMEs + sync-tools)
  - Rationale: receiver primitives (D1) first so other skills can reference them. /do reframing (D2) and /verify selective design (D3) carry the largest behavioral changes. /done + /escalate documentation (D4) closes the post-completion loop. /tend-pr-tick crosslink (D5) is a one-line touch that depends on /do's final wording (D2). README/version/sync (D6) closes the loop.

- **Risk Areas:**
  - [R-1] **Amendment loop oscillation** — repeated Self-Amendment without new external input compounds tokens and can deadlock. | Detect: count consecutive amendments without intervening user message or PR comment in execution log; existing /do guard (R-7) covers this for /do — extend to post-/done case.
  - [R-2] **Pure-question carve-out becomes ambiguous** — model can't reliably distinguish "what does this mean?" from "this is wrong, change it." | Detect: review reminder text + skill prompts for concrete examples; intent reviewer flags ambiguity.
  - [R-3] **No-manifest case (babysit, ad-hoc) regresses** — default-to-amend rule presumes a manifest. | Detect: confirm /tend-pr-tick babysit mode unchanged; confirm /do without prior /define unchanged; tests for hook fail-open when no manifest is in scope.
  - [R-4] **Selective verify misses cross-deliverable regressions** — a fix in D3 touches a shared file that breaks D5's AC; selective mode (D3 only + globals) doesn't catch it. | Detect: mandatory full final gate before /done catches anything the deliverable-scoped pass missed. This is the load-bearing safety mechanism — never skip.
  - [R-5] **Wrong deliverable scope inferred** — /verify must know which deliverables are in scope; if it can't infer correctly from /do args + execution log, the wrong subset runs. | Detect: explicit contract in execution log (AC-3.5) — /do writes the in-scope deliverables list; /verify reads it. No inference.
  - [R-6] **/auto autonomous flow regression** — /auto answers its own questions; if default-to-amend is too aggressive, it could amend in a runaway loop. | Detect: /auto already uses autonomous interview mode; ensure autonomous amend cycle still respects R-1 oscillation guard.
  - [R-7] **Cross-session "in scope" detection** — user returns next day with feedback on yesterday's manifest; without hook changes, /done's skill prompt is the only place that documents the rule. Per user direction, "after" has **no session boundary** — Claude must judge whether a manifest is in scope from any signal (current transcript references, `.manifest/` archives, conversation mentions, file paths). | Detect: skill prompts treat manifest-in-scope as a judgment call (not a mechanical check); when uncertain, ask the user once ("I see manifest X in scope — amend or treat as fresh?"). Skill-prompt language enumerates the heuristic signals: any `/tmp/manifest-*.md` or `.manifest/*.md` mentioned in conversation, current branch's archived manifest in `.manifest/`, manifest path implied by recent /do/verify activity.

- **Trade-offs:**
  - [T-1] Strict default (always amend, no carve-out) vs Pragmatic default (questions inline) → Prefer **Pragmatic** because pure questions amending is absurd ("what does AC-1.1 mean?" amending the manifest with a question note adds noise). Asymmetric: ambiguous cases default to amend (silent scope drift is the worse failure).
  - [T-2] No-manifest case: bootstrap a manifest vs fall back to inline → Prefer **fall back to inline** because the user explicitly noted "do without define is meaningless" — manifest discipline only kicks in once a manifest exists. Don't change babysit semantics.
  - [T-3] Selective verify granularity: per-AC scope tagging vs deliverable-level membership → **Deliverable-level, confirmed by user.** ACs already belong to deliverables; /do already has `--scope D2,D3`; globals always run. Selective verify = in-scope deliverables' ACs + globals. No new field, no path globs, no per-AC tagging burden. The natural unit of selection is the deliverable. (Initial draft proposed per-AC `scope:` glob field — dropped per user pushback as overengineered.)
  - [T-4] Final gate: auto-trigger before /done vs separate user-gated step → **Auto-trigger, hard rule.** Per user: "Done shouldn't be called until all is fully verified and passed. Done means nothing more to do." `/done` is **unreachable** without a full-suite pass. If selective fix-loop reports green, `/verify` immediately runs the full suite — only on full green does `/done` get called.
  - [T-5] `phase:` semantics extension vs new `scope:` field → **No new field — leverage existing structure.** `phase:` keeps its current meaning (ordering gates). Selection granularity = deliverable membership (existing) + `/do --scope` flag (existing). The "incremental verify" behavior emerges from these primitives without introducing a new schema field. (Earlier resolution proposed a separate `scope:` field; reversed per T-3 user pushback.)

## 3. Global Invariants

- [INV-G1] **Prompt quality across all modified prompts.** Every modified `SKILL.md`, `AMENDMENT_MODE.md`, hook docstring, and reminder string passes prompt-reviewer with no MEDIUM+ findings.
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review all modified prompt files in this changeset (SKILL.md files, AMENDMENT_MODE.md, hook reminder strings, README sections describing behavior) against prompt-engineering principles. Report any MEDIUM+ findings — clarity, no conflicts, structure, density, anti-patterns, invocation fit, edge case coverage, emotional tone."
  ```

- [INV-G2] **Intent analysis on the changeset.** change-intent-reviewer reports no LOW+ findings — every change in this changeset achieves its stated intent without behavioral divergence.
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Adversarially analyze whether the changes in this branch achieve their stated intent: (1) any user feedback during /do, /verify, or after defaults to amend manifest; (2) manifests capture full PR/branch changeset; (3) selective verification during fix-loop with auto-triggered full suite before /done. Report behavioral divergences, edge cases that break, and inconsistencies between modified skill files."
  ```

- [INV-G3] **No regression in existing /do amendment behavior.** The current Self-Amendment escalation flow, the in-/do `prompt_submit_hook.py` reminder, and the existing /escalate Self-Amendment template continue to function. This change is skill-prompt only — no hook code changes — so existing hook tests in `tests/hooks/` should still pass unchanged.
  ```yaml
  verify:
    method: bash
    command: "pytest tests/hooks/ -v --tb=short"
  ```

- [INV-G4] **No-manifest case unchanged.** Babysit mode in `/tend-pr-tick`, ad-hoc `/do` invocations without prior `/define`, and the hook's behavior when no manifest path is in scope all continue to work as today (no spurious amendment reminders, no broken flows).
  ```yaml
  verify:
    method: subagent
    agent: code-bugs-reviewer
    prompt: "Audit the changes for regressions in the no-manifest case: (1) /tend-pr-tick babysit mode still fixes directly without amendment routing; (2) /do invoked without prior /define still works; (3) prompt_submit_hook fails open (silent exit) when no manifest path is detectable in transcript or .manifest/. Report any code path that breaks the no-manifest case."
  ```

- [INV-G5] **Selective verification preserves safety.** Selective mode runs in-scope deliverables' ACs + all Global Invariants. The mandatory full final gate before /done is the safety net that catches any cross-deliverable regressions selective mode missed. The final gate is unconditional — no mode override, no opt-out.
  ```yaml
  verify:
    method: codebase
    prompt: "Read /verify SKILL.md and /do SKILL.md. Confirm: (1) selective mode runs in-scope deliverables (per /do --scope) + all INV-G* always; (2) when /do has no --scope, selective mode degenerates to full mode; (3) the full final gate before /done is documented as mandatory and unconditional — no override, no opt-out."
  ```

- [INV-G6] **Pre-PR commands pass.** `ruff check claude-plugins/`, `black --check claude-plugins/`, `mypy`, and `pytest tests/hooks/ -v` all pass clean.
  ```yaml
  verify:
    method: bash
    command: "ruff check claude-plugins/ && black --check claude-plugins/ && mypy && pytest tests/hooks/ -v"
  ```

- [INV-G7] **Plugin version bumped.** `claude-plugins/manifest-dev/.claude-plugin/plugin.json` version increments by minor bump from 0.90.0 (this is a behavior change touching multiple skills).
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; v = json.load(open('claude-plugins/manifest-dev/.claude-plugin/plugin.json'))['version']; major, minor, patch = map(int, v.split('.')); assert (major, minor) >= (0, 91), f'Expected >= 0.91.0, got {v}'\""
  ```

- [INV-G8] **READMEs reflect the new defaults.** Root `README.md`, `claude-plugins/README.md`, and `claude-plugins/manifest-dev/README.md` mention default-to-amend and selective-verification behaviors at the level appropriate to each (overview → behavior).
  ```yaml
  verify:
    method: subagent
    agent: docs-reviewer
    prompt: "Audit README.md (root), claude-plugins/README.md, and claude-plugins/manifest-dev/README.md against the changeset. Verify that the three new behaviors are documented at appropriate levels: (1) default-to-amend reflex (any feedback during/after /do or /verify amends manifest), (2) manifest captures full PR/branch changeset, (3) selective verification during fix-loop + mandatory full final gate before /done. Keep documentation high-level per CLAUDE.md README Guidelines."
  ```

## 4. Process Guidance

- [PG-1] **High-signal changes only.** Flip the existing default; don't add a parallel system. The hook already exists, the Self-Amendment escalation already exists, the `phase:` field already exists. Strengthen and extend; don't reinvent.
- [PG-2] **Trust capability, don't prescribe HOW.** State the default ("amend by default; pure questions answered inline") and provide examples. Don't enumerate decision trees for "is this a question or feedback?"
- [PG-3] **Calibrate emotional tone — low arousal in reminders.** Current hook reminder uses hedged language ("it's worth checking"). Replace with direct ("default to amend") without urgency or pressure framing. Trusted-advisor tone.
- [PG-4] **Manifest = canonical PR/branch artifact.** Throughout all skill prompts, frame the manifest as the source of truth for the PR/branch lifetime, not per-task. Language consistency matters — avoid implying transient or task-scoped framing.
- [PG-5] **Selective verify uses existing primitives.** No new schema field. Selection is driven by deliverable membership (existing) + `/do --scope` flag (existing). Don't introduce per-AC tagging; the natural unit of selection is the deliverable.
- [PG-6] **No mock/conditional verification.** The full final gate before /done runs the actual verifiers — no mocks, no "trust the loop." Per user: "Done means nothing more to do."
- [PG-7] **Treat the final gate as load-bearing.** Selective fix-loop green is a fast-feedback signal, not a completion signal. Resist the urge to skip the auto-triggered final pass even when "nothing meaningful changed since last full pass." The selective loop optimizes work-iteration speed; the final gate is the only completion contract.
- [PG-8] **Default-to-amend reflex is post-/define only.** During an active /define interview, all user feedback shapes the manifest in-place — don't treat in-interview feedback as triggering Self-Amendment. Self-Amendment exists precisely because /define has already finished.

## 5. Known Assumptions

- [ASM-1] **"After" means in-scope, not session-bound.** Per user direction, "after" has no session boundary. Claude judges manifest-in-scope from any signal (transcript references, `.manifest/` archives, conversation context). When uncertain, ask once. *Impact if wrong:* if user wanted strict in-session-only, the hook over-fires across sessions — easy revert by re-adding session boundary.
- [ASM-2] **Pure questions carve-out is desired.** User said "any update/feedback" but "questions about the manifest" don't change state — amending them is absurd. Carve-out is implicit. *Impact if wrong:* if user wants strict (every message → amend, even questions), drop the carve-out from skill prompts.
- [ASM-3] **Final gate respects active /do mode for parallelism + routing — does NOT force thorough.** Per AC-3.6 (mode preservation), final pass runs full suite (every AC + INV) but at the active mode's parallelism and model routing. So efficient-mode /do = full suite at efficient-mode concurrency/models, thorough-mode /do = full suite at thorough concurrency/models. The "full suite" is unconditional; the *intensity per criterion* follows mode. *Impact if wrong:* if user wants final gate to always force thorough regardless of /do mode (safer-but-slower), update AC-3.6 + ASM-4 to flip the rule. (Earlier draft of ASM-4 contradicted AC-3.6 — corrected here per verifier finding.)
- [ASM-4] **Branch-diff seeding triggers when commits exist ahead of base.** /define inspects `git diff <base>...HEAD` (base inferred from upstream tracking branch or origin/main) when starting fresh. If no commits ahead of base, no seeding. *Impact if wrong:* if base inference fails, /define asks user once for the base ref.
- [ASM-5] **/tend-pr-tick is unchanged.** Already routes PR comments through manifest amendment in manifest-aware mode (matches new default); babysit mode is the no-manifest case (unchanged). *Impact if wrong:* if /tend-pr-tick needs to align with new "default to amend" reminder strength, additional file changes needed.

## 6. Deliverables

### Deliverable 1: AMENDMENT_MODE + /define — manifest as full PR/branch artifact

*Files: `claude-plugins/manifest-dev/skills/define/references/AMENDMENT_MODE.md`, `claude-plugins/manifest-dev/skills/define/SKILL.md`. Receiver primitives — written first so other skills can reference.*

**Acceptance Criteria:**

- [AC-1.1] **AMENDMENT_MODE.md states the cumulative manifest rule.** A new section (or expanded "What to Preserve") makes explicit that the manifest is the canonical source of truth for the PR/branch lifetime. After every amendment, the manifest must describe the FULL PR state (intent + all deliverables + all globals + all PG), not just the latest increment. The receiver of an amendment is responsible for ensuring no prior content is silently dropped.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/define/references/AMENDMENT_MODE.md. Confirm it states: (1) manifest is canonical source of truth for the PR/branch lifetime; (2) after amendments, manifest describes full PR state, not just latest increment; (3) prior content must not be silently dropped during amendment. The language should be unambiguous and direct (no hedging like 'should generally')."
  ```

- [AC-1.2] **/define seeds from branch diff when commits exist ahead of base.** A new section in `define/SKILL.md` (or extension of an existing one) directs: when starting a fresh /define and the current branch has commits ahead of its base (default inference: upstream tracking branch, falling back to `origin/main` or `origin/master`), inspect `git diff <base>...HEAD` and incorporate the existing changeset into the manifest's Intent and starting Deliverables as discovered context. The user can confirm/adjust during the interview, but the existing changes are surfaced — not ignored. If base cannot be inferred, ask user once for base ref.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/define/SKILL.md. Confirm a new directive exists: when /define starts fresh on a branch with commits ahead of base, the existing branch diff is inspected and incorporated into Intent + starting Deliverables. Verify base inference order is documented (upstream tracking branch → origin/main → origin/master → ask user). Verify this only applies to fresh /define (not --amend, not Session-Default Amendment of in-session manifest)."
  ```

- [AC-1.3] **Session-Default Amendment language unchanged in spirit, but clarified to extend judgment beyond session.** Per ASM-1 (no session boundary), Session-Default Amendment in /define remains the in-session detection mechanism, but the directive now adds: when a relevant manifest is detectable from any signal (transcript, `.manifest/` archive matching current branch, conversation reference), default to amending it. Explicit `--amend <path>` always wins (unchanged).
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/define/SKILL.md Session-Default Amendment section. Confirm: (1) explicit --amend <path> still wins (unchanged precedence); (2) detection extends beyond in-session signals to include .manifest/ archives matching the current branch and conversation references to manifest paths; (3) when detection is ambiguous, /define asks user once before defaulting to amend; (4) when truly unrelated, fresh /define proceeds with one-line note (unchanged)."
  ```


### Deliverable 2: /do — default-to-amend reflex

*Files: `claude-plugins/manifest-dev/skills/do/SKILL.md`. Largest behavioral reframing — Mid-Execution Amendment becomes the default reflex for any feedback during /do or /verify.*

**Acceptance Criteria:**

- [AC-2.1] **Mid-Execution Amendment section reframed as default reflex.** The current "When to trigger" / "Clarifications and confirmations are NOT amendments" framing is replaced with: "Default to amend. Any user message during /do or /verify defaults to triggering Self-Amendment unless it's a pure question about the manifest or process. When ambiguous, amend." The asymmetric framing (silent scope drift > occasional unnecessary amendment) is explicit.
  ```yaml
  verify:
    method: codebase
    prompt: "Read the Mid-Execution Amendment section in claude-plugins/manifest-dev/skills/do/SKILL.md. Confirm: (1) default reflex is amend (not 'check whether'); (2) carve-out is narrow — only pure questions about manifest/process answered inline; (3) ambiguous cases default to amend with explicit reasoning (silent scope drift is the worse failure); (4) at least one concrete example each of 'amend' (e.g., 'also handle X', 'change Y') and 'inline' (e.g., 'what does AC-1.1 mean?'); (5) no hedged language ('it's worth checking', 'might want to consider')."
  ```

- [AC-2.2] **/verify-time feedback explicitly routed.** `do/SKILL.md` documents that user feedback received while `/verify` is running (between /do invoking /verify and /verify returning) follows the same default-to-amend rule. /verify is non-user-invocable; semantically the feedback is to /do and routes through Self-Amendment.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/do/SKILL.md. Confirm a directive exists stating: user feedback during /verify (which is invoked by /do) is treated as feedback to /do and follows the same default-to-amend rule. /verify itself does not handle user feedback — it forwards to /do's amendment flow."
  ```

- [AC-2.3] **Self-Amendment loop guard preserved + extended.** Existing R-7 guard ("If Self-Amendment escalations repeat without new external input...") is preserved. Extended to cover the post-/done case: if user feedback after /done triggers re-entry to /do via amendment, the same oscillation guard applies — count consecutive amendments without intervening user message or external trigger.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/do/SKILL.md. Confirm: (1) existing R-7 amendment loop guard is preserved (consecutive Self-Amendments without external input → escalate as Proposed Amendment); (2) the guard is documented as also applying to post-/done re-entry via amendment; (3) the guard's purpose is stated (prevent oscillation, prevent token burn)."
  ```

- [AC-2.4] **No-manifest case explicit.** A short note in /do (or in the Mid-Execution Amendment section) clarifies: if /do is invoked without a prior /define (no manifest), default-to-amend doesn't apply — there's nothing to amend. /do without /define is rare and unaddressed by this design (per ASM that "/do without /define is meaningless").
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/do/SKILL.md. Confirm a note exists stating: when /do is invoked without a manifest, the default-to-amend reflex does not apply (no manifest to amend). The note can be brief; the behavior is fail-open (existing inline handling applies)."
  ```

### Deliverable 3: /verify — selective verification (deliverable-level) + mandatory full final gate

*Files: `claude-plugins/manifest-dev/skills/verify/SKILL.md`, `claude-plugins/manifest-dev/skills/do/SKILL.md` (caller contract). No new schema fields — leverages existing deliverable membership + `/do --scope`.*

**Acceptance Criteria:**

- [AC-3.1] **`/verify` runs selectively when /do is scoped, fully when not.** A new section in `verify/SKILL.md` documents two execution modes: (a) **selective pass** — runs ACs only for the in-scope deliverables (passed by /do via existing `--scope D2,D3` flag, or computed from the deliverable owning a failed criterion in fix-loop) plus ALL Global Invariants. (b) **full pass** — runs every AC across every deliverable plus all globals. When /do invokes /verify with no scope (initial /do, all-deliverables run), selective mode degenerates to full. When /do invokes /verify with explicit scope (post-amendment, fix-loop), selective is the default.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/verify/SKILL.md. Confirm: (1) two execution modes documented — selective and full; (2) selective runs in-scope deliverables' ACs + all INV-G* always; (3) the in-scope deliverables come from /do's --scope flag or fix-loop failure context; (4) when no scope is provided, selective degenerates to full (no narrowing); (5) full pass runs every AC across every deliverable + all globals; (6) caller contract is explicit — /verify accepts a scope argument or reads it from execution log."
  ```

- [AC-3.2] **Fix-loop iteration narrows by failing-criterion's deliverable.** When /verify reports failure on AC-X.Y, /do fixes, then /verify re-runs in selective mode scoped to deliverable X (the failing criterion's owner) + all globals. Other deliverables' ACs are not re-run during this iteration — they get their pass at the mandatory full final gate. Documented in /do (caller of /verify) so the fix-loop logic is explicit.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/do/SKILL.md fix-loop section. Confirm: (1) on AC failure, fix-loop re-invokes /verify scoped to the failing criterion's deliverable + globals; (2) other deliverables are NOT re-verified during this iteration; (3) the rationale is documented (cross-deliverable regressions are caught by the mandatory full final gate); (4) when an INV-G fails, fix-loop re-runs that INV (globals always run); not deliverable-scoped."
  ```

- [AC-3.3] **`/done` is unreachable without a full-pass green — hard gate.** /verify's outcome handling: when called in selective mode and all selected criteria pass, /verify does NOT call /done. Instead, it auto-triggers the full pass (re-invokes itself in full mode) — only on full green does it call /done. /done is never reachable from selective-mode green alone. Per user directive: "Done means nothing more to do."
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/verify/SKILL.md outcome handling section. Confirm: (1) selective-mode green does NOT call /done — instead triggers full pass automatically; (2) only full-mode green calls /done; (3) the directive is unconditional (no mode override, no opt-out) — per user directive 'Done means nothing more to do'; (4) if the auto-triggered full pass fails, /verify enters the standard fix-loop reporting (returns failures to /do, no /done)."
  ```

- [AC-3.4] **Phase semantics preserved unchanged.** The existing `phase:` field meaning (Phase N+1 only runs if N passes; ascending order) is unchanged. Within a selective pass, phases still gate execution — selective filters by deliverable, then runs the filtered set in phase order.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/verify/SKILL.md. Confirm: (1) phase: field semantics are unchanged (ordering gates, ascending); (2) within a selective pass, phases still gate execution (selective filters by deliverable membership, then runs filtered set in phase order); (3) no conflation of phase ordering with deliverable selection."
  ```

- [AC-3.5] **Execution log records each pass type and scope (parseable contract).** Each /verify invocation logs a structured block at a known location with a parseable shape. Contract: a Markdown section header `## /verify pass {N}` followed by a fenced-yaml block with keys `mode: selective|full`, `scope: [<deliverable-id>, ...]` (empty list when full), `result: pass|fail`, `failures: [<criterion-id>, ...]` (empty when pass). /verify and /do read this to track what's been verified and what triggered the next pass. Pure markdown for humans; fenced YAML for deterministic parsing.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/do/SKILL.md and claude-plugins/manifest-dev/skills/verify/SKILL.md. Confirm: (1) execution log structured block contract is documented (markdown header + fenced YAML with keys mode, scope, result, failures); (2) the contract is unambiguous enough that /verify and /do can parse it without heuristics; (3) the convention lives in one canonical place (probably /verify SKILL.md, referenced from /do); (4) auto-triggered full pass is logged distinctly so audit trail shows the mandatory gate ran."
  ```

- [AC-3.6] **Mode-aware behavior preserved.** The existing execution modes (efficient/balanced/thorough) continue to control parallelism + model routing within each /verify pass. Selective vs full is orthogonal — both pass types respect the active mode. (Final full pass in efficient mode = every criterion verified, but at efficient mode's concurrency + model routing.)
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/do/references/execution-modes/efficient.md, balanced.md, thorough.md, and verify/SKILL.md. Confirm: (1) selective vs full is orthogonal to mode; (2) both pass types respect active mode for parallelism + model routing + skip rules; (3) the interaction is documented unambiguously — no mode 'forces' a pass type."
  ```

### Deliverable 4: /done + /escalate + /verify post-completion feedback routing

*Files: `claude-plugins/manifest-dev/skills/done/SKILL.md`, `claude-plugins/manifest-dev/skills/escalate/SKILL.md`, `claude-plugins/manifest-dev/skills/verify/SKILL.md`. Closes the loop on what happens after completion. Per user direction, /done and /escalate skill prompts carry the post-completion rule (no hook changes).*

**Acceptance Criteria:**

- [AC-4.1] **/done documents post-completion feedback default.** A new section in `done/SKILL.md` states: after /done has been called, if user feedback arrives in the same context (manifest still in scope per ASM-1's no-session-boundary rule), the default reflex is to amend the manifest and re-enter /do via `/define --amend <manifest>` followed by `/do <manifest> <log> --scope <new-or-affected-deliverables>`. Pure questions answered inline (consistent with /do's carve-out).
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/done/SKILL.md. Confirm a new section exists: (1) post-/done user feedback defaults to amend + re-enter /do; (2) pure questions remain inline (consistent with /do); (3) re-entry uses /define --amend then /do with --scope to limit work to new/affected deliverables; (4) the manifest-in-scope judgment is the same as /do's (per ASM-1, no session boundary)."
  ```

- [AC-4.2] **/verify documents user-feedback-during-verify routing.** A note in `verify/SKILL.md` (Principles or new section) clarifies: /verify is non-user-invocable orchestrator; user feedback received while /verify is running is semantically feedback to /do (which called /verify). /verify itself does not handle the feedback — the message arrives in the parent context, where /do's default-to-amend reflex applies.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/verify/SKILL.md. Confirm a directive exists clarifying: (1) /verify is non-user-invocable; (2) user feedback during /verify routes to /do (caller); (3) /verify does not handle feedback inline — it forwards via the orchestration context; (4) cross-reference to /do's default-to-amend reflex (so the rule lives in one place, not duplicated)."
  ```

- [AC-4.3] **/done remains called only by /verify after full-suite green.** Per AC-3.3, /done is unreachable except via /verify's full-pass green. /done's existing principle ("Called by /verify only") is preserved and strengthened to: "/verify only after a full-suite pass — never from selective-mode green alone."
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/done/SKILL.md. Confirm: (1) existing 'Called by /verify only' principle is preserved; (2) it's strengthened to specify /verify must have completed a full-suite pass (not just a selective-mode green); (3) the language is explicit and direct (no hedging); (4) cross-references AC-3.3's hard gate."
  ```

- [AC-4.4] **No-manifest case after /done.** Brief note: if /do completed without ever having a manifest (rare, but possible if the user manually invoked /do then /verify then /done somehow), post-completion feedback reverts to inline handling — no manifest to amend. Consistent with AC-2.4.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/done/SKILL.md. Confirm: (1) a brief note covers the no-manifest case after /done; (2) behavior is fail-open (inline handling); (3) consistent with AC-2.4's no-manifest carve-out in /do."
  ```

- [AC-4.5] **/escalate Self-Amendment template aligned with default-to-amend strength.** The Self-Amendment template in `escalate/SKILL.md` already exists (the mechanism). Update its framing to match the strengthened default: opening line states this is the standard reflex when user feedback or PR review contradicts/extends the manifest, not a fallback for ambiguous cases. Cross-references /do's Mid-Execution Amendment and /done's post-completion routing so all three skills present the same rule. The template's structural fields (Trigger, Affected items, What changed, Manifest path, Execution log path) are unchanged — wording around them strengthens.
  ```yaml
  verify:
    method: codebase
    prompt: "Read the Self-Amendment section in claude-plugins/manifest-dev/skills/escalate/SKILL.md. Confirm: (1) opening framing presents Self-Amendment as the standard reflex for user/reviewer feedback that contradicts or extends the manifest (not a fallback); (2) it cross-references /do's Mid-Execution Amendment and /done's post-completion routing — so the rule lives canonically in /do but is reinforced consistently across skills; (3) structural fields (Trigger, Affected items, What changed, Manifest path, Execution log path) are unchanged; (4) language strength matches /do AC-2.1 (no hedging like 'consider', 'might want to')."
  ```

### Deliverable 5: /tend-pr-tick alignment crosslink

*Files: `claude-plugins/manifest-dev/skills/tend-pr-tick/SKILL.md`. Single-line crosslink to keep behavior consistent across PR comments and in-session feedback.*

**Acceptance Criteria:**

- [AC-5.1] **/tend-pr-tick references the default-to-amend reflex.** A short note in the Routing section confirms that manifest-aware mode's amend-then-/do flow is the same default-to-amend reflex documented in /do (cross-reference, not duplication). Babysit mode is unchanged. The crosslink prevents the two flows from drifting.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev/skills/tend-pr-tick/SKILL.md Routing section. Confirm: (1) a one-line crosslink references /do's default-to-amend reflex (Mid-Execution Amendment); (2) no duplication of the rule (the canonical statement lives in /do); (3) babysit mode language is unchanged; (4) the cross-reference makes alignment between PR-comment routing and in-session feedback routing explicit."
  ```

### Deliverable 6: Plugin metadata + full README reconciliation

*Files: `claude-plugins/manifest-dev/.claude-plugin/plugin.json`, every `README.md` in the marketplace tree, `dist/`. Per user direction: "Ensure also readmes all around are fully aligned with the actual behavior in general reconcile" — this is a broader audit, not just additive mentions for the new behaviors.*

**Acceptance Criteria:**

- [AC-6.1] **plugin.json version bumped to 0.91.0.** Minor bump from 0.90.0 — this is a behavior change touching multiple skills. Patch is insufficient (per CLAUDE.md: minor = new features/skills/agents; behavior changes qualify).
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; v = json.load(open('claude-plugins/manifest-dev/.claude-plugin/plugin.json'))['version']; assert v == '0.91.0', f'Expected 0.91.0, got {v}'\""
  ```

- [AC-6.2] **All marketplace READMEs reconciled with actual current behavior.** Every README in scope is audited against the current state of the code/skills it describes — not just for the new defaults from this changeset, but for any pre-existing drift. READMEs in scope: root `README.md`, `claude-plugins/README.md`, `claude-plugins/manifest-dev/README.md`, `claude-plugins/manifest-dev-experimental/README.md`, `claude-plugins/manifest-dev-tools/README.md`, `claude-plugins/PLUGIN_TEMPLATE/README.md`, `claude-plugins/manifest-dev/skills/define/tasks/references/research/README.md`. Each is updated where claims no longer match behavior. The new behaviors from this changeset (default-to-amend, full PR/branch capture, selective verification with mandatory full final gate) are reflected at appropriate levels — overview in root README, plugin-level detail in manifest-dev README, brief in marketplace plugin table.
  ```yaml
  verify:
    method: subagent
    agent: docs-reviewer
    prompt: "Audit every README.md in this repo against the current state of code and skills it describes. READMEs in scope: README.md (root), claude-plugins/README.md, claude-plugins/manifest-dev/README.md, claude-plugins/manifest-dev-experimental/README.md, claude-plugins/manifest-dev-tools/README.md, claude-plugins/PLUGIN_TEMPLATE/README.md, claude-plugins/manifest-dev/skills/define/tasks/references/research/README.md. For each: (1) flag claims that no longer match actual skill/plugin/code behavior (any drift, not just from this changeset); (2) confirm the new behaviors are documented at appropriate levels — root README mentions default-to-amend + full-PR-capture + selective-verification at overview level; manifest-dev README documents at plugin-decision level; marketplace plugin table description fits. Per CLAUDE.md README Guidelines: keep high-level, no implementation detail. Report any unreconciled drift."
  ```

- [AC-6.3] **Marketplace plugin table accurate.** `claude-plugins/README.md` plugin table — manifest-dev row's description fits current behavior; other rows audited for drift. Updated where misrepresentation exists.
  ```yaml
  verify:
    method: subagent
    agent: docs-reviewer
    prompt: "Read claude-plugins/README.md plugin table. For each row, confirm the description matches the plugin's actual surface (read each plugin's plugin.json and SKILL.md files to verify). Pay special attention to manifest-dev row given this changeset. Report any misrepresentation."
  ```

- [AC-6.4] **Multi-CLI distributions regenerated via sync-tools.** The `sync-tools` skill is invoked (or its underlying script is run) as part of pre-PR finalization, regenerating `dist/codex/`, `dist/gemini/`, `dist/opencode/` from the updated source. After regeneration, `git status --porcelain dist/` is empty (regenerated content matches committed state). Verification runs sync-tools fresh, then asserts no drift — catching cases where /do completed without invoking sync-tools.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Verify dist/ regeneration was run as part of this changeset. Steps: (1) confirm the sync-tools skill or its underlying script was invoked during /do (check execution log for sync-tools invocation, OR run sync-tools dry-run/check mode now and confirm it would produce no changes); (2) run sync-tools (or its underlying script) in the working tree; (3) run `git status --porcelain dist/` and confirm output is empty (no drift between regenerated content and what was committed). Report any drift or missing invocation."
  ```

## 7. Amendments

*None yet. New amendments append here per AMENDMENT_MODE.md conventions.*
