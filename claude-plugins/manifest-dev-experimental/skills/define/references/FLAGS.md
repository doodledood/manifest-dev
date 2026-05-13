# Input Flags

`$ARGUMENTS` = task description, optionally with the flags below. Flags can appear anywhere. Empty `$ARGUMENTS` (or only flags with no free-form text) → ask: `What would you like to build or change?` — EXCEPT when amendment is detected from chat intent + transcript context (Session-Default Detection of a prior `Manifest complete:` line per `AMENDMENT_MODE.md`).

| Flag | Behavior |
|------|----------|
| `--autonomous` | Self-answer / no user wait. /define propagates to its `manifest-dev-experimental:figure-out` auto-invoke so figure-out plays both roles (see `figure-out/references/autonomous.md`). Skips Summary for Approval (treats as approved). Typically passed by `/auto`, but valid for direct user invocation when no user wait is desired. |
| `--babysit <pr-url>` | Synthesize a lifecycle-only manifest from an existing PR per `BABYSIT_MODE.md`. Missing or inaccessible URL → halt naming the failure. |
| `--platform github\|none` | PR-lifecycle platform. Omitted: with `--babysit`, infer from PR URL host; without `--babysit`, infer from `origin` remote (`github.com` → `github`, else `none`). When `--platform github` resolves, `tasks/PR_LIFECYCLE.md` composes onto `tasks/CODING.md`. Invalid value → halt. |
| `--canvas` | Generate a Shared Understanding Canvas per `CANVAS_MODE.md` (visual side-channel for misalignment-spotting during the interview). |

**Inferred (not flags) in experimental:**
- **Amendment intent** → chat-derived ("also handle X", "change Y", "that's wrong", "add a check for Z") + Session-Default Detection of a prior `Manifest complete:` line in transcript. Multiple ambiguous candidates → /define asks once which manifest to amend. Explicit override: user references a specific manifest path in chat (*"amend /tmp/manifest-X.md"*).
- **Fast-path (no Summary wait)** → caller context. /define infers whether it's invoked from /do's Self-Amendment path (no user wait) vs from a user typing `/define <task>` (interactive). The `--autonomous` flag is the explicit override.

**Dropped from experimental** (vs main plugin):
- `--mode efficient|balanced|thorough` (one mode in experimental)
- `--interview minimal|autonomous|thorough` (figure-out is the one interview style; `--autonomous` is the only mode dial)
- `--amend <path>` (inferred from chat + transcript)
- `--from-do` (inferred from caller context)
