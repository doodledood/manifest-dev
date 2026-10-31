---
kind: walk
covers: claude-plugins/manifest-dev/README.md
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Set a project up

A reader comes to these documents to set a project up, and should end able to say what setting a project up installs, and how an older setup gets updates.

## How a user reaches it

`claude-plugins/manifest-dev/README.md` → *A project that remembers*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Set a project up. End able to say what setting a project up installs, and how an older setup gets updates. The sections to rely on: claude-plugins/manifest-dev/README.md → A project that remembers.' claude-plugins/manifest-dev/README.md`
Proves: the reader ends able to say what setting a project up installs, and how an older setup gets updates, and names nothing it had to guess that blocks the task.
Check: read

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
