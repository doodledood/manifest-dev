# Multi-Repo Manifest Workflow

Canonical reference for tasks whose changeset spans multiple repositories. Read when a manifest declares `Repos:` in its Intent. Single-repo manifests are unaffected by everything below. PR-lifecycle work composes the `github-pr-lifecycle` agent per-repo via PR_LIFECYCLE.md's templated AC.

## a. Principle

Shared canonical manifest is the default for multi-repo: one manifest captures shared intent, all deliverables (each tagged with its repo), shared invariants, shared trade-offs. Splitting per repo is a legitimate user choice when work is loosely coupled — they accept carrying cross-PR coherence themselves; that case is just N independent single-repo manifests with no special rules.

The manifest is **internal** — a working document for user and agent. PR descriptions remain summary-only; no manifest embed, no PR-side surfacing.

## b. Persistence

Canonical manifest lives at `/tmp/manifest-{ts}.md`. No primary repo "owns" it. If lost (reboot, `/tmp` cleared, session death), re-run /define against the same task; the recreated manifest restarts the working state, in-flight PRs continue under the new path. Explicit trade-off: durability infrastructure costs more than occasional re-run pain.

## c. Schema Additions

Multi-repo manifests extend the standard schema with three optional fields. Single-repo manifests omit all of them.

**Intent & Context** adds two fields:

- **Repos:** name → absolute-path map listing every repo in scope. Names are short identifiers used by deliverables; paths are absolute filesystem locations.

  ```markdown
  - **Repos:**
      - backend: /home/user/projects/api
      - frontend: /home/user/projects/web
  ```

- **Branch:** single string naming the branch used in every repo (see §j; divergent per-repo branch names not supported in this version).

  ```markdown
  - **Branch:** claude/sso-integration
  ```

**Each deliverable** that belongs to a specific repo carries a `**Repo:**` tag matching one of the `Repos:` names:

```markdown
### Deliverable 3: SSO endpoint
**Repo:** `backend`
```

**Verify methods** include `deferred-auto` (valid in any manifest) for criteria the user explicitly triggers — most commonly cross-repo gates with user-controlled prerequisites. See §e.

**Documentation, not enforcement.** `Repos:` and `Repo:` are for readers (human and agent) — they don't gate /do or /verify (see §d).

## d. /do Navigation

/do reads `Repos:` and uses absolute paths in tool calls when a deliverable lives outside cwd. No filter logic, no cwd-to-repo matching, no per-repo config. LLM handles navigation natively.

User invokes /do once globally (agent navigates between repos) OR per-repo with `--scope` (parallel execution). Either works. A single /do invocation runs as a single conversational session — no per-repo session split.

Worked example:

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

## e. method: deferred-auto + chat-signaled readiness

Cross-repo gates often depend on prerequisites the user controls ("all PRs deployed to staging"). They're automatically verifiable, just user-triggered.

`method: deferred-auto` marks such criteria. Verify blocks MUST declare `inner_method:` (`subagent` | `bash` | `codebase` | `research`); when /verify includes deferred-auto criteria in a pass, the criterion is routed identically to a non-deferred criterion of that `inner_method`. Example:

```yaml
- [INV-G7] Frontend SSO login round-trips through deployed backend
  verify:
    method: deferred-auto
    inner_method: subagent
    agent: general-purpose
    prompt: "Hit https://staging.example.com/login with a test SAML assertion. Confirm successful redirect to /dashboard with a valid session cookie."
```

By default /verify skips deferred-auto criteria during the pass. **But /verify will not call /done while deferred-auto remain unverified** — routes to /escalate "Deferred-Auto Pending" instead, telling the user to signal readiness in chat and re-invoke /verify when prerequisites are ready. /verify's return block's `deferred: true|false` field tracks which prior runs covered the set.

