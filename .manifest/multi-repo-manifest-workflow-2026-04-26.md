# Definition: Multi-Repo Manifest Workflow

## 1. Intent & Context

- **Goal:** Make a single canonical manifest the source of truth for changesets that span multiple repos and PRs — including amendments — without forcing the user to hold cross-repo coherence in their head, and without engineering coordinator infrastructure.
- **Mental Model:**
  - One `/tmp` manifest, no repo "owns" it. Manifest is **internal** (not surfaced to reviewers).
  - `/do` works across repos as deliverables require — navigates paths declared in `Repos:`. **No filter logic** in `/do`; the LLM handles repo navigation natively. User can invoke `/do` once globally, or per-repo with `--scope`; either works.
  - `Repos:` and `repo:` tags exist for **documentation** and for `/tend-pr-tick` scope inference (which deliverables map to which PR for amendment routing) — not as a `/do` enforcement mechanism.
  - Cross-repo gates encoded as `method: deferred-auto` criteria — automatically verifiable but user-triggered (`/verify --deferred`). User is the coordinator.
  - Schema additions are **conditional** — single-repo manifests look exactly as today.
- **Mode:** thorough
- **Interview:** thorough
- **Medium:** local

## 2. Approach

- **Architecture:**
  - One shared convention doc — `claude-plugins/manifest-dev/skills/define/references/MULTI_REPO.md` — owns the multi-repo workflow rules. Skills (`/define`, `/do`, `/verify`, `/tend-pr`, `/done`, `AMENDMENT_MODE`) point to it, don't duplicate.
  - Schema additions live in `/define`'s manifest schema as conditional fields (`Repos:` in Intent + `repo:` on deliverables), shown only when multi-repo applies.
  - `/do` gains **no behavioral logic** — the LLM navigates paths declared in `Repos:` natively as deliverables require. Only the doc gets a small note clarifying this navigation behavior + the wording flex.
  - `/verify` gains `method: deferred-auto` and a `--deferred` invocation that runs only deferred-auto criteria; normal flow skips them.
  - `/tend-pr` runs per-repo against its repo's PR; all ticks amend the same canonical manifest. No locking — accept rare collisions.
  - `AMENDMENT_MODE` and `do/SKILL.md` flex "PR/branch" → "PR set / branch set" (no logic change).

- **Execution Order:**
  - D1 → D2 → D3 → D4 → D5 → D6 → D7 → D10 → D11 → D8 → D9
  - Rationale: Write the convention doc first (D1). Update `/define` schema (D2). Update `/do` (D3) and `/verify` (D4) to consume the conditional schema. Update `/tend-pr` (D5) and `/done` (D6) for multi-PR semantics. Flex AMENDMENT_MODE wording (D7). Replicate /tend-pr-style multi-PR pattern in `/drive` + `/drive-tick` (D10). Add /auto multi-repo footgun note (D11). Bump versions for both plugins + sync READMEs (D8). Verify single-repo backward compat unchanged (D9 — final regression check).

- **Risk Areas:**
  - [R-1] Single-repo regression — schema additions or filter logic accidentally affect single-repo flow. | Detect: existing single-repo manifests/tests behave identically.
  - [R-2] Convention drift across skills — each skill describes multi-repo subtly differently, especially across the two affected plugins (`manifest-dev`, `manifest-dev-experimental`). | Detect: convention doc is the only source of truth; skills only reference it (enforced by INV-G4 across all 10 affected files).
  - [R-3] `deferred-auto` over-engineered — concept introduced but rarely used. | Detect: post-implementation watch-item — if no real multi-repo task uses `deferred-auto` within first ~3 dogfooding cycles, propose simplifying in a follow-up. Not gated by an AC; this risk is accepted, not verified.
  - [R-4] LLM-navigation across repos in one `/do` invocation hits repo-state surprises (uncommitted changes, branch mismatches, missing remotes) that the agent doesn't surface clearly. | Detect: PG-7 instructs implementer to leave repo-state assumptions explicit in MULTI_REPO.md and let escalation surface failures; no special handling.
  - [R-5] Doc-only changes silently contradict actual behavior — rules written but skills don't reflect them. | Detect: every behavioral rule in MULTI_REPO.md is mirrored in the relevant skill's behavior section (enforced by INV-G4).

