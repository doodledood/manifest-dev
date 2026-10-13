# Surfaces versions

What each surfaces version gives a project that setup-project has set up. A project's context
file records the version it carries in its project-surfaces section; an update offers the
entries after that version, each on its own, and records the newest version once the user has
answered them.

## v1

- Decision records gain an `Enforced by` field naming the strongest check that holds the
  decision, or `not yet` with the check a later run should build. It is editable in place, and superseding or narrowing a record retargets or
  retires the old record's check.
- The project-surfaces section records its surfaces version and gains an entry for the
  project's verification surface, telling every contributor that a change to what an entry
  covers updates and exercises that entry.
- A verification surface is seeded for each artifact future runs will change: its form and
  location, existing verification assets adopted within the scope the project gave them,
  entries catalogued from source as `unverified` (`unmeasured` for an eval suite), its README,
  and a repository check that its entries still point at things that exist.

Digest: b311b82148f4a8ed815d6b7ac3df77a8d7a48b140f6781f128269c8ab3f122bc