When the user signals readiness in chat ("all PRs deployed", "staging is up", "go ahead"), the next /verify invocation reads the recent conversation context, detects the signal, and includes deferred-auto criteria in that pass. No flag needed.

Rules:

- `--scope` is supported alongside the chat signal — narrows the deferred set to in-scope deliverables.
- INV-G\* deferred-auto criteria are deliverable-scope-independent — `--scope` does not cover them. Only covered by an inclusion-firing pass with empty `--scope`. /done remains gated on the escalation until that uncovered set runs green.
- Ambiguous chat signals default to skip — uncovered deferred-auto blocks /done; user re-signals more explicitly if needed.

### Cross-repo path delivery to verifiers

When the manifest declares `Repos:`, every /verify invocation prepends a verbatim string to each verifier's prompt before the criterion's own:

```
Available repos: backend=/home/user/projects/api, frontend=/home/user/projects/web

[criterion's own prompt follows]
```

Applies on every pass — cross-repo verifiers can run during normal /do→/verify flow. That's what allows /done to fire once per multi-repo manifest (§g) without forcing per-repo /done independence. Single-repo manifests get no prefix injection.

## f. Shared Manifest Amendment Across PRs

The canonical /tmp manifest is shared across all PRs. Any tool that writes amendments operates on this single shared file.

**No concurrency engineering.** Two writers amending at the same instant → last-writer-wins. The later write may overwrite the earlier write's amendment block. Recovery: the writer who lost their amendment notices the missing change next iteration and re-triggers it. Collision rate is low (writes are brief); recovery cost is small vs locking complexity. Do not add file locking.

This pattern is the contract for any PR-tending consumer — including PR_LIFECYCLE.md's per-repo agent-AC templating, which writes one AC per repo against the same shared manifest.

## g. /done — One Per Manifest, Gated on Deferred-Auto

/done fires **once per manifest**, including for multi-repo. No per-repo /done independence. /verify's "every AC across every deliverable" rule preserved unchanged — every AC in every repo's deliverables must pass before /done is called.

Achievable because /verify's cross-repo prompt-prefix injection (§e) fires on every pass when `Repos:` is declared — verifiers have access to all repos' paths and can verify cross-repo behavior during normal /do→/verify flow.

**/done is gated on no deferred-auto pending.** When uncovered deferred-auto criteria exist, /verify routes to /escalate "Deferred-Auto Pending" instead of /done — making the user-as-coordinator handoff explicit. After user signals readiness and deferred-auto criteria pass, a subsequent normal /verify pass reaches /done.

Multi-repo /done summary lists which repos' deliverables were verified — clear inventory of what landed across the changeset.

## h. User as Coordinator

No coordinator process, no primary repo, no orchestrator skill. User coordinates by: (1) invoking /do or /auto (once globally, or per-repo with `--scope`); (2) managing each repo's PR with whatever workflow they prefer; (3) signaling readiness in chat when cross-repo prerequisites land. System supports this workflow but does not automate it.

## i. /auto Behavior

/auto chains figure-out → define → do. The /do step navigates all repos declared in `Repos:` per §d. Single /auto invocation can complete the whole multi-repo implementation phase.

Lifecycle tending is part of /do's execution when the manifest carries lifecycle ACs — PR_LIFECYCLE.md auto-templates one `github-pr-lifecycle` AC per repo (per §f shared-manifest pattern), and /do's verify-fix loop drives each PR to mergeable. No separate "drive" step.

`/auto --babysit <pr-url>` is single-PR by construction. For multi-repo lifecycle tending, declare `Repos:` in the manifest and let /define template the per-repo ACs.

## j. Branch-Name Convention

By default, all repos in a multi-repo changeset use the **same branch name**. Matches the existing harness pattern. Recorded in Intent as a single string:

```markdown
- **Branch:** claude/sso-integration
```

Divergent per-repo branch names not supported. Future extension could replace `Branch: <string>` with `Branches: [name -> branch]` if real cases demand it.
