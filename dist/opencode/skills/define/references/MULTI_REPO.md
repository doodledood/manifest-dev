# Multi-Repo Manifest Workflow

Canonical reference for tasks whose changeset spans multiple repositories. Single-repo manifests are unaffected.

A shared canonical manifest is the default: one manifest captures shared intent, every deliverable tagged with its repo, shared invariants, shared trade-offs. Splitting per repo is a legitimate user choice when work is loosely coupled — that case is just N independent single-repo manifests with no special rules. The manifest is **internal** (a working document for user and agent); PR descriptions stay summary-only. It lives at a writable scratch path (whatever `/define` chose at synthesis — emitted in the `Manifest complete:` line) with no primary repo owning it; if scratch is cleared, re-run /define against the same task and in-flight PRs continue under the new path. Multi-repo amendments use the single shared manifest — last-writer-wins on concurrent edits; collision rate is low, recovery is the writer noticing missing content and re-triggering. No file locking. /do reads `Repos:` and uses absolute paths when working in a non-cwd repo; user invokes /do once globally (agent navigates between repos) within one conversational session.

## Schema Additions

Multi-repo manifests extend the standard schema with two optional fields. Single-repo manifests omit both.

**Intent & Context** adds:

- **Repos:** name → absolute-path map listing every repo in scope. Names are short identifiers used by deliverables; paths are absolute filesystem locations.

  ```markdown
  - **Repos:**
      - backend: /home/user/projects/api
      - frontend: /home/user/projects/web
  ```

- **Branch:** single string naming the branch used in every repo. By default, all repos use the same branch name (matches the existing harness pattern). Divergent per-repo branch names not supported in this version; future extension could replace `Branch: <string>` with `Branches: [name → branch]`.

  ```markdown
  - **Branch:** claude/sso-integration
  ```

**Each deliverable** that belongs to a specific repo carries a `**Repo:**` tag matching one of the `Repos:` names:

```markdown
### Deliverable 3: SSO endpoint
**Repo:** `backend`
```

`Repos:` and `Repo:` are documentation for human and agent readers — they don't gate /do.

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

## Cross-repo gates and BLOCKED state

Cross-repo verification often depends on prerequisites the user controls ("all PRs deployed to staging"). The verifier subagent for such an AC returns **BLOCKED** with a note describing what's pending, and /do routes the BLOCKED via /escalate so the user can take the action. After the user signals readiness ("deployed", "go ahead"), re-invoke /do to re-evaluate the criterion.

When the manifest declares `Repos:`, every verifier subagent invocation gets the cross-repo path map injected as part of the verbatim prompt so verifiers have access to all repos' paths:

```
Available repos: backend=/home/user/projects/api, frontend=/home/user/projects/web

[criterion's verify.prompt: follows verbatim]
```

Single-repo manifests get no prefix injection.

## /done and /auto for multi-repo

/done fires **once per manifest**, including for multi-repo. No per-repo /done independence. Every AC + every Global Invariant across every repo's deliverables must verify PASS (with no BLOCKED pending) before /done is called. The cross-repo prompt-prefix injection above is what makes a single /done reachable: verifiers have all repo paths, so cross-repo behavior is checkable during normal /do flow. Multi-repo /done summary lists which repos' deliverables were verified.

/auto's chain (figure-out → define → do) covers the whole multi-repo implementation phase in one invocation, navigating between repos as deliverables require. Lifecycle tending is part of /do's execution when the manifest carries `github-pr-lifecycle` ACs (PR_LIFECYCLE.md auto-templates one per repo). `/auto --babysit <pr-url>` is single-PR by construction; for multi-repo lifecycle tending, declare `Repos:` in the manifest and let /define template the per-repo ACs.

The user is the coordinator: invoke /do (or /auto), manage each repo's PR with whatever workflow they prefer, signal readiness in chat when cross-repo prerequisites land (BLOCKED criteria re-evaluate on the next /do invocation). The system supports this workflow but does not automate it.
