---
kind: walk
covers: claude-plugins/manifest-dev/README.md
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Get design direction for an artifact

A reader comes to these documents to get design direction for an artifact, and should end able to ask `/design` for direction on an artifact and know which skill evaluates the result.

## How a user reaches it

`claude-plugins/manifest-dev/README.md` → *First-principles design*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Get design direction for an artifact. End able to ask /design for direction on an artifact and know which skill evaluates the result. The sections to rely on: claude-plugins/manifest-dev/README.md → First-principles design.' claude-plugins/manifest-dev/README.md`
Proves: the reader ends able to ask `/design` for direction on an artifact and know which skill evaluates the result, and names nothing it had to guess that blocks the task.
Check: read

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
