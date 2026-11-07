# ADR: A grant counts only by who set it

## Status
Accepted

## Area
Ticketing

## Decided by
An agent in an unattended run, with no review — under the owner's delegation to fix the
findings of an audit of the skills' state machines

## Context
Auto is a person's decision, or `orchestrate --autonomous`'s under its criterion
(20260810-auto-is-an-opt-in-grant-to-unattended-automation,
20261018-orchestrate-tickets-up-debt-and-grants-auto-where-the-criterion-holds). Two rules about
who counts did not match that.

- 20261019-the-comment-the-venue-created-first-decides-each-ticket-fact counts a record only when
  the automation identity created the comment and made its last edit. A grant-decision comment is
  one such record. A person who grants through `ticket-up` writes it as themselves, and a person
  answering a withhold that names them as asked edits it as themselves. Under that rule both were
  untrusted, so an autonomous orchestrator saw no decision on the Ticket and could record a
  withhold beside the person's standing grant.
- On GitHub the `auto` label was the grant, whoever applied it. Applying a label needs only the
  triage role, which cannot write to the repository. So a person who could not grant through any
  other path granted unattended landing by adding the label, while a Ticket that person wrote was
  never worked unattended at all.

## Decision
- A grant counts only when one of its grantors set it: a person with authority to grant — where
  the venue has permissions, write access to the repository — or `orchestrate --autonomous`
  writing as the automation identity. A grant anyone else sets grants nothing, and the Ticket
  reads as ungranted.
- The rule is stated once, in `AUTOMATED_EXECUTION.md` → *The automation identity*, beside the
  record-trust rule it is the one exception to. The convention, the venue references,
  `orchestrate` and `run-ticket` point to it rather than restating it, and each venue reference
  says only how its store reads who set a grant.
- A grant-decision comment counts when the account that created it and the one that last edited
  it are each the automation identity or a person with write access. This is the one record kind
  the automation-only rule does not govern; the first-created rule still says which of two
  decides.
- The venue's grant state counts when a person with authority to grant set it, or when the
  automation identity set it while the deciding grant decision records a grant —
  `orchestrate --autonomous`'s own, or a person's that `ticket-up` wrote for them. A grant state
  the automation identity set with no grant decided, such as a run's stray write, grants nothing.
  On GitHub who set the `auto` label is read from the issue's label events.
- In a file store an `Auto: yes` line counts once it is on the target branch, which takes changes
  only through someone with write access. A line `ticket-up` wrote in this working copy during the
  session, for the grantor it names, counts there too, as a Ticket that session authored passes
  the author check there: `orchestrate --autonomous`'s grants to its debt Tickets and a person's
  grant given in its conversation are written there and never land on their own. A line arriving
  from another branch or an unmerged contribution grants nothing.

## Alternatives Considered
- **Keep the label as the grant whoever applied it**: lets a triage collaborator or another app
  grant unattended landing, which is authority the repository does not give them.
- **State the rule in the convention and each venue reference**: the three copies drifted into
  three conditions. The convention left out a person's grant that the automation identity
  relays, the automation reference counted the automation identity's label unconditionally, and
  only the GitHub store asked for a grant decision behind it, so a tracker built from the generic
  rule would count a stray label.
- **Count only the grant-decision comment, not the label**: a person who removes the label to
  withdraw a grant would then also have to edit a comment, and a label added by hand with no
  comment would stop counting.

## Consequences

### Positive
- Only someone the repository trusts to write, or the orchestrator acting for the owner, can
  send a Ticket to unattended landing.
- A person's grant and their answer to an ask read as decided to every orchestrator.

### Negative
- Each grant read on GitHub costs a read of the issue's events and, for a person, a permission
  check.
- A label a triage collaborator adds sits on the issue without effect, so a person who expected
  it to grant learns otherwise only from the Ticket not landing on its own.

## Enforced by
partly — `tests/test_ticket_automation_prompts.py` — `test_a_grant_counts_only_by_who_set_it`
fails, on the source and the Codex copy, if the convention stops pointing to the rule, the automation
reference stops applying it to the grant state, or the GitHub or file store stops saying how it
reads who set a grant; `test_a_persons_grant_decision_counts` fails if a grant-decision comment
goes back to counting only when the automation identity wrote it;
`test_the_grant_and_record_trust_rule_has_one_owner` fails if any Ticket skill or reference
outside *The automation identity* restates the grant or record-trust rule. Whether a person has authority
to grant on a venue without permissions stays judgment.

## Source
- Session: an audit of the skills' state machines and the fixes to its findings (2026-11-07).
- Related: amends 20261019-the-comment-the-venue-created-first-decides-each-ticket-fact and
  20260810-auto-is-an-opt-in-grant-to-unattended-automation; see also
  20261019-the-first-grant-decision-stands-and-a-persons-decline-removes-the-grant
