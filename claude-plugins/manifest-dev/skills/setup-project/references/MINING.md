# Seeding from a project's history

Reconstruct what the project already decided, what it calls things, and the few steering preferences its owner has already explained.

## Sources, strongest first

Rationale and vocabulary survive in different places, and the ordering below is the whole reason a run that reads only `git log` comes back with `what` and never `why`.

| Source | Yields | Notes |
|--------|--------|-------|
| **Prose documentation** | Rationale, constraints, vocabulary | READMEs, `docs/`, design notes, wikis, architecture pages, long code comments. The strongest source: a decision explained anywhere is usually explained here. |
| **Pull request and issue discussion** | Rationale, alternatives, the tension resolved | Where a team argued, the alternatives are written down. Read bodies and review threads, not just titles. |
| **Code** | Vocabulary, structure, current state | Module and type names, domain nouns, boundaries. Says what *is*, never why. |
| **Commit history** | Chronology, what changed, when, by whom | Dates a decision and orders the corpus. Subjects describe the change; they almost never carry reasoning. |

Read across all four before writing anything. A decision usually shows up in several — the code shows the shape, a commit dates it, and a doc or a discussion carries the why. Assembling those is the work.

## What deserves a record

Apply the bar in the project's `docs/adr/CONVENTIONS.md` — the same bar a live decision must clear. A reconstruction is not exempt from it, and a mined corpus of low-stakes changes is worse than no corpus, because it buries the decisions that matter.

Prefer few and load-bearing. A handful of records covering the choices that still constrain the project beats thirty covering everything that ever changed.

Mark every mined record retroactive per the conventions, naming the sources it was assembled from.

## When the reasoning is gone

Most of it will be. Record the decision anyway, and say plainly in the body that the rationale was not recovered — the conventions file specifies the exact form, including why `Alternatives Considered` must say *not recovered* rather than being left empty.

Never write a rationale you inferred as though it were the reasoning that was used. A confident reconstruction is indistinguishable from a record of what actually happened, and it will be trusted as one. If the evidence supports a guess and nothing more, either say it is a guess or leave it out.

## Vocabulary

Everything mined here lands in a file loaded on every future session, so the count matters as much as the quality of each entry.

**The bar** — a term earns a place only if misreading it would change what someone builds. In practice that means at least one of:

- it means something in this project that ordinary usage would not supply;
- confusing it with a near-synonym already in use would change behavior;
- it marks where responsibility, authority, or completion changes hands;
- the relationship between it and another term is load-bearing.

**Rank, don't sweep.** A codebase yields hundreds of terms that pass the bar honestly. Order candidates by how much damage misreading causes — a term crossing module boundaries, sitting at a handoff, or already used inconsistently under two names does more damage than one confined to a single file — and take the top of that list. Leave the rest: figure-out captures vocabulary as sessions actually surface confusion, which is better evidence than an inventory pass.

**Ratify, don't write.** Present candidates to the user as one batch, each with its proposed definition and one line on why it earns entry. Write only what they accept. figure-out writes glossary entries inline without asking because the user just said the term; a mining pass has no such warrant, and a wrong entry is paid for by every session afterwards.

With no user available to ratify, write nothing to the glossary — report the candidate list instead and let a later session settle it.

## Taste

A Taste entry is a ratified personal steering preference that later sessions weigh at a call two careful people could make differently: the preference, the reason its owner gave, and when it yields, kept in a `## Taste` section of a memory file the host loads every session. A project new to this workflow has none, so its owner's overrides reach no session until corrections capture them one at a time — though many are already explained in its history.

**Only a reason the user stated.** A candidate comes from a reversal or a correction whose reason the user gave: a decision record whose reasoning is a preference rather than a constraint, a review or pull request thread where they turned a proposal down and said why, and their past session records where the host keeps them. Those records are private: ask before opening them, and read them only on a yes. A reason you inferred never founds an entry, as *When the reasoning is gone* rules for records.

**Overrides first.** The workflow already ships defaults — figure-out's default product stances (`../../figure-out/references/SEAT.md` → *Default stances*) and each skill's own defaults. Rank first the entries where the user leans differently from one of them; a stated lean that no default covers may follow. Offer nothing a shipped default already says, and nothing a decision record already settles: that record is the choice's home, and a second copy drifts.

**Few, and stated as principles.** Offer at most five, ranked by how many later calls each would steer. Draft each in the boundary form `../../figure-out/references/TASTE.md` → *Drafting (boundary form)* gives — a preference that carries to calls never discussed, not the details of the case that prompted it — and propose its write target as *Scope and write target* there says.

**Ratify, don't write.** Present the candidates as one batch, each with the source it came from. Write only what the user accepts, into the `## Taste` section of the memory file they pick, changing nothing outside it. With no user available to ratify, write nothing — report the candidates instead.

## Reporting

Close the run by saying what was recovered and what was not: which sources carried usable rationale, how many records were written, how many carry unrecovered reasoning, and which parts of the project's history yielded nothing. For Taste, say which candidates were offered and from which sources, which the user accepted and the file each was written to, and what was left out and why — a default already said it, a record already settles it, or no reason was stated. Understating a thin seed is the failure to avoid — a user who knows it is thin will grow it.
