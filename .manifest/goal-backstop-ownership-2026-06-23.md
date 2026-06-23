# Definition: Unify continuation backstop ownership

## 1. Intent & Context
- **Goal:** Make manifest-dev skills use one continuation/backstop ownership rule so nested workflow skills do not set or print competing narrower goals.
- **Mental Model:** The skill the user invoked as the workflow entrypoint owns the outer continuation contract. Nested skills execute their phase and may describe handoff, but they do not create another goal when a parent workflow already owns continuation.
- **Scope:** Prompt/skill text and generated dist copies only. No Pi runtime or TypeScript extension work.

## 2. Deliverables

### D1 — Entry-point continuation ownership is encoded in skills
- **What:** Update source skills so `/define`, `/do`, `/auto`, `/babysit-pr`, and `figure-out --autonomous` agree on continuation ownership.
- **Acceptance Criteria:**
  - **AC-1:** `/define` no longer emits the detailed `/do` execution goal contract as its own output; it hands off to `/do` and says `/do` owns standalone manifest-completion continuation.
    verify:
      prompt: "Inspect `claude-plugins/manifest-dev/skills/define/SKILL.md` and generated dist copies. PASS only if define's Complete handoff no longer emits a detailed execution goal contract beginning with `Deliver <deliverables>` or equivalent, and instead tells the user to invoke `/do <manifest-path>` while making clear `/do` handles unattended continuation when invoked standalone. FAIL if `/define` still owns or duplicates `/do`'s execution goal."
      phase: 1
  - **AC-2:** `/do` owns the standalone manifest-completion backstop and suppresses/does not replace a broader parent workflow backstop.
    verify:
      prompt: "Inspect `claude-plugins/manifest-dev/skills/do/SKILL.md` and generated dist copies. PASS only if `/do` establishes or prints a manifest-completion continuation contract when invoked standalone or when no broader parent workflow backstop is visible, and avoids setting/printing a competing narrower goal when invoked under `/auto`, `/babysit-pr`, or another parent workflow that already owns continuation. FAIL if `/do` always creates a new goal regardless of parent context."
      phase: 1
  - **AC-3:** `/auto` and `figure-out --autonomous` preserve one full-chain backstop without a nested Read-only goal.
    verify:
      prompt: "Inspect source and generated dist copies of `auto/SKILL.md` and `figure-out/references/autonomous.md`. PASS only if `/auto` owns the full-chain continuation contract and `figure-out --autonomous` suppresses its standalone Read-level backstop when clearly chained under a broader parent workflow such as `/auto`. FAIL if both would set/print goals for the same `/auto` run."
      phase: 1
  - **AC-4:** `/babysit-pr` owns standalone PR-tend continuation but suppresses nested `/define`/`/do` backstops.
    verify:
      prompt: "Inspect source and generated dist copies of `babysit-pr/SKILL.md`. PASS only if `/babysit-pr` retains an outer PR-tend continuation contract for standalone tends, including the `--manifest` path where `/define` is skipped, and states that nested `/define`/`/do` handoff/backstop text should not create competing narrower goals when the babysit backstop exists. FAIL if the prompt either removes the standalone babysit backstop entirely or allows duplicate nested goals."
      phase: 1

## 3. Global Invariants

- **INV-G1:** Prompt quality stays calibrated: concise, capability-based, not harness-specific, and no redundant backstop instructions beyond what closes the nesting gap.
  verify:
    prompt: "Activate the review-prompt skill. Review all changed prompt-bearing files. PASS only if no MEDIUM-or-higher prompt-engineering findings: the top-level-entrypoint ownership rule is clear, portable, and not over-specified; nested suppression is precise enough without making goal support mandatory. FAIL with severity and evidence otherwise."
    phase: 2
- **INV-G2:** Generated distribution copies stay in sync with source skills for Codex, OpenCode, and Pi.
  verify:
    prompt: "Inspect source skill files and generated copies under `dist/codex`, `dist/opencode`, and `dist/pi`. PASS only if the continuation-ownership wording is present consistently in each compatible distribution and no stale conflicting goal/backstop wording remains. FAIL with exact source/dist drift."
    phase: 2
- **INV-G3:** Existing test/static verification commands pass.
  verify:
    prompt: "Run the relevant test/static commands from repo root: `.venv/bin/python -m pytest -q`, `.venv/bin/ruff check claude-plugins/`, `.venv/bin/black --check claude-plugins/`, `.venv/bin/mypy`, and `git diff --check`. PASS only if available commands pass. Report any intentionally skipped unavailable command with evidence."
    phase: 3

## 4. Approach
- Update source skills first, keeping wording short.
- Sync matching generated dist files directly or via existing sync tooling if practical.
- Add/update tests only if existing tests encode stale goal/backstop expectations or need new coverage for the ownership rule.
- Commit and push after verification passes.
