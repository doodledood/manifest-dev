---
type: llm
focus: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The change touches the overdue page. Its recipe in the project's verification harness cannot be
relied on as it stands: a person has to start the page by hand on fixed port 8000, so two runs at
once collide, and its one recorded run failed with nothing kept that says why.

**First, list** the Manifest's Deliverables in order. For each, say whether it makes the overdue
page startable, observable and stoppable through the harness for each run on its own (declared
control commands, a per-run port or data directory), or makes a failed run keep what locates the
cause (the page's log).

**Then judge.** PASS if a Deliverable doing at least one of those comes before the Deliverable that
adds the days-overdue column, and a gate holds that repair. FAIL if the repair comes after the
feature, lives only in an assumption, note or process guidance, or is absent.
