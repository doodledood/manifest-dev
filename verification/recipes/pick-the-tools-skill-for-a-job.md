---
kind: walk
covers: claude-plugins/manifest-dev-tools/README.md
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Pick the tools skill for a job

A reader comes to these documents to pick the tools skill for a job, and should end able to name the tools skill that reviews another author's pull request, tends the reader's own, reviews a prompt, or hands a session to a fresh agent, or improves an existing artifact round after round toward a goal.

## How a user reaches it

`claude-plugins/manifest-dev-tools/README.md` → *Pull requests* and *Improving what exists* and *Prompts* and *People and sessions*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Pick the tools skill for a job. End able to name the tools skill that reviews another author’s pull request, tends the reader’s own, reviews a prompt, hands a session to a fresh agent, or improves an existing artifact round after round toward a goal, and say whether that one pushes the result without being asked. Also identify which review helper advises whether landing a change serves the project, whether the reader invokes it directly, and whether its advice binds. The sections to rely on: claude-plugins/manifest-dev-tools/README.md → Pull requests, Improving what exists, Prompts and People and sessions.' claude-plugins/manifest-dev-tools/README.md`
Proves: the reader ends able to name the tools skill that reviews another author's pull request, tends the reader's own, reviews a prompt, hands a session to a fresh agent, or improves an existing artifact toward a goal (`/hillclimb`, which pushes nothing unless asked), identifies review-pr-judgment as a helper called by review-pr rather than directly by the reader, describes its project-consequence advice as non-binding, and names nothing it had to guess that blocks the task.
Check: read

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
