# manifest-dev

The loop is the easy part. This is the understanding and verification around it: figure out the problem, write down what you'd accept, and let the loop build and prove it against every line before you open the diff.

Three skills, one for each way an autonomous loop fails — skipping understanding (`/figure-out`), never defining "done" (`/define`), and faking it (`/do`).

## Quick Start

```
/figure-out "how should rate limiting behave here?"   # think it through
/define "add rate limiting to the API"                # encode what you'd accept
# recommended — set your host's goal/continuation backstop to a completion contract that carries across turns:
Goal: Run /do ~/.manifest-dev/manifests/manifest-<timestamp>.md until every Acceptance Criterion and Global Invariant has fresh independent verifier PASS evidence in a manifest gate ledger and /done is reported; don't stop while any gate is unverified, FAIL, stale after a relevant change, BLOCKED/actionable, or escalation-pending. The ledger should list every AC/GI with gate id, phase, verify.prompt source, latest verifier verdict, evidence, and freshness. Do not accept self-attestation, "looks done", or a summary claim instead of verifier output; fix FAILs and re-verify. Escalate only a blocker that genuinely needs me. Record compact progress checkpoints after implementation milestones, verification/repair cycles, and blockers. Stop after N turns if it stalls.
/do ~/.manifest-dev/manifests/manifest-<timestamp>.md         # foreground variant, current turn only
```

`/figure-out` is where the understanding happens. `/define` encodes that understanding into a Manifest — it auto-invokes `/figure-out` for you when the conversation hasn't reached understanding yet, so in practice the minimum is `/define` then `/do` with a durable goal-setting or continuation backstop. `/do` executes the Manifest and verifies inline by spawning a subagent per Acceptance Criterion and Global Invariant. The backstop's argument should be the auditable all-criteria-PASS completion contract — a complete gate ledger with fresh independent PASS evidence — keeping the run alive across turns until the condition holds.

Non-Claude distributions are generated under `dist/`. OpenCode and Codex ship `/do`; Pi installs the repo-root package (`pi install git:github.com/doodledood/manifest-dev@main`) for the full skill set plus prompt-template aliases for `/do`, `/auto`, and `/babysit-pr`. Host goal/continuation support is optional and acts as an outer backstop for unattended runs. See the root README's [Multi-CLI Support](../../README.md#multi-cli-support).

The `/do` session doesn't need to remember the `/define` conversation — the manifest is external state. Run `/do` in a fresh session with a durable goal-setting/continuation backstop, or `/compact` before starting.

## The Mindset Shift

Stop thinking about *how* to build it. Start thinking about *what you'd accept* — that's the loop's real stop condition.

"What would make me approve this PR?" "What rules can't be broken?" "How would I know each piece is done?" The acceptance criteria are the pillar, not the implementation. LLMs are good at execution when they know exactly what's expected and bad at reading your mind — the manifest closes that gap before a line of code gets written.

You plan a feature with the agent. It implements. The code looks reasonable. Then you review it and half the things aren't how you'd want them: wrong error handling, conventions ignored, edge cases skipped. You send it back. It fixes some, breaks others. Three rounds later you're satisfied, but you've spent more time reviewing than you saved. Manifest-dev front-loads that review energy — you spell out the criteria before implementation starts, so the do phase becomes mechanical and the output lands closer to what you'd accept as a reviewer.

## Skills

