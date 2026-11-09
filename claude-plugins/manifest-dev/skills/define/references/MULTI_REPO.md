# Multi-Repo Manifest Workflow

Canonical reference for tasks whose changeset spans multiple repositories.

A shared canonical manifest is the default: one manifest captures shared intent, every deliverable tagged with its repo, shared invariants. Splitting per repo is a legitimate user choice when work is loosely coupled — that case is just N independent single-repo manifests with no special rules. The manifest is **internal** (a working document for user and agent); PR descriptions do not reproduce it: each describes its own change and, where `PR_LIFECYCLE.md` composes, shows that change working. It lives at the durable manifests home `/define` chose at synthesis (emitted in the `Manifest complete:` line) with no primary repo owning it; if the file is ever lost, re-run /define against the same task and in-flight PRs continue under the new path. Multi-repo amendments use the single shared manifest — last-writer-wins on concurrent edits; collision rate is low, recovery is the writer noticing missing content and re-triggering. No file locking.

## Schema Additions

Multi-repo manifests extend the standard schema with two optional fields and one Process Guidance entry. Single-repo manifests omit all three.

**Intent** adds:

- **Repos:** name → absolute-path map listing every repo in scope. Names are short identifiers used by deliverables; paths are absolute filesystem locations.

  ```markdown
  - **Repos:**
      - backend: /home/user/projects/api
      - frontend: /home/user/projects/web
  ```

- **Branch:** single string naming the branch every repo uses; per-repo branch names are not supported.

  ```markdown
  - **Branch:** claude/sso-integration
  ```

**Each deliverable** that belongs to a specific repo carries a `**Repo:**` tag matching one of the `Repos:` names:

```markdown
### Deliverable 3: SSO endpoint
**Repo:** `backend`
```

`Repos:` and `Repo:` are documentation for human and agent readers — they don't gate /do.

**Process Guidance** adds one entry. The executor reads only the Manifest, so the Manifest itself tells it how to use the map:

```markdown
- [PG-N] One run covers every repo in `Repos:`. Reach each repo by its absolute path from that map, whichever directory the run starts in, while working and while judging any gate, and give those paths to whatever evaluates a gate.
```

Worked example:

```markdown
- **Repos:**
    - backend: /home/user/projects/api
    - frontend: /home/user/projects/web

### Deliverable 1: SSO endpoint
**Repo:** `backend`

*What it is, and how it is exercised end-to-end:* the SSO entry point, exercised by posting a
real SAML assertion to a running backend and following the session it hands back.

#### AC-1.1 — POST /auth/sso accepts a SAML assertion

Authority: hard — the integration request requires SAML sign-in with a session cookie.

Valid SAML sign-in returns a session accepted by the backend.

Evidence: Posting a test SAML assertion to the backend repo's running service
(`curl -X POST http://localhost:8080/auth/sso -d @/tmp/saml-test.xml`) returns 200 with a
session cookie set.

Deterministic gate.
```

## Cross-repo gates

Cross-repo verification often depends on prerequisites the user controls ("all PRs deployed to staging"). Such a criterion stays an AC, as `SCHEMA.md` → *Verdicts* says of every criterion that waits on outside action, and its Evidence names the prerequisite, so an evaluation that cannot reach it can report the wait and what is pending.

The path map lives in `Repos:` and is put to use by the Process Guidance entry above. It is never part of a gate's own text, and changes no gate's threshold.

## Lifecycle criteria

Where `../tasks/PR_LIFECYCLE.md` composes, its criteria are written once per repo in `Repos:`. `--babysit <pr-url>` is single-PR by construction; for multi-repo lifecycle tending, declare `Repos:` in the manifest and write the per-repo ACs.
