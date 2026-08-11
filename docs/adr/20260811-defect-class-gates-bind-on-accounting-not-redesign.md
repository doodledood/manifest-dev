# ADR: The defect-class gate binds on accounting for the class, not on redesigning it

## Status
Accepted

## Area
define / do

## Context

The motivating instinct behind the `defect-class` dimension
(20260811-a-review-dimension-may-take-a-defect-as-input) is stronger than what that dimension
was admitted to do: stop patching instances and eliminate the class by better design. Written
literally into a gate, that instinct fires on every bug — including the many where a three-line
guard is the correct and complete fix — and runs straight into `code-simplicity`'s
over-engineering bar, which exists to catch exactly the abstraction a redesign mandate would
manufacture. A gate that mandates restructuring is a gate that mandates scope creep, against a
project stance that treats unbounded spend as a workflow defect rather than a price.

The opposite failure is equally real. A gate that asks only "did you fix the bug" is the status
quo, and the status quo is what lets a fix close one door and leave five open.

There is a second calibration question inside the same decision. When a change can add a check
that catches the whole class — a lint rule, a property test — that looks like the strongest
possible answer, and it is the answer the wider industry usually reaches for. It is also far
cheaper than restructuring, which matters because a list of acceptable answers is a list of
endorsements: the cheapest item on a menu becomes the default.

## Decision

The gate binds on **accounting for the class, not on redesigning it**. For the mechanism the
change fixes, every other site that mechanism reaches carries a stated disposition. Redesign is
one way to satisfy it, never the requirement.

Three dispositions, and **their order is the mechanism by which the preference is expressed**:

1. **The site no longer exists** — the fix concentrated the mechanism so there is one place
   instead of N.
2. **Fixed at the site.**
3. **Named out of scope, with why.**

First position reads as preferred; nothing is mandated. That is what lets the gate lean toward
eliminating surface while leaving a point fix fully valid, so it never collides with
`code-simplicity`. It is also, deliberately, where the preference lives: a lean every session
owes belongs in the prompt rather than in a ratified personal preference
(20260810-universal-discipline-belongs-in-the-prompt), and ordering encodes it structurally
instead of by exhortation.

**A check that detects the class is not a disposition.** A lint rule or property test permits
the mistake and complains; a removed site means it cannot be written. The durability such a
check is argued for — it catches code nobody has written yet — is what the design fix supplies
more completely, since there is no site at which the future instance could be written. And a
rule is a new artifact to maintain where the fix removes surface, so it works against the
maintainability the gate exists to buy. Adding one alongside a real disposition is fine; it does
not by itself account for a site.

Supporting rules:

- **The gate derives the mechanism from the fix**, never relying on a diagnosis having recorded
  it. `BUG.md`'s "Mechanism, not shape" is itself a Default, so a binding gate resting on it
  would rest on nothing.
- **The enumeration is bounded by the mechanism's specificity, not by a site or file cap.** The
  mechanism is narrower than the symbol it touches — not "every caller of `getUser`" but
  "callers that then read `.profile` without handling the create path" — and that predicate is
  already written into the fix. A cap would truncate silently and the report would read as
  having covered everything.
- **A convention-anchored mechanism has nothing to enumerate** and is discharged by disposition
  three, naming why the region is not walkable. `BLOCKED` is reserved for being unable to
  identify the mechanism at all.
- **This is verifiable from the output, which is what makes it a gate.** "Probe whether a
  pattern fix prevents recurrence" is a process act and stays advice; the enumeration and its
  per-site dispositions are an artifact a verifier can check. That is the project's own test for
  which of the two a task-file item is.

## Alternatives Considered

- **Bind on eliminating the class by design**: rejected. Correct on the cases that motivated the
  gate, wrong on every bug whose right fix is local, and in direct conflict with
  `code-simplicity`'s over-engineering bar.
- **Include "prevented by a new check" as a fourth disposition**: rejected. It loses on the axis
  it is argued for — detection permits the mistake where removal prevents it — adds a maintained
  artifact where the alternative removes surface, and, being the cheapest item on the list, would
  become the default answer and quietly hollow the gate out.
- **Let "prevented by a new check" satisfy only for future sites, with existing ones still
  needing a disposition**: rejected as unnecessary once the disposition itself was cut; a rule
  firing on five unfixed sites converts them into visible debt rather than accounting for them,
  which the three remaining dispositions already say better.
- **Unordered dispositions**: rejected. Equal presentation reads as indifference between removing
  a site and patching it, which is precisely the judgment the gate exists to shift.
- **Record the design preference as a ratified personal Taste entry**: rejected. It is a lean
  every session owes rather than one user's, which 20260810-universal-discipline-belongs-in-the-prompt
  routes to the prompt.
- **Cap the enumeration at N sites**: rejected. Silent truncation reads as complete coverage; a
  wide region is better surfaced as such.

## Consequences

### Positive

- The gate is satisfiable cheaply on a genuinely isolated bug — enumerate, find one site, done —
  so a defect-finder threshold does not become a redesign tax.
- The preference for removing surface rides in the prompt's structure rather than in an
  exhortation a verifier can weigh away.
- The check stays orthogonal to `code-simplicity` by construction: it never demands an
  abstraction, so the two cannot issue contradictory findings on the same change.
- What must be produced is an artifact, so the practice moves from unverifiable advice to a
  checkable gate without changing what a good fix looks like.

### Negative

- "Named out of scope, with why" is a disposition a weak evaluator can reach for on every site,
  which would satisfy the gate while accounting for nothing. The gate's teeth are that the
  enumeration must exist and each site must carry a stated reason; nothing detects a plausible
  reason given in bad faith.
- Dropping the detection disposition gives up a real durability benefit on the residual cases
  where no design fix exists and the mechanism is symbol-anchored.
- Ordering as a preference signal is weaker than a rule, and its effect is unmeasured. If runs
  keep landing on disposition two where one was available, the ordering is not carrying the
  weight and the decision needs revisiting.
- The mechanism-derived bound is only as good as the mechanism stated; an imprecise one produces
  a wide walk whose cost is real and whose findings are thin.

## Source

- Session: figure-out investigation, 2026-08-11 — `define/tasks/BUG.md` and `CODING.md`,
  `review-code`'s dimension references, and `/do`'s verification rules read at source. Matt
  Pocock's `codebase-design` skill supplied the locality framing behind disposition one.
  Self-graded: no independent re-derivation pass was run.
- Related: 20260811-a-review-dimension-may-take-a-defect-as-input (the dimension this gate
  delegates to), 20260810-universal-discipline-belongs-in-the-prompt,
  20260726-only-gates-bind-process-guidance-is-advisory, 20260807-a-gate-is-one-text-not-two
