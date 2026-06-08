# Babysit Mode

Synthesizes a lifecycle manifest from an existing PR so /do can tend it to mergeable. Entry path for "I have a PR open and want autonomous tending without authoring a manifest from scratch." User can amend later to add custom ACs beyond the lifecycle baseline. Babysit takes one URL; multi-repo changesets use fresh /define with `Repos:` declared.

Babysit is manifest-aware but manifest-optional. A user-authored manifest is the strongest grounding source when supplied to the caller; otherwise this mode synthesizes enough manifest structure from PR state for /do to execute safely.

## PR URL parsing

Canonical form: `https://github.com/<owner>/<repo>/pull/<N>`. Also accepted: `gh:owner/repo/N`, `owner/repo#N`. Reject non-`github.com` hosts with: `Cannot babysit: URL <url> is not a github PR URL. Babysit currently supports github.com only.` Extract owner, repo, pull number — they drive the AC's verifier invocation.

## Pre-flight (read-only — no side effects)

Halt on failure with an actionable error:

1. **GitHub backend reachable.** GitHub MCP tools loaded OR `gh` CLI authenticated. Reject naming what was tried.
2. **PR accessible.** Query the PR. Not found / not visible / auth errors → halt naming the URL and failure mode.
3. **PR not already terminal.** Closed/merged at synthesis → halt: `Cannot babysit: PR #<N> is already <state>. Babysit is for active PRs; closed/merged PRs need no further tending.`
4. **Fork convention.** When `headRepository` differs from `baseRepository` (cross-repo PR from a fork), babysit targets the **upstream** repo where the PR lives — the `baseRepository`'s owner/repo, not the fork. The verifier invocation uses that canonical URL. Log fork detection. *Consequence:* a code-fix the verifier suggests targets the PR's head branch, which lives on the fork — /do may not have push access. The verifier's hint flags this as unrecoverable from within /do (caller should escalate to a human), deferring to the contributor.
5. **Repo identity confirmation.** When `cwd` is a git checkout AND `origin` differs from the PR's base repo → note it (no halt): *"Babysit target (`<pr-owner/repo>`) differs from cwd `origin` (`<cwd-owner/repo>`). Continuing — babysit doesn't require a local checkout."*

## PR grounding

Ground the synthesized manifest in the strongest available evidence:

1. PR-linked or confidently discovered manifest.
2. PR title and description.
3. Commit messages and current diff.
4. PR comments and review threads.

Do not fuzzy-pick a repository manifest when confidence is low; synthesize from PR state instead. Comments are signals, not authority — they inform the lifecycle run but do not override stronger intent sources by recency.

## Intent seeding

After pre-flight succeeds, read PR title and body:

- **Goal:** derived from PR title and body's opening paragraph. One or two sentences naming what the PR is for.
- **Mental Model:** when the body has a "context" / "background" / "why" section, fold it in. Otherwise minimal.

If the PR description is stale or too thin to resolve substantive code decisions, encode that as a Known Assumption / Risk and let /do lower autonomy for ambiguous code changes while still tending mechanical lifecycle gates.

## AC templating

One AC, verified by a general-purpose agent that activates the `github-pr-lifecycle` skill, with PR URL + branch templated into the prompt field. There is no `verify.agent` field — `verify.prompt` instructs the verifier to activate the `github-pr-lifecycle` skill. Baseline template from `tasks/PR_LIFECYCLE.md` Quality Gates section. The `github-pr-lifecycle` skill owns canonical gate logic at runtime. /define populates `verify.prompt:` with baseline content (PR URL + branch); custom steering (named approvers, known-flaky CI, custom labels) is NOT probed during babysit — autonomous synthesis stays fast. User adds steering later via amendment.

## Output

Write manifest to `~/.manifest-dev/manifests/manifest-{ts}.md` — the same durable location /define uses, so the lifecycle manifest survives OS temp cleanup while a PR is tended over days. Fall back to a writable temp path only when the home directory isn't writable. Print the standard `Manifest complete:` line per /define's Complete — the line carries the actual path you wrote to. Callers such as `/auto --babysit` and `/babysit-pr` invoke `/do` directly after synthesis.

## Conflict halts

- `--babysit` without URL → halt: `--babysit requires a PR URL. Usage: /define --babysit <pr-url>.`
- `--babysit` + free-form task text in `$ARGUMENTS` → URL wins; text ignored with one-line note.
- `--babysit` + a manifest file path in `$ARGUMENTS` → halt: `Cannot babysit and amend simultaneously. --babysit synthesizes a new manifest from a PR; a manifest path triggers amendment. Pick one.`

## Gotchas

- **One-shot synthesis.** Does not poll or re-synthesize. Manifest written → /do takes over.
- **Externally-closed PR mid-/do.** Detected at runtime by the verifier (the general-purpose agent activating the `github-pr-lifecycle` skill); FAIL with a hint naming the terminal state. /do treats as terminal; does not reopen; autonomous amendment to suppress is forbidden.
- **PR description rewrites scoped to /do.** Babysit reads description for intent seeding but does not modify. /do's later sync hint handles description updates if the gate fires.
- **No retroactive seeding.** Intent seeded once at synthesis. If PR description changes substantively, user invokes amendment to re-sync intent — not by re-running babysit.
