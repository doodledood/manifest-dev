# Handoff Doc Shape

The receiving agent reads the whole doc top-to-bottom and arrives at the same working model you have right now — without you in the room.

## Skeleton

```markdown
# Handoff: <topic in 1-3 words>

## Topic
<One or two sentences. What's being figured out or worked on — enough that the new agent
knows the question, not the whole history.>

## Current Read
<The load-bearing understanding. The working model of the situation right now. What you'd
say if a colleague walked in and asked "where are we?" — but written so it stands alone.>

## Decisions
- **<decision in 3-7 words>**: <why this won, in one sentence>. Alternatives considered:
  <A> (rejected because <reason>), <B> (rejected because <reason>).
- **<decision>**: ...

## Verified Facts
- <fact> — verified via <file:line | command output | doc URL>.
- <fact> — verified via ...

## Open Threads
- <thread>: closes when <signal or answer>.
- <thread>: closes when ...

## Next Move
<One sentence. The immediate next step if it's known. Omit this section entirely if it isn't.>
```

## Annotated example

```markdown
# Handoff: Auth migration to Auth0

## Topic
Migrating session-based auth (Rails devise) to Auth0 for a small SaaS. We're choosing
between Auth0's Universal Login redirect flow and an embedded login form.

## Current Read
Universal Login is the right call for our scale (~5k MAU, no enterprise SSO yet). Embedded
forms looked appealing for UX continuity but require maintaining our own PKCE handling and
forfeit Auth0's adaptive MFA defaults. Migration risk centers on session-token compatibility
during the rollover window; the rollover plan is dual-write for two weeks then cut over.

## Decisions
- **Universal Login over embedded form**: less custom code, gets adaptive MFA + bot detection
  for free. Embedded form rejected because we'd own PKCE + brute-force defense ourselves.
- **Dual-write rollover window**: writes go to both old session store and Auth0 for 2 weeks,
  reads prefer Auth0. Big-bang cutover rejected because it strands logged-in users.
- **Email as user_id**: matches existing customers table; can change to Auth0 sub later if
  needed. Auth0 sub as primary rejected because it forces a customers-table migration up front.

## Verified Facts
- Auth0 free tier supports 7.5k MAU — verified via https://auth0.com/pricing (2026-05-13).
- Our customers table has 4,820 rows — verified via `SELECT COUNT(*) FROM customers;`.
- Devise session cookies are signed with Rails secret_key_base — verified via
  config/initializers/devise.rb:42.

## Open Threads
- Social login providers (Google, GitHub): closes when product confirms whether they're
  in scope for v1.
- Rate-limit defaults during the dual-write window: closes when we benchmark Auth0's free-
  tier rate limits against our peak login traffic (currently unknown).

## Next Move
Spike Auth0's Rails SDK in a branch, get a single test user through the Universal Login
flow end-to-end, then come back to the rollover plan with concrete API shapes.
```

## Notes on shape

- **Topic** is the question, not the journey. One or two sentences.
- **Current Read** is the working model — opinionated, falsifiable, the kind of paragraph
  you'd write at the top of a design doc. Not a summary of what's been said.
- **Decisions** include alternatives with their rejection reasons. That's the load-bearing
  part — the receiving agent shouldn't redo that thinking.
- **Verified Facts** name how the fact was grounded. "verified via file:line" or "via
  command output" or "via doc URL." This is what keeps the new agent from taking the
  outgoing agent's read on faith.
- **Open Threads** name what would close each thread. A thread that doesn't say what
  resolves it isn't actionable for the receiver.
- **Next Move** is single-sentence if known; omit the section if not. Don't pad it.
- **Verified vs inferred distinction is preserved throughout.** If something isn't in
  Verified Facts, it's understood to be inference. Don't smuggle inference into facts.
