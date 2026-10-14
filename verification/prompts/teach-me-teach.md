/manifest-dev-tools:teach-me

# Loans are stored in one JSON file

Status: accepted

## Context

The reading club runs shelfnote on three laptops that share a synced folder. Loans were kept in a spreadsheet that two people edited at once, and edits were lost.

## Decision

Shelfnote keeps every loan in one file, `data/loans.json`, written whole in a single step. The format only gains fields; it never renames or removes them.

## Consequences

A laptop that has not upgraded can still read the file. Two laptops writing at the same moment can still lose one write; we accept that until the club grows.
