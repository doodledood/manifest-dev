# manifest-dev

The loop is the easy part. This is the understanding and verification around it: figure out the problem, write down what you'd accept, and let the loop build and prove it against every line before you open the diff.

Three skills, one for each way an autonomous loop fails — skipping understanding (`/figure-out`), never defining "done" (`/define`), and faking it (`/do`).

## Quick start

```
/figure-out "how should rate limiting behave here?"   # think it through
/define "add rate limiting to the API"                # encode what you'd accept
# recommended — set your host's goal/continuation backstop to a completion contract that carries across turns:
Goal: Run /do ~/.manifest-dev/manifests/manifest-<timestamp>.md until every Acceptance Criterion and Global Invariant has fresh PASS evidence under the selected verification mode in a manifest gate ledger and /done is reported; don't stop while any gate is unverified, FAIL, stale after a relevant change, BLOCKED/actionable, or escalation-pending. The ledger should list every AC/GI with gate id, gate-text source, selected mode, evaluator provenance, explicit or inherited verifier model, latest verdict, evidence, and freshness. Do not accept unevidenced self-attestation, "looks done", or a summary claim instead of the selected mode's required evidence; fix FAILs and re-evaluate. Escalate only a blocker that genuinely needs me. Record compact progress checkpoints after implementation milestones, verification/repair cycles, and blockers. Stop after N turns if it stalls.
/do ~/.manifest-dev/manifests/manifest-<timestamp>.md         # foreground variant, current turn only
```

`/figure-out` is where the understanding happens. `/define` encodes that understanding into a Manifest — it auto-invokes `/figure-out` for you when the conversation hasn't reached understanding yet, so in practice the minimum is `/define` then `/do` with a durable goal-setting or continuation backstop. `/do` executes the Manifest and evaluates every gate under a launch-locked run policy. The default `per-gate` mode uses one fresh independent verifier per gate, run concurrently; `consolidated` is an explicit choice for large gate sets whose gates are each slight (one independent verifier for the outstanding set, worked in sequence) and `self` an explicit lower-assurance one. The backstop's argument should be the auditable all-criteria-PASS completion contract — a complete gate ledger with fresh evidence and provenance appropriate to the selected mode — keeping the run alive across turns until the condition holds.

Non-Claude distributions are generated under `dist/`. OpenCode and Codex ship `/do`; Pi installs the repo-root package (`pi install git:github.com/doodledood/manifest-dev@main`) for the full skill set plus prompt-template aliases for `/do`, `/auto`, and `/babysit-pr`. Host goal/continuation support is optional and acts as an outer backstop for unattended runs. See the root README's [Multi-CLI support](../../README.md#multi-cli-support).

The `/do` session doesn't need to remember the `/define` conversation — the manifest is external state. Run `/do` in a fresh session with a durable goal-setting/continuation backstop, or `/compact` before starting.

## The mindset shift

Stop thinking about *how* to build it. Start thinking about *what you'd accept* — that's the loop's real stop condition.

"What would make me approve this PR?" "What rules can't be broken?" "How would I know each piece is done?" The acceptance criteria are the pillar, not the implementation. LLMs are good at execution when they know exactly what's expected and bad at reading your mind — the manifest closes that gap before a line of code gets written.

You plan a feature with the agent. It implements. The code looks reasonable. Then you review it and half the things aren't how you'd want them: wrong error handling, conventions ignored, edge cases skipped. You send it back. It fixes some, breaks others. Three rounds later you're satisfied, but you've spent more time reviewing than you saved. Manifest-dev front-loads that review energy — you spell out the criteria before implementation starts, so the do phase becomes mechanical and the output lands closer to what you'd accept as a reviewer.

## Skills

