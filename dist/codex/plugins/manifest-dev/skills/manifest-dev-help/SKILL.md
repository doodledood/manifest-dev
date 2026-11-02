---
name: manifest-dev-help
description: 'Answer any question a person has about manifest-dev, with the why behind it: what it is for, its workflow and the autonomy ladder, each term a user meets (Manifest, Acceptance Criterion, Global Invariant, verification harness, recipe, ask-first, Lock, Debt, Ticket and the rest), how the parts relate, why each part exists, the practices it encodes, and what a Manifest, a run report, a pull request section or a file the workflow wrote means. Use when the user asks what something in manifest-dev is, why it works that way, how its skills relate, or where to start. Not for help with the user''s own task.'
---

# manifest-dev-help

People come here to ask about anything in manifest-dev that they do not understand, and why it works
that way. Answer each question with what the part is and why it exists. Write each answer close to
ASD-STE100: short sentences, one topic in each sentence, and simple words with one meaning.

## How to answer

1. When the question names a term or asks about a part, file or behavior, read `references/GLOSSARY.md`.
2. When the user asks for all the terms, give all of `references/GLOSSARY.md`.
3. When there is no question, give *What manifest-dev is for*, *The workflow* and *The autonomy ladder*.
4. When the user points at something, read it first: a Manifest, a log, a pull request or a file.
5. When the question is about the project of the user, also read its Project Surfaces.
6. When this skill does not give the answer or its reason, read the skill that owns that behavior.
7. Find that skill in the folder next to this one: its `SKILL.md` and its `references/` folder.
8. Answer only the question.
9. Give the reason for each part, not only what it is.
10. When the answer comes from a file other than this skill, name that file.
11. When no file gives the answer, say so instead of a guess.

## What manifest-dev is for

Agents can write almost all code now, but projects still drift. Each session must find again what
the project is for, what to do next, and what "done" means. The speed of the agent then makes more
work than a person can examine.

manifest-dev keeps these three things in the project, not in the head of a person. The agent reads
them, does the work against them, and examines its result before it says that it is done. The
promise: you give the agent a complex task, and you trust the result enough to ship it with minimal
review. Weeks later, the project still knows what it is for, what is next, and what "done" means.
The code is also easier to change correctly than before.

You can assign a project outcome within chosen limits. `/orchestrate` can investigate, shape work, deliver it and read the results. You retain the decisions you want to make. Reliable ongoing operation remains an ambition; a completed task does not prove that ambition.

manifest-dev is for developers who want results that they can trust. They agree to spend more tokens
and more work at the start to get them. They can work alone or in a team of any size, also in a
codebase where their colleagues do not use manifest-dev. It is not for a person who wants only the
fastest or the cheapest result.

| Question | Where the answer is | How long it stays |
|---|---|---|
| What is this project for? | The North Star, a file in the project | Until an authorized ruling changes it |
| What is the next work? | A Ticket, in your tracker or in files | Until that work is done |
| What does "done" mean for this work? | A finite Manifest where that work needs one | For one run |

## The workflow

1. Use `/figure-out <topic>` to understand the problem before you change something.
2. Use `/define` to write a Manifest: what you will accept as done.
3. Use `/do <manifest-path>` to do the work and show evidence for each gate.

`/auto` does the three steps without a stop between them. Each skill also works alone, and no
project needs this sequence. You can take a Read straight to `/ticket-up`, or assign direct work.
`/define` starts `/figure-out` first when you and the agent do not yet agree on the problem.

When your tool can show a question as a list of options, `/figure-out` and `/define` ask you that
way. The first option is the answer that they recommend. You can also answer in your own words.

`/do` works as if you are away. It makes delegated decisions and reports them. A decision you retain still waits for you. A
message that you send during `/do` changes the Manifest, and the run continues. It stops only when
each gate has evidence, or when a person must act.

When the work goes into a pull request, its description shows the change working. The top tells
what changed and why, how the run showed that it works, the decisions, and the Debt left. It also
lists the problems that the run fixed on the way. Screenshots show a change that you can see.

## The autonomy ladder

You can use manifest-dev at five levels. Each level works without the levels above it. Other people
on your team do not have to use any level. Stop at the level that fits your project.

| Level | What you do | What you get | What it costs |
|---|---|---|---|
| 1. One skill | Use one skill alone, for example `/figure-out` on a question. | A better answer or review, with no setup. | Nothing in the project. |
| 2. One piece of work | Use `/figure-out`, `/define` and `/do`, or `/auto`. | A result with evidence for each gate. | More tokens and time at the start. The Manifest and its log stay outside the repository. |
| 3. Project Surfaces | Use `/setup-project` one time. | Each session starts from the direction, words, decisions, and checks of the project. | Files in the repository that your team can see. |
| 4. A shared queue | Write work with `/ticket-up` and take it with `/next-ticket`. | The next work is in a store, not in the head of one person. | A Ticket Store: GitHub Issues, files or your own tracker. |
| 5. Coordination | Start `/orchestrate` with a queue or a stated outcome. Approve its plan, or use `--autonomous` within your chosen limits. | Separate inquiry and delivery jobs run as Tickets. Results guide the next move. Retained decisions and missing evidence stay visible. | Authority and evidence sources that fit the assignment. An existing host wake only when you want automatic continuation. |

