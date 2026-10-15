---
kind: skill
covers: claude-plugins/manifest-dev/skills/figure-out-team
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# figure-out-team

Runs a figure-out investigation in a Slack channel or thread with several people, owner by Slack handle overruling, with the operator in the local session.

## How a user reaches it

- `/figure-out-team [topic] [--no-docs] [--no-log]`; `--no-docs` and `--no-log` are forwarded unchanged to figure-out.
- Phrases its description matches: "figure out with the team", "press a group asynchronously", "get the team aligned".
- figure-out itself, when a topic needs people who cannot share one chat.

## Scenarios

### start
Run: `scripts/drive-skill.sh figure-out-team verification/prompts/figure-out-team-start.md`
Proves: a first message appears in the named channel; the local session reports where it posted. Each posted turn carries one ask; nothing posts outside the named channel.
Check: read
Workload: varies

## Gotchas

- The prompt file carries the placeholder `THROWAWAY_SLACK_CHANNEL`; replace it with a channel or thread the run owns before driving.
- Needs Slack access from the session and a channel or thread the run owns.
- Posts reach real people and cannot be unsent. Use a throwaway channel.
- The drive container has no Slack connection, so this recipe stays `unreachable` through `scripts/drive-skill.sh` until one is configured for a throwaway channel.
- It is a thin wrapper: a team-flow defect is almost always in figure-out's `references/team.md`.
- `tests/test_skill_frontmatter.py` and `tests/test_entry_points.py` hold that the skill parses and stays in the declared set. No behavior case measures it. Team mechanics live in figure-out's `claude-plugins/manifest-dev/skills/figure-out/references/team.md`.
