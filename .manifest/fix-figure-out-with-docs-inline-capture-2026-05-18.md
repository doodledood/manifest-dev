# Definition: Fix figure-out --with-docs to capture ADRs/CONTEXT inline; sharpen verb; remove --canvas from /auto

## 1. Intent & Context

- **Goal:** Make figure-out's `--with-docs` mode reliably raise and write context/ADR records inline (CONTEXT.md updates + ADR offers/writes), eliminating the user's need to manually run the post-hoc `/adr` sweep. Sharpen figure-out's master verb. Duplicate ADR format docs into figure-out's directory so the `/adr` skill can be removed later without breaking figure-out. Initialize a minimal CONTEXT.md for the manifest-dev repo (dogfood the new bootstrap behavior). Remove the meaningless `--canvas` flag from `/auto` (autonomous mode has no use for an interactive canvas).

- **Mental Model:** Two root causes drive the under-write failure: (1) competing frames — figure-out SKILL.md's "Don't leap to the implied move" wins over with-docs.md's "Capture as it happens"; (2) fuzzy triggers — current with-docs.md uses subjective "when a term resolves" and a 3-condition AND gate (hard-to-reverse + surprising + real trade-off). Fix attacks both: explicit override carve-out at the top of WITH_DOCS.md ("these writes ARE the action"), plus per-turn mechanical triggers replacing fuzzy resolution. Inline ADR gate unifies with post-hoc /adr's gate (category match + Decision Test + anti-patterns) — same coverage, two-pass capture (per-turn high-confidence + session-end sweep). Format docs DUPLICATED into figure-out's directory; /adr's copy stays frozen until /adr is removed.

## 2. Approach

