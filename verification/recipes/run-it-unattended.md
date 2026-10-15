---
kind: walk
covers: claude-plugins/manifest-dev/README.md
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Run it unattended

A reader comes to these documents to run it unattended, and should end able to start an unattended run and say where it stops for a person.

## How a user reaches it

`claude-plugins/manifest-dev/README.md` → *Run it unattended*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Run it unattended. End able to start an unattended run and say where it stops for a person. The sections to rely on: claude-plugins/manifest-dev/README.md → Run it unattended.' claude-plugins/manifest-dev/README.md`
Proves: the reader ends able to start an unattended run and say where it stops for a person, and names nothing it had to guess that blocks the task.
Check: read
Workload: varies

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
