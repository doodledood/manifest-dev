# Defect-class review

Audit a change that **fixes a defect** for completeness of remediation: given the mechanism the fix
closes, which other sites that same mechanism reaches, and what happened to each.

This dimension does not look for defects. It takes one as input — the defect this change fixes —
and asks whether the response to it is complete. Every other dimension reads code on its own terms
and reports what it finds there; this one starts from a fix and works outward along the mechanism
that fix closes. That is the whole of its territory, and it is what keeps it distinct from every
sibling.

**Applicability.** Run only where the change fixes a defect. On a change that fixes nothing there is
no input, and the correct outcome is PASS with a line saying no fix was found in scope. Do not
manufacture a defect to review.

## The boundary test

One test settles every question about what belongs here:

> **Delete the fix from the diff. Does the finding survive?**

If it survives, the finding is about code judged on its own terms — `code-bugs` owns it, or another
sibling does. If it collapses, because it existed only as *another instance of the thing just
fixed*, it belongs here.

Apply this to every candidate before reporting it. A finding that survives the deletion is one this
dimension is borrowing from a neighbour, and reporting it here means the same finding can arrive
twice from two reviewers.

**Ask it in the mode you were invoked in.** Under diff-based review — the default, and what a
manifest gate and `review-pr`'s fleet both use — a sibling site in unchanged code is invisible to
every other dimension, so the test collapses and the site is yours. Under explicit-path review,
where the caller named the paths, `code-bugs` and the rest accept pre-existing findings, so the
same site now survives the deletion and belongs to whichever of them owns it on its own terms;
report the site in your enumeration under the third disposition, naming the sibling's ownership as
the reason it is out of scope here, and leave the defect claim to them.

Either way exactly one dimension owns the site, and every site you enumerate still carries exactly
one disposition.

## Reading unchanged code

This is the one dimension that reports on code the change did not touch. That licence rests on the
trigger, not on a scope exemption, and the distinction is what stops it generalising.

`review-code`'s shared bar requires a **stated trigger** — the condition under which a defect
manifests — rather than a confidence level, and in diff-based review the sibling dimensions bar
pre-existing findings precisely because a defect nobody has observed in untouched code is
speculation dressed as a finding. Here the trigger is not speculative and not yours to supply:
the fix in front of you established it. The bug happened. A second site reachable by that same
mechanism is a door into a failure that has already occurred once.

So the licence extends **exactly as far as the proven mechanism reaches, and no further.** It is not
a general permission to surface technical debt found along the way. A problem you notice in
unchanged code that the fixed mechanism does not reach is out of scope here — leave it alone.
Whether any sibling can report it is theirs to decide under the mode they were invoked in.

## Deriving the mechanism

Derive the mechanism **from the fix itself**. Read what the change actually altered and state what
condition it now prevents: which value, held where, wrong how, reached by what sequence.

Do not depend on the author having written the mechanism down. A commit message, a linked issue, or
a manifest may state it, and where one does, use it as corroboration — but the diagnosis being
recorded is a practice, not a guarantee, and a gate resting on it would rest on nothing. Where the
recorded diagnosis and the fix disagree about what was wrong, trust the fix and say so in the
report.

A mechanism is specific enough to work with when you can state it as a condition a reader could
check at a site: *"the callback reads `userIdRef.current` after a cleanup path may have cleared it"*,
not *"stale state"*. If you cannot get past a shape, you cannot enumerate a region from it — see
*Handling ambiguity*.

## Enumerating the region

Walk the references to the specific thing the mechanism names — the field, the function, the shared
state, the call pattern — and for each, judge whether the mechanism reaches it.

**The mechanism bounds the walk, not a budget.** The mechanism is narrower than the symbol it
touches: not *every caller of `getUser`* but *callers that then read `.profile` without handling the
create path*. That predicate is already encoded in the fix, so stating the mechanism precisely is
what makes the region tractable. A vague mechanism produces a wide region and thin findings, which
is a signal to sharpen the mechanism rather than to sample the region.

**Never cap the walk at N sites or N files.** A cap truncates silently and the report then reads as
having covered everything when it covered a prefix. Where a region is genuinely too large to walk,
say so — that is a disposition (below), not a quiet trim.

## Dispositions

Every site the mechanism reaches carries exactly one disposition. **These are ordered: the first is
the preferred outcome where it is available.**

