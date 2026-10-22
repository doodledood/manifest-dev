# manifest-dev

Hand your agent a task. Get back work you can trust. This plugin is the workflow: your agent works out what you mean, writes down what done means, and calls nothing finished until every check passes. Around it sit the parts that let a project keep its direction, hold its work as Tickets, and run that queue while you make the calls only you can make.

[See it explained →](https://doodledood.github.io/manifest-dev/) Each part works on its own, and nobody else on your team has to use it.

```text
/plugin marketplace add doodledood/manifest-dev
/plugin install manifest-dev@manifest-dev
```

## What to run at each level

Run these to reach each level; the sections below say what each move does:

1. **One skill** — install the plugin, then `/figure-out` with a question.
2. **One piece of work** — `/auto` with a task (or `/figure-out`, `/define`, `/do` one step at a time).
3. **A project that remembers** — `/setup-project`, once.
4. **A shared queue** — `/ticket-up` writes work as Tickets; `/next-ticket` picks the next one.
5. **The queue runs** — `/orchestrate`, then approve its plan; or `/orchestrate --autonomous` from a scheduler you already run. Mark a Ticket Auto when it needs no one's judgment.

## One piece of work

Four skills cover one piece of work, and each is useful on its own:

| Skill | What it does |
|-------|--------------|
| `/figure-out` | Works out what you mean. It reads your code, finds the question that decides the work, and asks you only what the code can't answer, with its recommended answer first. It holds a position under pushback and changes it on evidence. Useful on its own, whether or not anything gets built after. |
| `/define` | Writes down what done means, as a Manifest: the pieces of work (Deliverables), a check each one must pass (Acceptance Criteria), and rules that hold across all of them (Global Invariants). Calls `/figure-out` first if the work isn't understood yet. Before you see it, a fresh context checks it against the session and the rules it was written under, and the summary lists every number the work will be held to. |
| `/do` | Builds until every check passes. A failed check sends that piece back to be fixed; done means every check passed on fresh evidence. |
| `/auto` | Runs all three in one go, without stopping for approval between them. |

`/do` assumes you are away for the whole run, even after you send it a steering message. It decides without asking and reports the decisions it made for you and why. It raises a blocker as soon as it finds one — including a target its measurements show is out of reach, whose bar only you can change — and carries on with work that doesn't depend on the answer. Before broader work starts, it may grow the planned change when that serves your outcome; your exclusions and binding requirements stay fixed.

Before it builds, `/do` points the host's goal-setting or continuation capability at the Manifest, so an interrupted run resumes against the same file. Where the host has neither, it prints the same completion contract for you to apply.

It finishes through `done`, which reports the work, or `escalate`, which hands unresolved blockers to you once no useful independent work remains. Neither is invoked by hand. When the work ships as a pull request, its top reads in about a minute: what changed and why, the change shown working, the decisions made for you, and the debt left — what the run found and didn't fix.

## A project that remembers

One skill sets the project up:

| Skill | What it does |
|-------|--------------|
| `/setup-project` | Gives the project a North Star — what it is for and for whom, how it measures progress, and what it never does — plus a glossary, decision-record conventions, and one command that checks the project still works, with the wiring that makes every session read them. It seeds them from the project's history where there is any. Run again on a set-up project, it audits the whole setup and offers each gap. `/figure-out` offers it when the setup is behind, so you rarely type it. |

The check command is recommended, not required. A project that verifies its own way opts out, and runs then use the project's own tests and scripts and never add the command. Where it is kept, it reads one recipe — a short file saying how to exercise one thing — per feature, skill, document, eval suite, and the checks run across the whole tree. A check that costs money, quota, or effects outside the repository asks first.

The same commands keep the codebase easier to change, with nothing extra to run:

- **Design before code** — `/figure-out` sketches the shape of a change, compares a second one, and screens both for patterns the next agent would copy; `/define` puts a behavior-preserving restructuring first when the area resists the change.
- **Corrections become checks** — `/do` turns a caught mistake into a scoped type, lint, or test, and the decision record names it.
- **Debt stays visible** — what a run leaves unfixed is listed when it finishes and in the pull request; the next change on that path is offered the fix.
- **Earlier work is not lost** — sessions on a repository start from what earlier ones ruled and found, and runs keep the glossary, decisions, and checks current where their work touches them.

## A shared queue

Two skills write and pick the work:

| Skill | What it does |
|-------|--------------|
| `/ticket-up` | Writes work as Tickets — from a finished Manifest, a direct request, an open question, or findings from other work — into GitHub Issues, files in the repository, or a tracker you describe. A Ticket carries everything a person or an agent needs to do one piece of work and know it's done. |
| `/next-ticket` | Reads the store, picks the Ticket whose wait costs most, claims it, and says why it leads. |

**Auto** marks a Ticket that needs no one's judgment to finish and land. A person grants it. `/orchestrate --autonomous` grants it too, but only to a Ticket an agent wrote that meets that test.

**New work is planned with you.** An effort is one goal and its own Tickets. You think it through together with `/figure-out`, and `/ticket-up` turns what you settled into the effort's Tickets.

## The queue runs

Two skills run the queue:

| Skill | What it does |
|-------|--------------|
| `/orchestrate` | Proposes a plan over an effort's ready Tickets and runs it after you approve: each Ticket in its own session, landed one at a time. Auto Tickets land on their own; the rest stop at a ready pull request for you to land. The debt they leave becomes new Tickets, and one status page shows what is running and what waits on you, and says in plain words what each Ticket is for. With `--autonomous`, started by a scheduler you already run, it starts a new run whenever one finishes, up to the number it may run at once, until no ready work remains, and grants Auto where no one's judgment is needed. |
| `/run-ticket` | Works one Ticket up to a ready pull request, keeping its Manifest and progress on the Ticket so a fresh run can resume it. It lands only when told to. `/orchestrate` starts it for each Ticket; you can run it by hand too. |

What waits for you: landing a Ticket without Auto, a review the repository requires from a person, escalations, Tickets from people without write access, a cause that paused an effort (such as a check failing on the base branch), planning a new effort, and each plan in the default mode. Each item comes with the answer it recommends, the risk of taking it, and the evidence behind it.

## Review and verification

Manifest criteria call these; you can also invoke them directly:

| Skill | What it does |
|-------|--------------|
| `/review-code` | Reviews a change along one named quality dimension and reports findings. Manifest criteria call it by dimension. |
| `/review-writing` | Reviews prose against this project's writing standards, in whichever register the text is in. |
| `/review-design` | Reviews artifacts using the delivered medium, applicable access and fidelity standards, bounded machine checks, and exercised behavior. Reports findings and unavailable verification; style defaults alone are not failures. Manifest criteria call it for design gates. |
| `/check-pr` | Inspects a pull request's state and reports whether it's ready. Read-only; never merges. |

## First-principles design

`/design` supplies standalone art direction, information design, and interaction design from the person an artifact is for, the moment they meet it in, and its subject. The moment sets the feeling and how strong it should be — a first glance, a meeting, a working day each want something different — and the subject and the audience's world supply the visual idea, palette, type, and texture instead of a house style. A request that names the intensity it wants overrides the moment's default.

Before a new composition or substantial redesign, `/design` infers artifact uses and creative directions from the brief, honoring explicit choices. It selects concise guides from two linked indexes: [artifacts](skills/design/references/artifacts/index.md), organized by how people use the work, and [creative directions](skills/design/references/directions/index.md), organized by the feeling it should create. For substantial work, it briefly states the approach and why. Material unresolved choices prompt concrete alternatives; sufficient context lets it proceed. Both repertoires allow combinations and approaches beyond the listed examples. App guidance covers coherence across screens; individual screen guides address their particular uses.

For example, a cinematic landing page combines the cinematic direction with landing-page guidance. An editorial collection can add playful discovery, while a reference tool can combine precision with interactive exploration. Naming a direction selects it without requiring a separate skill. Narrow refinements keep their scope.

For a concrete design question, `/design` also exposes [optional instruments](skills/design/references/instruments/index.md): local analysis of supplied images, HTML, text, and structured observations. The agent obtains artifacts and interaction evidence using the tools available in its environment. The model chooses what applies and keeps judgment over the result. There is no required suite, universal score, or fixed refinement loop. Coverage and limits travel with the observations; better numbers can still make a design worse. Dependencies and examples are in the instrument usage guide.

Technical implementation stays with the invoking agent; `/review-design` evaluates the result. The design skill has no dependency on the evaluator.

```text
/design explain these experiment results to a PM as a compact visual ELI5 page
/design turn this outline into clean HTML slides with purposeful motion
```

## Conversation

These run `/figure-out`'s deliberation with people who can't share one session:

| Skill | What it does |
|-------|--------------|
| `/figure-out-team` | Runs the same deliberation in a Slack channel or thread, for people who can't all sit in one session. |
| `poll-slack` | Reports what's new in a channel or thread since a cursor. Called by `/figure-out-team` rather than invoked by hand. |

## Help

One skill answers questions about manifest-dev itself:

| Skill | What it does |
|-------|--------------|
| `/manifest-dev-help` | Explains manifest-dev in plain, simplified English: what it is for, the workflow, the autonomy ladder from one skill to unattended runs, every term you meet with why it exists, and good practice. Ask it what a recipe, a gate, or a Lock is, or point it at a Manifest or a pull request and ask what something means. |

## How it fits together

A Manifest separates *what to build* — deliverables, each with criteria — from *what must hold throughout*. `/do` can't call it finished while any criterion lacks evidence, which is what makes "done" a finding rather than a claim.

The Manifest is the source of truth for a run. Feedback during `/do`, or after it finishes, amends the Manifest rather than being applied straight to the code.

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
