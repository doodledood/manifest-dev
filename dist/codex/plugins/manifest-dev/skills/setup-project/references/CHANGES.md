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

Digest: 5938102ffb1bb3fdb4d97adf659fbd34d40a5b18791c552f38d20716f47ff00b
