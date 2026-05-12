# Input Flags

`$ARGUMENTS` = task description, optionally with the flags below. Flags can appear anywhere. Empty `$ARGUMENTS` (or only flags with no free-form text) → ask: `What would you like to build or change?` — EXCEPT when any amend trigger applies (`--amend` is set, OR `$ARGUMENTS` contains a `/tmp/manifest-*.md` path).

| Flag | Behavior |
|------|----------|
| `--amend <path>` | Amend the manifest at `<path>` per `AMENDMENT_MODE.md`. Missing argument → halt: `Cannot amend: --amend requires a manifest path.` Path doesn't exist → halt: `Cannot amend: '<path>' not found.` |
| `--from-do` | Marks the amendment as triggered by /do (autonomous fast path — no summary approval). Used with `--amend`. Accepts no value. |
| `--babysit <pr-url>` | Synthesize a lifecycle-only manifest from an existing PR per `BABYSIT_MODE.md`. Missing or inaccessible URL → halt naming the failure. `--babysit` + `--amend` together → halt: `Cannot babysit and amend simultaneously.` |
| `--platform github\|none` | PR-lifecycle platform. Omitted: with `--babysit`, infer from PR URL host; without `--babysit`, infer from `origin` remote (`github.com` → `github`, else `none`). When `--platform github` resolves, `tasks/PR_LIFECYCLE.md` composes onto `tasks/CODING.md`. Invalid value → halt. |
| `--canvas` | Generate a Shared Understanding Canvas per `CANVAS_MODE.md` (visual side-channel for misalignment-spotting during the interview). |

**Dropped from experimental** (vs main plugin): `--mode efficient|balanced|thorough` (one mode in experimental), `--interview minimal|autonomous|thorough` (figure-out is the one interview style).
