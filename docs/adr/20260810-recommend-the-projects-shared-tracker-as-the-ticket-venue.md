# ADR: Recommend the project's shared tracker as the ticket venue

## Status
Accepted

## Area
Ticketing

## Context

`ticket-up` recommends files: "Files are the answer to *recommend* absent a reason otherwise — never one taken in silence." That was right while the venue was a storage preference. Files need no auth, no network, and no account, and the store is a rendering of the same convention either way.

Claiming at pick time (20260810-next-ticket-claims-the-ticket-it-picks) turns the venue into a capability question. A file store is versioned repo content — `tickets/<effort-slug>/NN-<ticket-slug>.md` at the project root — so a claim is visible only to a worker sharing that working tree. Workers in separate clones, worktrees, or branches never see each other's claims: each commits to its own branch, and the claim reaches the others only after a merge. Recommending files by default hands the ordinary parallel setup a venue that cannot do what the workflow now promises.

The discriminator is not GitHub. It is whether the store is a live surface every worker reads: GitHub Issues, Jira, Linear, or any hosted tracker qualifies equally.

## Decision

Recommend the project's shared tracker. GitHub Issues is the recommendation when the project has a GitHub remote the session can reach and no other tracker is in play; files are the recommendation when no shared tracker is available. The venue is still asked once and written to `tickets/store-config.md` — only which answer is recommended changes.

A venue already stated — in `tickets/store-config.md`, or in the project's own context file — is used without an ask and without argument, whatever it names. A stated preference is not something this recommendation overrides; it is what replaces the recommendation.

Both `ticket-up` and `next-ticket` say what a files store cannot do — coordinate workers who do not share a checkout — so a project that chooses it chooses it knowing.

## Alternatives Considered

- **Keep files as the recommendation**: the shipped behavior — Rejected: it recommends the one venue that cannot carry a claim across the isolation parallel work assumes.
- **Recommend GitHub Issues specifically**: name the shipped tracker as the default — Rejected: it reads as a GitHub dependency when the real requirement is a shared live store, and it argues with a project that already runs something else.
- **Drop the files venue**: support only shared trackers — Rejected: files stay right for a solo worker, an offline project, or a repo with no remote, and cost nothing to keep.
- **Make files coordinate by pushing claims to the shared branch**: commit and push each claim immediately so siblings can fetch it — Rejected: it needs write access to the shared branch from every worker, turns races into push rejections that need a retry loop, and builds a locking protocol onto the venue chosen precisely for having no protocol.

## Consequences

### Positive
- The recommended venue can do what the workflow promises.
- A project with an existing tracker gets its own tracker rather than an argument.

### Negative
- The recommended path now needs auth and network on the first run; the offline-capable option has to be chosen deliberately.
- More repositories end up with a `tickets/` directory holding only a config file — a cost 20260809-locate-the-ticket-store-by-convention-not-configuration already accepted as the exception, and which this makes the common case.
- On a public repository, tickets become public issues. The project's existing discipline for public issue text applies to them.

## Source
- Session: figure-out on parallel ticket sessions (2026-08-10)
- Related: 20260806-retire-decision-map-for-ticket-up-and-ticket-store (narrows its "files-in-repo as the zero-config default"), 20260809-locate-the-ticket-store-by-convention-not-configuration, 20260810-next-ticket-claims-the-ticket-it-picks, 20260810-generate-a-venue-reference-for-an-unmapped-tracker