- **Trade-offs:**
  - [T-1] Always-on schema vs conditional → Prefer **conditional** because zero overhead on single-repo (the common case) outweighs uniformity.
  - [T-2] Reuse `phase:` semantics for cross-repo gates vs new `deferred-auto` method → Prefer **`deferred-auto`** because reusing phase breaks `/verify`'s "all phases run sequentially" mental model.
  - [T-3] Detail in MULTI_REPO.md vs inline in each skill → Prefer **MULTI_REPO.md as single source**, skills point to it. DRY.
  - [T-4] Engineer concurrency for parallel `/tend-pr` amendments vs accept collisions → Prefer **accept collisions**. Ticks are slow; engineering locks adds complexity disproportionate to risk.
  - [T-5] Persistence engineering for `/tmp` manifest vs accept ephemerality → Prefer **accept ephemerality**. Re-run `/define` if lost; don't engineer durability.

## 3. Global Invariants

- [INV-G1] **change-intent-reviewer** finds no LOW+ issues on the diff.
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Review the diff in this branch against the stated intent: extending the manifest workflow so a single /tmp manifest is the source of truth across multiple repos/PRs, with conditional schema fields, repo-filtered /do, deferred-auto cross-repo gates, and no infrastructure for coordinator passes/persistence/concurrency. Flag any LOW+ behavioral divergence."
  ```

- [INV-G2] **prompt-reviewer** finds no MEDIUM+ issues across changed skill files and references.
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review changed prompts (define/SKILL.md, do/SKILL.md, verify/SKILL.md, tend-pr/SKILL.md, tend-pr-tick/SKILL.md, done/SKILL.md, auto/SKILL.md, AMENDMENT_MODE.md, MULTI_REPO.md, drive/SKILL.md, drive-tick/SKILL.md) for clarity, conflicts, anti-patterns, and structural issues. Flag any MEDIUM+ findings."
  ```

- [INV-G3] **Single-repo backward compat:** existing single-repo manifests and flows behave identically after the change. No new required fields. No new required steps in the single-repo path. **No new code paths in /do or /verify** (multi-repo support is doc + schema, not behavior).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Confirm: (1) the manifest schema in define/SKILL.md keeps Repos: and repo: fields explicitly conditional/optional with the single-repo path as default; (2) /do has NO new repo-filter logic, NO cwd matching, NO new code paths — only a doc note about LLM navigation when Repos: is present; (3) /verify --deferred is a new flag that does not affect default invocations; (4) /tend-pr behavior is unchanged when only one repo/PR is involved; (5) AMENDMENT_MODE wording change preserves the singular case for single-repo; (6) /auto behavior is unchanged for single-repo manifests; (7) /drive and /drive-tick behavior is unchanged for single-repo manifests. Read each affected file end-to-end. Report PASS/FAIL with evidence."
  ```

- [INV-G4] **Single source of truth for the convention:** every multi-repo rule lives in `references/MULTI_REPO.md`. Skill files only summarize and link out — they do not redefine rules.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Open MULTI_REPO.md and each skill file (define, do, verify, tend-pr, tend-pr-tick, done, auto, AMENDMENT_MODE, drive, drive-tick). For every multi-repo rule mentioned in a skill file, confirm the canonical statement is in MULTI_REPO.md and the skill references it (does not redefine or contradict). Flag duplicated definitions or contradictions. Report PASS/FAIL with citations."
  ```

