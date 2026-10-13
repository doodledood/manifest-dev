# Verification surface: reader tasks

This directory is how this project checks that its living documents still do their job: the
root `README.md`, `claude-plugins/README.md`, `claude-plugins/manifest-dev/README.md`,
`dist/pi/README.md`, `CONTRIBUTING.md`, and the explainer site, `site/index.html`. Runs use it
instead of working out each time what a reader comes to these documents to do, and keep it
current as they go.

## What it covers

`TASKS.md` holds one entry per task a reader comes to a document to do: the task, the document
and section the reader relies on, what the reader should end up able to do, and a status. A
Markdown section is named by its heading; a site section by its chapter name, the
`data-name` its `<section>` carries.

## How to run it

Give a reader with fresh context only the named document and the task, and ask it to do the
task from the document alone. Success is the reader ending able to do what the entry says. Record
where it got stuck as the entry's evidence.

`tests/test_reader_tasks.py` runs with the project's tests and fails when an entry names a file
or section that no longer exists, or carries no valid status.

## Statuses

Every entry carries one:

- `unverified` — catalogued but not yet walked. Not proof of anything.
- `verified` — walked by a fresh reader, with the date.
- `stale` — a run found it drifting from the document. The entry carries a dated line naming
  what differs, for example `stale (YYYY-MM-DD): the install section no longer names Pi`.

A run that changes something an entry covers updates and walks that entry. A run that finds an
entry it is not changing drifting marks it stale and leaves the repair to the next run that
touches it. A failure that is the document's fault, not the entry's, is reported, never papered
over by weakening the entry.

## Evidence

Walking an entry saves the reader's account to `docs/reader-tasks/evidence/`, named by entry and
date, which nothing removes.
