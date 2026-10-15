# Upgrading a project from v1 to v5

A project recording v1 may carry a verification surface in the v1 form (a harness with its
feature map, an eval suite or a reader-task list, with a README, statuses and a repository
check). Of what v2 and v3 added, only the ADR conventions change lasts; the feature-map shape v2
introduced and the bullet wording v3 changed are both replaced by v4, so never offer them. The harness arrives in its v5 shape. A v1
feature map is part of the surface the move below carries into recipes.

Offer, each as its own item and as a default the project may adapt or decline where its own way
already does the job. The harness is recommended, but the project may opt out of it whole and keep its own way of
verifying: then offer none of the harness items, and offer instead the own-way form of the
verification bullet from `../NORTH_STAR_FORMAT.md` → *The project-surfaces section*, naming its
commands and steps, so no later run builds or offers a harness:

1. **The ADR conventions' records-in-effect rule** (from v2), by comparison per the update pass:
   only an `Accepted` record is in effect, and backfilling `Enforced by`, building a `not yet`
   check, and citing a record as a ruling read only records in effect.
2. **The harness**, per `MOVE_TO_HARNESS.md` beside this file: the tool, `harness.md`, a recipe
   for each entry the v1 surface carries with its content and evidence, the `ask-first` marks,
   and the removal of the old surface, its README and its repository check — except an eval suite,
   which stays as it is. Where the project has
   no surface and holds something future runs will change, recommend a new harness seeded per
   `../VERIFICATION_HARNESS.md` → *What setup creates, and what runs build* instead; its
   ask-first choice and bullet are the items below.
3. **The ask-first setting** — `ask` by default, or `run`.
4. **Control commands**, per `../VERIFICATION_HARNESS.md` → *The parts*: `start`, `running`,
   `logs`, `reset` and `stop` declared in `harness.md` where the project's existing scripts already
   start, observe or stop what it runs, each on the run's `VERIFY_RUN_ID`; none where the project
   runs nothing.
5. **The context-file bullet** — the one verification bullet replacing the verification-surface
   bullet v1 carried.

Once every item has an answer, record v5.
