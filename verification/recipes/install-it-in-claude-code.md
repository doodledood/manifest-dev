---
kind: walk
covers: README.md
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Install it in Claude Code

A reader comes to these documents to install it in Claude Code, and should end able to install the marketplace and the plugin, and start a first `/figure-out`.

## How a user reaches it

`README.md` → *Install*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Install it in Claude Code. End able to install the marketplace and the plugin, and start a first /figure-out. The sections to rely on: README.md → Install.' README.md`
Proves: the reader ends able to install the marketplace and the plugin, and start a first `/figure-out`, and names nothing it had to guess that blocks the task.
Check: read

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