1. **The site no longer exists.** The fix concentrated the mechanism so there is one place to get it
   right instead of N, and the sites that used to be reachable are gone. This is the outcome worth
   reaching for, because it removes the class rather than each member of it.
2. **Fixed at the site.** The same defect, repaired where it lives.
3. **Named out of scope, with why.** The site is reachable in principle but not this dimension's to
   claim — dead code, a different lifecycle that makes the condition unreachable, a region too large
   or too diffuse to enumerate, or a site whose defect claim belongs to a sibling dimension under
   the mode you were invoked in. The reason is what makes this a disposition rather than an
   omission.

   A dead, unreachable, or un-walkable site is closed; a sibling-owned one is only re-homed, and the
   enumeration says which it is. Do not write "out of scope" over a site a sibling owns without
   naming the sibling — that reads as remediated when nobody has looked at it yet.

**The ordering expresses a preference and mandates nothing.** A change whose every site is fixed in
place satisfies this dimension completely — do not report a finding because a restructure was
available and not taken, and never make "you should have redesigned this" the finding. Demanding an
abstraction is `code-simplicity`'s over-engineering territory in reverse, and this dimension must
not be the thing that manufactures one.

**A check that detects the class is not a disposition.** Adding a lint rule, a property test, or a
static-analysis rule is often good work, and it does not account for a site:

- A check **permits** the mistake and complains about it; a removed site means the mistake cannot be
  written. Detection is the weaker of the two on the exact axis it is usually argued for.
- A check is a **new artifact to maintain**, where the first disposition removes surface.
- A rule that fires on five unfixed sites has converted them into visible debt, not accounted for
  them.

It is also cheaper than any of the dispositions above, which is why it is not one of them. Offered
beside them, a detection check wins nearly every time on effort alone — so listing it would quietly
make it the answer, and the gate would stop buying what it exists for.

A change may add such a check alongside a real disposition, and that is fine. It does not by itself
discharge any site.

## Actionability filter

Before reporting, a finding must pass ALL of these. **If it fails ANY, drop it entirely.**

1. **A defect is actually fixed in this change.** No fix, no input, no findings.
2. **It survives the boundary test in the right direction** — deleting the fix collapses the
   finding. If it survives the deletion, it belongs to a sibling; drop it here.
3. **The mechanism is stated concretely** — the variable, location, value, and sequence, per
   *Deriving the mechanism*. A shape ("same kind of race") is not a mechanism.
4. **The site is genuinely reached by that mechanism.** Similar-looking code that the mechanism
   cannot reach — different lifecycle, different ownership, a guard already present upstream — is
   not a finding. Trace it, don't pattern-match it.
5. **No disposition is stated for it.** A site the change fixed, removed, or explicitly named as out
   of scope is accounted for. Judge a stated reason on whether it is a reason, not on whether you
   would have made the same call.
6. **Matches codebase rigor.** If the surrounding code accepts this condition everywhere by
   deliberate convention, the fixed site may be the exception rather than the first of a sweep —
   check before reporting a sweep nobody wants.

## Out of scope (orthogonality boundaries)

Do NOT report on (owned by other dimensions):

- **Defects judged on their own terms** — anything that would be a finding if the fix were not in
  the diff → the code-bugs dimension. This is the boundary test, and it is the one that matters
  most.
- **Completeness against a designed artifact** — a shared interface, data format, or contract whose
  consumers were not all updated; a new pattern introduced without migrating old sites; a constraint
  applied to one schema and not its siblings → the code-design dimension's PR-coherence categories.
  Each of those is anchored to something *designed* that has instances. A defect mechanism is not a
  designed artifact, which is why a guard replicated across call sites falls through all of them and
  lands here.
- **The next sibling forgetting a cross-cutting behavior** — 2+ components each manually replicating
  something that belongs at a higher level → the code-maintainability dimension's extensibility
  risk. That is about instances not yet written; this is about existing instances already broken by
  a mechanism that has fired.
- **Duplication, coupling, cohesion, dead code, consistency** → the code-maintainability dimension.
- **A type system that could make the mechanism unrepresentable** → the type-safety dimension. That
  a discriminated union would have prevented the class is its finding, not this one's; this
  dimension reports the unaccounted sites regardless of what could have typed them away.
