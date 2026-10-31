# The verification harness — what it is and how to create one

A verification harness is a project's one way to check that its work still does its job: a small
command-line tool, built once, kept current by the runs that touch it, and used by every later
run instead of each run working out again how to launch, drive and observe the result. An agent
or a person learns everything about verifying the project from one command, `verify --help`. A
harness that is wrong is worse than none, so it claims nothing a run has not just shown: it keeps
no status, and what a change runs comes from its diff.

What follows is a default shape, not a specification. It is what setup seeds when a project takes
a harness and what this workflow's skills expect of one that says nothing else, and it is worth
converging on where it fits. A project's harness should fit the project and the people who work on it, so adopt each part
where it fits, and adapt or replace it where it does not. Whatever its shape, every harness owes the
same few things: one place a newcomer learns how to verify the project, the ask-first mark
following cost, and the jobs in *Fit to trust*.

## When a project gets one

A harness is optional and recommended. Setup installs one by default when a project holds
something future runs will change; one-shot work — a single report, a throwaway script — is
checked in its own run and gets none. A project that already verifies its own way — its own
scripts, suites or checklists — may opt out, and every workflow skill still does its whole job
without a harness. The choice lives in one place: the verification bullet of the context file's
project-surfaces section, in its harness form or its own-way form (`NORTH_STAR_FORMAT.md` beside
this file → *The project-surfaces section*). Every run reads it there:

- **Harness form:** runs use the harness, build the parts the work needs that it lacks and keep it
  fit, as this file describes.
- **Own-way form:** runs verify through the means the bullet names, add any check a change needs in
  that same form, and never build, gate on or offer a harness; only a setup run offers the
  upgrade, adopting the project's checks.
- **No bullet yet:** a harness already on disk counts as chosen — runs treat it as the harness form
  and suggest recording its bullet. Otherwise runs verify through what the project already has, add
  only the check a change needs in the project's own form, build no harness, and recommend one in
  their report.

The line is build versus maintain, not harness versus none. No run builds a verification system the
project did not choose; every run keeps sound the checks the project has, in whatever form — a
test, a script, a checklist step, a recipe — where its work touches them, by the jobs in *Fit to
trust*.

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
  are what this workflow's skills call: `--help` (the whole picture, including where the recipes,
  settings and evidence live), `list` (every recipe, its kind and ask-first mark), `help <recipe>`,
  `drive <recipe> [scenario]` (with `walk` and `eval` as the same for those kinds), `doctor`
  (prerequisites, free), `check` (every recipe parses and names only paths that exist),
  and `affected [BASE]` (the recipes a diff touches and the changed paths no recipe covers). A port
  that keeps these subcommands and what they print keeps every skill's instructions working
  unchanged; one that departs from them says so in its own `--help`.
- **Recipes.** Every check the project keeps is a recipe: one Markdown file per thing a user
  reaches or a reader relies on, and one for the checks the project runs across the whole tree —
  its lint, type checks, test suite, build or gate runner — in the recipes directory
  (`verification/recipes/` by default). Front matter: `kind` (a free label — feature, skill, walk,
  eval, suite, …), `covers` (the paths whose change the recipe checks), `ask-first`
  with a one-line reason when it applies, and `dry-run: honored` when its commands obey
  `VERIFY_DRY_RUN=1`. Body: a title and one paragraph on what the user sees it do; *How a user
  reaches it* — every entry point past the obvious one; *Scenarios* — each a `### name` heading
  with `Run:` (the exact command), `Proves:` (what a passing run shows), and `Check: read` when the
  exit code cannot decide; *Gotchas* — traps that waste or invalidate a run. A recipe carries
  what a reader cannot get elsewhere; one that restates a description the artifact already shows
  its users costs upkeep and guides nobody. Where in the code a feature lives is read from the
  code at run time.
- **Settings.** `harness.md` beside the recipes directory (`verification/harness.md` by
  default), never inside it: the `ask-first` setting, an optional `doctor:` command, the control
  commands, optional `grace:` (seconds between SIGTERM and SIGKILL when a run stops what it
  started), and notes `--help` prints — what every run
  starts from, what it needs (a running service, a credential), driving conventions. `harness/`
  beside this file carries an example settings file and four example recipes: a free
  browser-and-CLI feature, an ask-first agent skill, an ask-first document walk, and the free
  checks the project runs across the whole tree.
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
- **Evidence.** Each run writes `<evidence>/<recipe>/<stamp>.md`, in the evidence directory
  `verify --help` names (`verification/evidence/` by default): the scenario, command, exit code,
  outcome (`passed`, `failed`, or `unreachable` when a prerequisite was missing and the command
  exited 3; a passing run whose proof needs reading says so), run identity, kind of machine,
  duration, what it proves, and the output with local paths removed. It replaces that scenario's
  older summary. A failed or unreachable run also keeps what the declared `logs:` command printed
  for it, so the failure explains itself in the run that met it. Whatever a command started is
  stopped when it ends, SIGTERM first so it can clean up. An interrupted run keeps none; a command
  that crashes is failed. Evidence stays on the machine that ran: the tool has git ignore the
  evidence directory, so nothing a run writes is committed. Fuller evidence — transcripts, screenshots — stays where
  the scenario's command keeps it, and the summary says where.

