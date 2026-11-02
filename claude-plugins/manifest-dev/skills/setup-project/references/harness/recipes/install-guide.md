---
kind: walk
covers: README.md
ask-first: a fresh AI reader walks the document, which uses model quota
---
# Install Notes from the README

A new user installs Notes and creates a first note using only the README.

## How a user reaches it

The *Install* and *First note* sections of the project README.

## Scenarios

### fresh-reader
Run: `scripts/agent-session --read-only README.md --prompt 'Using only README.md, install Notes and create a first note. Say where you got stuck.'`
Proves: the reader ends able to install Notes and create a note, and names nothing it had to guess.
Check: read

## Gotchas

- The reader must get only the named document; a reader that can browse the code proves nothing
  about the README.
