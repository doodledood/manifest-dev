---
kind: walk
covers: claude-plugins/manifest-dev/README.md
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Deliberate with people who cannot share a session

A reader comes to these documents to deliberate with people who cannot share a session, and should end able to run a figure-out deliberation in a Slack channel or thread with `/figure-out-team`.

## How a user reaches it

`claude-plugins/manifest-dev/README.md` → *Conversation*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Deliberate with people who cannot share a session. End able to run a figure-out deliberation in a Slack channel or thread with /figure-out-team. The sections to rely on: claude-plugins/manifest-dev/README.md → Conversation.' claude-plugins/manifest-dev/README.md`
Proves: the reader ends able to run a figure-out deliberation in a Slack channel or thread with `/figure-out-team`, and names nothing it had to guess that blocks the task.
Check: read
Workload: varies

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