- [INV-G5] **No singular-only 'PR/branch' wording where the changeset can span multiple.** AMENDMENT_MODE.md, do/SKILL.md, drive/SKILL.md, and drive-tick/SKILL.md flex from "the PR/branch" to "PR set / branch set" or equivalent that covers both cases.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read AMENDMENT_MODE.md, do/SKILL.md, drive/SKILL.md, drive-tick/SKILL.md. For every occurrence of 'PR/branch' or singular 'the PR' / 'the branch' that refers to the canonical-source-of-truth concept, confirm wording has been flexed to cover the multi-PR/multi-branch case (e.g., 'PR set / branch set' or equivalent that names both single and multi cases). Quote each occurrence and assert PASS or FAIL. Singular wording in unrelated contexts (e.g., specific operations on a single PR) is fine and should not be flagged."
  ```

- [INV-G6] **Lint / format / typecheck pass:**
  ```yaml
  verify:
    method: bash
    command: "cd /home/user/manifest-dev && ruff check claude-plugins/ && black --check claude-plugins/ && mypy"
  ```

## 4. Process Guidance

- [PG-1] **High-signal changes only.** Don't restructure existing single-repo guidance unless the multi-repo work directly requires it. One edge case doesn't warrant restructuring.
- [PG-2] **Schema additions stay conditional.** Never make `Repos:` or `repo:` required. Single-repo path must look identical to today.
- [PG-3] **MULTI_REPO.md is the canonical source.** When tempted to inline a rule into a skill file, write a one-line summary + link to MULTI_REPO.md instead.
- [PG-4] **No concurrency/persistence engineering.** Resist the pull to add file locks, archival, retry logic. The user's stance is explicit: accept ephemerality, accept rare collisions.
- [PG-5] **No coordinator infrastructure.** Don't add a coordinator pass, primary repo concept, or cross-repo orchestrator. User-as-coordinator via `/verify --deferred` is the design.
- [PG-6] **Calibrate emotional tone (PROMPTING default).** All prompt edits stay low-arousal — no urgency language, excessive praise, or pressure framing. "Trusted advisor" tone. Failure normalized in iterative skills.
- [PG-7] **Trust LLM navigation; don't add filter logic.** `/do` and `/verify` already navigate paths via the LLM; do not add cwd-matching, repo-filter, or path-resolution code paths. When a deliverable lives in a different repo than cwd, the LLM reads the manifest's `Repos:` map and navigates. Doc additions describe the convention, not enforcement.

## 5. Known Assumptions

- [ASM-1] Convention doc lives at `claude-plugins/manifest-dev/skills/define/references/MULTI_REPO.md`. Default chosen by precedent (AMENDMENT_MODE.md sits in the same place and is referenced by `/do`). Impact if wrong: file moves, all references update.
- [ASM-2] Branch coordination = same branch name across repos by convention; manifest records the branch name (single string, since names match). The harness already declares per-repo branches with the same name. Impact if wrong: schema needs `Branch:` to become `Branches: [name -> branch]` map.
- [ASM-3] `/do` navigation across repos relies on the LLM reading `Repos:` from manifest Intent and using absolute paths in tools. No filter logic, no cwd matching. Impact if wrong: agent may need a hint via PG or doc note; not a code change.
- [ASM-4] `/verify --deferred` runs without `--scope`; covers all `method: deferred-auto` criteria across the manifest. Verifier agents receive `Repos:` paths from Intent for cross-repo file access. Impact if wrong: invocation may need `--repo` filter or per-criterion scoping.
- [ASM-5] Multi-repo support is implemented for "code repos" but the conventions are written in a way that doesn't preclude future extension to non-code/non-git "scope sets" (e.g., research with multiple data sources). No special accommodations made today. Impact if wrong: doc may need a generalization pass.
- [ASM-6] PROMPTING task file's "Defaults" — *Identify skill type*, *Assess config needs*, *Probe for memento needs*, *Define empty input behavior* — do not apply to this task. This is updates across existing skills, not creation of a new skill type, so type/config decisions are inherited from the affected skill, no memento additions, and empty-input behavior is unchanged. *Emotional tone* default IS applied — encoded as PG-6.
- [ASM-7] PROMPTING quality gate thresholds adopted as written from `tasks/PROMPTING.md`: change-intent-reviewer at "no LOW+" (INV-G1), prompt-reviewer at "no MEDIUM+" (INV-G2). The skill-specific gates (Folder architecture, Progressive disclosure, Gotchas, Description as trigger) do not apply because no new skill is being created — only existing skills updated and one new reference doc (MULTI_REPO.md) which is not a skill. Impact if wrong: tighten thresholds or add additional gates per task file.

## 6. Deliverables

*Document order is D1–D8, then D10, D11, D9. D9 (final regression check) is intentionally last in execution even though its ID precedes D10/D11 — execution order is recorded in Approach §Execution Order. /do extracts deliverables by ID, so document order is informational.*

### Deliverable 1: MULTI_REPO.md Convention Doc

**Repo:** `manifest-dev` (single-repo task — `Repos:` field omitted; this is a non-multi-repo manifest about *adding* multi-repo support)

**Acceptance Criteria:**

- [AC-1.1] File exists at `claude-plugins/manifest-dev/skills/define/references/MULTI_REPO.md` and covers: (a) the principle (manifest = source of truth across PRs, internal-only), (b) `/tmp` ephemerality (no archival, re-run if lost), (c) `Repos: [name: path]` registration in Intent + `repo:` deliverable tag (purpose: **documentation only**; consumer skills like `/tend-pr-tick` may use it for scope inference, but `/define`/`/do`/`/verify`/`/done` do not), (d) `/do` navigates across repos via the LLM reading `Repos:` and using absolute paths — no filter logic, no cwd matching, (e) `method: deferred-auto` semantics + `/verify --deferred` + **deferred-pending escalation routing** — when normal /verify flow completes green but deferred-auto criteria remain unverified, /verify routes to /escalate ("Deferred-Auto Pending") instead of /done, signaling that the user must run /verify --deferred when prerequisites are ready, (f) shared-manifest amendment pattern across PRs — concurrent amendments are last-writer-wins, no locking; described abstractly without naming `/tend-pr` or `/drive` as core (those skills are optional add-ons that ride this pattern), (g) **`/done` fires once per manifest, gated on no deferred-auto pending** — for multi-repo, `/done` means every AC across every repo's deliverables is green AND every deferred-auto criterion has been verified green via /verify --deferred; the summary lists which repos' deliverables were verified, (h) the user-as-coordinator stance, (i) `/auto` multi-repo behavior (single invocation handles cwd's slice of work for `/tend-pr` only — `/do` itself navigates all repos), (j) **branch-name convention**: same branch name across all repos by default (matches harness pattern); manifest's Intent records the branch name as a single string. Divergent names per repo are not supported by this version.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev/skills/define/references/MULTI_REPO.md. Confirm each of the 10 sections (a-j listed in AC-1.1) is present and substantive. Flag any missing or stub-only section. Report PASS/FAIL with section-by-section evidence."
  ```

