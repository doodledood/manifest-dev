# The verification harness — what it is and how to create one

A verification harness is a project's one way to check that its work still does its job: a small
command-line tool, built once, kept current by the runs that touch it, and used by every later
run instead of each run working out again how to launch, drive and observe the result. An agent
or a person learns everything about verifying the project from one command, `verify --help`. A
harness that is wrong is worse than none, so every status it shows comes from evidence.

What follows is a default shape, not a specification. It is what setup seeds when a project takes
a harness and what this workflow's skills expect of one that says nothing else, and it is worth
converging on where it fits. A project's harness should fit the project and the people who work on it, so adopt each part
where it fits, and adapt or replace it where it does not. Whatever its shape, every harness owes the
same few things: one place a newcomer learns how to verify the project, statuses that come from
evidence rather than anyone's say-so, the ask-first mark following cost, and the jobs in *Fit to
trust*. It is judged by those, never by how closely it matches this file.

## When a project gets one

A harness is offered, never imposed. Offer one when a project holds something future runs will
change; one-shot work — a single report, a throwaway script — is checked in its own run and gets
none. A project that already verifies its own way — its own scripts, suites or checklists — may
decline it. The choice lives in one place: the verification bullet of the context file's
project-surfaces section, in its harness form or its own-way form (`NORTH_STAR_FORMAT.md` beside
this file → *The project-surfaces section*). Every run reads it there:

- **Harness form:** runs use the harness, build the parts the work needs that it lacks and keep it
  fit, as this file describes.
- **Own-way form:** runs verify through the means the bullet names, add any check a change needs in
  that same form, and never build, repair, gate on or offer a harness.
- **No bullet yet:** runs verify through what the project already has, add only the check a change
  needs in the project's own form, build no harness, and offer one in their report.

A project that keeps a harness keeps one, whatever it holds: a product's features, a plugin's
skills, prompts with behavior cases, and living documents are all recipes in the same harness.

## The parts

- **The command-line tool.** `harness/verify` and `harness/verify.mts` beside this file are a
  working implementation to copy into the project (`scripts/` by default) and adapt. The default
  is TypeScript with no dependencies, which Node 22.18 or newer (23.6 or newer on Node 23) runs
  directly; `verify` is a
  shell entry that starts it, and stops with exit 3 naming that Node when it is missing or older.
  Seed this default without asking and say so in the offer. The user may override it, at setup
  or later: a project that wants another language, or whose environments cannot run Node, ports
  the tool and keeps the `verify` entry, so nothing that calls it changes. A machine that merely
  lacks Node is not a reason to port: the entry's exit-3 message goes in the report. Its subcommands
  are what this workflow's skills call: `--help` (the whole picture), `list` (every recipe, its kind,
  status and ask-first mark), `help <recipe>`, `drive <recipe> [scenario]` (with `walk` and
  `eval` as the same for those kinds), `judge` (record the verdict on evidence that needed
  reading), `doctor` (prerequisites, free), `check` (every recipe parses and names only paths
  that exist), `affected [BASE]` (the recipes a diff touches and the changed paths no recipe
  covers), and `raise` and `freeze` (move or hold a time line, below). A port that keeps these
  subcommands and what they print keeps every skill's instructions working unchanged; one that
  departs from them says so in its own `--help`.
- **Recipes.** One Markdown file per thing a user reaches or a reader relies on, in the recipes
  directory (`verification/recipes/` by default). Front matter: `kind` (a free label — feature,
  skill, walk, eval, …), `covers` (the paths whose change makes its evidence stale), `ask-first`
  with a one-line reason when it applies, and `dry-run: honored` when its commands obey
  `VERIFY_DRY_RUN=1`. Body: a title and one paragraph on what the user sees it do; *How a user
  reaches it* — every entry point past the obvious one; *Scenarios* — each a `### name` heading
  with `Run:` (the exact command), `Proves:` (what a passing run shows), `Check: read` when the
  exit code cannot decide, and `Workload: varies` when its work changes from run to run; *Gotchas* — traps that waste or invalidate a run. A recipe carries
  what a reader cannot get elsewhere; one that restates a description the artifact already shows
  its users costs upkeep and guides nobody. Where in the code a feature lives is read from the
  code at run time.
