# Surfaces versions

What each surfaces version gives a project that setup-project has set up. A project's context
file records the version it carries in its project-surfaces section; an update offers what
changed after that version, as the upgrade guide for it in `upgrades/` says, and records the
newest version once the user has answered.

## v1

- Decision records gain an `Enforced by` field naming the strongest check that holds the
  decision, or `not yet` with the check a later run builds. It is editable in place, and superseding or narrowing a record retargets or
  retires the old record's check.
- The project-surfaces section records its surfaces version and gains an entry for the
  project's verification surface, telling every contributor that a change to what an entry
  covers updates and exercises that entry.
- A verification surface is seeded for each artifact future runs will change: its form and
  location, existing verification assets adopted within the scope the project gave them,
  entries catalogued from source as `unverified` (`unmeasured` for an eval suite), its README,
  and a repository check that its entries still point at things that exist.

Digest: da90c4ccd748aa536d84461ee3530690097de3080a519644f9e1437fb5d880da

## v2

- A setup-project run audits the whole setup against what the references describe, whatever
  version the project records, and offers each gap on its own, naming the need it serves now;
  what the project has no current need for is not offered, and what changed since the recorded
  version is marked new. For an existing verification surface it offers only missing parts —
  statuses, README, repository check, the feature-map shape — never harness or drive work, which
  grows with the work that needs it.
- A verification surface is judged fit to trust by its jobs — a cold proof run of one entry,
  a health check, isolation, the real path exercised — not by its tooling, only for the paths a
  run's work touches; and setup drives one entry end to end where existing assets reach, or says
  which entry it could not drive.
- The feature map takes a fixed shape: an index carrying baseline preconditions, driving
  conventions and proof and skip rules, and one file per feature with a `Status:` line and the
  sections `Sub-features`, `How to get to it (user POV)`, `Driving it`, `How it is checked` and
  `Gotchas`, with a worked example. It covers whatever users invoke — a plugin's skills included
  — not only a runnable app; a `verified` line names any entry point the drive did not use, and
  an `unreachable` status names the missing prerequisite;
  the surface README template gains that status, and the project-surfaces section gains a
  feature-map entry where the map is not already the verification surface.
- The ADR conventions state that only an `Accepted` record is in effect, and that backfilling
  `Enforced by`, building a `not yet` check, and citing a record as a ruling read only records
  in effect.

Digest: 5eb79c2e86bc14e2238e3982f48453e0c33db05d376b0a7e4abb0a730efcb794

## v3

- The project-surfaces section's feature-map entry says the map's README holds the commands and
  what a drive needs, and that a change to a feature updates that feature's entry and drives it,
  so a session knows how to use and keep the map from the context file alone.

Digest: 80bc7de905bfb2a9d5eebb592ab7335742eac591ad98a58b73bc4b1a5e307178

## v4

- One verification harness replaces the verification surface, the feature map and the
  reader-task list: a command-line tool (`scripts/verify` by default, copied from a shipped
  implementation in TypeScript that Node 22.18 or newer runs directly, ported on request) whose
  `--help` tells anyone how to verify the project, reading one Markdown recipe per feature,
  skill, document walk or eval suite. Recipes delegate to the project's
  existing test and drive commands; statuses are worked out from committed evidence, not kept by
  hand, and go stale when a covered file no longer matches the fingerprint its evidence recorded;
  `verify check` is the repository check.
- Recipes whose runs cost something a person should weigh — money or quota, long run time,
  shared environments, effects outside the repository — carry an `ask-first` mark with the
  reason. By default the tool runs them only with `--yes`, given when a person ran them or
  agreed; the user picks that default at setup and can change it in the harness settings.
- The project-surfaces section carries one verification bullet, written for any reader with or
  without this workflow: the command, when to run it, and how ask-first recipes run here. It
  replaces the verification-surface and feature-map bullets.
- An update moves an existing verification surface, feature map and reader-task list into
  recipes, keeping their content, customizations and evidence, following the upgrade guide for
  the version the project records.

Digest: 932d17190a24d0fb7e0b99b039d1821ac54a13769d05b56f2b32b2bff7f118e9

## v5

- The harness controls what it checks: `harness.md` can declare `start`, `running`, `logs`,
  `reset` and `stop` commands, which `verify` runs and `--help` lists only when declared; setup
  declares those the project's existing scripts already provide, and none where nothing runs.
  Every command a run starts receives `VERIFY_RUN_ID`, so instances, data and ports are per run
  and runs can go side by side; `--run ID` reaches an instance an earlier run started.
- A failed or unreachable run's evidence keeps what the `logs:` command printed for it.
- Evidence records each run's duration and kind of machine. A fixed-workload scenario gets a time
  line from its first passing run on that kind of machine plus headroom: two runs over it in a row
  show `over its line` and make `drive` exit 5; a faster run lowers it; `verify raise` (with a
  reason) and `verify freeze` (with a debt Ticket) move or hold it. Lines live in evidence, never
  in a file every run edits; `Workload: varies` scenarios — the affected tests, an agent session —
  get none.
- The evidence folder keeps one summary per scenario: a new run replaces the older one, and git
  keeps the history.
- `verify affected [BASE]` lists the recipes a diff touches and the changed paths no recipe
  covers.
- The stop grace is a `grace:` setting (2 s when unset), and kept output drops paths under the
  running user's actual home and temporary directories, wherever they are.
- The ask-first mark means cost only — money or quota, load on shared systems, effects outside
  the repository; run time alone is not a reason, and every other check is free to run as often
  as it helps. Agreement can come from the project's setting, the user, or an approved Manifest
  whose gate runs the recipe.
- *Fit to trust* gains three jobs: fast enough (no touched check over its line without a reason),
  controllable (started, observed and stopped through the harness, each run on its own), and a
  failure explains itself.
- The project-surfaces section's verification bullet says unmarked recipes are free to run as
  often as they help, and gives cost, never time, as the ask-first reason.
- The shipped example settings declare control commands on a per-run data directory and a free
  port, and its feature recipe shows a `Workload: varies` scenario.

Digest: 88671dc725dea89d9ef23818fd8461c9c3a0f28b535228f383c745acd47b6b07
