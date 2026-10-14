---
kind: walk
covers: claude-plugins/manifest-dev/README.md
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Read a Manifest

A reader comes to these documents to read a Manifest, and should end able to read a Manifest and say what each section binds.

## How a user reaches it

`claude-plugins/manifest-dev/README.md` → *Manifest sections*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Read a Manifest. End able to read a Manifest and say what each section binds. The sections to rely on: claude-plugins/manifest-dev/README.md → Manifest sections.' claude-plugins/manifest-dev/README.md`
Proves: the reader ends able to read a Manifest and say what each section binds, and names nothing it had to guess that blocks the task.
Check: read

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
