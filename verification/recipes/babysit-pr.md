---
kind: skill
covers: claude-plugins/manifest-dev-tools/skills/babysit-pr
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# babysit-pr

Tends the user's own pull request through CI, review threads, description sync and mergeability, fixing what it can, with or without an existing Manifest.

## How a user reaches it

- `/babysit-pr [pr-url] [--manifest <path>] [--ci] [--no-log]`; the Pi template `dist/pi/prompts/babysit-pr.md`.
- Phrases its description matches: "babysit my PR", "get this PR through CI and reviews".
- No other skill calls it.
- With no URL it takes the current branch's only open pull request. `--manifest <path>` uses that Manifest; otherwise it runs define `--babysit <url> --autonomous`, then do. Its journal is append-only at `~/.manifest-dev/logs/babysit-<owner>-<repo>-<N>.md`; `--no-log` turns it off.

## Scenarios

### ci-pass
Run: `scripts/drive-skill.sh babysit-pr verification/prompts/babysit-pr-ci-pass.md --tools`
Proves: one advance in the transcript, then exit; the journal file exists. Every push or reply on the pull request appears in the journal.
Check: read
Workload: varies

### external-feedback
Run: `scripts/drive-skill.sh babysit-pr verification/prompts/babysit-pr-external-feedback.md --scaffold verification/fixtures/pr-feedback --tools --max-turns 120`
Proves: the tend passes the existing journal to do, which repairs the demonstrated total defect while declining optional, false, and separate-scope suggestions with reasons. Existing dispositions survive new thread IDs; current thread handling still appears in local outbound records. The human thread stays open. The required approval remains pending or blocked, and no merge or live network mutation occurs. Inspect the actual export result, source diff, action records, and appended journal.
Check: read
Workload: varies

## Gotchas

- The prompt file carries the placeholder `THROWAWAY_PR_URL`; replace it with a throwaway pull request the run may push to before driving.
- Needs `gh auth status` to succeed in the session.
- It pushes commits and replies on GitHub; those reach reviewers and do not undo.
- A drive through `scripts/drive-skill.sh` runs as you, with whatever GitHub access the driving machine has, so drive it only with a prompt naming a throwaway repository the run owns; where `gh` is not signed in, its GitHub entry points are `unreachable`.
- `--ci` is one advance, not a waiter.
- The external-feedback replay uses local observations and action records. It does not establish live GitHub transport, bot scheduling, or successful mutations. Its ask-first drive is unmeasured.
- `tests/test_goal_contract_blocks.py` checks it owns the goal; `tests/test_dist_skill_references.py` checks its define coupling, journal contract, and Pi template.