- **Architecture:** figure-out skill becomes self-contained for ADR concerns via duplication. Two reference files separate operational protocol (`WITH_DOCS.md`) from format spec (`ADR_FORMAT.md`). The `--with-docs` flag retains its kebab-case form (it's a flag, naming convention preserved); only the *loaded reference file* renames to caps-and-underscores.

- **Execution Order:**
  - D3 (`ADR_FORMAT.md` — written first since D2 references it) → D2 (`WITH_DOCS.md` rewrite + rename + SKILL.md path update) → D1 (verb sharpening, independent) → D4 (`CONTEXT.md` at repo root, dogfoods bootstrap) → D7 (remove `--canvas` from /auto, independent) → D8 (figure-out-team verb) → D9 (figure-out-team read-only --with-docs) → D5 (version bump) → D6 (README sync)
  - Rationale: D2 references D3 so D3 must exist when D2 is written. D1, D4, D7, D8, D9 are independent and order-flexible (grouped here by skill — D1-D4 figure-out, D7 auto, D8-D9 figure-out-team). D5/D6 are admin, last.

- **Risk Areas:**
  - [R-1] Renaming `with-docs.md` → `WITH_DOCS.md` may leave stale references in plugin code, docs, or distribution mirrors | Detect: full-repo grep for `with-docs.md` after rename returns zero
  - [R-2] Symlink `.claude/skills/figure-out` resolution must continue to expose the renamed file | Detect: `ls .claude/skills/figure-out/references/WITH_DOCS.md` resolves to the plugin file
  - [R-3] Verb change "Probe" → "Press" must not break cross-skill triggers (other skills may grep figure-out's description) | Detect: grep across all skills for cross-references to figure-out's old trigger language
  - [R-4] Duplicated ADR format may drift over time vs /adr's legacy copy | Detect: drift policy explicitly documented inside the new `ADR_FORMAT.md` (figure-out's = canonical; /adr's = frozen legacy)
  - [R-5] Removing `--canvas` from /auto may break callers that pass it (none expected, but check) | Detect: grep across repo for `/auto.*--canvas` returns zero outside the auto skill source itself
  - [R-6] Read-only `--with-docs` on figure-out-team may confuse users who expect symmetry with figure-out's write-capable `--with-docs` | Detect: SKILL.md contains an explicit boundary statement naming both what the flag does (load CONTEXT.md/CONTEXT-MAP.md) AND what it does not (no writes, no proposals, no ADR offers from Slack)

- **Trade-offs:**
  - [T-1] Duplicate ADR format vs cross-plugin reference → Prefer duplication. /adr is destined for removal; figure-out must be self-contained. Drift risk accepted (canonical owner named in the doc).
  - [T-2] Per-turn only vs two-pass capture (per-turn + session-end sweep) → Prefer two-pass. Per-turn alone misses recall on subtle decisions; session-end-only loses immediacy. Two-pass = high-confidence inline + sweep at natural close.
  - [T-3] Verb "press" vs keeping "probe" → Prefer "press". Semantically commits to asking insistently; no idiom baggage; user confirmed in figure-out.
  - [T-4] Caps-and-underscores naming for reference files (`WITH_DOCS.md`, `ADR_FORMAT.md`) vs existing kebab-case convention → Prefer caps for these two. User-set convention. Other skill files keep kebab-case; this is a per-file naming choice, not a repo-wide rename.
  - [T-5] Read-only `--with-docs` for figure-out-team vs full inline capture (mirror of figure-out's `--with-docs`) → Prefer read-only. Slack-mediated capture requires substantial design (who owns writes, owner approval cadence, multi-stakeholder visibility, who can speak for the team). Read-only enriches the agent's context without that complexity; the team captures via other channels (manual, or figure-out --with-docs in Claude Code chat).

## 3. Global Invariants

- [INV-G1] Symlink `.claude/skills/figure-out → claude-plugins/manifest-dev/skills/figure-out` remains intact and resolves new reference filenames
  ```yaml
  verify:
    prompt: "Check that .claude/skills/figure-out is a symlink (ls -la). Verify it points to claude-plugins/manifest-dev/skills/figure-out. Verify that .claude/skills/figure-out/references/WITH_DOCS.md and .claude/skills/figure-out/references/ADR_FORMAT.md both resolve to readable files via the symlink. Return PASS only if all three checks hold; FAIL with the specific failure otherwise."
  ```

- [INV-G2] figure-out's default flow (without --with-docs) is behaviorally unchanged except for the verb sharpening
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md and compare it to the version on the main branch (git show main:claude-plugins/manifest-dev/skills/figure-out/SKILL.md). Verify the only differences are the verb change (Probe→Press) and related description/trigger updates. Specifically verify these unchanged: the 'walk every branch', 'tackle the next load-bearing question', 'one question at a time', 'recommended answer with each' structure; the 'don't drop threads' line; the 'clarifying answers feed exploration, not action' line; the load-this-reference-when-args-contain pattern. PASS only if the non-verb-related behavior is intact, FAIL with the differing lines quoted."
  ```

- [INV-G3] The /adr post-hoc skill's ADR_FORMAT.md is NOT modified
  ```yaml
  verify:
    prompt: "Compare claude-plugins/manifest-dev-tools/skills/adr/references/ADR_FORMAT.md on the current branch vs main (git diff main -- claude-plugins/manifest-dev-tools/skills/adr/references/ADR_FORMAT.md). Verify the diff is empty (no changes). PASS if no diff, FAIL with the diff shown otherwise."
  ```

- [INV-G4] Reference files use caps-and-underscores naming (no kebab-case for WITH_DOCS.md and ADR_FORMAT.md)
  ```yaml
  verify:
    prompt: "Verify these two files exist in caps-and-underscores form: claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md and claude-plugins/manifest-dev/skills/figure-out/references/ADR_FORMAT.md. Also verify neither claude-plugins/manifest-dev/skills/figure-out/references/with-docs.md nor claude-plugins/manifest-dev/skills/figure-out/references/adr-format.md exists. PASS only if caps versions exist and kebab versions do not; FAIL with the specific mismatch."
  ```

- [INV-G5] No stale references to old `with-docs.md` path remain anywhere in the repo
  ```yaml
  verify:
    prompt: "Run from repo root: grep -r 'with-docs.md' --include='*.md' --include='*.json' --include='*.py' . 2>/dev/null. Verify zero matches. FAIL with the offending lines quoted. PASS if no matches."
  ```

- [INV-G6] All edits to figure-out plugin files went through `claude-plugins/manifest-dev/skills/figure-out/` (not the symlink view)
  ```yaml
  verify:
    prompt: "Check git log for files changed in this branch (git diff main --name-only). Verify that any figure-out-related changes touch paths under claude-plugins/manifest-dev/skills/figure-out/, NOT paths under .claude/skills/figure-out/ (which would mean the symlink view was edited and could have broken the link). PASS if all figure-out edits are under the plugin path, FAIL with the offending paths quoted."
  ```

- [INV-G7] change-intent-reviewer finds no LOW+ severity issues on prompt changes
  ```yaml
  verify:
    prompt: "Invoke the change-intent-reviewer subagent on the prompt changes in this branch (figure-out/SKILL.md, figure-out/references/WITH_DOCS.md, figure-out/references/ADR_FORMAT.md, and auto/SKILL.md). The agent should compare the stated intent (fix under-write failure mode, sharpen verb, remove --canvas from /auto) against the actual changes. PASS only if the agent reports no LOW+ severity findings (i.e., only INFO/NONE-level observations). FAIL with the findings quoted otherwise."
    agent: change-intent-reviewer
  ```

- [INV-G8] prompt-reviewer finds no MEDIUM+ severity issues on prompt changes
  ```yaml
  verify:
    prompt: "Invoke the prompt-reviewer subagent on the prompt changes in this branch (figure-out/SKILL.md, figure-out/references/WITH_DOCS.md, figure-out/references/ADR_FORMAT.md, and auto/SKILL.md). PASS only if the agent reports no MEDIUM+ severity findings. FAIL with the findings quoted otherwise."
    agent: prompt-reviewer
  ```

## 4. Process Guidance

- [PG-1] High-signal changes only: every modification must address the diagnosed failure mode (under-write of CONTEXT.md/ADRs) or be one of the explicitly scoped supplements (lifecycle, immutability, etc.). Do not refactor adjacent code. Do not "improve while you're there."

- [PG-2] Calibrate emotional tone in all prompt writing. Low arousal — no urgency language, no excessive praise, no pressure framing. Trusted-advisor tone. Failure normalized in iterative prompts.

- [PG-3] Folder architecture: keep `WITH_DOCS.md` (operational) and `ADR_FORMAT.md` (canonical format) as separate companion reference files. Do NOT inline ADR_FORMAT contents into WITH_DOCS.md; the split is intentional progressive disclosure.

- [PG-4] Description as trigger (for SKILL.md verb update): description field is a trigger spec, not a summary. Preserve broad trigger coverage ("figure out", "investigate", "work through", "why does") alongside the new "press" idiom for discoverability.

- [PG-5] Edit via the plugin path, not the symlink: `claude-plugins/manifest-dev/skills/figure-out/...` is the canonical edit path. Editing through `.claude/skills/figure-out/` (symlink view) risks breaking the link.

- [PG-6] Preserve git history on rename: use `git mv` (or stage as rename) for `with-docs.md` → `WITH_DOCS.md` so the rename is recognized as a rename in the diff, not delete+add.

## 5. Known Assumptions

- [ASM-1] (auto) Verb "press" applies to the default figure-out flow, not just --with-docs. Default: master verb is universal in SKILL.md; --with-docs is a flag adding behavior, not replacing the core posture. Impact if wrong: minor — verb is a tone shift; if user wanted it scoped to --with-docs only, the body opener can be revised in a one-line follow-up.

- [ASM-2] (auto) Plugin version bump is MINOR (1.0.1 → 1.1.0). Default: new behavior in existing skill + new reference file; not breaking. Impact if wrong: low — semver discipline mismatch only, easily corrected.

- [ASM-3] (auto) Triggers preserve broad coverage and add "press" idiom; no triggers removed wholesale. Default: discoverability over purity. Impact if wrong: low — extra triggers are noise at worst.

- [ASM-4] (auto) CONTEXT.md at repo root captures *only* minimal domain vocabulary (Manifest, Deliverable, AC, GI, PG, Task File, Plugin, Skill, Agent, Hook). Does NOT duplicate CLAUDE.md operational instructions. Impact if wrong: low — the file is a starting scaffold and is expected to grow from future sessions per the WITH_DOCS.md format spec.

- [ASM-5] (auto) `--canvas` removal from /auto means: remove from argument-hint frontmatter, remove from usage string in body, remove the "passes through to /define" sentence. The /define skill's own `--canvas` flag is unchanged (it's still valid for direct interactive `/define` invocation). Impact if wrong: low — if some other caller passed `--canvas` through /auto, they'd get an "unknown flag" warning, easily restored.

## 6. Deliverables

### Deliverable 1: Sharpen figure-out master verb

Change the master verb in `figure-out/SKILL.md` from "Probe" to "Press" — body opener, description, and triggers updated. Default-flow behavior otherwise unchanged.

**Acceptance Criteria:**

- [AC-1.1] Body opener uses "Press"
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md. Verify the body opener (first sentence after the YAML frontmatter) reads exactly: 'Press the topic relentlessly.' (period included). PASS if exact match; FAIL with actual text quoted otherwise."
  ```

- [AC-1.2] Description updated to reflect "press" verb
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md frontmatter `description:` field. Verify: (a) it does NOT contain the old phrasing 'Probes a topic relentlessly'; (b) it uses 'press' (or 'presses') as the action verb; (c) it preserves the rest of the description shape (walk every branch, load-bearing question, return to dropped threads, recommended answers). PASS only if all three; FAIL with the actual description quoted."
  ```

- [AC-1.3] Triggers include "press" while preserving broad coverage
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md frontmatter description's 'Triggers:' list. Verify: (a) includes 'press' as a trigger term; (b) still includes the existing broad triggers (at minimum: 'figure out', 'investigate', 'work through', 'why does', 'help me think through', 'dig deeper'); (c) trigger list is comma-separated. PASS only if all three; FAIL with the trigger list quoted."
  ```

### Deliverable 2: Rename with-docs.md → WITH_DOCS.md and rewrite content

Rename the reference file and replace its content with the new structure (override carve-out, bootstrap section, per-turn glossary trigger, two-pass ADR capture, delegated format details to ADR_FORMAT.md). Update SKILL.md's load reference to use the caps filename. Flag `--with-docs` itself stays kebab-case.

**Acceptance Criteria:**

- [AC-2.1] File exists at caps path; kebab path is gone
  ```yaml
  verify:
    prompt: "Verify claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md exists as a regular file. Verify claude-plugins/manifest-dev/skills/figure-out/references/with-docs.md does NOT exist. PASS only if both conditions hold; FAIL with the failure details."
  ```

- [AC-2.2] SKILL.md load reference uses caps path; the `--with-docs` flag (kebab) is unchanged
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md. Find the line that maps the --with-docs flag to its reference file (currently: 'When args contain `--with-docs`, also load `references/with-docs.md`...'). Verify the load path now reads 'references/WITH_DOCS.md' (caps). Verify the flag itself still appears as '--with-docs' (kebab-case, lowercase). PASS only if path is caps AND flag is kebab; FAIL with the actual line quoted."
  ```

- [AC-2.3] WITH_DOCS.md has an override carve-out section near the top
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md. Verify within the first 40 lines after the file title there is a section heading (e.g., '## Override' or similar) whose content EXPLICITLY tells the agent that --with-docs writes (glossary captures and ADR offers) are an EXCEPTION to figure-out SKILL.md's 'don't leap to action' frame — these writes ARE the action, not deferred work. PASS only if both elements present (early position + explicit exception language); FAIL with the actual section quoted."
  ```

- [AC-2.4] WITH_DOCS.md has a bootstrap section covering missing-CONTEXT and multi-context cases
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md. Verify it contains a session-start bootstrap section that instructs the agent to: (a) check whether CONTEXT.md exists at repo root; (b) if missing, propose minimal initialization (not silent write); (c) if CONTEXT-MAP.md exists, follow it to the relevant context; (d) if multiple distinct domains emerge mid-session, propose CONTEXT-MAP.md to split. PASS only if all four behaviors are described; FAIL listing missing items."
  ```

- [AC-2.5] Glossary captures use per-turn mechanical triggers (not "when a term resolves")
  ```yaml
  verify:
    prompt: "Read the glossary-captures section of claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md. Verify: (a) trigger is per-turn (e.g., 'after every user response' or equivalent — concrete cadence, not 'when a term resolves'); (b) trigger enumerates concrete signals (noun defined; clash with existing glossary; fuzzy/overloaded term canonicalized); (c) write semantics state 'no offer, no batch' (or equivalent — write immediately, not deferred). PASS only if all three; FAIL with the actual section quoted."
  ```

- [AC-2.6] ADR offers describe two-pass capture (per-turn + session-end sweep)
  ```yaml
  verify:
    prompt: "Read the ADR-offers section of claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md. Verify two distinct passes are described: (Pass 1) per-turn high-confidence offers (e.g., when user makes an explicit trade-off mid-conversation, offer right then); (Pass 2) session-end sweep — agent reviews the session before naming the read or handing off to /define and presents missed candidates as a batched offer. PASS only if both passes are explicit and ordered; FAIL with the actual content quoted."
  ```

- [AC-2.7] ADR section delegates format/lifecycle/immutability details to ADR_FORMAT.md
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md. Verify it references the adjacent ADR_FORMAT.md by filename for format, gate criteria, lifecycle, and immutability details. Verify WITH_DOCS.md does NOT itself contain: the full MADR template; the Status lifecycle progression; the immutability discipline section. Those belong in ADR_FORMAT.md. PASS only if WITH_DOCS.md references ADR_FORMAT.md AND does not duplicate its detailed content; FAIL with offending duplication quoted."
  ```

- [AC-2.8] CONTEXT.md format and Multi-context repos sections preserved
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md. Verify it retains a 'CONTEXT.md format' section that specifies: one-sentence-per-definition; bold term names; Language + Relationships + Flagged ambiguities structure; project-specific vocabulary only (no architecture/code/file paths). Verify it retains a 'Multi-context repos' section covering CONTEXT-MAP.md usage. PASS if both sections are present and faithful to the prior spec; FAIL with what's missing."
  ```

### Deliverable 3: New canonical ADR_FORMAT.md owned by figure-out

Create a new reference file at `figure-out/references/ADR_FORMAT.md`. Content = the existing /adr ADR_FORMAT.md (template, decision-worthiness criteria, anti-patterns, filename convention) PLUS new supplements (lifecycle, immutability, cross-references, granularity, retroactive policy, unified-gate note, duplication note).

**Acceptance Criteria:**

- [AC-3.1] File exists at the figure-out reference path
  ```yaml
  verify:
    prompt: "Test that claude-plugins/manifest-dev/skills/figure-out/references/ADR_FORMAT.md exists as a regular readable file. Return PASS or FAIL."
  ```

- [AC-3.2] MADR template present with all sections
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/references/ADR_FORMAT.md. Verify it contains a MADR template (presented as a code block) with these sections in order: '# ADR: [Decision Title]' (title format); '## Status' (with default 'Accepted'); '## Context'; '## Decision'; '## Alternatives Considered'; '## Consequences' (with '### Positive' and '### Negative' subsections); '## Source'. Verify the filename convention 'YYYYMMDD-kebab-title.md' is specified outside the template. PASS only if all template sections + filename convention are present; FAIL listing missing items."
  ```

- [AC-3.3] Decision-worthiness criteria and anti-patterns present
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/references/ADR_FORMAT.md. Verify three elements: (a) ADR-worthy categories table or list naming at minimum: Architecture choices, Trade-off resolutions, Scope decisions with rationale, Key constraint decisions, Approach pivots; (b) NOT-ADR-worthy categories naming at minimum: Quality gate selections, Process guidance defaults, Mechanical choices, Known assumptions, Bug fixes; (c) Decision Test stated as 'Would a new team member joining in 6 months benefit from knowing WHY this was decided this way?' (or near-verbatim equivalent). PASS only if all three; FAIL with what's missing."
  ```

- [AC-3.4] Status lifecycle supplement present
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/references/ADR_FORMAT.md. Verify it documents the status lifecycle as a progression naming all four states in order: Proposed → Accepted → Deprecated → Superseded. PASS if all four states are named in lifecycle order; FAIL with the actual content quoted."
  ```

- [AC-3.5] Immutability discipline supplement present with all required elements
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/references/ADR_FORMAT.md. Verify the immutability discipline section includes: (a) explicit append-only statement; (b) editable-in-place list (typos, broken links, formatting, cross-references, clarifying prose without changing the decision); (c) NOT-editable list (changing the decision itself, retroactively rewriting context, deleting rejected alternatives, backdating); (d) practical diff test that contrasts 'changed their mind' (→ new ADR) vs 'fixed a typo' (→ in-place edit OK). PASS only if all four elements present; FAIL listing missing."
  ```

- [AC-3.6] Cross-reference format supplement present (full filename without .md)
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/references/ADR_FORMAT.md. Verify it specifies the cross-reference format using the FULL FILENAME WITHOUT the .md extension, with examples like 'Supersedes 20260518-kebab-title' and 'Superseded by 20260518-kebab-title'. PASS only if format is unambiguous (full filename, no .md, both Supersedes/Superseded-by forms shown); FAIL with the actual format quoted."
  ```

- [AC-3.7] Granularity, Retroactive ADRs, unified-gate note, and Duplication note present
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/references/ADR_FORMAT.md. Verify it contains: (a) Granularity statement (one decision per ADR); (b) Retroactive ADRs policy — permitted; Source field notes retroactivity (with reference to git ref or PR); Status remains Accepted (no new lifecycle value); (c) Gate note stating that inline (figure-out --with-docs) and post-hoc (/adr) BOTH use the same gate (category + Decision Test + anti-patterns) — NO mention of a 3-condition AND gate as current; (d) Duplication note naming this file as canonical, identifying claude-plugins/manifest-dev-tools/skills/adr/references/ADR_FORMAT.md as a legacy frozen copy used by /adr post-hoc, and stating drift may occur over time with figure-out's version winning when /adr is removed. PASS only if all four are present; FAIL listing what's missing."
  ```

### Deliverable 4: Initialize CONTEXT.md at repo root (minimal scaffold)

Create `CONTEXT.md` at the manifest-dev repo root with manifest-dev's project vocabulary, following the format spec in WITH_DOCS.md. Dogfoods the new bootstrap behavior.

**Acceptance Criteria:**

- [AC-4.1] CONTEXT.md exists at repo root
  ```yaml
  verify:
    prompt: "Test that CONTEXT.md exists as a regular file at the repo root (not docs/CONTEXT.md or any subdirectory). Return PASS or FAIL."
  ```

- [AC-4.2] CONTEXT.md structure matches the WITH_DOCS.md format spec
  ```yaml
  verify:
    prompt: "Read CONTEXT.md at repo root AND read claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md's CONTEXT.md format section. Verify CONTEXT.md structurally follows the spec: (a) Markdown # title (project name); (b) one or two introductory sentences explaining what the project is and why; (c) ## Language section with bolded term names and one-sentence definitions; (d) ## Relationships section showing cardinality where load-bearing; (e) ## Flagged ambiguities section (may be empty). PASS if all five structural elements present; FAIL listing what's wrong."
  ```

- [AC-4.3] Language section covers manifest-dev's core domain terms
  ```yaml
  verify:
    prompt: "Read CONTEXT.md at repo root. Verify the ## Language section defines (one sentence each, what-the-term-IS not what-it-does) at minimum these terms: Manifest, Deliverable, Acceptance Criterion, Global Invariant, Process Guidance, Task File. The Claude Code primitives (Plugin, Skill, Agent, Hook) should also appear. PASS only if all six manifest-dev-specific terms + all four Claude Code primitives are defined; FAIL listing missing terms."
  ```

- [AC-4.4] CONTEXT.md is vocabulary-only (no architecture/code/file paths)
  ```yaml
  verify:
    prompt: "Read CONTEXT.md at repo root. Verify it contains ONLY project-specific vocabulary and conceptual relationships. It must NOT contain: file paths, code structure descriptions, architecture diagrams, design decisions, implementation details. (Per WITH_DOCS.md format spec: 'Implementation belongs in ADRs.') PASS if vocab-only; FAIL with the offending lines quoted."
  ```

### Deliverable 5: Plugin version bump

Bump the plugin version in `claude-plugins/manifest-dev/.claude-plugin/plugin.json` (minor: new feature + new reference file).

**Acceptance Criteria:**

- [AC-5.1] Plugin version is bumped (minor)
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/.claude-plugin/plugin.json's version field. Compare to the version on main (git show main:claude-plugins/manifest-dev/.claude-plugin/plugin.json | grep version). Verify the new version's minor component is incremented by 1 (e.g., 1.0.1 → 1.1.0). The patch component should reset to 0 on a minor bump per semver. PASS only if minor incremented and patch reset; FAIL with both versions quoted."
  ```

### Deliverable 6: README sync

Update READMEs (root, claude-plugins/, claude-plugins/manifest-dev/) to reflect: WITH_DOCS.md rename, new ADR_FORMAT.md reference, and the modified --with-docs behavior. Keep high-level per CLAUDE.md README Guidelines.

**Acceptance Criteria:**

- [AC-6.1] No README references the old `with-docs.md` path
  ```yaml
  verify:
    prompt: "Run from repo root: grep -l 'with-docs.md' README.md claude-plugins/README.md claude-plugins/manifest-dev/README.md 2>/dev/null. Verify zero matches. PASS if grep finds nothing; FAIL with the offending file(s) and lines quoted."
  ```

- [AC-6.2] READMEs mention --with-docs behavior at a high level if they discuss figure-out or figure-out-team
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/README.md. (1) If it discusses the figure-out skill, verify that any reference to --with-docs accurately describes its NEW behavior at a high level (inline glossary capture + inline ADR offers with bootstrap) — without implementation detail. (2) If it discusses the figure-out-team skill, verify any reference to its new --with-docs flag accurately notes the flag is READ-ONLY (loads CONTEXT.md/CONTEXT-MAP.md for context; does not write) — at a high level, no implementation detail. If either skill is not discussed in this README, PASS by N/A for that part. Per CLAUDE.md README Guidelines: high-level, no implementation details. PASS if all discussed mentions are high-level and accurate (or N/A); FAIL with the offending lines."
  ```

- [AC-6.3] READMEs are kept high-level (no churn-prone implementation detail)
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/README.md. Verify per CLAUDE.md README Guidelines: high-level overview, what it does, how to use. No specific filenames besides top-level skill/agent names; no per-section implementation detail that requires updates when internals change. PASS if high-level; FAIL with the offending low-level content quoted."
  ```

### Deliverable 7: Remove --canvas pass-through from /auto skill

Remove `--canvas` from `/auto`'s argument-hint, usage string, and the "passes through to /define" sentence. `--canvas` remains valid for direct interactive `/define` invocation; only its `/auto`-mediated pass-through is removed.

**Acceptance Criteria:**

- [AC-7.1] /auto's argument-hint no longer mentions --canvas
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/auto/SKILL.md frontmatter. Verify the `argument-hint:` field does NOT contain '--canvas'. Verify it still contains the other hints (task, --babysit <pr-url>). PASS only if --canvas absent and other hints preserved; FAIL with the argument-hint line quoted."
  ```

- [AC-7.2] /auto's body no longer mentions --canvas pass-through
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/auto/SKILL.md body. Verify it does NOT contain '--canvas' anywhere (no usage-string mention, no 'passes through to /define' sentence, no other reference). PASS if zero occurrences of '--canvas' in the file; FAIL with each remaining occurrence's line number and content quoted."
  ```

- [AC-7.3] /define's --canvas flag is unchanged (still works for interactive direct invocation)
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/define/SKILL.md. Verify it still documents --canvas as a flag (e.g., references CANVAS_MODE.md or describes Shared Understanding Canvas). PASS if --canvas remains a valid /define flag; FAIL if /define lost --canvas as a side-effect."
  ```

### Deliverable 8: Sharpen figure-out-team master verb (Probe → Press)

Align figure-out-team's questioning verb with figure-out's new master verb. Body opener "Probe rigorously" → "Press rigorously"; description and triggers updated to use "press" where they reference the agent's questioning posture. Other content preserved.

**Acceptance Criteria:**

- [AC-8.1] Body opener uses "Press rigorously"
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out-team/SKILL.md. Verify the body opener (first sentence(s) after frontmatter) contains 'Press rigorously' and does NOT contain 'Probe rigorously'. The key transformation: 'Probe rigorously' → 'Press rigorously' in the opening directive. PASS only if 'Press rigorously' is present and 'Probe rigorously' is not present anywhere in the file; FAIL with actual text quoted."
  ```

- [AC-8.2] Description and triggers reflect "press" verb
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out-team/SKILL.md frontmatter. Verify: (a) description does not contain 'probes' as the agent's questioning verb (the description currently says 'probes rigorously, brings evidence...' — must become 'presses rigorously, brings evidence...' or equivalent); (b) the triggers list includes a 'press'-style trigger (e.g., 'team press' replacing 'team probe'); (c) preserves the broad triggers — at minimum: 'figure out with team', 'slack figure-out', 'async deliberation', 'group thinking', 'get the team aligned'. PASS only if all three hold; FAIL with the actual frontmatter quoted."
  ```

### Deliverable 9: Read-only --with-docs flag for figure-out-team

Add a new `--with-docs` flag to figure-out-team with strict READ-ONLY semantics. When present, the agent loads `CONTEXT.md` (and `CONTEXT-MAP.md` if applicable) at session start and uses it as background context for the deliberation. The agent does NOT propose docs initialization if missing, does NOT write CONTEXT.md captures, does NOT offer or write ADRs from the Slack thread. The team's docs capture happens via other channels (manual, or figure-out --with-docs in Claude Code chat).

**Acceptance Criteria:**

- [AC-9.1] argument-hint includes --with-docs
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out-team/SKILL.md frontmatter. Verify the `argument-hint:` field contains '--with-docs' (e.g., '[topic] [--with-docs]'). PASS if --with-docs appears in argument-hint; FAIL with the argument-hint line quoted."
  ```

- [AC-9.2] SKILL.md describes --with-docs as read-only with explicit no-write boundary
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out-team/SKILL.md body. Verify it contains a section or paragraph describing the --with-docs flag with EXPLICIT read-only semantics. The text must state at minimum: (a) when --with-docs is present, the agent loads CONTEXT.md (and CONTEXT-MAP.md if present); (b) the agent does NOT write CONTEXT.md captures; (c) the agent does NOT propose or write ADRs from the Slack thread; (d) docs capture for the team happens via other channels (manual or figure-out --with-docs in Claude Code chat). PASS only if all four points are explicit in the SKILL.md text; FAIL listing what is missing."
  ```

- [AC-9.3] SKILL.md instructs the agent to load CONTEXT.md (and CONTEXT-MAP.md if present)
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out-team/SKILL.md body. Verify it instructs the agent that when --with-docs is set, the agent should: (a) load CONTEXT.md from repo root if present; (b) follow CONTEXT-MAP.md if it exists at repo root (i.e., honor multi-context structure). PASS if both behaviors are described; FAIL with actual text quoted otherwise."
  ```

- [AC-9.4] SKILL.md does NOT instruct the agent to write CONTEXT.md/ADR files
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out-team/SKILL.md body. Verify it does NOT contain instructions to: write CONTEXT.md, propose CONTEXT.md initialization, write ADR files, offer ADRs from Slack, batch ADR offers at session end, or any other writes to documentation files. The flag is strictly read-only — load and use, never write. PASS if no write instructions are present anywhere in the file; FAIL with offending lines quoted."
  ```

## Out of Scope

- Modifying `/adr` skill or its `ADR_FORMAT.md` (frozen legacy)
- Adding new hooks, tests, or agents
- Changing the CONTEXT.md format spec (kept as-is)
- Removing the `/adr` skill itself (left for a future session per user direction)
- Adding `--canvas` rejection logic to `/define` when called with `--autonomous` (not requested; only `/auto`'s pass-through removed)
- **Write-capable `--with-docs` for figure-out-team** — read-only is the chosen shape; designing Slack-mediated writes (owner cadence, multi-stakeholder approval, capture provenance) is its own session

## Approach notes

- Architecture: figure-out skill becomes self-contained for ADR concerns via duplication. Two reference files (`WITH_DOCS.md` operational protocol, `ADR_FORMAT.md` canonical format) keep operational vs descriptive concerns separated for progressive disclosure.
- Verb change is high-leverage: one word shifts agent posture across all figure-out sessions while preserving default-flow behavior.
- The `--with-docs` flag stays kebab-case (it's a flag, naming convention preserved). Only the *loaded reference file* renames to caps-and-underscores per the user's convention for these two reference files specifically.
