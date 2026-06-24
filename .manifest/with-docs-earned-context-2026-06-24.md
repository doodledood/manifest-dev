# Definition: Tighten figure-out --with-docs context capture

## 1. Intent & Context
- **Goal:** Fix `figure-out --with-docs` so it keeps inline glossary capture but writes only high-value project language, offers to initialize a missing `CONTEXT.md` for both single-context and multi-context repos, and clean this repo's `CONTEXT.md` where existing entries violate that standard.
- **Mental Model:** The prior `--with-docs` fix intentionally made capture triggers mechanical to prevent under-writing. The new defect is the opposite: the broad “noun got defined” trigger is closer to the action than the later “project-specific vocabulary only” rule, so the prompt can over-capture obvious or implementation-shaped terminology. The durable fix is an earned-entry gate before writing, not removing inline writes. Bootstrap should resolve the active context first, then offer a minimal scaffold whenever that active context file is missing.

## 2. Approach
- **Architecture:** Update the source skill reference at `claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md`; let sync tooling regenerate distribution copies. Clean `CONTEXT.md` by trimming/removing implementation details and redundant generic entries while preserving durable project vocabulary and conceptual relationships. In bootstrap, resolve `CONTEXT-MAP.md` before deciding which `CONTEXT.md` is active so missing per-context files get initialization offers.
- **Execution Order:**
  - D1 tighten `WITH_DOCS.md` capture rules → D2 clean `CONTEXT.md` → D3 bump/sync distribution surfaces → verification.
  - Rationale: `CONTEXT.md` cleanup should follow the new earned-entry standard; generated copies and versions come last.
- **Risk Areas:**
  - [R-1] Overcorrecting back into the original under-write failure | Detect: `WITH_DOCS.md` still mandates inline capture with no offer/batch when the earned-entry gate passes.
  - [R-2] Making `CONTEXT.md` too sparse | Detect: core manifest-dev workflow and distribution boundary terms that guide future work remain defined.
  - [R-3] Generated `dist/*` copies drift from source | Detect: compare generated `WITH_DOCS.md` copies after sync.
  - [R-4] Single-context bootstrap works but multi-context missing files do not get an offer | Detect: `WITH_DOCS.md` resolves the active context via `CONTEXT-MAP.md` first and offers initialization when that active file is missing.
- **Trade-offs:**
  - [T-1] Broad mechanical trigger vs quality gate → Prefer quality gate while retaining inline action, because the reported defect is low-value capture, not failure to write.
  - [T-2] Delete platform terms vs trim implementation details → Prefer trim where the term is durable project vocabulary; delete packaging/distribution terms when they function as architecture or migration history rather than shared language.

## 3. Global Invariants
- [INV-G1] Prompt changes match intent with no LOW+ issues.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=change-intent and review this branch's changes against the intent: keep `figure-out --with-docs` inline glossary capture but prevent low-value/redundant `CONTEXT.md` terminology, and clean `CONTEXT.md` only where entries fail the earned project-language gate.
      PASS only if there are no LOW-or-higher findings. Report findings with severity and file:line evidence.
    phase: 1
  ```

- [INV-G2] Prompt quality has no MEDIUM+ issues.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev-tools:review-prompt skill and review the prompt/documentation changes to `figure-out`'s `WITH_DOCS.md` behavior.
      Focus on: whether the new capture gate closes the observed over-capture gap without regressing inline capture; whether every added/changed line earns its place; whether rules avoid contradictions, brittle absolutes, and redundant restatements.
      PASS only if there are no MEDIUM-or-higher prompt-quality findings. Report findings with severity and file:line evidence.
    phase: 1
  ```

- [INV-G3] `CONTEXT.md` follows its own glossary contract.
  ```yaml
  verify:
    prompt: |
      Inspect `CONTEXT.md` and `claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md`'s CONTEXT.md format rules.
      PASS only if `CONTEXT.md` contains project-specific vocabulary and conceptual relationships; definitions are one sentence each; it avoids architecture details, file paths, code structure, and design-decision prose; and it preserves durable manifest-dev workflow terms needed by future work.
      FAIL with quoted offending lines or missing core terms.
    phase: 1
  ```

## 4. Process Guidance
- [PG-1] High-signal prompt edits only: replace the broad trigger with an earned-entry decision rule near the write instruction; do not add a long checklist or unrelated prompt polish.
- [PG-2] Preserve the inline-write override: when a term earns capture, write before the next question without offer or batching.
- [PG-3] Edit plugin source paths under `claude-plugins/manifest-dev/`; generated `dist/*` copies are updated through sync tooling.
- [PG-4] Keep `CONTEXT.md` as project language, not architecture documentation. Trim implementation details before deleting a useful project term.

