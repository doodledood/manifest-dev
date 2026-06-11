---
name: figure-out-team
description: 'Drive a multi-party deliberation in a Slack channel or thread. The agent is an involved orchestrator — presses rigorously, brings evidence, names trade-offs, surfaces disagreements, advances when answers cohere; owner-by-Slack-handle overrules. Use when the people involved cannot all sit in one chat, when deliberation has to happen in Slack, or when the user asks to figure out with the team, press a group asynchronously, or get the team aligned.'
argument-hint: '[topic] [--with-docs] [--log [path]]'
user-invocable: true
---

Discovery wrapper for figure-out's team mode. The deliberation itself — trust boundary, Slack polling, mrkdwn, convergence and wrap-up rules — lives in the figure-out skill's `references/team.md` overrides, so team sessions inherit figure-out's full investigation discipline.

Invoke the figure-out skill with: "$ARGUMENTS --team"

Forward the topic and any flags (`--with-docs`, `--log [path]`) exactly as given.
