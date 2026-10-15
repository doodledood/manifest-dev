---
kind: walk
covers: README.md, claude-plugins/manifest-dev/README.md, site/index.html
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Know what persists between runs

A reader comes to these documents to know what persists between runs, and should end able to name what a later run inherits from an earlier one, and where each piece lives.

## How a user reaches it

`README.md` → *The codebase gets easier to change, run by run*; `claude-plugins/manifest-dev/README.md` → *What the workflow maintains*; `site/index.html` → *Weeks later*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Know what persists between runs. End able to name what a later run inherits from an earlier one, and where each piece lives. The sections to rely on: README.md → The codebase gets easier to change, run by run; claude-plugins/manifest-dev/README.md → What the workflow maintains; site/index.html → Weeks later.' README.md claude-plugins/manifest-dev/README.md site/index.html`
Proves: the reader ends able to name what a later run inherits from an earlier one, and where each piece lives, and names nothing it had to guess that blocks the task.
Check: read
Workload: varies

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