- **`/figure-out`** — the thinking partner, and the conceptual core. Walks every branch of the decision tree (design, diagnostic, commitment, exploratory), takes the next load-bearing question first, recommends an answer, returns to dropped threads, investigates instead of asking when something is discoverable, and keeps a belief register on evidence-heavy work. Its read ships with an Evidence Ledger (load-bearing claims with provenance and verified/inferred/assumed status), confidence, and overturn conditions; loads probe task files by topic shape (code change, diagnosis, research) and runs an independent fresh-context re-derivation before confident reads nobody will audit. `/define` auto-invokes it when the transcript lacks understanding; call it directly when figuring it out IS the goal. Docs mode and narrative logging are on by default; `--no-docs` skips bootstrap/glossary/ADR conventions, `--no-log` skips the default log under the user's home `.manifest-dev/logs/` directory, `--autonomous` lets it self-answer (used by `/auto`), `--team` moves the deliberation into a Slack channel or thread (used by `/figure-out-team`), and `--scratch` (off by default) maintains a rough, domain-native supporting artifact under `.manifest-dev/scratch/` to ground long or complex sessions.
- **`/define`** — encodes shared understanding into a verifiable Manifest. Not an interview: it makes the manifest-specific judgment calls (invariant vs process guidance, AC scope and pass threshold, phase ordering, trade-offs to lock as `[T-N]`) and pulls in `/figure-out` first if the understanding isn't there. Pass an existing manifest path in `$ARGUMENTS` to amend it in place. Supports `--babysit <pr-url>` and `--canvas`. Emits a foreground `/do <manifest-path>` handoff; `/do` owns the durable manifest-completion contract.
- **`/do`** — executes a Manifest, running one verifier execution context per Acceptance Criterion and Global Invariant (using `verify.prompt:` verbatim), respecting `phase:` ordering, calling `/done` when every gate has fresh PASS evidence or routing through `/escalate` when blocked. Caller overlays can narrow retry cadence, e.g. CI one-shot runs report wait-only states instead of sleeping. The recommended unattended invocation uses the host's goal-setting or continuation backstop with the manifest's auditable completion condition: every criterion appears in a gate ledger with fresh independent PASS evidence and `/done` reported. Bare `/do` runs a single foreground turn. Mid-`/do` user messages default to invoking `/define` for amendment.
- **`/auto`** — chains `figure-out → define → do` autonomously, no approval gates. Use the host's goal-setting or continuation backstop with one chain-complete condition for unattended cross-turn execution (recommended): if figure-out runs, full autonomous Read anatomy is a checkpoint before `/define`; terminal completion is manifest written plus `/do` gate-ledger PASS. Add `--babysit <pr-url>` for PR-lifecycle work.
- **`/figure-out-team`** — thin discovery wrapper over `/figure-out --team`: the full figure-out discipline applied to a multi-party async Slack conversation, with the Slack mechanics (session-bound trust, `/loop` polling with `poll-slack` reads, mrkdwn, owner-by-Slack-handle convergence) living in figure-out's `references/team.md` overrides so team sessions inherit every figure-out upgrade. Docs context is loaded read-only by default unless `--no-docs`; local logging is on by default under the user's home `.manifest-dev/logs/` directory unless `--no-log`, and the log is never posted to Slack.
- **`/done`** — completion summary in plain prose, called by `/do` after every criterion has fresh verifier PASS evidence.
- **`/escalate`** — structured blocker: criterion, attempts and why each failed, possible resolutions, what's needed from you. Routed by `/do`.
- **`/review-code`** — quality review along **one dimension per invocation** (bugs, design, simplicity, maintainability, testability, test quality, type safety, contracts, operational readiness, docs, prose value, change intent, or CLAUDE.md adherence). Loads exactly that dimension's reference (progressive disclosure) and returns a PASS/FAIL report. Verifier execution contexts activate it from a `verify.prompt`; it replaces the per-dimension reviewer agents.

## Manifest Schema — Three Fields per Verify Block

Every verify block has the same shape:

```yaml
verify:
  prompt: "..."     # required, verbatim instruction to a general-purpose verifier (may activate a skill)
  model: "..."      # optional, default = inherit from invoking context
  phase: 1          # optional integer, default 1 (lower phases run first)
```

Verifiers return one of three states. **PASS** — the criterion holds. **FAIL** — violated, with evidence: either a per-gate directive `/do` runs literally (when the prompt activates a specialized skill like `check-pr`) or a prose fix hint read with judgment (plain prompts). **BLOCKED** — can't be evaluated yet because an external action or state is pending (deploy, human approval); `/do` routes BLOCKED via `/escalate`.

Authors put whatever the verifier needs directly into the prompt — run a bash command and check the exit code, inspect files, query an API, fetch docs. There's no separate `method:` or `command:` field; the subagent runs whatever its prompt asks for.

## Manifest Sections

| Section | Purpose | ID Scheme |
|---------|---------|-----------|
| **Intent & Context** | Goal and mental model | -- |
| **Initial Approach** (complex tasks) | Architecture, execution order, risks, trade-offs | `R-{N}`, `T-{N}` |
| **Global Invariants** | Task-level rules (task fails if violated) | `INV-G{N}` |
| **Process Guidance** | Non-verifiable recommendations for how to work | `PG-{N}` |
| **Known Assumptions** | Low-impact items resolved with a default | `ASM-{N}` |
| **Deliverables** | Ordered work items with Acceptance Criteria | `AC-{D}.{N}` |

## Example Manifest

````markdown
# Definition: User Authentication

## 1. Intent & Context
- **Goal:** Add password-based auth to an Express app with JWT sessions.
- **Mental Model:** Auth is cross-cutting. Security invariants apply
  globally; endpoint behavior is per-deliverable.

## 2. Initial Approach
- **Architecture:** Middleware-based auth, JWT in httpOnly cookies
- **Execution Order:** D1 (Model) → D2 (Endpoints) → D3 (Protected Routes)
- **Trade-offs:**
  - [T-1] Simplicity vs Security → Prefer security (bcrypt, not md5)

## 3. Global Invariants (The Constitution)
- [INV-G1] Passwords never stored in plaintext
  ```yaml
  verify:
    prompt: "Run: grep -r 'password.*=' src/ | grep -v hash | grep -v test. PASS only if there are no matches."
  ```

