---
kind: walk
covers: CONTRIBUTING.md, claude-plugins/README.md, claude-plugins/PLUGIN_TEMPLATE/README.md
ask-first: a fresh AI reader walks the documents, which uses model quota
dry-run: honored
---
# Add a plugin

A reader comes to these documents to add a plugin, and should end able to create a plugin from the template, register it in the marketplace, and test it locally.

## How a user reaches it

`CONTRIBUTING.md` → *Plugin Development Process*; `claude-plugins/README.md` → *Add a plugin*; `claude-plugins/PLUGIN_TEMPLATE/README.md` → *Layout* and *Steps*

## Scenarios

### fresh-reader
Run: `scripts/walk.sh 'Add a plugin. End able to create a plugin from the template, register it in the marketplace, and test it locally. The sections to rely on: CONTRIBUTING.md → Plugin Development Process; claude-plugins/README.md → Add a plugin; claude-plugins/PLUGIN_TEMPLATE/README.md → Layout and Steps.' CONTRIBUTING.md claude-plugins/README.md claude-plugins/PLUGIN_TEMPLATE/README.md`
Proves: the reader ends able to create a plugin from the template, register it in the marketplace, and test it locally, and names nothing it had to guess that blocks the task.
Check: read

## Gotchas

- The reader gets only the named documents, whole, and the sections to rely on; a reader that can browse the code proves nothing about the documents.
- When the document is at fault, not the recipe, report it and fix the document; never weaken the recipe to pass.
