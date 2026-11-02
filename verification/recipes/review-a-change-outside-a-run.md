---
kind: walk
covers: claude-plugins/manifest-dev/README.md
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Review a change outside a run

A reader comes to these documents to review a change outside a run, and should end able to pick the review skill for code, prose, or a design, or check a pull request's readiness, and invoke it directly.

## How a user reaches it

`claude-plugins/manifest-dev/README.md` → *Review and verification*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Review a change outside a run. End able to pick the review skill for code, prose, or a design, or check a pull request’s readiness, and invoke it directly. The sections to rely on: claude-plugins/manifest-dev/README.md → Review and verification.' claude-plugins/manifest-dev/README.md`
Proves: the reader ends able to pick the review skill for code, prose, or a design, or check a pull request's readiness, and invoke it directly, and names nothing it had to guess that blocks the task.
Check: read

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
