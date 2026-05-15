# Multi-Repo Manifest Workflow

Canonical reference for tasks whose changeset spans multiple repositories. Read when a manifest declares `Repos:` in its Intent. Single-repo manifests are unaffected by everything below. PR-lifecycle work composes the `github-pr-lifecycle` agent per-repo via PR_LIFECYCLE.md's templated AC.

## a. Principle

Shared canonical manifest is the default for multi-repo: one manifest captures shared intent, all deliverables (each tagged with its repo), shared invariants, shared trade-offs. Splitting per repo is a legitimate user choice when work is loosely coupled — they accept carrying cross-PR coherence themselves; that case is just N independent single-repo manifests with no special rules.

The manifest is **internal** — a working document for user and agent. PR descriptions remain summary-only; no manifest embed, no PR-side surfacing.

## b. Persistence

Canonical manifest lives at `/tmp/manifest-{ts}.md`. No primary repo "owns" it. If lost (reboot, `/tmp` cleared, session death), re-run /define against the same task; the recreated manifest restarts the working state, in-flight PRs continue under the new path. Explicit trade-off: durability infrastructure costs more than occasional re-run pain.

## c. Schema Additions

Multi-repo manifests extend the standard schema with two optional fields. Single-repo manifests omit both.

**Intent & Context** adds:

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

**Documentation, not enforcement.** `Repos:` and `Repo:` are for readers (human and agent) — they don't gate /do (see §d).

## d. /do Navigation

/do reads `Repos:` and uses absolute paths in tool calls when a deliverable lives outside cwd. No filter logic, no cwd-to-repo matching, no per-repo config. LLM handles navigation natively.

User invokes /do once globally (agent navigates between repos). A single /do invocation runs as a single conversational session — no per-repo session split.

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
    prompt: |
      Hit POST /auth/sso at the backend repo with a test SAML assertion
      (curl -X POST http://localhost:8080/auth/sso -d @/tmp/saml-test.xml).
      PASS if response is 200 with a session cookie set.
  ```
```

## e. Cross-repo gates and BLOCKED state

Cross-repo verification often depends on prerequisites the user controls ("all PRs deployed to staging"). The verifier subagent for such an AC returns **BLOCKED** with a note describing what's pending, and /do routes the BLOCKED via /escalate so the user can take the action. After the user signals readiness ("deployed", "go ahead"), re-invoke /do to re-evaluate the criterion.

When the manifest declares `Repos:`, every verifier subagent invocation gets the cross-repo path map injected as part of the verbatim prompt so verifiers have access to all repos' paths:

```
Available repos: backend=/home/user/projects/api, frontend=/home/user/projects/web

[criterion's verify.prompt: follows verbatim]
```

Single-repo manifests get no prefix injection.

## f. Shared Manifest Amendment Across PRs

The canonical /tmp manifest is shared across all PRs. Any tool that writes amendments operates on this single shared file.

**No concurrency engineering.** Two writers amending at the same instant → last-writer-wins. The later write may overwrite the earlier write's amendment block. Recovery: the writer who lost their amendment notices the missing change next iteration and re-triggers it. Collision rate is low (writes are brief); recovery cost is small vs locking complexity. Do not add file locking.

This pattern is the contract for any PR-tending consumer — including PR_LIFECYCLE.md's per-repo agent-AC templating, which writes one AC per repo against the same shared manifest.

## g. /done — One Per Manifest

/done fires **once per manifest**, including for multi-repo. No per-repo /done independence. The rule "every AC across every deliverable must PASS before /done" is preserved unchanged — every AC in every repo's deliverables must verify PASS (with no BLOCKED pending) before /done is called.

Multi-repo /done summary lists which repos' deliverables were verified — clear inventory of what landed across the changeset.

## h. User as Coordinator

No coordinator process, no primary repo, no orchestrator skill. User coordinates by: (1) invoking /do or /auto; (2) managing each repo's PR with whatever workflow they prefer; (3) signaling readiness in chat when cross-repo prerequisites land (BLOCKED criteria are re-evaluated on the next /do invocation). System supports this workflow but does not automate it.

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
