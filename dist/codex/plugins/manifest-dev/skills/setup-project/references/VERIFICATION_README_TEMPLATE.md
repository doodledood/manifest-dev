# Verification surface

<!-- Template: setup-project emits everything below this comment as the README of a project's
     verification surface, adapted to its form. Changing the emitted text needs a new surfaces
     version in CHANGES.md; the repository test enforces it. -->

This directory is how this project checks that <artifact> still does its job. Runs use it
instead of working out each time how to <launch and drive the product | run the behavior cases |
walk the reader tasks>, and keep it current as they go.

## What it covers

<One line per entry kind: features of the product, behaviors the prompts owe, or tasks a reader
comes to the document to do.>

## How to run it

<The commands that launch, check, exercise and clean up — or run the cases, or walk the tasks —
each with what success looks like.>

## Statuses

Every entry carries one. <For a feature map or a reader-task list:>

- `unverified` — catalogued but not yet exercised. Not proof of anything.
- `verified` — exercised by a run, with the date.
- `stale` — a run found it drifting from <the product | the document>. The entry carries a
  dated line naming what differs, for example
  `stale (YYYY-MM-DD): the route moved from /settings to /preferences`.

<For an eval suite:>

- `unmeasured` — written but never run. Not proof of anything.
- `measured` — run, with the date and the result.
- `stale` — a prompt it covers changed after it was measured, so its numbers no longer hold.

A run that changes something an entry covers updates and exercises that entry. A run that finds
an entry it is not changing drifting marks it stale and leaves the repair to the next run that
touches it. A failure that is the product's fault, not the entry's, is reported, never papered
over by weakening the entry.

## Evidence

Exercising an entry saves its evidence to <location>, which cleanup never removes.
