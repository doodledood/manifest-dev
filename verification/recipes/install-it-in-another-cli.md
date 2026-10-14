---
kind: walk
covers: README.md, dist/codex/README.md, dist/opencode/README.md, dist/pi/README.md
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Install it in another CLI

A reader comes to these documents to install it in another CLI, and should end able to install it in Codex, OpenCode, or Pi, and name what differs from Claude Code.

## How a user reaches it

`README.md` → *Other CLIs*; `dist/codex/README.md` → *Install* and *Parity with Claude Code*; `dist/opencode/README.md` → *Install* and *Parity with Claude Code*; `dist/pi/README.md` → *Install* and *Parity with Claude Code*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Install it in another CLI. End able to install it in Codex, OpenCode, or Pi, and name what differs from Claude Code. The sections to rely on: README.md → Other CLIs; dist/codex/README.md → Install and Parity with Claude Code; dist/opencode/README.md → Install and Parity with Claude Code; dist/pi/README.md → Install and Parity with Claude Code.' README.md dist/codex/README.md dist/opencode/README.md dist/pi/README.md`
Proves: the reader ends able to install it in Codex, OpenCode, or Pi, and name what differs from Claude Code, and names nothing it had to guess that blocks the task.
Check: read

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
