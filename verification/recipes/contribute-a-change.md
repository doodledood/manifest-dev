---
kind: walk
covers: CONTRIBUTING.md, README.md
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Contribute a change

A reader comes to these documents to contribute a change, and should end able to run the checks a pull request needs and open one.

## How a user reaches it

`CONTRIBUTING.md` → *Pull Request Process*; `README.md` → *Development*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Contribute a change. End able to run the checks a pull request needs and open one. The sections to rely on: CONTRIBUTING.md → Pull Request Process; README.md → Development.' CONTRIBUTING.md README.md`
Proves: the reader ends able to run the checks a pull request needs and open one, and names nothing it had to guess that blocks the task.
Check: read

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