- [AC-1.2] MULTI_REPO.md is written as a reference doc (not a how-to) — declarative rules with rationale, no step-by-step prescriptions.
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review claude-plugins/manifest-dev/skills/define/references/MULTI_REPO.md for prompt-engineering quality: WHAT and WHY, not HOW. Flag prescriptive HOW patterns, weak language, anti-patterns. No MEDIUM+ findings."
  ```

- [AC-1.3] MULTI_REPO.md contains at least one **worked example** for each of: the conditional schema (Intent's `Repos:` block + a deliverable's `repo:` tag), `/do` navigating across repos (sample invocation + showing the LLM uses absolute paths from `Repos:`), and a `method: deferred-auto` criterion (sample YAML block). Examples make the rules concrete and reduce implementer guessing.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read MULTI_REPO.md. Confirm worked examples exist for: (1) conditional schema (Repos: + repo: tag in a manifest snippet), (2) /do navigating across repos using paths from Repos: (no filter logic shown — just the agent navigating), (3) method: deferred-auto criterion YAML block. Each example must be a real code/yaml block, not just prose. Report PASS/FAIL."
  ```

### Deliverable 2: /define — Conditional Multi-Repo Schema

**Acceptance Criteria:**

- [AC-2.1] `define/SKILL.md` "Multi-Repo Scope" section is rewritten to reference MULTI_REPO.md as canonical, summarize the conditional schema additions (Intent's `Repos: [name: path]` and deliverables' `repo: name` field), and clarify that single-repo manifests omit these fields entirely. **The section must NOT mention `/tend-pr`, `/tend-pr-tick`, or `/drive`** — `/define` is core and stays decoupled from optional PR-tending tools. The `repo:` tag's stated purpose is "documentation" only.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read define/SKILL.md Multi-Repo Scope section. Confirm: (1) links to MULTI_REPO.md; (2) summarizes (does not redefine) Repos and repo: tagging; (3) explicitly states single-repo manifests omit these fields; (4) does NOT mention /tend-pr, /tend-pr-tick, or /drive (core skill stays decoupled from optional add-ons). Report PASS/FAIL with quoted lines."
  ```

- [AC-2.2] The Manifest Schema example in `define/SKILL.md` shows the conditional fields with comments marking them as optional/multi-repo-only, in a way that makes the single-repo path obvious at a glance. The example includes: `Repos: [name: path]` in Intent, optional `Branch: <name>` in Intent (single string per AC-1.1(j)), and `repo: <name>` on a deliverable.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read the Manifest Schema example in define/SKILL.md. Confirm: (1) Repos: shown with 'optional, multi-repo only' annotation; (2) Branch: shown as optional single string; (3) repo: on a deliverable shown with same annotation; (4) a reader skimming the schema can tell single-repo manifests omit all three. Report PASS/FAIL."
  ```

- [AC-2.3] Detection: `define/SKILL.md` does NOT add a special multi-repo probe step. Multi-repo recognition flows through normal context/domain grounding (Coverage Goal: Domain Understanding). The Multi-Repo Scope section includes a one-line note explaining this — *"Multi-repo detection rides on the existing Domain Understanding coverage goal: when conversation, task description, or branch context indicates multiple repos, treat as multi-repo and populate Repos: accordingly. No separate probe step is added."* — or equivalent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read define/SKILL.md. Confirm: (1) no new multi-repo-specific probe/question step is added; (2) the Multi-Repo Scope section explicitly states detection rides on Domain Understanding via conversation/task description/branch context; (3) no contradiction with the existing Domain Understanding section. Report PASS/FAIL with quoted lines."
  ```

### Deliverable 3: /do — Multi-Repo Navigation Note + Wording Flex (no behavioral change)

**Acceptance Criteria:**

- [AC-3.1] `do/SKILL.md` adds a small note documenting multi-repo navigation: when manifest has `Repos:`, `/do` reads the path map and uses absolute paths in tool calls (Read/Edit/Write/Bash). **No filter logic, no cwd matching, no per-repo configuration.** The LLM navigates as deliverables require. Single-repo behavior unchanged (no `Repos:` field → no navigation note triggers). Reference MULTI_REPO.md for full convention.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read do/SKILL.md. Confirm: (1) multi-repo navigation note added with explicit 'no filter logic, no cwd matching' statement; (2) note that LLM uses absolute paths from Repos:; (3) explicit statement that single-repo (no Repos: field) is unchanged; (4) link to MULTI_REPO.md. Confirm there is NO new repo-filter or cwd-matching code/rule. Report PASS/FAIL with citations."
  ```

