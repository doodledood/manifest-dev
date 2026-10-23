# Resolve the work store

Read `tickets/store-config.md` first, or the location the project context file names. Reuse
the chosen venue and its reference. When neither exists, ask once and recommend the project's
shared tracker; GitHub Issues is the recommendation when the project has a reachable GitHub
remote and no other tracker is in play. Recommend files only where no shared tracker exists
or nobody else will pick work, and explain that claims do not cross clones, worktrees or
branches. Show the concrete configuration and its destination before recording a new choice.

- **Files:** use `FILE_STORE.md` for the mapping.
- **GitHub Issues:** use `GITHUB_STORE.md` for the mapping.
- **Another tracker:** use the required mapping rows in `GITHUB_STORE.md`, ask what supplies
  each capability, and record that venue reference at `tickets/<venue>-store.md`. An existing
  custom reference is reused. The config names the venue and reference.

Record shared choices at `tickets/store-config.md`, or the configured location. For unattended
coordination, resolve the stable automation identity and a distinguishable human escalation
recipient using the venue's mapping and `AUTOMATED_EXECUTION.md` → *The automation identity*.
Check whether this session can use that identity; record unavailable access as a prerequisite,
not an implied grant. Keep credentials and personal restrictions in existing private mechanisms.

Resolving configuration creates no Tickets, claims, sessions or operating assignment. A caller
that is authoring Tickets continues with the chosen venue mapping. Before first outward-facing
creation on a venue the project has not used, show the planned Tickets, labels, tracking item and
relations and get confirmation. A configured venue already records its choice; configuration
alone does not authorize a new assignment or its external actions.
