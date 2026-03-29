# LOCAL Messaging — Terminal Interaction

The user is at a terminal in the same session.

## Interaction Tool

Use `AskUserQuestion` for all decision-locking interactions. This is the tool that presents structured options to the user.

## Format Constraints

- 2-4 numbered options per question, one marked "(Recommended)"
- Never ask open-ended questions — present concrete options the user can accept, reject, or adjust
- Checkpoints and finding-sharing use normal conversation (not AskUserQuestion) — only lock decisions with the tool

## Channel Bootstrap

Not applicable — the user is already in the session.

## Discovery Log and Manifest

Write to `/tmp/` as normal. Present directly to the user in the terminal.

## Security

Not applicable — local session, no untrusted external input.
