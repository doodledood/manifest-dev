---
kind: walk
covers: claude-plugins/manifest-dev-tools/README.md
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Pick the tools skill for a job

A reader comes to these documents to pick the tools skill for a job, and should end able to name the tools skill that reviews another author's pull request, tends the reader's own, reviews a prompt, or hands a session to a fresh agent.

## How a user reaches it

`claude-plugins/manifest-dev-tools/README.md` → *Pull requests* and *Prompts* and *People and sessions*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Pick the tools skill for a job. End able to name the tools skill that reviews another author’s pull request, tends the reader’s own, reviews a prompt, or hands a session to a fresh agent. The sections to rely on: claude-plugins/manifest-dev-tools/README.md → Pull requests and Prompts and People and sessions.' claude-plugins/manifest-dev-tools/README.md`
Proves: the reader ends able to name the tools skill that reviews another author's pull request, tends the reader's own, reviews a prompt, or hands a session to a fresh agent, and names nothing it had to guess that blocks the task.
Check: read
Workload: varies

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
