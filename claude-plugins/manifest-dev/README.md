# manifest-dev

The workflow: understand the problem, write down what you'd accept, then build and verify against it. Plus the surfaces that keep a project's direction and its queue of work out of any one person's head.

[See it explained →](https://doodledood.github.io/manifest-dev/)

```bash
/plugin install manifest-dev@manifest-dev
```

## The three beats

Run them in order, though each works on its own:

| Skill | What it does |
|-------|--------------|
| `/figure-out` | Presses on a problem until you both understand it. Investigates on its own, asks when your contribution changes the answer, and carries acknowledgments forward into the next question. Holds a position under pushback and changes it on evidence. Useful on its own, whether or not anything gets built after. |
| `/define` | Turns that understanding into a Manifest — the deliverables, the criteria each has to meet, and the rules holding across all of them. Calls `/figure-out` first if understanding isn't there yet. |
| `/do` | Implements against the Manifest and verifies every criterion before reporting completion. Verification runs independently of the work by default. |

`/done` reports completed `/do` work. `/escalate` is the terminal handoff for either executor when unresolved blockers need outside intervention and no useful independent work remains.

## Run it unattended

`/do` assumes you are away for the entire execution, even after you send a steering message. It decides without asking follow-up questions and reports material choices and their rationale afterward. A failed approach calls for another approach; a blocker requires something the executor cannot responsibly supply. Blockers are reported promptly while useful independent work continues.

Both may revise Appetite — the planned size of the change — before broader work starts when the benefit to your requested outcome justifies added complexity and maintenance. Explicit exclusions and binding requirements stay fixed. Unrelated improvements and changing the contract to excuse excess work are outside that delegation.

These entrypoints extend unattended work through planning or reduce its process:

| Skill | What it does |
|-------|--------------|
| `/auto` | Chains figure-out, define and do without stopping for approval between them. |

## Project surfaces

These set up and feed the two longer-lived tiers:

| Skill | What it does |
|-------|--------------|
| `/init-context` | Sets a repository up with a North Star, a glossary, and decision-record conventions, plus the wiring that makes every session read them. Seeds them from the project's own history where there is any. |
| `/ticket-up` | Writes work into your ticket store — from a finished Manifest, a direct request, an open question, or findings from other work. |
| `/next-ticket` | Reads the store, picks the one to work on now, claims it, and says why it leads. |
| `/run-ticket` | Takes one specific ticket end to end and records the outcome back on it. |
| `/sweep-tickets` | Picks up or resumes a single unattended ticket, for scheduled runs. |

## Review and verification

Manifest criteria call these; you can also invoke them directly:

| Skill | What it does |
|-------|--------------|
| `/review-code` | Reviews a change along one named quality dimension and reports findings. Manifest criteria call it by dimension. |
| `/review-writing` | Reviews prose against this project's writing standards, in whichever register the text is in. |
| `/review-design` | Reviews artifacts using the delivered medium, applicable access and fidelity standards, bounded machine checks and exercised behavior. Reports findings and unavailable verification; style defaults alone are not failures. Manifest criteria call it for design gates. |
| `/check-pr` | Inspects a pull request's state and reports whether it's ready. Read-only; never merges. |

## First-principles design

`/design` supplies standalone art direction, information design and interaction design from the person an artifact is for, the moment they meet it in, and its subject. The moment sets the feeling and how strong it should be — a first glance, a meeting, a working day each want something different — and the subject and the audience's world supply the visual idea, palette, type and texture instead of a house style. A request that names the intensity it wants overrides the moment's default.

Technical implementation stays with the invoking agent; `/review-design` evaluates the result. The design skill has no dependency on the evaluator.

```text
/design explain these experiment results to a PM as a compact visual ELI5 page
/design turn this outline into clean HTML slides with purposeful motion
```

## Conversation

These shape where a session's answers land:

| Skill | What it does |
|-------|--------------|
| `/figure-out-team` | Runs the same deliberation in a Slack channel or thread, for people who can't all sit in one session. |
| `poll-slack` | Reports what's new in a channel or thread since a cursor. Called by `/figure-out-team` rather than invoked by hand. |

## How it fits together

A Manifest separates *what to build* — deliverables, each with criteria — from *what must hold throughout*. `/do` can't call it finished while any criterion lacks evidence, which is what makes "done" a finding rather than a claim.

The Manifest is the source of truth for a run. Feedback during `/do`, or after it finishes, amends the Manifest rather than being applied straight to the code.

For an unattended run, `/do` sets a host-native goal-setting or continuation contract before implementation, with the Manifest’s absolute path included. Where a host offers neither capability, the executor prints the same contract for you to apply manually. `/auto` leaves this to the executor: understanding and definition have no continuation goal, so an interruption there needs a restart.

## Manifest sections

A Manifest has six sections, each with its own ID scheme:

| Section | Purpose | IDs |
|---------|---------|-----|
| Intent | Problem, appetite, out of bounds | — |
| Initial Approach | Starting direction, departable | — |
| Global Invariants | Rules that hold across the whole run | `INV-G{N}` |
| Process Guidance | Advice on how to work; weighed, not enforced | `PG-{N}` |
| Known Assumptions | Items resolved with a recorded default | `ASM-{N}` |
| Deliverables | Work items with their criteria, least-proven first | `AC-{D}.{N}` |

Each criterion is one text: a title, a body saying what done means, an optional why, and a declared kind. The kind is what tells `/do` how to re-verify it.

## Example manifest

An abbreviated Manifest for adding authentication:

````markdown
# Definition: User Authentication

## 1. Intent
- **Problem:** Anyone with the app URL reads every user's data — there is
  no login at all.
- **Appetite:** Session auth over the existing endpoints, not an identity
  subsystem.
- **Out of bounds:** OAuth providers, account recovery, role permissions.

## 2. Initial Approach
- **Architecture:** Middleware-based auth, JWT in httpOnly cookies

## 3. Global Invariants

### INV-G1 — Passwords are never stored in plaintext

Done when `grep -r 'password.*=' src/ | grep -v hash | grep -v test` returns no matches.

Why: a plaintext password in the store is unrecoverable once shipped — every other auth
control is downstream of this one.

Deterministic gate.

## 4. Process Guidance
- [PG-1] Follow existing error handling patterns in the codebase

## 6. Deliverables

### Deliverable 1: Login round-trip

*What it is, and how it is exercised end-to-end:* signing in from the browser and reaching a
protected page — the credential check, the cookie, and the redirect exercised together.

#### AC-1.1 — POST /login returns a session for valid credentials

Done when POST /login with valid credentials returns 200 and sets a JWT in an httpOnly cookie
the protected routes accept.

Deterministic gate.

#### AC-1.2 — Invalid credentials fail cleanly

Done when the manifest-dev:review-code skill, activated with dimension=code-bugs over the auth
routes, reports nothing at or above that dimension's threshold — an invalid-credential path
returning 500 instead of 401 is the shape this catches.

Judgment gate.
````