- **Settings.** `harness.md` beside the recipes directory (`verification/harness.md` by
  default), never inside it: the `ask-first` setting, an optional `doctor:` command, the control
  commands, optional `grace:` (seconds between SIGTERM and SIGKILL when a run stops what it
  started), `headroom:` (25% by default, at least 1 s) and `raise:` (`run` lets an agent raise a
  line with its reason, `ask` needs a person) for time lines, and notes `--help` prints — what every run
  starts from, what it needs (a running service, a credential), driving conventions. `harness/`
  beside this file carries an example settings file and three example recipes: a free
  browser-and-CLI feature, an ask-first agent skill, and an ask-first document walk.
- **Control.** `verify start` (an isolated instance in a known state), `running`, `logs`, `reset`
  and `stop` each run a command the project declares under that key in `harness.md`, as `doctor:`
  does. They are offered where they fit, never required: a project declares only the ones that
  apply, and `--help` lists only those; a project with nothing to run, such as documents only,
  declares none. The tool stays a thin runner over
  the project's own commands.
- **Run identity.** Every command the tool starts — scenarios, control, doctor, dry runs —
  receives `VERIFY_RUN_ID`, one per invocation, so data directories, ports and containers can be
  per run and runs can go side by side. A later drive or control command reaches an instance an
  earlier one started with `--run ID`; `logs`, `reset` and `stop` refuse to run without one.
- **Evidence.** Each run writes `evidence/<recipe>/<stamp>.md`: the scenario, command, exit
  code, outcome, run identity, kind of machine, duration, time lines, a fingerprint of the files
  the recipe covers, what it proves, and the output with local paths removed. It replaces that
  scenario's older summary, so the tree holds one per scenario and git keeps the history. A
  failed or unreachable run also keeps what the declared `logs:` command printed for it, so the
  failure explains itself. Whatever a command started is stopped when it ends, SIGTERM first so
  it can clean up. An interrupted run keeps none; a command that crashes is recorded failed. It
  is committed with the change it checked. Fuller evidence — transcripts, screenshots — stays
  where the scenario's command keeps it, and the summary says where.

## Statuses come from evidence

Nothing about a status is kept by hand. The tool works it out from the latest evidence of each
of a recipe's scenarios and shows the worst: `unverified` (none yet — proves nothing),
`verified` (every scenario's latest run passed; a scenario that never ran leaves the recipe
`unverified`, naming it), `failed`, `unreachable` (a prerequisite was
missing; the command exits 3), `unjudged` (the run finished and its proof needs reading,
until `verify judge` records the verdict), or `over its line` (every scenario passed, but one
crossed its time line), each with its date; and `stale` when a file the
recipe covers no longer matches the fingerprint that evidence recorded, or when someone found it drifting and added a
`Drift (YYYY-MM-DD): <what differs>` line to the recipe, which the run that repairs it removes. A run never reports an entry point as verified because a
different one worked: the evidence names the scenario it came from.

## Time lines

A scenario with a fixed workload gets a time line: its first verified run on a kind of machine
(a run whose proof needs reading counts once judged verified), plus headroom for noise. It is an alarm against a check slowly getting slower, and it only
reports — it never decides when a check runs or who may run it. One run over is noise; two in a
row show `over its line` and make `drive` exit non-zero. A run faster by more than the headroom
lowers the line, so the gain is kept. It moves up only by `verify raise` with a reason, or is held at the overshoot by
`verify freeze` naming the debt Ticket that pays it down. A scenario whose work varies — the affected
tests, or an agent session whose work the model decides each run — declares `Workload: varies`
and gets none. Lines are derived
from each scenario's latest evidence, never kept in a file every run edits; when merged branches
leave two summaries, the next run keeps the line allowing the most, so a raise or freeze survives.

## Ask first

Some checks cost something a person should weigh: money or quota (an agent session, a paid
API, cloud resources), load on shared environments or other teams, or effects outside the
repository (a deploy, a message sent). Mark such a recipe `ask-first` with its reason. Run time
alone is not a reason: every unmarked check is free, and agents run it as often as it helps,
judging from the durations its evidence shows. The mark follows what a run costs, not its kind:
driving a web app in a local browser, running a CLI, or calling a local API is unmarked and runs
freely, as do tests, dry runs and static checks.

An ask-first recipe runs with a person's agreement, which the project's setting, the user in the
session, or a Manifest a person approved whose gate runs that recipe can carry. A Manifest written
and executed in one unattended chain carries none. By default
(`ask-first: ask`) the tool refuses one unless the run passes `--yes`, which an agent passes only
on that agreement. The default is the
user's to change: setup offers the choice, records it in `harness.md`, `--help` prints it, and
the user can edit it there at any time (`run` lets ask-first recipes run freely). A project that
never wants some runs started by an agent says so in its own rules; the mark asks, it does not
forbid.

