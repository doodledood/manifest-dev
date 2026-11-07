# ADR: The tending identity can answer a review body

## Status
Accepted

## Area
PR lifecycle

## Decided by
An agent in an unattended run, with no review — under the owner's delegation to fix the
findings of an audit of the skills' state machines

## Context
`20261021-check-pr-review-feedback-is-one-inbox` counts a review body or top-level comment as
addressed when the PR author has later replied to it on the Conversation. That record assumed
the author-side work is done by the PR's author. It is not always: `babysit-pr` tends a pull
request under any identity with normal push permission, such as a maintainer tending a
contributor's branch. That identity's replies never counted, so `check-pr` failed the gate on
a body the tender had answered, and the run went on until it escalated a block that did not
exist. The record did not weigh this case, so the choice is open again. The decision sits
inside the North Star's Purpose: delegated work proceeds without needless intervention.

## Decision
A review body or top-level comment is addressed when someone other than its author — the PR
author, or the identity this inspection runs as, the one tending the pull request — has later
replied on the Conversation with a response clearly tied to that item, or when the review is
dismissed or superseded as before. An identity's reply never addresses an item it wrote, so a
reviewer's own follow-up cannot clear their `CHANGES_REQUESTED`. The rest of the inbox decision
stands.

## Alternatives Considered
- **Any collaborator with write access**: covers every tender — Rejected: a second reviewer's
  "+1" to a body would count as addressing it.
- **Any reply from the PR author or the inspecting identity**: simpler — Rejected: where the
  inspection runs as the reviewer who wrote a body, that reviewer's own follow-up would clear
  their own request for changes.
- **A tending identity passed in as an input**: explicit — Rejected: every caller, and every
  Manifest gate that activates `check-pr`, would have to carry it, and the inspection already
  knows which identity it runs as.

## Consequences

### Positive
- A tender who is not the PR's author can clear a body or comment by answering it.

### Negative
- A person running `check-pr` on a pull request they review, under their own account, has
  their own Conversation replies to other reviewers' bodies counted as addressing them.

## Enforced by
partly — `tests/test_check_pr_feedback_gate.py::test_the_tending_identity_can_address_a_body`
fails if gate 3 stops counting a reply from the identity the inspection runs as, or counts a
reply from the item's own author; whether a reply is tied to its item stays judgment.

## Source
- Amends 20261021-check-pr-review-feedback-is-one-inbox
