---
kind: walk
covers: README.md, claude-plugins/manifest-dev/README.md
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Pick the entry point for a piece of work

A reader comes to these documents to pick the entry point for a piece of work, and should end able to choose between `/figure-out`, `/define`, `/do`, and `/auto` for a given task.

## How a user reaches it

`README.md` → *One piece of work*; `claude-plugins/manifest-dev/README.md` → *The three beats*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Pick the entry point for a piece of work. End able to choose between /figure-out, /define, /do, and /auto for a given task. The sections to rely on: README.md → One piece of work; claude-plugins/manifest-dev/README.md → The three beats.' README.md claude-plugins/manifest-dev/README.md`
Proves: the reader ends able to choose between `/figure-out`, `/define`, `/do`, and `/auto` for a given task, and names nothing it had to guess that blocks the task.
Check: read
Workload: varies

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