A recipe has no status. What a change runs comes from its diff and each recipe's `covers`
(`verify affected`), and each run says what it found in the run itself. A run never reports an
entry point as working because a different one did: each summary names the scenario it came from.

## Run time

Every run reports how long it took, in its output and its evidence, and that is the only time
signal. Keep checks fast and treat a slow harness as friction to fix — a check that makes agents
wait is one they stop running. Never block, gate, fail, ticket or exit non-zero on run time, and
never make a check faster by having it check less.

## Ask first

Some checks cost something a person should weigh: money or quota (an agent session, a paid
API, cloud resources), load on shared environments or other teams, or effects outside the
repository (a deploy, a message sent). Mark such a recipe `ask-first` with its reason. Run time
alone is not a reason: every unmarked check is free, and agents run it as often as it helps,
judging from the durations its runs report. The mark follows what a run costs, not its kind:
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

The checks a project runs across the whole tree — lint, type checks, its test suite, a build — are
assets too, whatever else the project already has. They become one recipe of kind `suite` that
`covers` the whole tree: where a gate runner already runs them, its scenarios call that runner or
its subsets; otherwise each check is a scenario calling the project's own command. It is adopted
on every path that builds or audits a harness: a first install, an upgrade that moves an older
surface into recipes, and an audit of a harness that lacks it. Because it covers every path, it
is always among the recipes `verify affected` names and never marks a path as covered: a changed
path a user reaches is judged covered or not by the other recipes alone. A verification command
the context file names outside its verification bullet, run by no recipe, teaches a second way
in, which an audit offers to close. Calling a command directly while iterating stays fine; the
evidence a run reports a change on comes through the harness, so every check is run, timed and
reported one way.

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

A check can exist and still not be worth trusting. These jobs apply to whatever checks a project
keeps, in any form: a harness's recipes, a test suite, a script, a checklist. A run judges them
only for the checks its own work touches, repairs what fails there within its scope in the check's
own form, and reports the rest as debt; a harness grows with the work, never ahead of it. Judge a
check by the jobs it has to do there, never by how this file would have built it:

- **A cold proof run passes** — one scenario, run from nothing, leaves evidence that is still
  there after cleanup.
- **Health is checkable** — something tells a usable instance from one that merely answers.
- **Runs are isolated** — a run cannot drive a shared instance or another run's data.
- **PASS means the real path** — not mocks past a boundary the product does not isolate, not a
  test-only endpoint, not a skipped entry point counted as another's success.
- **Controllable** — what the work touches can be started in a known state, observed and stopped
  through the harness or the project's own scripts, each run on its own.
- **A failure explains itself** — failed evidence carries what locates the cause: the instance's
  logs or traces from that run, or where they are.
- **It was seen to fail** — the check failed on a scratch break of what it proves, a change that
  makes the checked behavior wrong, and the break was then dropped. A check never seen failing may
  pass on anything.

For a behavior case, the cold proof run is one case run against the prompt as shipped and
graded; for a document walk, one task walked by a fresh reader given only the document, whose
account is kept. A job with no counterpart for a recipe — an instance health check or control for a walk —
is not a gap, and a case left unmeasured on purpose is the suite's choice, not a failed proof run. Scripts
instead of one tool, another test runner, another layout: those are the project's choices, not
gaps, as long as one command still tells a newcomer how to verify.

## What setup creates, and what runs build

Where setup installs the harness (the user did not opt out), it seeds it in this default shape, fitted to what the project already has: it copies and adapts the tool in the language *The parts* sets, asks the
ask-first choice (default `ask`) and writes it to `harness.md`, declares the control commands
the project's existing scripts already provide (and none where nothing runs), adopts existing
assets as recipes that delegate to them — the checks it runs across the whole tree among them
(*Build on what exists*) — catalogs recipes
from source (routes, commands, menus, invocable skills, the tasks readers bring to the documents)
so a vague report about any of them can be placed, adds the repository check, and wires the context-file bullet. It writes
scenarios only as far as existing assets already reach. Then, where one can run without asking,
it runs one scenario end to end and checks the evidence survives cleanup; where none can, its
report names the recipe it tried and what stopped it, and builds nothing more to get there. A
harness nobody has run reads as proof it is not, so it is never handed over unsaid. The run that
first needs to exercise a recipe builds the rest, inside the change that needs it.
