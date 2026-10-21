# Surfaces versions

A project's context file records the surfaces version it carries in its project-surfaces section.
Each version below has one line here and a file in `changes/` listing what it gives a project set
up at an earlier version. The last line is the newest version. An update reads only the files for
versions after the one the project records, and offers them as the upgrade guides in `upgrades/`
from that version on say; it records the newest version once the user has answered.

- v1 — `changes/v1.md`: decision records name the check that enforces them; a verification surface per artifact.
- v2 — `changes/v2.md`: setup audits the whole setup; surfaces judged fit to trust by their jobs; a fixed feature-map shape.
- v3 — `changes/v3.md`: the feature-map entry says where its commands live and that a changed feature's entry is updated and driven.
- v4 — `changes/v4.md`: one verification harness of recipes replaces the surface, map and reader tasks.
- v5 — `changes/v5.md`: the harness is optional, controls what it checks, holds run time against creep, and reads as a default shape.
- v6 — `changes/v6.md`: every check a harness project keeps is a recipe, the checks run across the whole tree included, and the evidence a change rests on comes through the harness.
- v7 — `changes/v7.md`: the harness commits no evidence and keeps no status, and each timed scenario's line lives in its recipe.
- v8 — `changes/v8.md`: the North Star holds only what decisions are judged against, in six sections; chosen options move to `Strategy` decision records on the owner's ruling.
