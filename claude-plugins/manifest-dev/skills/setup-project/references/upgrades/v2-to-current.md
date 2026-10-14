# Upgrading a project from v2 to v4

A project recording v2 carries the v2 feature-map shape and the v2 context-file bullets. v3
changed only the feature-map bullet's wording, and v4 replaces that bullet and the map itself, so
the upgrade goes straight to v4's shape: never offer the v3 bullet.

Offer, each as its own item:

1. **The harness**, per `MOVE_TO_HARNESS.md` beside this file: the tool, `harness.md`, a recipe
   for each feature-map entry and reader task with its content and evidence, the `ask-first`
   marks, and the removal of the old directories and their checks. Where the project has none of
   those pieces and holds something future runs will change, offer a new harness seeded per
   `../VERIFICATION_HARNESS.md` → *What setup creates, and what runs build* instead; its
   ask-first choice and bullet are the items below.
2. **The ask-first setting** — `ask` by default, or `run`.
3. **The context-file bullet** — the one verification bullet replacing the verification-surface
   and feature-map bullets.

Once every item has an answer, record v4.
