# Surfaces versions

A project's context file records the surfaces version it carries in its project-surfaces section.
Each version below has one line here and a file in `changes/` listing what it gives a project set
up at an earlier version. The last line is the newest version. An update reads only the files for
versions after the one the project records, and offers them as the upgrade guide for that version
in `upgrades/` says; it records the newest version once the user has answered.

- v1 — `changes/v1.md`: decision records name the check that enforces them; a verification surface per artifact.
- v2 — `changes/v2.md`: setup audits the whole setup; surfaces judged fit to trust by their jobs; a fixed feature-map shape.
- v3 — `changes/v3.md`: the feature-map entry says where its commands live and that a changed feature's entry is updated and driven.
- v4 — `changes/v4.md`: one verification harness of recipes replaces the surface, map and reader tasks.
- v5 — `changes/v5.md`: the harness controls what it checks, holds run time against creep, and reads as a default shape.
