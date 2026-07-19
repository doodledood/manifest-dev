# figure-out: taste capture

In an autonomous or otherwise unattended run — no counterparty in the loop to ratify — taste capture is fully inert: no offers, no writes. Ratified entries already present in loaded memory files still inform the work — inertness is about capture, not use.

Taste is a durable personal steering preference persisted only by offer-and-ratify: the agent drafts, the user's explicit yes writes. Never infer a preference and store or apply it silently — an unratified behavioral prior can only be obeyed, not weighed, and it self-seals: once the agent preempts the preference, the pushback that would test or correct it stops occurring. Ratification is what converts an observed pattern into standing context.

## Detection gate

Watch for directional preferences the user steers by, not one-off situational calls. A candidate earns an offer when it is all three:

- **Directional** — it would steer future judgment calls the same way ("prefer the smallest clean change", "prose over tables"), not a fact about this task.
- **Durable** — recurring across the session, or explicitly stated as a standing way of working; a single situational correction is not taste.
- **Behavior-changing** — a future session that knew it would act differently; if the model already behaves this way unprompted, there is nothing to write.

**Per-turn:** when the signal is unmistakable — the same pushback has recurred, or the user states a standing preference in so many words — offer immediately, while the instance is concrete. **Session-end sweep:** before the session closes (for figure-out, before naming the read), review for candidates that accumulated without individually clearing the per-turn bar; batch any that now clear the gate into one offer. Anything below the gate: keep working, don't offer.

## Drafting (boundary form)

A taste entry is a prompt line that will ride in every future session, so draft it as one: invoke the prompt-engineering skill if it is available; otherwise apply its core discipline inline — keep only what closes a real gap in natural model behavior, and check the line holds at the edges. Boundary form is required:

- **Preference** — the lean, stated plainly.
- **Rationale** — why, so future sessions can weigh it rather than obey it.
- **Flip condition** — when it should yield, so it doesn't over-fire on adjacent cases.

Example: `Prefer the smallest change that stays clean; go bigger only when the small version leaves debt costlier than the restructure.` A bare preference ("keep changes small") over-fires on the cases where bigger is right; a hedge-wrapped one ("consider smaller changes where appropriate") under-fires into noise. The rationale and flip condition are the calibration.

## Scope and write target

Classify before offering:

- **User-level** — how this user likes things everywhere → the harness's user-level memory file (for Claude Code, `~/.claude/CLAUDE.md`; on other harnesses, the AGENTS.md-style user-level equivalent).
- **Project-level** — how this project does things, binding on anyone working in it → the project's memory file.

When scope is ambiguous, the offer asks: *"save this for you everywhere, or as a rule of this project?"*

Write into a marked `## Taste` section of the target file, creating the section if absent. The rest of the file is untouchable: never modify content outside the section. Within the section, ratified revisions and merges are allowed (see curation).

## The offer

Name the observed pattern, show the drafted entry verbatim, name the scope. Only the user's explicit yes writes; silence, deflection, or a topic change is a no. Don't re-offer a declined candidate in the same session.

## Curation — the section is a prompt

The section stays healthy the way any prompt does — every line earns its place — not by a numeric cap:

- **Coverage check before append** — if an existing entry already covers or nearly covers the candidate, offer to sharpen or generalize that entry instead of adding a sibling. Entries stay orthogonal.
- **Displacement on entry** — if a new entry makes an existing one redundant, the same offer proposes the merge or retirement.
- **Clash-driven re-ratification** — when the user's live steering contradicts a stored entry, surface the clash instead of silently obeying either the file or the moment: *"Your taste entry says X; you're steering Y here — has the default moved, or is this an exception?"* Their answer re-ratifies, revises, or removes the entry — or confirms the case sits inside the flip condition, changing nothing.

Every curation change is ratified like a new entry — the agent never rewrites the section on its own judgment.
