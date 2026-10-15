# ADR: The shipped verification harness is a default shape a project adapts

## Status
Accepted

## Area
define / do

## Decided by
The user

## Context
20261014-one-verification-harness-per-project made the tool's subcommands "the contract", and
20261015-the-verification-harness-controls-what-it-checks adds control commands to the harness.
Read as a contract, the harness text tells every project what it must contain, down to
`reset`, the run-identity variable, the evidence layout and the settings keys. Projects differ in
their stacks, their teams and the checks they already trust. A harness built to a specification
that does not fit them gets worked around or abandoned, and the work it was meant to protect goes
unchecked.

## Decision
The harness setup-project ships, with its tool, subcommands, control commands, settings, evidence
layout, recipe fields and directory layout, is a recommended default. It is the shape to converge
on where it fits. Each project adopts a part where it fits, and adapts or replaces it where its own
way serves its stack and its people better.

What every harness owes, whatever its shape:

- one place a newcomer learns how to verify the project;
- statuses that come from evidence, never kept by hand;
- an ask-first mark that follows cost (20261015-ask-first-marks-cost-not-slowness);
- the jobs in *Fit to trust* (20261015-runs-keep-the-harness-fit-for-speed-control-and-diagnosis).

A harness is judged by those, never by how closely it matches the shipped one. A port that keeps
the default subcommands and what they print keeps this workflow's skills working unchanged, so a
port that departs from them says so in its own `--help`. setup-project and the upgrade guides offer
each part as a default the project may adapt or decline where its own way already does the job.

## Alternatives Considered
- **Keep the subcommands and control commands as a contract every project keeps**: rejected. A
  contract that does not fit a project's stack gets worked around, and the harness then proves
  less than one shaped to fit.
- **Ship no default shape, only the jobs**: rejected. Every project would rebuild the tool, and the
  workflow's skills would have nothing common to call.

## Consequences

### Positive
- A project gets a harness that fits it, judged by what it does rather than by its parts.
- The jobs stay the single hook every workflow skill routes through.

### Negative
- A project that departs from the default subcommands must say so in its `--help`, and a skill
  following its default instructions there has to read that first.

## Enforced by
none — whether a project's harness fits it is judged by the *Fit to trust* jobs at the point a run
touches it; no check can tell a fitting departure from a careless one.

## Source
- Session: the owner's steering during the surfaces v5 change, 2026-10-15
- Related: Amends 20261014-one-verification-harness-per-project; see also
  20261015-the-verification-harness-controls-what-it-checks
