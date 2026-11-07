---
name: audit-state-machines
description: 'Find every implicit and explicit state machine in a codebase, model each one formally, and report every bug the model shows and the code confirms — a bad state that can be reached, a forbidden transition, a state with no way out — with its fix and an offer to turn the findings into Tickets. Changes no code. Use when the user asks to audit state machines, find implicit state machines, check status or lifecycle logic across an app, or find bugs that span several files.'
argument-hint: '[path or area] [--no-log]'
user-invocable: true
---

Audit a codebase for state-machine bugs. A state machine is a value whose changes follow a lifecycle — a status, or flags whose combinations act as states — and `../review-code/references/code-bugs.md` → *State machines* says how to find one, rebuild it, check it and confirm what the check finds. figure-out runs the audit with its whole investigation discipline; this skill adds the brief below and the offer at the end.

Invoke the figure-out skill with the brief below, the person's arguments, `--autonomous` and `--no-docs`. `--no-docs` keeps figure-out's project-document writes out of the audited project; forward `--no-log` when given. With no path or area, the scope is the whole repository. With no codebase in reach, say so and stop.

Brief:

> Audit [the scope] for state machines, implicit and explicit, following `../review-code/references/code-bugs.md` → *State machines*. Every bug you find counts, whether or not anything changed recently: this is an audit, not a review of a change. Machines written as instructions count too, checked as that section says.
>
> - List every machine in the scope searched: what it tracks, explicit or implicit, its states, and its writers by file and line. Say which parts of the scope you searched and which you did not, with why. On a large repository, record each machine in your log as you finish it.
> - Rank confirmed bugs by consequence. For each, give each site by file and line, the sequence that reaches the bad state, and the model that found it — its saved path, or its scratch path when no log is kept. For a bug in an implicit machine, the fix is to make the machine explicit: one owner of its transitions, and a test or a type that fails when anything else writes the state.
> - After the bugs, ranked lower: each implicit machine with no bug but writers in several files, with the recommendation to make it explicit. An implicit machine kept inside one function gets no recommendation.
> - For a machine whose model found nothing, say what the model covered; never call the machine correct.
> - Write no file in the audited project. Models and scripts stay outside it.

When figure-out returns its read, give the person the read and offer to turn the confirmed bugs and the make-explicit recommendations into Tickets — self-contained work items in the project's tracker or files — recorded as debt, the issues found and not yet fixed. On their yes, invoke the ticket-up skill with those findings. With no person to answer, as when another workflow runs this skill, list the offer in the result and invoke ticket-up only where that caller's assignment authorizes writing Tickets.
