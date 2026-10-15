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

At the higher levels of the autonomy ladder, the project advances alone. It takes its next work from
its queue, and it asks you only for a judgment, a taste or an authority.

manifest-dev is for developers who want results that they can trust. They agree to spend more tokens
and more work at the start to get them. They can work alone or in a team of any size, also in a
codebase where their colleagues do not use manifest-dev. It is not for a person who wants only the
fastest or the cheapest result.

| Question | Where the answer is | How long it stays |
|---|---|---|
| What is this project for? | The North Star, a file in the project | Until the owner changes it |
| What is the next work? | A Ticket, in your tracker or in files | Until that work is done |
| What does "done" mean for this work? | A Manifest, written for each run | For one run |

## The workflow

1. Use `/figure-out <topic>` to understand the problem before you change something.
2. Use `/define` to write a Manifest: what you will accept as done.
3. Use `/do <manifest-path>` to do the work and show evidence for each gate.

`/auto` does the three steps without a stop between them. Each skill also works alone. `/define`
starts `/figure-out` first when you and the agent do not yet agree on the problem.

`/do` works as if you are away. It makes decisions without questions and reports them at the end. A
message that you send during `/do` changes the Manifest, and the run continues. It stops only when
each gate has evidence, or when a person must act.

## The autonomy ladder

You can use manifest-dev at five levels. Each level works without the levels above it. Other people
on your team do not have to use any level. Stop at the level that fits your project.

| Level | What you do | What you get | What it costs |
|---|---|---|---|
| 1. One skill | Use one skill alone, for example `/figure-out` on a question. | A better answer or review, with no setup. | Nothing in the project. |
| 2. One piece of work | Use `/figure-out`, `/define` and `/do`, or `/auto`. | A result with evidence for each gate. | More tokens and time at the start. The Manifest and its log stay outside the repository. |
| 3. Project Surfaces | Use `/setup-project` one time. | Each session starts from the direction, words, decisions and checks of the project. | Files in the repository that your team can see. |
| 4. A shared queue | Write work with `/ticket-up` and take it with `/next-ticket`. | The next work is in a store, not in the head of one person. | A Ticket Store: GitHub Issues, files or your own tracker. |
| 5. Unattended runs | Grant Auto on Tickets, and start `/run-ticket` or `/sweep-tickets` from a schedule or an orchestrator. | The project advances without you. You act only for a blocker, a judgment, a taste or an authority. | A scheduler or orchestrator that you install, and gates that you trust. |

To climb a level:

1. Use your current level until you trust its results.
2. Add the next level where the current level does not give enough.
3. Grant Auto only when the work and its "done" need no judgment, taste or authority of a person.

## The other skills

| Skill | Use it to |
|---|---|
| `/setup-project` | Give a project its North Star, glossary, decision-record conventions and verification harness. Run it again to find gaps. |
| `/ticket-up` | Write work into your Ticket Store as Tickets. |
| `/next-ticket` | Select the next Ticket, claim it, and see why it is first. |
| `/run-ticket` | Do one Ticket from start to end and record the result on it. |
| `/sweep-tickets` | Start or continue one unattended Ticket from a schedule. |
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
- A project keeps a North Star, a glossary, decision records and a verification harness.
  `/setup-project` installs them, and normal runs keep them current.
- The verification harness has one Recipe for each feature, skill, document walk or eval suite.
  `/do` runs the recipes that a change touches.
- A Ticket holds one unit of work. `/ticket-up` writes it, `/next-ticket` selects it, and
  `/run-ticket` does it.
- When a run corrects a mistake, it adds a Lock. What it finds and does not fix is Debt. The next
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
- Trust evidence, not a summary. A gate passes only with evidence.
- Agree to a costly check before it runs. A recipe with the ask-first mark costs money, quota or
  load on shared systems.
- Run `/setup-project` one time to install the Project Surfaces. Normal runs keep them current,
  and a new run of `/setup-project` finds the gaps.
- Make each correction a check, so that the same mistake fails for each later person.
- Read the "Debt left" section of each pull request. Fix the Debt when your next change touches that code.
- Expect more tokens and more work at the start. In return, you get a result that you can
  examine, not only trust.
