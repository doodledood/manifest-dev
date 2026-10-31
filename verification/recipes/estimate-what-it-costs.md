---
kind: walk
covers: README.md
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Estimate what it costs

A reader comes to these documents to estimate what it costs, and should end able to judge whether a task is worth the workflow's extra time and tokens.

## How a user reaches it

`README.md` → *What it costs*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Estimate what it costs. End able to judge whether a task is worth the workflow’s extra time and tokens. The sections to rely on: README.md → What it costs.' README.md`
Proves: the reader ends able to judge whether a task is worth the workflow's extra time and tokens, and names nothing it had to guess that blocks the task.
Check: read

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
