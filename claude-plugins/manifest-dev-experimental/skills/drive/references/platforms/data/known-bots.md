# Known Bots

> **Source of truth:** `claude-plugins/manifest-dev/skills/tend-pr/references/known-bots.md`. This file is a copy kept in sync intentionally (the experimental plugin's github adapter duplicates `tend-pr-tick` semantics per `T-1`). If you edit one, edit the other.

Use this reference to determine whether a PR commenter is a bot or human.

## Identification Rules

A commenter is a **bot** if ANY of the following match:

1. **Known bot names**: github-actions, dependabot, renovate, codecov, sonarcloud, codeclimate, snyk, deepsource, coderabbit, cursor, bugbot, copilot, claude, sweep, gitguardian, semgrep, trunk, sourcery, graphite, linear, vercel, netlify, railway, render, circleci, travisci
2. **[bot] suffix**: Username ends with `[bot]` (e.g. `dependabot[bot]`, `github-actions[bot]`)
3. **App-type account**: GitHub shows the account as "App" rather than "User" in the API response
4. **Bot badge**: The comment or review shows a "Bot" badge in the UI

## When Uncertain

If you can't determine bot vs human from the above rules, **default to human**. Treating a bot as human is safe (you'll leave threads open for "the reviewer" — harmless). Treating a human as a bot is risky (you might resolve their threads prematurely).
