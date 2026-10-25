/manifest-dev-tools:prompt-engineering update this skill so it also writes a one-line summary at the top of every release note. Return the whole updated SKILL.md.

```markdown
---
name: release-notes
description: 'Draft release notes from merged pull requests. Use when preparing a release.'
---

Draft release notes for the next release from the pull requests merged since the last tag.

Group the changes under Added, Changed and Fixed. Previously this skill used a single flat list;
it now groups by type.

Write each entry as one line in the past tense, naming the user-visible effect rather than the
code change. (Per the maintainer, 2026-09-14: entries say what users notice, not what files moved.)

Skip pull requests labelled `internal`.

Keep the notes short where you can, and try to make them easy to skim if possible.

Write each entry as one line naming the user-visible effect.

Link each entry to its pull request.
```