- [AC-3.2] Wording flex: where `do/SKILL.md` says "the PR/branch" referring to canonical-source-of-truth, it accommodates the multi-PR case (e.g., "PR set / branch set" or equivalent that names both single and multi cases).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read do/SKILL.md end-to-end. For every occurrence of 'PR/branch' or singular 'the PR' / 'the branch' that refers to the canonical-source-of-truth concept, confirm wording has been flexed to cover the multi-PR/multi-branch case (e.g., 'PR set / branch set' or equivalent that names both single and multi cases). Quote each occurrence and assert PASS or FAIL. Singular wording in unrelated contexts (e.g., specific operations on a single PR) is fine and should not be flagged."
  ```

### Deliverable 4: /verify — `deferred-auto` Method + `--deferred` Flag

**Acceptance Criteria:**

- [AC-4.1] `verify/SKILL.md` documents `method: deferred-auto` as a new criterion method: automatically verifiable but skipped during normal `/do→/verify` flow, runnable only via `/verify --deferred`. Rationale: user signals when prerequisites (e.g., all PRs deployed) are ready. **Deferred-pending escalation:** when normal /verify completes green but the manifest contains deferred-auto criteria that have not yet been verified green (no prior `deferred: true result: pass` block in the execution log covering them), /verify routes to /escalate with a "Deferred-Auto Pending" type — NOT to /done. The escalation message instructs the user to run `/verify --deferred` when prerequisites are in place. Once /verify --deferred completes green for all such criteria, a subsequent normal /verify pass can call /done.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read verify/SKILL.md. Confirm: (1) method: deferred-auto is documented with semantics; (2) normal /verify invocations skip these criteria; (3) /verify --deferred invocation is documented; (4) when normal /verify completes green but deferred-auto criteria remain unverified, /verify routes to /escalate (type: Deferred-Auto Pending) instead of /done; (5) /done is reachable only after deferred-auto criteria have been verified green via /verify --deferred. Report PASS/FAIL with citations."
  ```

- [AC-4.2] `--deferred` flag interactions are explicit: (i) **mutually compatible with `--scope`** — `--scope` narrows the deferred-auto set to in-scope deliverables (rationale: `--scope` is the universal narrowing primitive); (ii) **does not interact with `--final`** — `--deferred` runs only deferred-auto criteria, never enters the final-gate machinery; (iii) **inherits the active mode flag** — same parallelism/model routing as the parent invocation. `--deferred` invoked without `--scope` covers all deferred-auto criteria across the manifest.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read verify/SKILL.md --deferred section. Confirm: (1) --deferred + --scope is supported and narrows the deferred set; (2) --deferred does not interact with --final/final-gate; (3) --deferred inherits --mode; (4) --deferred without --scope covers all deferred-auto criteria. Report PASS/FAIL."
  ```

- [AC-4.3] **Cross-repo path delivery to verifiers** is specified concretely and applies to **all `/verify` passes** (selective, full, `--deferred`) when the manifest declares `Repos:`. `/verify` resolves the manifest's `Repos: [name: path]` map and prepends a verbatim string to each verifier's prompt — `Available repos: name1=/path/1, name2=/path/2, ...` — before the criterion's own prompt. This makes cross-repo verifiers work in normal flow (so `/done` can fire once per multi-repo manifest), not just under `--deferred`. Single-repo manifests (no `Repos:` field) get no prefix; behavior unchanged.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read verify/SKILL.md and MULTI_REPO.md. Confirm: (1) the path-delivery mechanism (prompt prefix injecting the Repos map verbatim) applies to every /verify pass when manifest has Repos: — selective, full, and --deferred — NOT just --deferred; (2) the prefix format is shown ('Available repos: name=/path, ...'); (3) single-repo manifests get no prefix injection; (4) the rule appears in BOTH verify/SKILL.md and MULTI_REPO.md without contradiction. Report PASS/FAIL with citations."
  ```

