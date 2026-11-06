# ADR: Hill-climbing runs through figure-out, define and do, started by an optional thin /hillclimb command

## Status
Accepted

## Area
Task guidance

## Decided by
The user

## Context
Sometimes a requester wants an existing artifact improved as far as it will go for its purpose, not just made acceptable. The artifact might be a page, a prompt, a query's speed or a document. `/do` stops at good enough by design. It finishes once the Outcome and every current gate hold on fresh evidence. A reviewer's grade is not an acceptance end (`20261106-review-evidence-serves-substantive-acceptance`). The North Star's *Quality decides* principle calls a run that keeps repairing after its gates hold a defect. So "make it as good as it can get" has no home today unless the Manifest itself says what counts as better and when to stop.

The parts a climb needs already exist:
- `/do`'s loop pursues a Manifest's gates on evidence. Its execution log is keyed to the Manifest, so a relaunched run finds its record again.
- define encodes task-file Quality Gates and Defaults into a Manifest.
- figure-out's task files carry probes.
- `define/tasks/PERF.md` held the measurable form of the discipline: prove the harness, then freeze it; a noise floor; a fair comparison.
- The eval suite's hill-climbing guide (`claude-plugins/manifest-dev/evals/README.md`) climbs a prompt against a behavior suite, with held-out cases as guards.
- `babysit-pr` already starts define and then do from one thin command (`20260914-one-skill-per-beat-built-from-the-lean-body`).

This decision sits inside what the North Star's *Purpose* names: work moves toward an outcome without the person choosing every next step.

## Decision
- **No new machinery.** No new loop skill, engine, state store or built-in judge. `/do` runs a climb as its ordinary loop over a Manifest whose gates say what counts as better and when to stop. The climb's record lives where a run's record already lives: the Manifest and `/do`'s execution log, and the pull request description only where the work was pushed.
- **A mirror pair of task files carries the discipline.** `define/tasks/HILLCLIMB.md` holds Quality Gates and Defaults, and `figure-out/tasks/HILLCLIMB.md` holds probes. Each composes onto `MEASURE.md` and onto the artifact's own task file (`UI.md`, `PERF.md`, `PROMPTING.md`, `WRITING.md` and the rest), whose gates become floors every kept version holds. A judge-crafting reference, `define/tasks/references/AI_JUDGE.md`, loads only when a climb's measure is an AI judge. All of them load whenever a climb is asked for, through any entry.
- **What the task files carry are defaults.** define encodes them into the climb's Manifest. A requester's own measure, limits, rules or wish to take part come first. The requester states these in the request, in their own rules or in their project's context file.
- **A thin entry command.** `/hillclimb <target> [measure] [--autonomous]` in `manifest-dev-tools` runs figure-out, define and do, the way `babysit-pr` starts define and do, and owns nothing else. A climb is quick by default and thorough when asked or when the stakes call for it (`20261106-a-climb-is-quick-by-default-and-thorough-when-it-matters`). Without `--autonomous`, the requester takes part in defining a thorough climb; the rounds run without a person choosing (`20261106-a-climb-runs-without-a-person-choosing-by-default`). It pushes only when the requester wants it.
- **Narrows `20261007-design-exposes-optional-instruments-with-bounded-evidence` on one point.** A design may be improved in a loop when a person asks for a climb, against a measure designed for that task (`20261106-a-climb-designs-its-measure-and-search-for-its-task`). That record rejected a loop because a universal score treats unlike tasks as one and rewards shortcuts such as hiding content. Its reason does not cover a per-task measure that protects content on every kept version. The design skill still supplies no universal score, required suite, pass threshold or fixed loop of its own.

## Alternatives Considered
- **A standalone loop skill that generates, judges and keeps state.** Not chosen: it would duplicate `/do`'s loop, its evidence rules and its log. A second loop is a second place for those rules to drift.
- **No entry command; a climb only through `/auto` or `/define`.** Not chosen: the requester would then have to know how to ask for a climb. The task files still load through those entries, so the command is an optional way in, as `20261013-new-capabilities-live-inside-the-four-workflow-entry-points` allows for skills outside the four.
- **The discipline inside each domain task file.** Not chosen: the same measuring and stopping rules would be restated in `UI.md`, `PERF.md`, `PROMPTING.md` and `WRITING.md`, and the copies would drift apart.
- **A built-in judge and a study that measures it before it ships.** Not chosen: it would measure one model on one set of artifacts and age with each model generation (`20261106-an-ai-judge-decides-between-two-versions-and-each-climb-proves-its-own`).

## Consequences

### Positive
- A climb gets `/do`'s evidence rules, Ratchet, logging and recovery with no new code to maintain.
- Any artifact with a task file can be climbed. A new domain needs no climb-specific work.
- Runs that are not climbs carry nothing extra, because the task files load only when a climb is asked for.

### Negative
- Prose has to carry the bookkeeping of rounds and votes, and a long climb may miscount.
- A re-run on another machine finds the earlier record only where the work was pushed, because local logs stay on the machine that wrote them.
- `HILLCLIMB.md` is the first task file that composes onto any domain's file as well as its base. Both skills' task-file indexes state that composition.

## Enforced by
`tests/test_hillclimb.py` (`test_command_hands_the_climb_to_figure_out_define_and_do` and `test_each_climb_and_measure_file_has_its_mirror_and_composes_onto_measure`) fails when the command stops handing off to figure-out, define and do or gains a loop of its own, or when a climb or measure task file loses its mirror or its composition. Whether any other machinery is added stays judgment.

## Revisit when
Climbs miscount rounds or votes, or a re-run fails to find the earlier climb's record, often enough that prose cannot carry the bookkeeping; read in the climbs' reports and execution logs.

## Source
- Session: a figure-out session, 2026-11-06 (log kept locally).
- Narrows 20261007-design-exposes-optional-instruments-with-bounded-evidence
- Related: 20260914-one-skill-per-beat-built-from-the-lean-body, 20261106-a-climb-designs-its-measure-and-search-for-its-task, 20261106-an-ai-judge-decides-between-two-versions-and-each-climb-proves-its-own, 20261106-a-climb-stops-on-patience-and-a-rerun-continues-its-record, 20261106-a-climb-runs-without-a-person-choosing-by-default, 20261106-a-climb-is-quick-by-default-and-thorough-when-it-matters, 20261013-new-capabilities-live-inside-the-four-workflow-entry-points