Too many marks defeat the harness: agents would ask before every check and stop verifying on
their own. Where a costly recipe has a cheap scoped variant — the affected tests, one feature's
flow — offer the variant beside it, so most changes are checked without asking.

## Build on what exists

Before writing anything, look for verification assets the project already has: end-to-end
specs, test commands, scripts that drive the product, an eval suite, a verification skill,
documented manual checks. The harness adopts them by delegation: a recipe's `Run:` line calls
the existing command (`npm run e2e -- --grep checkout`, a Makefile target, an eval runner), so
there is still one way to verify each thing. A second runner beside an existing one gives the
next run two ways to check the same thing, and it will pick either.

An adopted asset keeps the scope the project gave it. Setup adds no recipes for what that scope
leaves out: an eval suite that covers two skills on purpose is not a gap for every other skill.
Measurement suites — behavior evals with baselines and noise floors — stay what they are; a
recipe of kind `eval` names and starts their cases and does not redefine what a case's status
means.

## What makes the tool good to use

A small interface over a lot of capability; subcommands that reveal functionality a level at a
time; `--dry-run` on anything costly or destructive; rich `--help`; errors that say what to do
instead. Scenario commands start what the project needs from an empty state to a usable one
(data, configuration, test users), drive through stable handles (routes, commands, accessible
names) rather than coordinates, expose what the stack can show (logs, traces, console output),
and clean up only what they started, never the evidence. Control commands take their data
directory, port and container names from `VERIFY_RUN_ID` rather than a fixed value, so two runs
never meet; one given an id it has no instance for exits non-zero and says so, and the `logs:`
command prints what locates a failure for that run.

## A repository check

`verify check` fails when a recipe no longer parses or names a path that does not exist. It runs
with the project's tests where there are some — a test that calls it is enough — or on its own
through `verify doctor`, so structural drift fails even for contributors who never read a recipe.
It needs no CI.

## Fit to trust

A harness can have every part and still not be worth trusting. A run judges it only for the
recipes its own work touches, and builds only what that work needs; the harness grows with the
work, never ahead of it. Judge it by the jobs it has to do there, never by how this file would
have built it:

- **A cold proof run passes** — one scenario, run from nothing, leaves evidence that is still
  there after cleanup.
- **Health is checkable** — something tells a usable instance from one that merely answers.
- **Runs are isolated** — a run cannot drive a shared instance or another run's data.
- **PASS means the real path** — not mocks past a boundary the product does not isolate, not a
  test-only endpoint, not a skipped entry point counted as another's success.
- **Fast enough** — no check the work touches sits over its time line without a raise or a
  freeze that says why.
- **Controllable** — what the work touches can be started in a known state, observed and stopped
  through the harness, each run on its own.
- **A failure explains itself** — failed evidence carries what locates the cause: the instance's
  logs or traces from that run, or where they are.

For a behavior case, the cold proof run is one case run against the prompt as shipped and
graded; for a document walk, one task walked by a fresh reader given only the document, whose
account is kept. A job with no counterpart for a recipe — an instance health check or control for a walk —
is not a gap, and a case left unmeasured on purpose is a status, not a failed proof run. Scripts
instead of one tool, another test runner, another layout: those are the project's choices, not
gaps, as long as one command still tells a newcomer how to verify.

## What setup creates, and what runs build

Where the user accepts the harness, setup seeds it in this default shape, fitted to what the project already has: it copies and adapts the tool in the language *The parts* sets, asks the
ask-first choice (default `ask`) and writes it to `harness.md`, declares the control commands
the project's existing scripts already provide (and none where nothing runs), adopts existing
assets as recipes that delegate to them, catalogs recipes
from source (routes, commands, menus, invocable skills, the tasks readers bring to the documents)
so a vague report about any of them can be placed, adds the repository check, and wires the context-file bullet. It writes
scenarios only as far as existing assets already reach. Then, where one can run without asking,
it runs one scenario end to end and checks the evidence survives cleanup; where none can, its
report names the recipe it tried and what stopped it, and builds nothing more to get there. A
harness nobody has run reads as proof it is not, so it is never handed over unsaid. The run that
first needs to exercise a recipe builds the rest, inside the change that needs it.