- [AC-4.4] Single-repo manifests are unaffected: a manifest with no `deferred-auto` criteria sees no change in `/verify` behavior; `--deferred` invoked on such a manifest reports "no deferred-auto criteria" and exits cleanly.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read verify/SKILL.md. Confirm: a manifest without deferred-auto criteria gets identical /verify behavior to today. /verify --deferred on such a manifest is a no-op with clean message. Report PASS/FAIL."
  ```

### Deliverable 5: /tend-pr — Multi-PR Amendment Routing

**Acceptance Criteria:**

- [AC-5.1] `tend-pr/SKILL.md` documents multi-PR pattern: each repo runs its own `/tend-pr` against its own PR; all ticks amend the same canonical `/tmp` manifest. Reference MULTI_REPO.md for full rules. PR descriptions stay summary-only (no manifest embed).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read tend-pr/SKILL.md. Confirm: (1) multi-PR pattern documented (per-repo invocation against shared /tmp manifest); (2) link to MULTI_REPO.md; (3) PR description sync remains summary-only with no manifest embed; (4) single-repo behavior unchanged. Report PASS/FAIL."
  ```

- [AC-5.2] Concurrency note: `tend-pr/SKILL.md` (or `tend-pr-tick`) explicitly states no locking or concurrency-engineering; rare collisions are acceptable. Rationale captured.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read tend-pr/SKILL.md and tend-pr-tick/SKILL.md. Confirm explicit statement that concurrent amendments across N ticks are accepted without locking, with rationale. Report PASS/FAIL."
  ```

- [AC-5.3] **Collision behavior shape** documented. When two ticks amend the same `/tmp` manifest concurrently, the expected behavior is **last-writer-wins** — the later write may overwrite the earlier write's amendment block. Recovery: user notices missing amendment in next iteration → re-trigger the lost tick (e.g., re-add the comment, re-run `/tend-pr-tick`). This rule appears explicitly so an implementer does not silently add file locking thinking it is required.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read tend-pr/SKILL.md or tend-pr-tick/SKILL.md or MULTI_REPO.md. Confirm: (1) explicit statement that collision behavior is last-writer-wins; (2) explicit recovery procedure (re-trigger the lost tick); (3) explicit instruction NOT to add file locking. Report PASS/FAIL with quoted lines."
  ```

### Deliverable 6: /done — Per-Repo Completion Semantics

**Acceptance Criteria:**

- [AC-6.1] `done/SKILL.md` documents that **`/done` fires once per manifest** — including multi-repo manifests. /verify's "every AC across every deliverable" rule is preserved (no per-repo /done independence). For multi-repo, the summary lists which repos' deliverables were verified. **`/done` is gated on no deferred-auto criteria pending** — when deferred-auto criteria exist and have not been verified green via /verify --deferred, /verify routes to /escalate ("Deferred-Auto Pending") instead of /done; the user runs /verify --deferred when ready, after which a subsequent /verify pass can reach /done. The /verify cross-repo prompt-prefix injection (per AC-4.3) makes verifiers in normal flow able to reach all repos, so the full final pass is achievable for multi-repo manifests. **Must NOT mention `/tend-pr`** — core skill stays decoupled.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read done/SKILL.md. Confirm: (1) /done is one-per-manifest (no per-repo independence); (2) multi-repo summary format lists which repos' deliverables were verified; (3) /done is gated on no deferred-auto criteria pending — when deferred-auto criteria exist unverified, /escalate (Deferred-Auto Pending) fires instead of /done; (4) single-repo summary unchanged; (5) does NOT mention /tend-pr (core skill decoupled from optional add-ons). Report PASS/FAIL with quoted lines."
  ```

### Deliverable 7: AMENDMENT_MODE.md Wording Flex

**Acceptance Criteria:**

- [AC-7.1] `AMENDMENT_MODE.md` Cumulative Manifest Rule flexes from singular "PR/branch" to wording that covers both single-PR and multi-PR-set cases (no logic change). Link to MULTI_REPO.md for the multi-repo specifics. **Must NOT mention `/tend-pr`, `/tend-pr-tick`, or `/drive` by name** — AMENDMENT_MODE is core and stays decoupled from optional PR-tending tools. Generic wording like "consumer skills that amend the manifest" or "amendment writers" is fine; specific naming is not.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read AMENDMENT_MODE.md. Confirm: (1) Cumulative Manifest Rule wording covers both single-PR and multi-PR-set cases without ambiguity; (2) link to MULTI_REPO.md for multi-repo specifics; (3) no behavioral logic changed; (4) does NOT name /tend-pr, /tend-pr-tick, or /drive (core ref doc decoupled from optional add-ons). Report PASS/FAIL with citations."
  ```

### Deliverable 8: Plugin Version Bumps + READMEs

