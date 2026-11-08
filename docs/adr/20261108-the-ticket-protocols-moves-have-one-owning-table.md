# ADR: The Ticket protocol's moves have one owning table, kept single by a test

## Status
Accepted

## Area
Ticketing

## Decided by
The user decided that one section owns every Ticket and effort transition, that the other files
point to it, that a test keeps it single and that the model covers pauses, grants and the hand-run
handoff. An agent in a hand run chose the table's layout, the pointer form, how the test detects a
restatement and how the model is extended, under that delegation, with no review.

## Context
The Ticket skills run one state machine: a claim and its release, the attempt record and its
launch count, a ready mark and its adoption, the escalation mark, an Auto grant counted by who set
it, an effort paused by a person or by an orchestrator for each cause, and a person's pick followed
by a hand run. Its rules were stated in prose across `orchestrate`, `run-ticket`, `next-ticket`,
the ticket convention, the automation reference and both venue references, and no section owned
them. One review of that prose found 29 defects, most of them one rule changed in one file while
another still stated the old one. Who a grant counts by was stated three ways;
20261107-a-grant-counts-only-by-who-set-it fixed that one rule by giving it one owner and a test
that fails on a restatement. The same failure was open for every other move.

The subject sits inside the North Star's Purpose: unattended work a person can delegate and trust.

## Decision
- `AUTOMATED_EXECUTION.md` → *Transitions* states every state a Ticket and its effort pass through,
  every move between them, and who may make each move, as a table with one row per move: the
  state it starts from, who may make it, and the state it leaves. Its *Who acts* list defines each
  actor a row names.
- Every other shipped file that relies on a move names its row —
  `` `AUTOMATED_EXECUTION.md` → *Transitions*, row *Launch* `` — instead of stating its condition.
  How to carry a move out stays with its procedure: *The attempt record*, *Landing* and *Waiting
  and acceptance*, and `orchestrate`'s sort and check-in. A venue reference says only how its store
  keeps each fact.
- The test reads a restatement as any run of eight words from a row's cells found in another
  shipped file, plus a list of wordings that once stated a move a second way. Shorter runs are the
  protocol's shared vocabulary, which every file needs to name a state.
- The TLA+ model of the protocol covers grant provenance, a person's pick and the hand run started
  under it, and an effort paused by a person or by an orchestrator for each cause, with the repair
  Ticket's exception. Its old behaviors are a named set, so each prefix configuration restores one,
  and another cannot hide its violation.

## Alternatives Considered
- **Keep each rule where it is used, with cross-checking tests per rule**: the one-owner test for
  the grant rule showed the pattern works for one rule; a test per rule grows with every rule, and
  a rule nobody wrote a test for still drifts.
- **One row per state and event pair**: most pairs are empty or say "nothing happens", which buries
  the moves a reader needs. A row per move names its start state, so every pair a move covers is
  still found in one place.
- **Detect restatements by a curated phrase list only**: catches only wordings someone already saw
  drift. Word runs catch any copied clause, and the list stays for paraphrases.
- **Put the table in its own file**: the moves rest on *The automation identity* and *The attempt
  record*, which every Ticket skill already loads with this file; another file would be one more
  load for the same readers.

## Consequences

### Positive
- A change to who may make a move, or when, is one edit to one row; a stale copy elsewhere fails
  the suite before it ships.
- A reader finds every state, move and actor in one place.
- The model can now fail on the bug classes the review found in grants, pauses and the hand-run
  handoff.

### Negative
- A paraphrase that shares fewer than eight words with its row passes the test; only review catches
  it, unless its wording joins the list.
- Each Ticket skill reads the table's whole section, longer than the few rules any one of them
  needs.

## Enforced by
partly — `tests/test_ticket_automation_prompts.py`: `test_no_other_file_restates_a_move` fails, on
the source and the Codex copy, when another shipped file shares eight words with a row or carries a
listed old wording; `test_every_row_a_file_names_exists` fails when a pointer names a row the table
lacks; `test_each_protocol_file_points_to_the_moves_it_relies_on` fails when a protocol file names
no row; `test_every_move_names_its_states_and_who_may_make_it` fails when a row lacks a cell or names
no defined actor. `verification/recipes/ticket-protocol-model.md` → `grant`, `pause`, `handoff` and
`prefix` model-check the new areas. A paraphrase sharing fewer than eight words stays judgment.

## Source
- Session: Ticket doodledood/manifest-dev#431
- Related: See also 20261107-a-grant-counts-only-by-who-set-it,
  20261019-a-model-checks-the-ticket-protocol-against-the-prose-it-quotes
