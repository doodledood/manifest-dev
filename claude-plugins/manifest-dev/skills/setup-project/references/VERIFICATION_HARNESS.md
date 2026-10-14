# The verification harness — what it is and how to create one

A verification harness is a project's one way to check that its work still does its job: a small
command-line tool, built once, kept current by the runs that touch it, and used by every later
run instead of each run working out again how to launch, drive and observe the result. An agent
or a person learns everything about verifying the project from one command, `verify --help`. A
harness that is wrong is worse than none, so every status it shows comes from evidence.

## When a project gets one

Give a project a harness when it holds something future runs will change. One-shot work — a
single report, a throwaway script — is checked in its own run and gets none. A project keeps one
harness, whatever it holds: a product's features, a plugin's skills, prompts with behavior
cases, and living documents are all recipes in the same harness.

## The parts

- **The command-line tool.** `harness/verify` and `harness/verify.mts` beside this file are a
  working implementation to copy into the project (`scripts/` by default) and adapt. The default
  is TypeScript with no dependencies, which Node 22.18 or newer (23.6 or newer on Node 23) runs
  directly; `verify` is a
  shell entry that starts it, and stops with exit 3 naming that Node when it is missing or older.
  Seed this default without asking and say so in the offer. The user may override it, at setup
  or later: a project that wants another language, or whose environments cannot run Node, ports
  the tool and keeps the `verify` entry, so nothing that calls it changes. A machine that merely
  lacks Node is not a reason to port: the entry's exit-3 message goes in the report. Its subcommands are the contract: `--help` (the whole picture), `list` (every recipe, its kind,
  status and ask-first mark), `help <recipe>`, `drive <recipe> [scenario]` (with `walk` and
  `eval` as the same for those kinds), `judge` (record the verdict on evidence that needed
  reading), `doctor` (prerequisites, free) and `check` (every recipe parses and names only paths
  that exist). A port keeps these subcommands and what they print.
- **Recipes.** One Markdown file per thing a user reaches or a reader relies on, in the recipes
  directory (`verification/recipes/` by default). Front matter: `kind` (a free label — feature,
  skill, walk, eval, …), `covers` (the paths whose change makes its evidence stale), `ask-first`
  with a one-line reason when it applies, and `dry-run: honored` when its commands obey
  `VERIFY_DRY_RUN=1`. Body: a title and one paragraph on what the user sees it do; *How a user
  reaches it* — every entry point past the obvious one; *Scenarios* — each a `### name` heading
  with `Run:` (the exact command), `Proves:` (what a passing run shows) and `Check: read` when the
  exit code cannot decide; *Gotchas* — traps that waste or invalidate a run. A recipe carries
  what a reader cannot get elsewhere; one that restates a description the artifact already shows
  its users costs upkeep and guides nobody. Where in the code a feature lives is read from the
  code at run time.
- **Settings.** `harness.md` beside the recipes directory (`verification/harness.md` by
  default), never inside it: the `ask-first` setting, an optional
  `doctor:` command, and notes `--help` prints — what every run starts from, what it needs (a
  running service, a credential), driving conventions. `harness/` beside this file carries an
  example settings file and three example recipes: a free browser-and-CLI feature, an ask-first
  agent skill, and an ask-first document walk.
- **Evidence.** Each run writes `evidence/<recipe>/<stamp>.md`: the scenario, command, exit
  code, outcome, a fingerprint of the files the recipe covers, what it proves, and the output
  with local paths removed. An interrupted run keeps none and stops what its command started; a command
  that crashes is recorded failed. It is committed with
  the change it checked. Fuller evidence — transcripts, screenshots — stays where the scenario's
  command keeps it, and the summary says where.

## Statuses come from evidence

Nothing about a status is kept by hand. The tool works it out from the latest evidence of each
of a recipe's scenarios and shows the worst: `unverified` (none yet — proves nothing),
`verified` (every scenario's latest run passed; a scenario that never ran leaves the recipe
`unverified`, naming it), `failed`, `unreachable` (a prerequisite was
missing; the command exits 3), or `unjudged` (the run finished and its proof needs reading,
until `verify judge` records the verdict), each with its date; and `stale` when a file the
recipe covers no longer matches the fingerprint that evidence recorded, or when someone found it drifting and added a
`Drift (YYYY-MM-DD): <what differs>` line to the recipe, which the run that repairs it removes. A run never reports an entry point as verified because a
different one worked: the evidence names the scenario it came from.

## Ask first

Some checks cost something a person should weigh: money or quota (an agent session, a paid
API, cloud resources), run time well beyond the project's usual test run (a company-wide
end-to-end suite), load on shared environments or other teams, or effects outside the repository
(a deploy, a message sent). Mark such a recipe `ask-first` with its reason. The mark follows what
a run costs, not its kind: driving a web app in a local browser, running a CLI, or calling a
local API is unmarked and runs freely, as do tests, dry runs and static checks.

By default (`ask-first: ask`) the tool refuses an ask-first recipe unless the run passes
`--yes`, which an agent passes only when a person ran it or agreed to it. The default is the
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
and clean up only what they started, never the evidence.

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

For a behavior case, the cold proof run is one case run against the prompt as shipped and
graded; for a document walk, one task walked by a fresh reader given only the document, whose
account is kept. A job with no counterpart for a recipe — an instance health check for a walk —
is not a gap, and a case left unmeasured on purpose is a status, not a failed proof run. Scripts
instead of one tool, another test runner, another layout: those are the project's choices, not
gaps, as long as one command still tells a newcomer how to verify.

## What setup creates, and what runs build

Setup seeds the harness: it copies and adapts the tool in the language *The parts* sets, asks the
ask-first choice (default `ask`) and writes it to `harness.md`, adopts existing assets as recipes that delegate to them, catalogs recipes
from source (routes, commands, menus, invocable skills, the tasks readers bring to the documents)
so a vague report about any of them can be placed, adds the repository check, and wires the context-file bullet. It writes
scenarios only as far as existing assets already reach. Then, where one can run without asking,
it runs one scenario end to end and checks the evidence survives cleanup; where none can, its
report names the recipe it tried and what stopped it, and builds nothing more to get there. A
harness nobody has run reads as proof it is not, so it is never handed over unsaid. The run that
first needs to exercise a recipe builds the rest, inside the change that needs it.