**Acceptance Criteria:**

- [AC-8.1] `claude-plugins/manifest-dev/.claude-plugin/plugin.json` version is bumped (minor — new feature: multi-repo support).
  ```yaml
  verify:
    method: bash
    command: "cd /home/user/manifest-dev && git diff main -- claude-plugins/manifest-dev/.claude-plugin/plugin.json | grep -E '^\\+.*\"version\"' && echo 'PASS' || echo 'FAIL: version not bumped'"
  ```

- [AC-8.2] `claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json` version is bumped (minor — new feature: multi-repo support in /drive).
  ```yaml
  verify:
    method: bash
    command: "cd /home/user/manifest-dev && git diff main -- claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json | grep -E '^\\+.*\"version\"' && echo 'PASS' || echo 'FAIL: experimental version not bumped'"
  ```

- [AC-8.3] READMEs synced per repo's checklist — root `README.md`, `claude-plugins/README.md`, `claude-plugins/manifest-dev/README.md`, and `claude-plugins/manifest-dev-experimental/README.md` mention multi-repo capability where the existing structure surfaces components/features.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read README.md, claude-plugins/README.md, claude-plugins/manifest-dev/README.md, claude-plugins/manifest-dev-experimental/README.md. Confirm the new multi-repo capability appears wherever component/feature lists exist. Report PASS/FAIL with citations."
  ```

### Deliverable 10: /drive + /drive-tick — Multi-PR Pattern (manifest-dev-experimental)

**Acceptance Criteria:**

- [AC-10.1] `drive/SKILL.md` documents multi-PR pattern: each repo runs its own `/drive` against its own PR; all `/drive-tick` instances amend the same canonical `/tmp` manifest. Reference MULTI_REPO.md for full rules. Note that run-id qualification (`gh-{owner}-{repo}-{pr-number}`) already provides per-repo lock + log isolation.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read drive/SKILL.md. Confirm: (1) multi-PR pattern documented (per-repo invocation against shared /tmp manifest); (2) link to MULTI_REPO.md; (3) explicit note that run-id already isolates locks/logs per PR; (4) single-repo behavior unchanged. Report PASS/FAIL."
  ```

- [AC-10.2] `drive-tick/SKILL.md` documents that Amendment routing sends amendments to the canonical `/tmp` manifest shared across all `/drive` instances on the same multi-repo manifest. Last-writer-wins behavior matches AC-5.3 (no locking, rare collisions accepted).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read drive-tick/SKILL.md Amendment section. Confirm: (1) explicit statement that amendments target the shared canonical manifest; (2) collision behavior matches AC-5.3 (last-writer-wins, no locking); (3) link to MULTI_REPO.md or AC-5.3-equivalent rule. Report PASS/FAIL."
  ```

- [AC-10.3] Wording flex: `drive/SKILL.md` and `drive-tick/SKILL.md` references to "the PR" / "the branch" in canonical-source-of-truth contexts are flexed to cover the multi-PR/multi-branch case (matching INV-G5's pattern).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read drive/SKILL.md and drive-tick/SKILL.md. For every occurrence of 'PR/branch' or singular 'the PR' / 'the branch' that refers to the canonical-source-of-truth concept, confirm wording has been flexed to cover the multi-PR/multi-branch case. Quote each occurrence and assert PASS or FAIL. Singular wording referring to a specific PR operation (e.g., 'open the PR via GitHub MCP') is fine and should not be flagged."
  ```

### Deliverable 11: /auto — Multi-Repo Footgun Note

**Acceptance Criteria:**

