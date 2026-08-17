# figure-out: taste capture

With no counterparty in the loop to ratify — an unattended run — taste capture is fully inert: no offers, no writes. Ratified entries already present in loaded memory files still inform the work — inertness is about capture, not use.

Taste is a durable personal steering preference persisted only by offer-and-ratify: the agent drafts, the user's explicit yes writes. Never infer a preference and store or apply it silently — an unratified behavioral prior can only be obeyed, not weighed, and it self-seals: once the agent preempts the preference, the pushback that would test or correct it stops occurring. Ratification is what converts an observed pattern into standing context.

## Override: a ratified write is the action

The master frame in `SKILL.md` says answers and agreement feed exploration, not action — don't leap to the implied move, not the edit, not even the proposal. **A ratified taste write is an exception: it is the action of this capture, not deferred work.** The user's yes is the authorization; execute the write inline when it lands. Nothing here licenses acting on the *content* of the preference — only writing the entry.

## Detection gate

Watch for directional preferences the user steers by, not one-off situational calls. A candidate is eligible when it is all four:

- **Directional** — it would steer future judgment calls the same way ("prefer the smallest clean change", "prose over tables"), not a fact about this task.
- **Durable** — recurring within the session, or explicitly stated as a standing way of working; a single situational correction is not taste.
- **Behavior-changing** — a future session that knew it would act differently; if the model already behaves this way unprompted, there is nothing to write.
- **Personal** — you could want the opposite for some other user. Where the opposite would simply be the skill working badly, the behavior is owed by every session rather than preferred by this one, and capturing it here makes weighable what should be held and binds it to whoever happened to ratify it. Make no offer, and don't reach for the prompt either: name the gap as one the prompt itself should close, and leave it there.

Passing the gate makes a candidate eligible, not offered — an offer must also repay its interruption. When a preference is real but too minor for future sessions to meaningfully profit from, don't stop the session for it: let it ride the session-end sweep, where batching amortizes the cost, or leave it unoffered.

**Per-turn:** when the signal is unmistakable — the same pushback has recurred, or the user states a standing preference in so many words — and the entry is consequential enough to repay the interruption, offer immediately, while the instance is concrete. **Session-end sweep:** before the session closes (for figure-out, before naming the read), review for candidates that accumulated without individually clearing the per-turn bar; batch any that now clear the gate into one offer. Anything below the gate: keep working, don't offer.

## Drafting (boundary form)

A taste entry is a prompt line that will ride in every future session, so draft it as one: invoke the prompt-engineering skill if it is available; otherwise apply its core discipline inline — keep the line only where it carries something the model would not reach on its own, and check it holds at the edges. Boundary form is required:

- **Preference** — the lean, stated plainly.
- **Rationale** — why, so future sessions can weigh it rather than obey it.
- **Flip condition** — when it should yield, so it doesn't over-fire on adjacent cases.

Example: `Prefer the smallest change that stays clean — small diffs are cheaper to review, revert, and reason about; go bigger only when the small version leaves debt costlier than the restructure.` A bare preference ("keep changes small") over-fires on the cases where bigger is right; a hedge-wrapped one ("consider smaller changes where appropriate") under-fires into noise. The rationale and flip condition are the calibration.

## Scope and write target

Classify before offering:

- **User-level** — how this user likes things everywhere → the harness's user-level memory file (for Claude Code, `~/.claude/CLAUDE.md`; on other harnesses, the AGENTS.md-style user-level equivalent).
- **Project-level** — how this project does things, binding on anyone working in it → the project's memory file. Available only once the investigation is relevant to the active project or one of its mapped contexts, on the same relevance test that gates project docs — and never under `--no-docs`, where opting out of project documentation opts out of project-binding writes too. Absent that, the entry is user-level or it is not offered — an investigation that merely happened to run in a repo must not write a rule binding everyone who works in it.

When scope is ambiguous and project-level is available, the offer asks: *"save this for you everywhere, or as a rule of this project?"* Where project-level isn't available, offer user-level alone rather than a choice one branch of which cannot be honored.

Write into a marked `## Taste` section of the target file, creating the section if absent. The rest of the file is untouchable: never modify content outside the section. Within the section, ratified revisions and merges are allowed (see curation).

## The offer

Name the observed pattern, show the drafted entry verbatim, name the scope. Only the user's explicit yes writes; silence, deflection, or a topic change is a no. Don't re-offer a declined candidate in the same session.

## Curation — the section is a prompt

The section stays healthy the way any prompt does — every line earns its place — not by a numeric cap:

- **Coverage check before append** — if an existing entry already covers or nearly covers the candidate, offer to sharpen or generalize that entry instead of adding a sibling. Entries stay orthogonal.
- **Displacement on entry** — if a new entry makes an existing one redundant, the same offer proposes the merge or retirement.
- **Clash-driven re-ratification** — when the user's live steering contradicts a stored entry, surface the clash instead of silently obeying either the file or the moment: *"Your taste entry says X; you're steering Y here — has the default moved, or is this an exception?"* Their answer re-ratifies, revises, or removes the entry — or confirms the case sits inside the flip condition, changing nothing.

Every curation change is ratified like a new entry — the agent never rewrites the section on its own judgment.