## 4. Process Guidance (Non-Verifiable)
- [PG-1] Follow existing error handling patterns in the codebase

## 6. Deliverables (The Work)

### Deliverable 1: Auth Endpoints
**Acceptance Criteria:**
- [AC-1.1] POST /login validates credentials, returns JWT
- [AC-1.2] Invalid credentials return 401, not 500
  ```yaml
  verify:
    prompt: "Activate the manifest-dev:review-code skill with dimension=code-bugs and review the auth routes. PASS only if no LOW-or-higher findings (e.g. auth failures returning 500 instead of 401)."
  ```
````

## Manifest = Current State

Amendments overwrite in place with stable IDs (modify `INV-G1` and it stays `INV-G1`; remove one and it's gone, no renumbering). No `## Amendments` log, no `INV-G1.1 amends INV-G1` chain — git carries the history.

The manifest is the canonical source of truth for the PR or branch, not for a single task — feedback flows through it. When something's off mid-`/do` or after `/done` (a missed edge case, a reviewer comment, a late requirement), Self-Amendment routes it automatically: `/escalate` → `/define` re-invoked on the manifest path to amend → `/do` resumes with the updated manifest. Pure questions about the manifest get answered inline; everything else amends. `/done` stays unreachable until every criterion verifies PASS again, so each round trip grows the verification surface — bug fixes and late requirements become permanent checked criteria.

## Verification Skills

manifest-dev ships **no agents of its own**. Every criterion is verified by a general-purpose subagent driven by `verify.prompt`, which can run bash, inspect files, query external tools, or activate a skill. Read-only behavior is enforced by the prompt, so authors can point a verifier at MCP servers or extra CLI tools the user has configured.

Quality review (code, operational readiness, prose, contracts, types, design, testability, intent, docs) is the **`review-code` skill** — one dimension per invocation; a verifier activates it from `verify.prompt`. The other functional skills are `check-pr` (PR mergeability checks) and `poll-slack` (tails Slack threads for `/figure-out-team`).

| Dimension | Role | Focus |
|-----------|------|-------|
| `change-intent` | defect (no LOW+) | Adversarial intent analysis: reconstructs intent, finds behavioral divergences |
| `code-bugs` | defect (no LOW+) | Mechanical defects: races, data loss, edge cases, resource leaks, dangerous defaults |
| `contracts` | defect (no LOW+) | Bidirectional API/interface contract checks against docs, schemas, codebase definitions |
| `type-safety` | defect (no LOW+) | Typed-language safety: type holes, representable invalid states, narrowing |
| `operational-readiness` | advisory (no MEDIUM+) | Runtime/deploy readiness: env wiring, migrations, retries, rollback, scale, CI, observability |
| `code-design` | advisory (no MEDIUM+) | Design fitness: reinvented wheels, wrong responsibility, under-engineering, PR coherence |
| `code-maintainability` | advisory (no MEDIUM+) | DRY violations, coupling, cohesion, dead code, consistency |
| `code-simplicity` | advisory (no MEDIUM+) | Over-engineering, premature optimization, cognitive complexity |
| `code-testability` | advisory (no MEDIUM+) | Excessive mocking, logic buried in IO, hidden dependencies |
| `test-quality` | advisory (no MEDIUM+) | Coverage gaps plus independent-oracle checks for tautology, mirror-impl, mock-SUT |
| `docs` | advisory (no MEDIUM+) | Documentation accuracy against code changes |
| `prose-value` | advisory (no MEDIUM+) | Comment/doc value: narrating-the-obvious, puffery, AI rhetorical patterns |
| `context-file-adherence` | advisory (no MEDIUM+) | Compliance with CLAUDE.md / AGENTS.md project rules |

## Task Guidance and References

Task files come in two parallel, decoupled sets, each loaded by task type by its own skill: `skills/define/tasks/` carry domain-specific quality gates and Defaults that `/define` encodes into the manifest; `skills/figure-out/tasks/` carry probing fuel — blind-spot probes and forced trade-offs (verification among them) that `/figure-out` surfaces during understanding as awareness, not a checklist. Source-type research material lives under `skills/define/tasks/research/sources/`. Mode and domain references in `skills/define/references/` (`BABYSIT_MODE.md`, `CANVAS_MODE.md`, `MULTI_REPO.md`, `WRITING-REFERENCE.md`) cover specialized flows.

**Multi-repo** (`MULTI_REPO.md`): by default a single manifest covers the whole changeset (Intent declares `Repos:`, deliverables tag `repo:`). `/do` navigates absolute paths from the map natively. PR-lifecycle work templates one `check-pr` skill run per repo against the shared manifest. Splitting into per-repo manifests is fine when the work is loosely coupled.
