# Upgrading a project from v8: what v9 gives it

A project recording v8 keeps its North Star in six sections, and its *Purpose* opens with what is
in the way. Written from a README, that is usually the barrier the project's first feature removes,
so the purpose is only as wide as the first means and later work sits outside it. v9 opens the
*Purpose* with the end the person is after and tests the *Goal* and its measures against that end.
It also gives decision records a signpost — a `Revisit when` field the strategy list shows — and
offers a check that rebuilds the index and the list. A project with no `NORTH_STAR.md` gets items
1 and 3 only.

Offer each item on its own. Items 1 to 3 go first, because items 4 and 5 write under the
conventions items 1 and 2 change:

1. **The ADR conventions** — the spans of `../../../figure-out/references/ADR_FORMAT.md` the
   project's copy lacks, offered section by section per *Compare, then offer* in `../../SKILL.md`:
   the `Revisit when` section of the template and the paragraph explaining it; `Revisit when`
   among the fields editable in place; the *Strategy* paragraph's list derived with signposts; the
   one-act write rebuilding that list, signposts included; and the paragraph on *Context*: where a
   decision's subject sits outside what the North Star's *Purpose* names, the record says so in
   one line.
2. **The North Star conventions** — where the project keeps a North Star conventions file, the
   spans its v8 copy lacks, offered the same way: the *Purpose*, *Goal* and *How we know* rows,
   the rebuild rule for *Strategy choices in force*, the skeleton's lines for those sections, and
   the paragraph of *Produce it honestly* that asks for the end.
3. **The index-and-list check** — where the project keeps automated checks and nothing rebuilds
   its index or strategy list yet, the check `../../SKILL.md` step 2 describes, in the project's
   own test form or as a harness scenario.
4. **The end of the North Star** — ask the owner, in their own words, what the person the project
   serves is after, and of each answer "why does that matter?", until there is no deeper answer.
   Compare that end with what the *Purpose* opens with now. Where the *Purpose* states a barrier
   rather than an end, propose a *Purpose* that opens with the end and keeps that barrier as one
   thing in its way. Then read the *Goal* and *How we know* against the end: where the goal is
   features written as outcomes and the measures count their use while nothing measures the end,
   propose the end's own measure, `empty` with what would fill it where nothing counts it yet.
   Show each proposed line beside the current one; the owner rules each, and only what the owner
   ruled is written, with a decision record remembering why it moved. A run with no person present
   to rule flags this item in its report, names the lines it would propose, and writes nothing.
5. **Signposts on the strategy choices** — for each `Strategy` record in effect, ask the owner
   whether an observable condition would reopen it, and where it is read; write a `Revisit when`
   only from the owner's answer, never one inferred, then rebuild the list. A run with no person
   present flags the records that carry none and writes nothing.
