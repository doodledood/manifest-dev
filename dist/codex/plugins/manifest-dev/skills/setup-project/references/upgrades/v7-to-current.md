# Upgrading a project from v7: what v8 gives it

A project recording v7 keeps its North Star in nine fields, and those fields let chosen options in:
a price, a channel, a launch plan, a number to reach by a date. v8 keeps in the North Star only
what decisions are judged against — what the project is for and whom it serves, how it tells
progress, the principles it holds against evidence, and the bets it rests on — and moves each
chosen option to a decision record, where a later session meets it as a choice it may revisit
rather than as the purpose. A project with no `NORTH_STAR.md` gets item 1 only.

Offer each item on its own. Items 1 to 3 go first, since the reshape in item 4 writes records
under the conventions item 1 changes:

1. **The `Strategy` area in the ADR conventions** — the paragraph that follows the *Area*
   paragraph in `../../../figure-out/references/ADR_FORMAT.md`, added at the same place in the
   project's conventions file: a record of a guiding choice carries the area `Strategy`, and the
   North Star's *Strategy choices in force* list holds the titles of those records in effect, so
   writing, superseding or retiring one rebuilds the list in the same act.
2. **The North Star conventions** — where the project keeps a North Star conventions file, the
   spans its v7 copy lacks, offered section by section per *Compare, then offer* in
   `../../SKILL.md`: the opening that says the document holds what decisions are judged against,
   *What a line may be*, *The sections*, *What it anchors*, the one-line provenance note, the
   skeleton, and *Produce it honestly*.
3. **The North Star line of the project-surfaces section** — its newest wording from
   `../NORTH_STAR_FORMAT.md` → *The project-surfaces section*, which names what the North Star
   holds and says the choices made along the way live in the decision records. Show it before and
   after.
4. **The North Star reshape** — the project's own `NORTH_STAR.md` moved into the six sections.
   This item changes positions, and only the owner moves a position, so it is never written
   without the owner's ruling on each line. A run with no person present to rule, such as an
   unattended one, flags the reshape as one item with the lines it would move, and changes nothing
   in the North Star, its records or their states.

   First sort every line of the current document — each position, each list entry, and each
   provenance note — by the test in `../NORTH_STAR_FORMAT.md` → *What a line may be*: an end, a
   measure, a principle or a bet stays; a line the owner would re-tune when evidence moves is a
   chosen option; a value a measure should reach by a date is a dated target; and the part of a
   provenance note that tells how a position came to read as it does is history. A line that names
   one example, setting, number, channel or path is nearly always a choice, however long it has
   stood.

   Then propose a destination for each line:

   | Line | Goes to |
   |---|---|
   | An end | *Purpose* (the problem, then *For* and *Not for*) or *Goal* |
   | A measure | *How we know*, one per part of the goal, with its direction and any floor |
   | A principle | *Principles*, phrased as what it rules out |
   | A bet | *What this rests on*, the main bet first |
   | A chosen option | the decision record that already holds it, named; otherwise a new record under the project's conventions, with the area `Strategy` where other decisions derive from it |
   | A dated target | the destination of the effort pursuing it, where the project keeps a Ticket store; otherwise the decision record that holds the choice it serves |
   | History | cut; the note keeps its state, its date and the titles of the records behind it |

   The nine fields map to the six sections like this, line by line rather than field by field:
   *Diagnosis* gives *Purpose* its problem and *What this rests on* its main bet; *Who it's for*
   becomes *Purpose*'s *For* and *Not for*; *Promise* becomes *Goal*; *Winning, and the number
   watched* gives *Goal* what reaching it means for the project and *How we know* its measure;
   *How they arrive* and *Money — or what it feeds* give *Principles* what the owner holds against
   evidence, and the rest is chosen options; *Never* becomes *Principles*; *What this rests on* and
   *Open* keep their names.

   Show the proposed document beside the current one, with a table of every line that leaves it
   and where it goes. The owner rules each line — keep, move, reword or drop — and only what the
   owner ruled is written. A position keeps its text unless the owner rewords it, and no state
   rises in the move. Write the result as one act under the project's conventions: the reshaped
   document; a record for each chosen option that has none; the area `Strategy` on each record
   that holds a guiding choice; the *Strategy choices in force* list rebuilt from those records;
   one decision record of the reshape itself, naming each line that moved and where; and the index
   rebuilt.