To climb a level:

1. Use your current level until you trust its results.
2. Add the next level where the current level does not give enough.
3. Grant Auto only when all needed decisions are settled or delegated, with no retained acceptance or missing access.

## Assignment and authority

An assignment says what to do. Delegation says which decisions the worker can make within that activity. Standing delegation starts no work, and a mode flag grants no wider scope.

Use `/setup-project` to record needed adjustments in the project instructions. Keep personal rules in private instructions. Setup shows the proposed text before it saves a new choice. It starts no operations.

For example, delegate visual direction but retain acceptance of the rendered result. The worker can build and recommend, then wait at that acceptance. Approval applies to that artifact and version; a material change needs another acceptance.

## The other skills

| Skill | Use it to |
|---|---|
| `/setup-project` | Give a project its North Star, glossary and decision-record conventions, and add a verification harness unless you opt out. Run it again to find gaps. |
| `/ticket-up` | Write work into your Ticket Store as Tickets. |
| `/next-ticket` | Select the next Ticket, claim it, and see why it is first. |
| `/run-ticket` | Investigate a Question or deliver Shaped work, keeping its result and progress on the same Ticket. |
| `/orchestrate` | Coordinate a queue or assigned outcome, with a status page and a list of what waits for you. |
| `/figure-out-team` | Do the work of `/figure-out` with a team in a Slack channel or thread. |
| `/review-code` | Review a change for one quality dimension. Manifest gates use it. |
| `/review-writing` | Review text against its style standards. |
| `/design` | Get design direction for a page, app, document or other visual work. |
| `/review-design` | Review a design in the medium that it is for. |
| `/check-pr` | Find if a pull request is ready to merge. It does not merge. |
| `/manifest-dev-help` | Read this guide, or ask it a question. |

This guide writes each skill as `/name`. Your host can use a different prefix, for example `$name`
or `/skill:name`.

## How the parts relate

- A Manifest has one or more Deliverables. Each Deliverable has one or more Acceptance Criteria.
- Global Invariants apply to all Deliverables. Process Guidance is advice and does not bind.
- Each Acceptance Criterion and Global Invariant is one gate. A gate is a Judgment Gate or a
  Deterministic Gate.
- `/do` makes each gate pass with evidence. When a gate fails, `/do` repairs the work and examines
  the gate again.
- A project keeps a North Star, a glossary and decision records. It can also keep a verification
  harness. `/setup-project` installs them, and normal runs keep them current.
- A verification harness has one Recipe for each feature, skill, document walk or eval suite.
  It also has one Recipe for the checks on all of the project, such as lint and tests.
  `/do` runs the recipes that a change touches. A project can opt out of the harness and keep its own
  checks. Then `/do` uses those checks.
- A Ticket holds one unit of work. `/ticket-up` writes it, `/next-ticket` selects it, and
  `/run-ticket` does it. `/orchestrate` runs many Tickets and lands them.
- When a run corrects a mistake, it adds a Lock. What it finds and cannot fix in its pull request is Debt. The next
  run that changes that code offers to fix the Debt.

## Why it works this way

- "Done" is written before the work starts. An agent cannot examine a result against a target that
  does not exist.
- A gate passes only with evidence. A summary that says "done" can be wrong.
- `/do` works as if you are away, so that it can finish without you. It reports each decision that
  it took for you.
- Each correction becomes a check, so that the same mistake does not occur again.
- The direction, the words and the decisions are in the repository. Each new session starts from
  them, not from zero.
- A costly check asks first, and a free check runs often. Run time alone is not a cost.
- Each level works alone. Thus you can start inside a team that does not use manifest-dev.

## Good practice

- Start with `/figure-out` on a real problem. Let it read the code before it asks you questions.
- Read the gates of the Manifest before `/do` starts. The gates are the contract.
- Let `/do` find and repair small problems. Do not stop it for them.
- Send a change of direction as a message to `/do`, so that it goes into the Manifest. Do not
  change the code yourself during the run.
- Trust evidence, not a summary.
- Agree to a costly check before it runs. A recipe with the ask-first mark costs money, quota or
  load on shared systems.
- Run `/setup-project` one time to install the Project Surfaces.
- Make each correction a check, so that the same mistake fails for each later person.
- Read the "Debt left" section of each pull request. Fix the Debt when your next change touches that code.
- Expect more tokens and more work at the start. In return, you get a result that you can
  examine, not only trust.
