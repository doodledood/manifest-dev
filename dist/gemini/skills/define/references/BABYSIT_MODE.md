# Babysit Mode

You are reading this file because `/define --babysit <pr-url>` was set. SKILL.md routes here; this file owns the entire babysit behavior — pre-flight, intent seeding, AC templating, interview style, error paths.

## Why this exists

The user wants to tend an existing PR without authoring a manifest from scratch. The PR may live in a repo that doesn't use manifest-dev. Babysit mode synthesizes a lifecycle-only manifest from the PR itself: intent seeded from title/body, ACs templated from PR_LIFECYCLE.md (a single AC invoking the `github-pr-lifecycle` agent). After synthesis, /do drives the PR to a mergeable state.

This is the entry path for "I have a PR open and want autonomous tending without a pre-existing manifest." The user can re-invoke `/define --amend <manifest>` later to add custom ACs beyond the lifecycle baseline.

## PR URL parsing

Canonical form: `https://github.com/<owner>/<repo>/pull/<N>`. Accept also: `gh:owner/repo/N`, `owner/repo#N`. Reject any URL whose host is not `github.com` (or platform-equivalent when `--platform` resolves to a non-github value) with: `Cannot babysit: URL <url> is not a <platform> PR URL.`

Extract owner, repo, pull number. These drive the agent invocation in the synthesized AC.

## Pre-flight (read-only — no side effects)

Pre-flight runs before any manifest is written or any side effect occurs. On failure: halt with an actionable error and exit.

1. **GitHub backend reachable.** Verify a working GitHub backend is available — GitHub MCP tools loaded OR `gh` CLI authenticated. The rejection message names what was tried.
2. **PR accessible.** Query the PR via the available backend. If the PR is not found, not visible to the authenticated user, or the API returns auth/permission errors → halt naming the URL and the specific failure mode.
3. **PR not already terminal.** If the PR is already closed or merged at synthesis time → halt with: `Cannot babysit: PR #<N> is already <state>. Babysit is for active PRs; closed/merged PRs need no further tending.` This is distinct from /do's "mergeable" terminal — here we're rejecting a PR someone else has already closed or merged, not the agent's own lifecycle terminal.
4. **Fork convention.** When the PR's `headRepository` differs from its `baseRepository` (cross-repo PR from a fork), babysit targets the **upstream repo where the PR lives** — i.e., the `baseRepository`'s owner/repo — not the fork. The agent invocation uses that canonical URL. Log the fork detection so the user can correct if they meant the fork copy. *Consequence*: any `push-update` or `fix-code` hint the agent emits would target the PR's head branch, which lives on the fork — /do may not have push access. In practice the agent surfaces this as a halt-shaped FAIL when a write is needed against a fork-origin head branch, deferring to the contributor to land the change themselves.
5. **Repo identity confirmation.** When `cwd` is a git checkout AND `origin` is configured AND its owner/repo differ from the PR's base repo → log a note, don't halt: "Babysit target (`<pr-owner/repo>`) differs from cwd `origin` (`<cwd-owner/repo>`). Continuing — babysit doesn't require a local checkout."

## Platform routing

`--platform` resolves before this file is entered. Babysit requires the resolved platform to match the PR URL's host:

- `--platform github` + github.com URL → proceed.
- `--platform github` + non-github URL → halt: `Cannot babysit: --platform github was set but URL host is <host>.`
- `--platform none` + any URL → halt: `Cannot babysit: --platform none cannot tend a PR; pass --platform github (or omit for auto-detection).`

When `--platform` was not explicitly passed, /define infers it from the PR URL's host (github.com → github). This differs from /define's fresh-mode inference (which uses the local `origin` remote) because babysit's use case is repos that may not be locally cloned.

## Intent seeding

After pre-flight succeeds, read PR title and body. Seed the manifest's Intent section:

- **Goal:** derived from PR title and the body's opening paragraph. Concise — one or two sentences naming what the PR is for.
- **Mental Model:** when the PR body contains a "context" / "background" / "why" section, fold it in. Otherwise leave minimal.
- **Mode:** thorough (default — babysit is for shipping work that matters).
- **Interview:** autonomous (rationale below).
- **Medium:** local.

## AC templating

Babysit synthesizes a lifecycle-only manifest. AC composition comes from `tasks/PR_LIFECYCLE.md` — one AC, invoking the `github-pr-lifecycle` agent, with the PR URL and branch templated into the prompt field. The baseline AC template (from PR_LIFECYCLE.md's Quality Gates section) is what /define writes; the agent owns the canonical gate logic at runtime.

**Steering surface.** /define populates the AC's `verify.prompt:` with baseline content (PR URL + branch). Custom steering (named approvers, known-flaky CI, custom labels) is **not probed during babysit** — autonomous interview keeps the synthesis fast. The user adds steering nuances later via `/define --amend <manifest-path>`, which routes through Amendment Mode for an interactive scoped interview.

**Multi-repo babysit.** Out of scope for this mode — babysit takes one PR URL. A user with a multi-repo changeset uses fresh /define with `Repos:` declared, not babysit.

## Interview style

Default: autonomous. Babysit's only AC is templated; there are no interview-resolvable scenarios, risks, or trade-offs beyond what PR_LIFECYCLE.md already encodes (which become PG/INV without probing).

The user can override with `--interview thorough` to force a probing pass — useful when they want to surface steering nuances upfront rather than via /define --amend after. /define honors the flag.

## Output

Write the manifest to `/tmp/manifest-{timestamp}.md`. Print the standard `Manifest complete:` line per /define's Complete section. The user runs /do (or invoked /auto --babysit, which chains automatically).

## Conflicts with other modes

- `--babysit` + `--amend` → halt: `Cannot babysit and amend simultaneously. --babysit synthesizes a new manifest from a PR; --amend modifies an existing one. Pick one.`
- `--babysit` without a URL argument → halt: `--babysit requires a PR URL. Usage: /define --babysit <pr-url>.`
- `--babysit` + free-form task description in `$ARGUMENTS` → the URL wins; the free-form text is ignored with a one-line log note. (Babysit's intent comes from the PR, not from $ARGUMENTS.)

## Post-babysit path

After /do reaches a terminal state (mergeable, or escalation), the manifest at `/tmp/manifest-{timestamp}.md` is archivable per the project's manifest archival convention. The user can re-invoke `/define --amend <manifest>` at any point to add custom ACs, steering refinements, or scope changes — Amendment Mode handles the rest.

## Gotchas

- **Babysit is one-shot synthesis.** It does not poll the PR or re-synthesize over time. Once the manifest is written, /do takes over.
- **Externally-closed PR mid-/do.** Detected by the agent at runtime, surfaced via FAIL with halt-shaped hint. /do treats this as terminal — it does not attempt to reopen.
- **PR description rewrites are scoped to /do.** Babysit reads the PR description for intent seeding but does not modify it. /do's `[push-update]` dispatch is what later syncs the description if the gate fires.
- **No retroactive seeding.** Intent is seeded once at synthesis. If the PR description changes substantively after babysit, the user re-invokes `/define --amend` to re-sync intent — not via re-running babysit.