## 5. Known Assumptions
- [ASM-1] The exact over-captured entries from the failing session are unavailable. Default: fix the verified prompt mechanism and clean currently visible format violations. Impact if wrong: a separate duplicate-write mechanism may remain and need follow-up.
- [ASM-2] This is a patch-level plugin/package change. Default: bump patch versions for the plugin and Pi package because behavior/assets change without adding a new component. Impact if wrong: version semantics can be corrected before release.

## 6. Deliverables

### Deliverable 1: Earned-entry gate for `--with-docs` glossary captures

**Acceptance Criteria:**
- [AC-1.1] `WITH_DOCS.md` defines a capture gate that requires project-specific, ambiguity-reducing, or workflow-boundary value before writing a term.
  ```yaml
  verify:
    prompt: |
      Read `claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md`.
      PASS only if the Glossary captures section requires an earned-entry gate before writing to `CONTEXT.md`, and the gate includes positive criteria such as project-specific meaning, ambiguity/synonym resolution, durable workflow boundary, load-bearing relationship/cardinality, or observed ambiguity.
      FAIL with the relevant section quoted if the rule still permits capture merely because a noun was defined.
    phase: 1
  ```

- [AC-1.2] `WITH_DOCS.md` explicitly rejects low-value glossary captures without weakening conflict/canonicalization handling.
  ```yaml
  verify:
    prompt: |
      Read `claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md`.
      PASS only if it tells the agent not to write obvious ordinary terms, generic platform vocabulary without project-specific meaning, implementation labels/file paths/code structure, one-off explanations, and already-known terms unless the meaning changes or a clash is found.
      Also verify the conflict and fuzzy/overloaded-term behavior remains: clashes are surfaced, fuzzy terms are canonicalized through the user's articulation, and earned captures are written inline before the next question.
      FAIL with quoted missing or contradictory text.
    phase: 1
  ```

- [AC-1.3] `WITH_DOCS.md` offers to initialize a missing active `CONTEXT.md` in both single-context and multi-context repos.
  ```yaml
  verify:
    prompt: |
      Read `claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md`.
      PASS only if Bootstrap resolves the active context file, follows `CONTEXT-MAP.md` for multi-context repos, treats the repo-root `CONTEXT.md` as active when no map exists, loads the active file if present, and offers a minimal scaffold when the active `CONTEXT.md` is missing. Also verify it says that if a split creates a new context and the per-context `CONTEXT.md` is missing, the same initialization offer applies.
      FAIL with quoted missing or contradictory text.
    phase: 1
  ```

### Deliverable 2: `CONTEXT.md` cleanup

**Acceptance Criteria:**
- [AC-2.1] Existing `CONTEXT.md` entries are trimmed or removed to match the earned-entry standard.
  ```yaml
  verify:
    prompt: |
      Inspect `CONTEXT.md`.
      PASS only if definitions avoid file paths, code structure, install mechanics, packaging architecture, and design-decision narration, while retaining concise definitions for terms that encode manifest-dev-specific workflow language. Packaging/distribution terms should remain only if they are necessary shared vocabulary rather than README/ADR material.
      FAIL with quoted lines that are still implementation documentation rather than glossary language, or with core workflow terms that were removed without an equivalent surviving concept.
    phase: 1
  ```

- [AC-2.2] Relationships remain conceptual and useful.
  ```yaml
  verify:
    prompt: |
      Inspect the `## Relationships` section of `CONTEXT.md`.
      PASS only if relationship bullets describe conceptual relationships among glossary terms, not file layouts or implementation procedures, and if they still cover the core Manifest→Deliverable→Acceptance Criterion/Global Invariant structure and `/define`→`/do` workflow relationship.
      FAIL with quoted offending or missing relationship bullets.
    phase: 1
  ```

### Deliverable 3: Version and generated distribution sync

**Acceptance Criteria:**
- [AC-3.1] Generated `WITH_DOCS.md` copies match the source prompt reference.
  ```yaml
  verify:
    prompt: |
      Compare `claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md` with every generated `WITH_DOCS.md` copy under `dist/`.
      PASS only if each generated copy exists and matches source byte-for-byte.
      FAIL with missing paths or diff summaries.
    phase: 1
  ```

- [AC-3.2] Versions are bumped consistently for changed plugin/Pi assets.
  ```yaml
  verify:
    prompt: |
      Inspect `claude-plugins/manifest-dev/.claude-plugin/plugin.json`, root `package.json`, and `.claude/skills/sync-tools/references/pi-cli.md` if it mentions the Pi package version.
      PASS only if the manifest-dev plugin version and Pi package version were patch-bumped relative to `main`, and any documented Pi package manifest example matches the root `package.json` version.
      FAIL with current and main versions or mismatched documentation.
    phase: 1
  ```
