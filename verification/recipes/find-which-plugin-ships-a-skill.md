---
kind: walk
covers: claude-plugins/README.md
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Find which plugin ships a skill

A reader comes to these documents to find which plugin ships a skill, and should end able to name the plugin that ships a given skill and install only that one.

## How a user reaches it

`claude-plugins/README.md` → *The plugins*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Find which plugin ships a skill. End able to name the plugin that ships a given skill and install only that one. The sections to rely on: claude-plugins/README.md → The plugins.' claude-plugins/README.md`
Proves: the reader ends able to name the plugin that ships a given skill and install only that one, and names nothing it had to guess that blocks the task.
Check: read
Workload: varies

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