- [AC-11.1] `auto/SKILL.md` adds a note explaining `/auto`'s multi-repo behavior **accurately**: `/auto`'s `/do` invocation navigates **all repos** declared in the manifest's `Repos:` map (per `/do`'s Multi-Repo Navigation; PG-7 — no filter logic in `/do`). The per-cwd limitation is **only** `/tend-pr`: with `--tend-pr`, only cwd's PR is set up for tending, because `/tend-pr` is PR-bound by construction. To tend other repos' PRs, the user invokes `/tend-pr` from each other repo's cwd. This wording must NOT contradict `/do`'s navigation contract or `MULTI_REPO.md` §d/§i.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read auto/SKILL.md. Confirm a multi-repo behavior note exists that: (1) explicitly states /auto's /do invocation navigates all repos declared in Repos: (does NOT claim /do is limited to cwd); (2) identifies /tend-pr as the per-PR limitation when --tend-pr is set; (3) instructs the user to invoke /tend-pr from each other repo's cwd to tend other PRs; (4) links to MULTI_REPO.md §i. Cross-check against do/SKILL.md Multi-Repo Navigation and MULTI_REPO.md §d to confirm no contradiction. Report PASS/FAIL with quoted lines from auto/SKILL.md and citations from do/SKILL.md and MULTI_REPO.md."
  ```

### Deliverable 9: Single-Repo Backward Compat — Final Regression Check

**Acceptance Criteria:**

- [AC-9.1] An existing archived single-repo manifest from `.manifest/` is walked through the updated skills end-to-end, confirming zero behavior change. The verifier follows an enumerated checklist, not an open-ended walk.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Pick the most recent single-repo manifest in .manifest/. For EACH of the following skill files, identify the multi-repo branch (the new note/rule) and confirm the single-repo manifest does NOT enter it. Use this exact checklist:\n\n1. define/SKILL.md — does the manifest produce Repos:/repo: fields? It must not (no multi-repo signal in source).\n2. do/SKILL.md — does the multi-repo navigation note trigger? It must not (no Repos: in manifest). Confirm /do log path is unchanged.\n3. verify/SKILL.md — does any criterion have method: deferred-auto? It must not.\n4. verify/SKILL.md — would --deferred ever be invoked in normal flow? It must not.\n5. tend-pr/SKILL.md and tend-pr-tick/SKILL.md — does multi-PR amendment routing apply? It must not (single PR).\n6. done/SKILL.md — does multi-repo summary format apply? It must not.\n7. AMENDMENT_MODE.md — does the wording flex still cover the singular case? It must (no regression).\n8. auto/SKILL.md — does the multi-repo footgun note apply? It must not (single-repo manifest doesn't trigger it).\n9. drive/SKILL.md and drive-tick/SKILL.md — does multi-PR pattern apply? It must not (single PR; per-PR run-id behavior unchanged).\n\nFor each item, quote the rule from the updated skill file and confirm the single-repo manifest skips it. Report PASS/FAIL per item plus an overall PASS/FAIL."
  ```

- [AC-9.2] Hook tests pass (no hook code changed, but linting/typecheck must remain green per project's "Before PR" checklist).
  ```yaml
  verify:
    method: bash
    command: "cd /home/user/manifest-dev && pytest tests/hooks/ -v"
  ```

## Amendments

- **2026-04-26 (Self-Amendment, INV-G2 fix-loop)** — AC-11.1 rewritten. The original AC required auto/SKILL.md to assert "/auto handles cwd's repo only" — this directly contradicted /do's Multi-Repo Navigation (PG-7: /do navigates all repos via the LLM, no filter logic) and MULTI_REPO.md §d (single /do invocation can cover the whole multi-repo task). prompt-reviewer (INV-G2) caught this contradiction. The corrected AC reflects the actual per-cwd limitation: only /tend-pr (PR-bound by construction) is per-cwd; /do is not. auto/SKILL.md and MULTI_REPO.md §i updated to match. No new behavior; correction of an inaccurate framing.

- **2026-04-26 (Self-Amendment, user message — deferred-auto escalation routing)** — User flagged that when /do is done with regular work but deferred-auto criteria remain, the system should /escalate (waiting for user signal) rather than silently /done. Amended AC-1.1(e), AC-1.1(g), AC-4.1, AC-6.1: when normal /verify completes green with unverified deferred-auto criteria, /verify routes to /escalate ("Deferred-Auto Pending") instead of /done. Once user runs /verify --deferred and those go green, a subsequent normal /verify pass can call /done. verify/SKILL.md, done/SKILL.md, and MULTI_REPO.md §e/§g updated. No new behavior for manifests without deferred-auto criteria.

- **2026-04-26 (Self-Amendment, user pushback + INV-G1 fix-loop)** — Multiple ACs rewritten in response to:
  1. **User pushback**: "Define do and the rest shouldn't know about tend pr. It's an optional piece." Core skills (/define, /do, /verify, /done, AMENDMENT_MODE) decoupled from /tend-pr/-tick/drive. Affected: AC-1.1(c), AC-1.1(f), AC-2.1, AC-7.1.
  2. **INV-G1 (change-intent-reviewer) HIGH divergence**: per-repo /done unreachable because /verify's hard final gate requires every-AC-everywhere green, but cross-repo prefix injection was --deferred-only. Resolved by (a) dropping per-repo /done independence — /done fires once per manifest including multi-repo (AC-6.1, AC-1.1(g)); (b) extending /verify cross-repo prompt-prefix injection to all passes when manifest declares Repos:, not just --deferred (AC-4.3, AC-1.1(e)).
  
  The /tend-pr and /drive skill files (D5, D10) are consumers of MULTI_REPO.md, so they continue to describe how they ride the shared-manifest pattern; only the core ref doc + skills strip /tend-pr-specific framing.
