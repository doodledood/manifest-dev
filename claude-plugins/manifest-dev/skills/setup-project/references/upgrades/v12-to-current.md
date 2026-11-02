# Upgrading a project from v12: what v13 gives it

v13 adds one item, and changes no file setup-project emitted into the project. Offer it once, as a
default the user may decline. `--no-mine`, or a project with no history to read, skips it, and that
counts as its answer.

1. **Taste from the project's history** — the candidates `../MINING.md` → *Taste* describes,
   drawn and ratified as it says. Where a memory file the project keeps already holds a
   `## Taste` section, say so and offer only candidates its entries do not already state.

   Done when the user has accepted, changed or declined each candidate. A run with no candidate
   to put forward says so and which sources it read. With no user to ask, report the candidates
   and write nothing: the item has no answer yet.

Record the newest surfaces version only once the item has an answer, as the setup skill
specifies. Whatever the answer, a project that records v13 is not offered this item again.
