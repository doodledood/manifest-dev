# ADR: The verification harness controls what it checks, through commands the project declares

## Status
Accepted

## Area
define / do

## Decided by
The user

## Context
20261013-runs-build-and-maintain-a-project-verification-surface described a product's harness
as a tool that also sets up the development environment and exposes debugging, and the setup
reference named Launch, Doctor, Debug and Cleanup as its parts.
20261014-one-verification-harness-per-project reshaped the harness into a recipe runner whose
contract is `list`, `help`, `drive`, `judge`, `doctor` and `check`. Control survived only as
one sentence about what scenario commands should do. The shipped example calls a separate
`scripts/control-notes` that nothing tells a project to build. It relies on a `$RUN_ID` the tool
never sets, and it serves every run at one fixed port. So an agent that needs to start the app,
reproduce a report or see why a check failed finds nothing in `verify --help`. Two runs on one
machine would also collide.

The owner wants one place, for agents and people, to control and check the work: start it in a
known state, drive it, observe it, stop it. It should be debuggable enough that an agent learns
how to improve what it is changing, not only that a check failed. The owner also wants many
agents working at once, which needs runs that cannot touch each other.

## Decision
- Control is part of the harness contract. `verify` gains commands to start an isolated instance
  in a known state, say what is running, show its logs and traces, reset it, and stop what the
  run started. Each one delegates to a command the project declares in the harness settings, the
  way `doctor:` works today. A project declares only the commands that apply, and `--help` shows
  only those. A project with nothing to run, such as documents only, declares none.
- The tool gives every run its own identity and passes it to every command it starts. Data
  directories, ports and containers can then be per run, and runs can go side by side.
- A failure explains itself. Failed evidence keeps the instance's logs or traces from that run,
  or says where they are. Debugging comes from richer evidence that the agent reads, not from
  analysis inside the tool, which stays a thin runner over the project's own commands.

## Alternatives Considered
- **A separate project control tool beside `verify`**, as the shipped example has: two places to
  look, against one command for everything. Where a project already has a mature development
  tool, the declared commands call it, so nothing is duplicated.
- **Control only inside scenario commands**, as in v4: invisible to an agent that has to start
  or inspect the app outside a scripted scenario, which is how most bug reports begin.
- **A visual dashboard or a control server for one protocol**: a dashboard is a second surface
  to keep true, and a protocol server works only on hosts that load it. Agents are the main
  users, and a command-line tool reaches every host.
- **A tool that analyzes failures itself**: more machinery in the tool every project copies. The
  logs and traces in the evidence, read by the agent, do the same job.

## Consequences

### Positive
- One command for every QA action: start, drive, observe, check, stop.
- Runs can go side by side without colliding.
- A failed check carries what the agent needs to find its cause.

### Negative
- More subcommands and settings keys in the tool every project copies, and a new surfaces
  version to ship them.
- Projects whose launch fixes a port or a data path have to take the run identity instead.

## Enforced by
`tests/test_verify.py`: `test_a_declared_control_command_runs_through_verify`,
`test_an_undeclared_control_command_is_absent_from_help`,
`test_every_command_a_run_starts_receives_its_identity`, and
`test_failed_evidence_keeps_the_instances_logs`; end to end,
`test_a_real_instance_is_started_driven_diagnosed_and_stopped`.

## Source
- Session: figure-out investigation of the verification harness's control, speed and
  confidence, 2026-10-15.
- Related: amends 20261014-one-verification-harness-per-project; see also
  20261013-runs-build-and-maintain-a-project-verification-surface
