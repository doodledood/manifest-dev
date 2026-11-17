#!/usr/bin/env bash
# Relay: a repository of agent prompts whose context file points, in its own words, to a principles
# skill under the area word "assistant". One line departs from a prompt-engineering default and the
# prompt under review follows it; the other the prompt departs from, with no person's choice. The
# prompt's own note claims that line's yield, which the context file contradicts.
set -euo pipefail
git rev-parse --git-dir >/dev/null 2>&1 || git init -q
git branch -M main
git config user.name "Lee Moreau"
git config user.email "lee@relay.example"
git config commit.gpgsign false
git config core.hooksPath /dev/null
mkdir -p .agents/skills/assistant-principles .claude prompts
ln -s ../.agents/skills .claude/skills
cat > AGENTS.md <<'EOF'
# Relay

The prompts our release and support agents run. Every prompt in `prompts/` runs behind the tool
gateway.

Before you write or review anything in `prompts/`, read
`.agents/skills/assistant-principles/SKILL.md`: it is how we want those prompts written, and why.
EOF
ln -s AGENTS.md CLAUDE.md
cat > .agents/skills/assistant-principles/SKILL.md <<'EOF'
---
name: assistant-principles
description: 'Assistant principles for Relay: how the team wants the prompts in prompts/ written, and why. Use before writing or reviewing a prompt in this project.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- Hard limits go last, one line per limit, each starting with NEVER in capitals — reviewers scan the end of a prompt for them, and a limit worded as a positive target was missed in an incident. Yields for a prompt with no hard limit.
- A prompt that calls a tool ends with a `Tools:` line naming each tool it may call — the gateway grants only the tools on that line, and a prompt without it runs with none and fails quietly. Yields for a prompt that runs outside the gateway.

Before calling prompt work done, check it against these principles from a fresh start. Name each
departure kept, with the principle and why.
EOF
cat > prompts/release-notes.md <<'EOF'
<!-- Author's note: this prompt runs as a local script on the release machine, outside the gateway, so it needs no Tools: line. -->

Write the release notes for the next version of our app, for the people who use it.

Read the pull requests merged since the last tag with `gh pr list --state merged --search "merged:>=<tag date>"`. Group them as Features, Fixes and Internal, one line per pull request, in the past tense, each linking its pull request. If nothing was merged, say so in one line and stop.

NEVER include a pull request labelled internal-only.
EOF
git add -A
git commit -qm 'Release notes prompt'
