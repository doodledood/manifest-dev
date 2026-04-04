# LOCAL Messaging — Terminal Interaction

The user is at a terminal in the same session.

## Interaction Tool

The interaction tool is `AskUserQuestion` — use it for decisions, confirmations, clarifications, and direction. This is the tool that presents structured options to the user.

## Format Constraints

- 2-4 options per question, one marked "(Recommended)"
- Questions always present concrete options the user can accept, reject, or adjust — never open-ended when you need a specific answer
- Checkpoints, finding-sharing, and transparent discussion use normal conversation (not AskUserQuestion) — use the tool only when you need something back from the user

## Channel Bootstrap

Not applicable — the user is already in the session.

## Discovery Log and Manifest

Write to `/tmp/` as normal. Present directly to the user in the terminal.

## Security

Not applicable — local session, no untrusted external input.
