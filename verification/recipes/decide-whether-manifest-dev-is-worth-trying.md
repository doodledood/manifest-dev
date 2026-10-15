---
kind: walk
covers: README.md, site/index.html
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Decide whether manifest-dev is worth trying

A reader comes to these documents to decide whether manifest-dev is worth trying, and should end able to say what problem it solves and what it costs them to adopt.

## How a user reaches it

`README.md` → *The three things, and where they live* and *What it costs*; `site/index.html` → *Intro*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Decide whether manifest-dev is worth trying. End able to say what problem it solves and what it costs them to adopt. The sections to rely on: README.md → The three things, and where they live and What it costs; site/index.html → Intro.' README.md site/index.html`
Proves: the reader ends able to say what problem it solves and what it costs them to adopt, and names nothing it had to guess that blocks the task.
Check: read
Workload: varies

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
