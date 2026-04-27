# Multi-Repo Manifest Workflow

Canonical reference for tasks whose changeset spans multiple repositories. Read this when a manifest declares `Repos:` in its Intent. Core skills (`/define`, `/do`, `/verify`, `/done`, `/auto`, `AMENDMENT_MODE`) summarize the rules below and link here for the full specification. Optional consumer skills (`/tend-pr`, `/tend-pr-tick`, `/drive`, `/drive-tick`) describe how they ride the shared-manifest pattern in their own files — they are add-ons, not part of the core multi-repo workflow.

Single-repo manifests (no `Repos:` field) are unaffected by everything below.

## a. Principle

The shared canonical manifest is the **default and recommended** approach for multi-repo changesets: one manifest captures the whole thing — shared intent, all deliverables (each tagged with its repo), shared invariants, shared trade-offs. The reason it's the default: splitting per PR forces the user to hold cross-PR coherence in their head, which is the work the manifest exists to externalize.

Splitting per repo (one manifest per repo's PR) is a **legitimate user choice** when the work is loosely coupled and the user prefers independent scopes — they accept carrying the cross-PR coherence themselves. Everything below describes the shared-manifest case (when `Repos:` is declared in Intent); the split case is just N independent single-repo manifests and needs no special rules.

The manifest is **internal**. It is a working document for the user and the agent. PR descriptions remain summary-only — no manifest embed, no PR-side surfacing.

## b. Persistence

The canonical manifest lives at `/tmp/manifest-{timestamp}.md`. No archival. No copying to `.manifest/` for multi-repo. No primary repo "owns" it.

If the file is lost (reboot, `/tmp` cleared, session death), re-run `/define` against the same task. The recreated manifest restarts the working state; in-flight PRs continue under the new manifest path.

This is an explicit trade-off: durability infrastructure is more cost than re-running `/define` is occasional pain.

## c. Repo Registration

The manifest's `## 1. Intent & Context` section declares its multi-repo scope:

```markdown
- **Repos:**                                  # optional, multi-repo only
    - backend: /home/user/projects/api
    - frontend: /home/user/projects/web
- **Branch:** claude/sso-integration          # optional, single string (see §j)
```

Each deliverable that belongs to a specific repo carries a `repo:` tag matching one of the names above:

```markdown
### Deliverable 3: SSO endpoint
**Repo:** `backend`
```

`Repos:` and `repo:` exist for **documentation** — readers (human and agent) know which deliverable lives where. They are **not** an enforcement mechanism for `/do` or `/verify` (see §d). Optional consumer skills may use the tags for their own scope inference (e.g., a PR-tending tool routing feedback on backend's PR to backend-tagged deliverables), but core skills do not depend on this.

Single-repo manifests omit both `Repos:` and `repo:` entirely.

## d. /do Navigation

`/do` reads `Repos:` from the manifest and uses absolute paths in tool calls (Read/Edit/Write/Bash) when a deliverable lives outside cwd. The LLM handles navigation natively — there is no filter logic, no cwd-to-repo matching, no per-repo configuration in `/do`.

The user can invoke `/do` once globally (the agent navigates between repos as deliverables require), or per-repo with `--scope` (each `/do` handles its repo's slice). Either works.

`/do`'s execution log remains a single file per invocation: `/tmp/do-log-{timestamp}.md`. No per-repo log naming.

Worked example — manifest declares:

```markdown
- **Repos:**
    - backend: /home/user/projects/api
    - frontend: /home/user/projects/web

### Deliverable 1: SSO endpoint
**Repo:** `backend`
**Acceptance Criteria:**
- [AC-1.1] POST /auth/sso accepts SAML assertion
  ```yaml
  verify:
    method: bash
    command: "curl -X POST http://localhost:8080/auth/sso -d @/tmp/saml-test.xml"
  ```
```

`/do` invoked from any cwd reads `Repos:`, navigates to `/home/user/projects/api` for D1's edits via absolute paths, runs the verify command. No filter required.

## e. method: deferred-auto + /verify --deferred

Cross-repo gates often cannot run during normal `/do→/verify` flow because they depend on prerequisites the user controls (e.g., "all PRs deployed to staging"). They are still **automatically verifiable** — just user-triggered.

`method: deferred-auto` marks such criteria. Worked example:

```yaml
- [INV-G7] Frontend SSO login round-trips through deployed backend
  verify:
    method: deferred-auto
    agent: general-purpose
    prompt: "Hit https://staging.example.com/login with a test SAML assertion. Confirm successful redirect to /dashboard with a valid session cookie."
```

Normal `/verify` invocations skip `deferred-auto` criteria during the pass itself. **However, `/verify` will not call `/done` while deferred-auto criteria remain unverified** — instead it routes to `/escalate` with type "Deferred-Auto Pending," signaling the user to run `/verify --deferred` when prerequisites are ready. Only after the deferred-auto criteria pass via `/verify --deferred` does a subsequent normal `/verify` pass reach `/done`. The pass log's `deferred: true|false` field tracks which prior runs covered the deferred-auto set.

When the user signals readiness ("all PRs deployed"), they invoke:

```
/verify <manifest> <log> --deferred
```

This runs **only** `deferred-auto` criteria. Flag interactions:

- `--deferred` + `--scope` is supported. `--scope` narrows the deferred set to in-scope deliverables.
- `--deferred` does not interact with `--final`. It never enters the final-gate machinery.
- `--deferred` inherits `--mode`. Same parallelism and model routing as the parent invocation.

### Cross-repo path delivery to verifiers

When the manifest declares `Repos: [name: path, ...]`, every `/verify` invocation (selective, full, and `--deferred`) prepends a verbatim string to each verifier's prompt before the criterion's own prompt:

```
Available repos: backend=/home/user/projects/api, frontend=/home/user/projects/web

[criterion's own prompt follows]
```

This applies on every pass — not just `--deferred` — so cross-repo verifiers can run during normal `/do→/verify` flow. That's what allows `/done` to fire once per multi-repo manifest (§g) without forcing per-repo /done independence.

Single-repo manifests (no `Repos:` field) get no prefix injection. Manifests with no `deferred-auto` criteria see `/verify --deferred` as a no-op with a clean message.

## f. Shared Manifest Amendment Across PRs

The canonical `/tmp` manifest is shared across all PRs in a multi-repo changeset. Any tool that writes amendments — whether the user editing the file directly, or any optional consumer skill — operates on this single shared file.

There is **no concurrency engineering**. Two writers amending the same manifest at the same instant — last-writer-wins. The later write may overwrite the earlier write's amendment block. Recovery: the writer who lost their amendment notices the missing change in the next iteration and re-triggers it (e.g., re-add the comment that prompted it, or re-invoke whatever workflow generated it).

**Do not add file locking.** The collision rate is low (writes are brief), and the recovery cost is small compared to the complexity of locking, deadlock handling, and stale-lock cleanup.

This pattern is the contract for any optional PR-tending consumer skill (e.g., `/tend-pr`, `/drive`); those skills describe their per-PR usage in their own files.

## g. /done — One Per Manifest, Gated on Deferred-Auto

`/done` fires **once per manifest**, including for multi-repo manifests. There is no per-repo `/done` independence. /verify's "every AC across every deliverable" rule is preserved unchanged; for multi-repo, that means every AC in every repo's deliverables must pass before `/done` is called.

This is achievable because `/verify`'s cross-repo prompt-prefix injection (§e) fires on every pass when `Repos:` is declared — verifiers in normal `/do→/verify` flow have access to all repos' paths and can verify cross-repo behavior without `--deferred`.

**`/done` is gated on no deferred-auto criteria pending.** When the manifest contains `method: deferred-auto` criteria that have not been verified green via a prior `/verify --deferred`, `/verify` routes to `/escalate` ("Deferred-Auto Pending") instead of `/done` — making the user-as-coordinator handoff explicit rather than silently completing. After the user runs `/verify --deferred` and the deferred-auto criteria pass, a subsequent normal `/verify` pass reaches `/done`.

For multi-repo manifests, the `/done` summary lists which repos' deliverables were verified — providing a clear inventory of what landed across the changeset.

## h. User as Coordinator

There is no coordinator process, no primary repo, no orchestrator skill. The user coordinates by:

1. Invoking `/do` or `/auto` (once globally to navigate all repos, or per-repo with `--scope` for parallel execution).
2. Opening / managing each repo's PR with whatever PR-management workflow they prefer (manual, or via an optional consumer skill).
3. Triggering `/verify --deferred` once cross-repo prerequisites are in place (e.g., "all PRs merged and deployed").

The system supports this workflow but does not automate it. Coordination is a human concern that the manifest captures the *state* of, not a state machine the system drives.

## i. /auto Behavior

`/auto` chains `/define` → `/do` → optionally `/tend-pr`. The `/do` step **navigates all repos** declared in `Repos:` (per §d — no filter logic, LLM uses absolute paths from the map). A single `/auto` invocation can therefore complete the whole multi-repo implementation phase.

The per-cwd limitation is `/tend-pr`: when `--tend-pr` is set, `/auto` invokes `/tend-pr` from cwd, which sets up tending for cwd's PR only — `/tend-pr` is PR-bound by construction (see §f). To tend the other repos' PRs, invoke `/tend-pr` from each other repo's cwd.

This is the only multi-repo footgun in `/auto`: users may assume `--tend-pr` covers all PRs, when it covers only cwd's. The implementation phase itself runs to completion across all repos in one go.

## j. Branch-Name Convention

By default, all repos in a multi-repo changeset use the **same branch name**. This matches the existing harness pattern (per-repo branch declarations in the system prompt that share a branch identifier).

The manifest's Intent records the branch name as a single string:

```markdown
- **Branch:** claude/sso-integration
```

Divergent branch names per repo are not supported by this version. A future extension could replace `Branch: <string>` with `Branches: [name -> branch]` if real cases demand it.
