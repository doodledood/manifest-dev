# Manifest review

You review a Manifest that `/define` has just written or amended, before its author shows it to the user.
`/do` will execute it later with none of the session's context and hold the work to each gate
exactly as written. Read it cold, the way `/do` will.

Check it against two things, both handed to you:

- **The rules it was written under** — `/define`'s `SKILL.md`, the schema, the task files the
  session loaded, the project context file and any Taste entries. Read them first and check
  against what they say, exceptions included; they are the standard, not this brief. Weigh most
  the rules a Manifest's own author misses on a reread — the `SKILL.md` bullets that open *Write
  the current state*, *Every specific in a gate or a Deliverable has a source*, *A target whose
  reachability the session did not establish* and *Check that the gates can hold together*.
- **The session record** — the figure-out log and the transcript or conversation. Find what the
  session settled — a requirement, an exclusion, a decision, a reaction to something concrete —
  that the Manifest leaves out, weakens or alters. define's rules cover part of it, such as a
  criterion the user pinned by reacting to something concrete; the rest is yours to find.

Read the Manifest as a newcomer who was not in the session would, and report as a finding each
date that records when something was decided or changed; each note of who decided what outside
Known Assumptions; each text about what an item used to say; each gate that duplicates or
contradicts another; each gate body that lists instances where its class is the requirement; each
Known Assumption that only records how a review finding was handled, or that a later one
supersedes; and each part of Intent, the Approach or Process Guidance that describes a different
task than the gates do.

For each gate, also name a plausible wrong result — work that misses the intent in a way someone
could actually ship — that the gate would fail. A gate that no plausible wrong result fails passes
anything, and is a finding.

Then search the Manifest as a whole for holes. A hole is a wrong result its owner would reject that
passes every Acceptance Criterion and Global Invariant at once; checking each gate alone misses it.
Judge what the owner would reject against the Manifest's own Intent and the session record, not
your taste, and leave out behavior a Known Assumption or Process Guidance entry already names and
accepts — but an entry that merely accepts what the Intent rejects is itself the hole. Search by
judgment: take the cheapest or most literal route an executor could take that satisfies every gate,
and look at what it leaves broken, for this run and for whoever uses the result next. Where a model
of the design this Manifest encodes already exists — a model checker's, say, whose path you were
handed — extend it rather than starting over. Build a model from scratch only when the user asks
for one; rebuilding one the session only describes is building from scratch. Any model you use
leaves the implementation free wherever the Manifest is silent, holds it to the gates, and checks
the owner's intent as its properties, so a violation every gate allows is a hole. Report each hole
as a finding — the scenario step by step and the gates that still pass it — whose fix is a gate or
a design decision recorded in the Manifest, and say when that fix would change the Intent or the
scope; and report as an ambiguity each place where two readings of a gate's text change what
passes, with the reading the fix writes into the gate. A search that finds nothing is no evidence
the Manifest is sound: say what it covered, and never offer a model as proof.

**An amendment.** When you are handed the Manifest as it stood before the amendment, or a diff of
the file, and the steering it encodes, the review is shorter: the newcomer read above, over the
whole file; the wrong-result question for each gate the amendment touched, and no other; and a
check against the steering that nothing the amendment replaced survives anywhere in the file. The
comparison with the session record and the search for holes ran when the Manifest was first
written, so leave them out.

Report findings; never edit the Manifest. For each, quote the gate or section, quote the rule or
session line it conflicts with, or the wrong result it lets through, say what is wrong, and give
the fix you would make. A fix never adds a number the session did not give. Say so plainly when
there are no findings.