- **Intent-behavior divergence** (does the fix achieve what the author intended?) → the
  change-intent dimension.
- **API contract correctness** → the contracts dimension.
- **Whether a regression test exists for the fix** → the test-quality dimension.
- **Whether the fixed code is hard to test** → the code-testability dimension.

**Key distinctions from the closest neighbours:**

- **code-bugs** asks: *does this code have a defect?* This asks: *is the defect this change fixed
  accounted for everywhere it can occur?*
- **code-design** asks completeness questions too, but always about a designed thing with instances.
  If you can name the interface, pattern, or schema, it is code-design's. If the only thing with
  instances is the failure mode itself, it is this dimension's.

## Severity calibration (this dimension)

Severity reflects what happens at the **unaccounted site**, not how many sites there are. A single
unaccounted site on a critical path outranks four on a debug page. Refining the shared ladder:

- **Critical**: An unaccounted site where the mechanism produces data loss, corruption, a security
  failure, or complete feature failure, with no workaround. The same grade the original defect would
  have carried at that site.
- **High**: An unaccounted site on a core or happy path — the mechanism fires for common inputs, and
  the failure is the one just fixed elsewhere.
- **Medium**: An unaccounted site reachable only through edge cases, optional parameters, or error
  recovery paths.
- **Low**: An unaccounted site requiring several unusual preconditions.

A site carrying a stated out-of-scope reason is accounted for and has no grade — it was dropped by
the actionability filter before reaching this ladder. Judging a stated reason thin is not a finding
at any severity; that a plausible reason given in bad faith goes undetected is a cost this dimension
accepts rather than a gap to close by grading reasons.

This is a **defect-finder** dimension: PASS requires no LOW-or-higher findings. Every finding here
carries a trigger the fix already demonstrated, so there is no taste-level band to tolerate — which
is also why a finding you cannot ground in the proven mechanism must be dropped rather than filed
low.

**Calibration check**: a change that fixed an isolated defect should routinely PASS with one site
enumerated. If most reviews produce findings, the mechanisms are being stated too broadly.

## Report expectations (this dimension)

Beyond the shared report format, this dimension adds two sections to the report **body, between
`Files analyzed` and `## Findings`**. Both are required on PASS as well as FAIL — on the expected
outcome, an empty findings list, they are the only thing distinguishing a walk that found nothing
from a walk that never happened.

- **`## Mechanism`** — the mechanism stated as a condition a reader could check at a site. Every
  finding is measured against it, and a reader cannot judge the findings without it.
- **`## Enumeration`** — the sites the mechanism reaches and the disposition of each, not only the
  failures, plus how the region was derived (the symbol searched, the paths followed) so the walk is
  reproducible.

Then, within the shared format:
- Each finding names the **site**, the **path by which the mechanism reaches it**, and what a
  disposition would look like there. The shared **Trigger** field carries the mechanism's condition
  as it manifests at that site.
- Where the first disposition was available and not taken, that is **not** a finding. Mention it at
  most as a note, and never as a severity-bearing item.

An empty findings list with a stated mechanism and a complete enumeration is the expected outcome on
a well-scoped fix. Do not fabricate reachable sites to fill the report.

## Handling ambiguity

- **Cannot identify the mechanism at all** — the change is large enough or diffuse enough that what
  it fixes cannot be stated as a condition: return **BLOCKED**, saying what you could not determine
  and what would resolve it (usually a narrower scope or the author's diagnosis). This is the only
  *enumeration* case that returns BLOCKED — the shared verifier contract's own BLOCKED cases still
  apply, and this does not narrow them.
- **Mechanism identified, region not enumerable** — the mechanism is anchored to a convention rather
  than to a symbol ("anything that assumes this callback fires before mount"), so there is nothing
  to search on. This is **not** BLOCKED. The region is named out of scope under the third
  disposition, with why it is not walkable, and the gate passes on that.
- **Cannot tell whether a site is reached** — trace further. If it still will not resolve, drop it;
  a speculative sibling site is exactly the finding this dimension's licence does not cover.
- **The change fixes several distinct defects** — treat each as its own mechanism with its own
  enumeration. Do not merge them; two mechanisms rarely reach the same region.
- **An empty report is better than a false positive.** A wrongly-reported sibling site sends an
  author to read code that was never at risk, and it spends the credibility this dimension needs to
  report unchanged code at all.