- **`/figure-out`** — the thinking partner, and the conceptual core. Walks every branch of the decision tree (design, diagnostic, commitment, exploratory), takes the next load-bearing question first, recommends an answer, returns to dropped threads, investigates instead of asking when something is discoverable, and keeps a belief register on evidence-heavy work. Its read ships with an Evidence Ledger (load-bearing claims with provenance and verified/inferred/assumed status), confidence, and overturn conditions; loads probe task files by topic shape (code change, diagnosis, research, tech-design docs) and runs an independent fresh-context re-derivation before confident reads nobody will audit. `/define` auto-invokes it when the transcript lacks understanding; call it directly when figuring it out IS the goal. In attended sessions it can also offer to capture durable personal steering preferences (**Taste**) — drafted with rationale and flip condition, written to a marked section of the user-level or project-level memory file only on your explicit yes; autonomous, team, and unattended runs never offer or write taste. Docs mode and narrative logging are on by default; `--no-docs` skips bootstrap/glossary/ADR conventions, `--no-log` skips the default log under the user's home `.manifest-dev/logs/` directory, `--autonomous` lets it self-answer (used by `/auto`), `--team` moves the deliberation into a Slack channel or thread (used by `/figure-out-team`), `--scratch` (off by default) maintains a rough, domain-native supporting artifact under `.manifest-dev/scratch/` to ground long or complex sessions, and `--surface <name>` (default `text`) selects where the answers land — every value activates the `/chat-surface` skill, which owns how a turn is shaped for its destination: `text` in text mode, `chat-surface` in html mode, rendering the conversation live into an HTML page while you keep typing in the terminal.
- **`/chat-surface`** — owns how a turn is shaped for wherever its text lands. One destination-neutral rendering contract: every element earns its place by cutting reading load below what prose would cost, a non-prose form earns it by carrying a relationship prose would need several sentences for, form is chosen per point, tool runs render as meaning, weight follows information, and the skim layer is the test. Two modes supply the vocabulary. **Text mode** adds tables, box diagrams, fenced code and emphasis, under the rule that a form must stay readable when nothing renders it — no artifact is created. **HTML mode** adds charts, hand-drawn SVG diagrams, decision cards and unfolds, with the conversation landing in an auto-updating HTML page the user keeps open (their messages verbatim), updating live with no server as the page re-reads a `data.js` the agent extends each turn; activating it mid-conversation backfills everything so far, and it ships a default template (`assets/template.html`) that is the starting vocabulary, not a cage. Activated directly, or by `figure-out --surface <name>`.
- **`/define`** — encodes shared understanding into a verifiable Manifest. Not an interview: it makes the manifest-specific judgment calls (invariant vs process guidance, AC scope and pass threshold, gate kind) and pulls in `/figure-out` first if the understanding isn't there. Pass an existing manifest path in `$ARGUMENTS` to amend it in place. Supports `--babysit <pr-url>`. Emits a foreground `/do <manifest-path>` handoff; `/do` owns the durable manifest-completion contract.
- **`/do`** — executes a Manifest and evaluates every Acceptance Criterion and Global Invariant by pointing an evaluator at that gate in the manifest, never at a copy of its text. `--verification` selects `per-gate` (default), `consolidated`, or `self`; optional `--verifier-model` applies to the independent modes. Re-verification follows each gate's declared kind: a Deterministic Gate re-runs in full, while a Judgment Gate takes one full look and thereafter judges only its prior findings' repairs and the changed delta; `--exhaustive-verification` restores full re-sampling for a run that wants it. An evaluation expensive to repeat — a long end-to-end suite, the whole-change quality sweep — is spent once the gates whose failures would move its subject are settled. It calls `/done` when every gate has fresh mode-appropriate PASS evidence, or routes through `/escalate` when blocked. The policy is fixed at launch and never downgrades itself. Caller overlays can narrow retry cadence, e.g. CI one-shot runs report wait-only states instead of sleeping. The recommended unattended invocation uses the host's goal-setting or continuation backstop with the manifest's auditable completion condition: every criterion appears in a gate ledger with fresh evidence and provenance under the selected mode and `/done` reported. Bare `/do` runs a single foreground turn. An append-only execution log is on by default under the user's home `.manifest-dev/logs/` directory (`--no-log` opts out; a caller-supplied journal path is used instead when given), recording deviations from the Initial Approach or the Deliverable order, Process Guidance departures, dead ends, and operational notes — execution history lives there, never in the manifest. Mid-`/do` user messages default to invoking `/define` for amendment, with a one-line digest of amendment-time assumptions surfaced after.
- **`/just-do`** — goal-based Manifest executor beside `/do`. Reads a Manifest and pursues a state where every Acceptance Criterion and Global Invariant holds as written, deciding order, method, and how much checking for itself — no gate ledger, no verification modes, no execution log. The Manifest is read-only to the run: a statement gone false or a user redirect stops it for `/define` amendment and relaunch rather than being absorbed. When the host offers a goal-setting or continuation capability it sets the all-gates-hold goal and continues; otherwise it prints that goal for you to activate and re-invoke.
- **`/auto`** — chains `figure-out → define → do` autonomously, no approval gates. It accepts and forwards `/do`'s `--verification` and `--verifier-model` options without encoding them in the Manifest. Use the host's goal-setting or continuation backstop with one chain-complete condition for unattended cross-turn execution (recommended): if figure-out runs, full autonomous Read anatomy is a checkpoint before `/define`; terminal completion is manifest written plus `/do` gate-ledger PASS. Add `--babysit <pr-url>` for PR-lifecycle work.
- **`/just-auto`** — goal-based autonomous chain beside `/auto`: invokes `figure-out --autonomous`, then `define --autonomous`, then `just-do` with the resulting Manifest path — no approval waits, no verification flags. Arms one chain-spanning goal up front (understanding reached → Manifest written → every Acceptance Criterion and Global Invariant holds and completion reported), referencing the task and Manifest by path only; on a host without a goal capability it prints the goal and proceeds.
- **`/figure-out-team`** — thin discovery wrapper over `/figure-out --team`: the full figure-out discipline applied to a multi-party async Slack conversation, with the Slack mechanics (session-bound trust, `/loop` polling with `poll-slack` reads, mrkdwn, owner-by-Slack-handle convergence) living in figure-out's `references/team.md` overrides so team sessions inherit every figure-out upgrade. Docs context is loaded read-only by default unless `--no-docs`; local logging is on by default under the user's home `.manifest-dev/logs/` directory unless `--no-log`, and the log is never posted to Slack.
- **`/ticket-up`** — the single Ticket-authoring boundary. It accepts a finished Manifest, direct work, an independently managed question, or findings linked to a source Ticket, then shapes, deduplicates, grants, types, links, and renders the result through the project's configured venue. A Manifest becomes one coherent Shaped Ticket by default; split by Deliverable only when the caller explicitly wants delegation or parallel pickup. Questions and findings become separate Tickets only when separate assignment, priority, blocking, or closure has value. A follow-up receives Auto only when its source has Auto and the follow-up independently earns the grant. Stores: the project's shared tracker, GitHub Issues out of the box, or files where nobody needs cross-checkout claiming.
- **`/next-ticket`** — reads the store, names the single best ready Ticket under its priority rule, claims it, and presents the complete Ticket. It stops there: choosing work never starts an execution attempt.
- **`/run-ticket`** — receives one exact Ticket from a person or hosted trigger, claims or recovers it through one durable branch and pull request, invokes `/auto`, completes the required protected landing, and writes the terminal outcome back to the same store item. DONE follows the observed landing and closes the Ticket. ESCALATED leaves the same Ticket open and claimed for human continuation. It never scans the backlog or enforces Auto eligibility at dispatch.
- **`/sweep-tickets`** — the scheduled one-Ticket correctness path. It resumes one interrupted automation-owned Auto Ticket first, otherwise selects one ready Auto Ticket, invokes `/run-ticket`, and stops. Issue events remain the optional fast path; no label pulse, retry status, or batch orchestrator is introduced.

