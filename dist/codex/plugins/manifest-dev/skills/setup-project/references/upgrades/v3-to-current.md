# Upgrading a project from v3 to v5

A project recording v3 gains v4's change — one verification harness replaces the verification
surface, the feature map and the reader-task list — in v5's shape, with its control commands.

Offer, each as its own item and as a default the project may adapt or decline where its own way
already does the job. The project may also decline the harness whole and keep its own way of
verifying: then offer none of the harness items, and offer instead the own-way form of the
verification bullet from `../NORTH_STAR_FORMAT.md` → *The project-surfaces section*, naming its
commands and steps, so no later run builds or offers a harness:

1. **The harness**, per `MOVE_TO_HARNESS.md` beside this file: the tool, `harness.md`, a recipe
   for each feature-map entry and reader task with its content and evidence, the `ask-first`
   marks, and the removal of the old directories and their checks. Where the project has none of
   those pieces and holds something future runs will change, offer a new harness seeded per
   `../VERIFICATION_HARNESS.md` → *What setup creates, and what runs build* instead; its
   ask-first choice and bullet are the items below.
2. **The ask-first setting** — `ask` by default, or `run`.
3. **Control commands**, per `../VERIFICATION_HARNESS.md` → *The parts*: `start`, `running`,
   `logs`, `reset` and `stop` declared in `harness.md` where the project's existing scripts already
   start, observe or stop what it runs, each on the run's `VERIFY_RUN_ID`; none where the project
   runs nothing.
4. **The context-file bullet** — the one verification bullet replacing the verification-surface
   and feature-map bullets v3 carried.

Once every item has an answer, record v5.
