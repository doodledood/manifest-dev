# The verification surface — what it is and how to create one

A verification surface is a project's durable way to check that an artifact still does its job:
built once, kept current by the runs that touch it, and used by every later run instead of each
run working out again how to launch, drive and observe the result. A surface that is wrong is
worse than none, so every part of it says how much it can be trusted.

## When an artifact gets one, and which form

Give a surface to an artifact that future runs will change. One-shot work — a single report, a
throwaway script — is checked in its own run and gets none.

The form follows the artifact:

| Artifact | Form | What one entry covers |
|---|---|---|
| A runnable product — service, CLI, UI, app | A harness plus a feature map | One user-facing feature |
| Prompts, skills, agents | A behavior eval suite | One behavior the prompt owes |
| A living document — README, runbook, guide, or a site or page whose job is to inform | A list of reader tasks, each walked by a reader with fresh context | One task a reader comes to do |

A project with several such artifacts keeps one surface per artifact and lists each in the
project-surfaces section of the context file.

## Build on what exists

Before writing anything, look for verification assets the project already has: end-to-end
specs, test harnesses, scripts that drive the product, an eval suite, a verification skill,
documented manual checks. Adopt and extend them. A second harness beside an existing one gives
the next run two ways to verify the same thing, and it will pick either.

An adopted asset keeps the scope the project gave it. Setup adds the parts the surface lacks —
statuses, the README, the repository check — and never entries for what that scope leaves out:
an eval suite that covers two skills on purpose is not a gap for every other skill. Where the
asset already has a README, extend that README instead of writing a second one.

## A runnable product: the harness

The harness is a small command-line tool kept with the surface, so a run executes a command
instead of writing a throwaway script each time. It covers:

- **Launch** — start the product from an empty data directory to a state where it is usable,
  not merely answering: migrations, seed data, test users, configuration, and a consistent
  bring-up of whatever it depends on.
- **Doctor** — one read-only check that says whether an instance is worth driving: it is up,
  it runs the expected build, the ports and data belong to this run, auth works.
- **Drive** — the actions a user takes, through stable handles (routes, commands, accessible
  names, data attributes) rather than coordinates or tab order.
- **Debug** — whatever the stack can expose: logs, traces, profiles, console and network
  output. A stack that is hard to observe makes every later run guess.
- **Evidence** — capture the action and the resulting state, side effects included, as files
  that survive cleanup, at a location the harness names, so a person can open them.
- **Cleanup** — remove what this run started, never what it did not, and never the evidence.

Make it easy for an agent to use well: a small composable interface over a lot of capability;
subcommands that reveal functionality a level at a time; `--dry-run` on anything destructive;
rich `--help`; machine-readable output; and errors that say what to do instead. Give the
harness its own checks, so a broken harness fails loudly instead of failing every run that
uses it.

## A runnable product: the feature map

One entry per user-facing feature, each answering from the user's side:

- how to reach it — every entry point;
- how to drive it with the harness — the exact commands, from a stated precondition;
- what observable end state proves it works;
- gotchas that can waste or invalidate a run.

Every entry carries a status:

- `unverified` — catalogued but not yet driven; not proof of anything;
- `verified` — driven by a run, with the date;
- `stale` — a run found it drifting from the product, with a dated line naming what differs.

The first build catalogs the product from its source — routes, commands, menus, documented
features — and marks each entry `unverified`. That gives the map its breadth, so a vague report
about any feature can be placed. Runs then verify the entries they exercise.

## Prompts, skills, agents: the eval suite

One case per behavior the prompt owes, run against the prompt as shipped, judged on what it
did — files it opened and wrote, what it reported — never on its own account of what it did,
and with no eval wording in what the candidate sees. Each case carries a status:

- `unmeasured` — written but never run; not proof of anything;
- `measured` — run, with the date and the result;
- `stale` — a prompt it covers changed after it was measured, so its numbers no longer hold.

## A living document: the reader-task list

One entry per task a reader comes to the document to do, with what the reader needs to end up
able to do. A check walks each task with a fresh reader that has only the document, and records
where it got stuck. Each entry carries the same three statuses as a feature map.

## Every form

- **A repository check** fails when an entry points at something that no longer exists — a
  route, a command, a selector, a case, a section. It runs with the project's tests, or as a
  script the harness's doctor calls where the project has
  no test runner, with or without CI, so structural drift fails even for contributors who never
  use this
  workflow.
- **The surface's own README** says what the surface covers, how to run it, what each status
  means, and how a stale line reads. Emit it from `VERIFICATION_README_TEMPLATE.md` beside this
  file, adapted to the form.
- **Location** — keep the surface with the project, where any runner that checks out the
  repository finds it, and name the location in the project-surfaces section.

## What setup creates, and what runs build

Setup seeds the surface: it records the form and location, adopts existing assets, catalogs
entries from source in the form's first status (`unverified`, or `unmeasured` for an eval
suite), writes the README and the repository check, and wires the project-surfaces entry. It
builds harness commands only as far as existing assets already
reach. The run that first needs to exercise an entry builds the rest, inside the change that
needs it.