For hosted automation, the complete adapter is two invocations: an eligible issue event calls
`/run-ticket <issue>`, and a schedule calls `/sweep-tickets`. The adapter supplies a stable
automation identity, per-Ticket single-flight, finite provider retries, and one terminal runner-
failure handoff to a configured person. The harness-neutral contract and minimal GitHub shape live
in [`AUTOMATED_EXECUTION.md`](skills/ticket-up/references/AUTOMATED_EXECUTION.md).
- **`/init-context`** — sets a repository up with the surfaces the workflow reads from: a North Star (`NORTH_STAR.md`, the project's standing strategy surface — who it's for, the promise, what winning means — every line carrying a dated state, seeded only from what the repo's own artifacts evidence and never invented), an ADR conventions file the project owns (self-contained, so a teammate running no tooling can use it), a glossary, and a project-context-file section that makes every session read all three and maintain them — the North Star under its update asymmetry: evidence may lower a line's state, positions change only by the owner's ruling. Where the project has history, it seeds vocabulary and decision records from it — docs and pull-request discussion for reasoning, code and commits for what and when — and says so in the record when the reasoning could not be recovered rather than inventing one. Glossary candidates are ratified in one batch before anything is written, because that file is loaded on every session. Mining runs by default; `--no-mine` installs the wiring alone. `/figure-out` offers it when a project has neither surface.
- **`/done`** — completion summary in plain prose, called by `/do` after every criterion has fresh PASS evidence under the selected mode.
- **`/escalate`** — structured blocker: criterion, attempts and why each failed, possible resolutions, what's needed from you. Routed by `/do`.
- **`/review-code`** — quality review along **one dimension per invocation** (bugs, design, simplicity, maintainability, testability, test quality, type safety, contracts, operational readiness, docs, prose value, change intent, defect-class completeness after a fix, or CLAUDE.md adherence). Loads exactly that dimension's reference (progressive disclosure) and returns a PASS/FAIL report. A gate's body activates it; it replaces the per-dimension reviewer agents.
- **`/review-writing`** — reviews prose against the project's writing standards, in whichever register governs it: documentation (specs, reports, READMEs, reference material) or human-voiced writing (articles, copy, narrative). Detects the register, applies that register's rules plus the rules holding in both, and reports graded findings with the fix. Point it at a file, a directory, or pasted text; a project's own style sheet outranks the shipped standard. Review only — it reports, you edit.

## Manifest schema — one gate, one text

Every Acceptance Criterion and Global Invariant is a single text: a title, a body, and — where it earns its place — a why.
The text a reviewer reads is the text that binds — there is no separate evaluator-facing copy.

```markdown
#### AC-1.1 — Health endpoint answers under load

Done when /health returns 200 on all 50 concurrent requests, with no 5xx.

Why: the load balancer drops a node after one failed check.

Deterministic gate.
```

The title summarizes the body's headline requirement and never adds to it; a requirement living
only in the title is a defect. The why is optional and binds nothing — written where the body's
purpose would not be obvious cold, omitted where the body already carries it. The body says what done
means — and where the procedure that settles a criterion *is* what done means, that procedure
belongs in the body. Where a skill is the definition of done, the body names the skill and its
dimension and stops there: the skill owns its own threshold, so a bar copied into a gate is a
second statement that can contradict the first.

`kind` is the only structured metadata, carried on the closing line. It declares what settles
the gate, and `/do`
re-verifies by it: a `deterministic` gate re-runs in full every round, while a `judgment` gate
reads the whole change once and afterwards judges only its prior findings' repairs and the
changed delta. A gate mixing a command with a judgment is `judgment`; its commands still run in
full. A Manifest whose gate omits `kind` is invalid — nothing is guessed. So is one whose gates
carry a `verify` block or state a `phase`: both are the superseded schema, rejected with an
instruction to regenerate rather than migrated.

Gate evaluations return one of three states. **PASS** — the criterion holds. **FAIL** —
violated, with evidence: either a directive `/do` runs literally (when the body activates a
specialized skill like `check-pr`) or a prose fix hint read with judgment. **BLOCKED** — can't
be evaluated yet because an external action or state is pending (deploy, human approval), or the
Manifest itself could not be read; `/do` routes an actionable BLOCKED via `/escalate`.

A gate body says whatever an evaluator needs — run a bash command and check the exit code,
inspect files, query an API, fetch docs. It must not assume one agent per gate, a consolidated
verifier, self-verification, or a model, and it does not restate the run-wide comparison or the
verdict contract: those are `/do` launch choices and `/do` policy, not Manifest schema.

## Manifest sections

| Section | Purpose | ID Scheme |
|---------|---------|-----------|
| **Intent** | Problem, appetite, out of bounds | -- |
| **Initial Approach** (complex tasks) | Architecture — starting direction, departable | -- |
| **Global Invariants** | Task-level rules (task fails if violated) | `INV-G{N}` |
| **Process Guidance** | Advisory recommendations on how to work; weighed, not enforced | `PG-{N}` |
| **Known Assumptions** | Low-impact items resolved with a default | `ASM-{N}` |
| **Deliverables** | Work items with Acceptance Criteria, least-proven first | `AC-{D}.{N}` |

## Example Manifest

````markdown
# Definition: User Authentication

## 1. Intent
- **Problem:** Anyone with the app URL reads every user's data — there is
  no login at all.
- **Appetite:** Session auth over the existing endpoints, not an identity
  subsystem.
- **Out of bounds:** OAuth providers, account recovery, role permissions.

## 2. Initial Approach
- **Architecture:** Middleware-based auth, JWT in httpOnly cookies

## 3. Global Invariants (The Constitution)

### INV-G1 — Passwords are never stored in plaintext

Done when `grep -r 'password.*=' src/ | grep -v hash | grep -v test` returns no matches.

Why: a plaintext password in the store is unrecoverable once shipped — every other auth
control is downstream of this one.

Deterministic gate.

## 4. Process Guidance
- [PG-1] Follow existing error handling patterns in the codebase

## 6. Deliverables (The Work)

### Deliverable 1: Login round-trip

*What it is, and how it is exercised end-to-end:* signing in from the browser and reaching a
protected page — the credential check, the cookie, and the redirect exercised together.

#### AC-1.1 — POST /login returns a session for valid credentials

Done when POST /login with valid credentials returns 200 and sets a JWT in an httpOnly cookie
the protected routes accept.

Deterministic gate.

#### AC-1.2 — Invalid credentials fail cleanly

Done when the manifest-dev:review-code skill, activated with dimension=code-bugs over the auth
routes, reports nothing at or above that dimension's threshold — an invalid-credential path
returning 500 instead of 401 is the shape this catches.

Judgment gate.
````

## Manifest = current state

Amendments overwrite in place with stable IDs (modify `INV-G1` and it stays `INV-G1`; remove one and it's gone, no renumbering). No `## Amendments` log, no `INV-G1.1 amends INV-G1` chain — git carries the history.

The manifest is the canonical source of truth for the PR or branch, not for a single task — feedback flows through it. When something's off mid-`/do` or after `/done` (a missed edge case, a reviewer comment, a late requirement), Self-Amendment routes it automatically: `/escalate` → `/define` re-invoked on the manifest path to amend → `/do` resumes with the updated manifest. Pure questions about the manifest get answered inline; everything else amends. `/done` stays unreachable until every criterion verifies PASS again, so each round trip grows the verification surface — bug fixes and late requirements become permanent checked criteria.

## Verification skills

manifest-dev ships **no agents of its own**. `/do` uses host execution contexts according to the selected verification mode, and every mode reads the same gate text from the manifest, which can call for running bash, inspecting files, querying external tools, or activating a skill. Read-only behavior is enforced by that text, so authors can point an evaluator at MCP servers or extra CLI tools the user has configured.

Quality review (bugs, design, types, contracts, testability, …) is the **`review-code` skill** — one dimension per invocation; a gate body activates it when needed. The other functional skills are `check-pr` (PR mergeability checks) and `poll-slack` (tails Slack threads for `/figure-out-team`).

| Dimension | Role | Focus |
|-----------|------|-------|
| `change-intent` | defect (no LOW+) | Adversarial intent analysis: reconstructs intent, finds behavioral divergences |
| `code-bugs` | defect (no LOW+) | Mechanical defects: races, data loss, edge cases, resource leaks, dangerous defaults |
| `contracts` | defect (no LOW+) | Bidirectional API/interface contract checks against docs, schemas, codebase definitions |
| `type-safety` | defect (no LOW+) | Typed-language safety: type holes, representable invalid states, narrowing |
| `defect-class` | defect (no LOW+) | Completeness of a fix: the other sites the fixed mechanism reaches, and the disposition of each |
| `operational-readiness` | advisory (no MEDIUM+) | Runtime/deploy readiness: env wiring, migrations, retries, rollback, scale, CI, observability |
| `code-design` | advisory (no MEDIUM+) | Design fitness: reinvented wheels, wrong responsibility, under-engineering, PR coherence |
| `code-maintainability` | advisory (no MEDIUM+) | DRY violations, coupling, cohesion, dead code, consistency |
| `code-simplicity` | advisory (no MEDIUM+) | Over-engineering, premature optimization, cognitive complexity |
| `code-testability` | advisory (no MEDIUM+) | Excessive mocking, logic buried in IO, hidden dependencies |
| `test-quality` | advisory (no MEDIUM+) | Coverage gaps plus independent-oracle checks for tautology, mirror-impl, mock-SUT |
| `docs` | advisory (no MEDIUM+) | Documentation accuracy against code changes |
| `prose-value` | advisory (no MEDIUM+) | Comment/doc value: narrating-the-obvious, puffery, AI rhetorical patterns |
| `context-file-adherence` | advisory (no MEDIUM+) | Compliance with CLAUDE.md / AGENTS.md project rules |

## Task guidance and references

Task files come in two parallel, decoupled sets, each loaded by task type by its own skill: `skills/define/tasks/` carry domain-specific quality gates and Defaults that `/define` encodes into the manifest; `skills/figure-out/tasks/` carry probing fuel — blind-spot probes and forced trade-offs (verification among them) that `/figure-out` surfaces during understanding as awareness, not a checklist. Tech-design documents use both halves: figure-out surfaces audience/source/visual/taste probes, while /define encodes document gates. Source-type research material lives under `skills/define/tasks/research/sources/`. Mode and domain references in `skills/define/references/` (`BABYSIT_MODE.md`, `MULTI_REPO.md`, `WRITING-REFERENCE.md`) cover specialized flows.

**Multi-repo** (`MULTI_REPO.md`): by default a single manifest covers the whole changeset (Intent declares `Repos:`, deliverables tag `repo:`). `/do` navigates absolute paths from the map natively. PR-lifecycle work templates one `check-pr` skill run per repo against the shared manifest. Splitting into per-repo manifests is fine when the work is loosely coupled.
