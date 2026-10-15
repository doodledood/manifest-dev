---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
append_system_prompt: |
  The user's memory file (~/.claude/CLAUDE.md, user-level, loaded in every session) contains:

  ## Taste

  - When choosing a messaging vendor (SMS, email, push), prefer one we already pay for over a new contract — every new vendor means another data-processing review and another bill to watch; yield when the existing vendor cannot deliver the channel at all.
  - Keep builds small — the plainest version that does the job beats a clever one; yield when the plain version would mislead a customer.
---
use the figure-out skill with --autonomous for this.

our vet clinic app needs appointment reminders by text message, because no-shows cost us about 30 slots a month. figure out how the reminders should work so we can plan the build: which sms provider, when the reminders go out and what they say, and how sending retries when the provider fails.

what we know:

- we already pay Textwell for the "your appointment is confirmed" texts. it supports scheduled sends and has a status webhook.
- Pingbird quoted 0.6p per text against Textwell's 0.8p. we'd need a new contract and a data-processing review.
- Textwell's docs: on a 429 or 5xx, retry with exponential backoff and jitter, at most 5 attempts, and honour the `Retry-After` header. a send is idempotent when you pass a `client_ref`.
- pet owners are a mix: some book months ahead for vaccines, some book the same week for a sick animal.

i'm afk for the next few hours - dont ask me anything, work it out on your own and come back with what you land on, how sure you are, what its based on, and what would change your mind.
