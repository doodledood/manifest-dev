# Surfaces versions

What each surfaces version gives a project that setup-project has set up. A project's context
file records the version it carries in its project-surfaces section; an update offers the
entries after that version, each on its own, and records the newest version once the user has
answered them.

## v1

- Decision records gain an `Enforced by` field naming the strongest check that holds the
  decision. It is editable in place, and superseding or narrowing a record retargets or
  retires the old record's check.
- The project-surfaces section records its surfaces version and gains an entry for the
  project's verification surface.
- A verification surface is seeded for each artifact future runs will change: its form and
  location, existing verification assets adopted within the scope the project gave them,
  entries catalogued from source as `unverified` (`unmeasured` for an eval suite), its README,
  and a repository check that its entries still point at things that exist.

Digest: ee6a51649c1478a9810c1984a3108e7f67a90a61debbe9392d94f43630c08b01
