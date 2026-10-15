---
kind: walk
covers: site/index.html
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Try the workflow from the site

A reader comes to these documents to try the workflow from the site, and should end able to install it and run a first session from the site alone.

## How a user reaches it

`site/index.html` → *Try it*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Try the workflow from the site. End able to install it and run a first session from the site alone. The sections to rely on: site/index.html → Try it.' site/index.html`
Proves: the reader ends able to install it and run a first session from the site alone, and names nothing it had to guess that blocks the task.
Check: read
Workload: varies

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
