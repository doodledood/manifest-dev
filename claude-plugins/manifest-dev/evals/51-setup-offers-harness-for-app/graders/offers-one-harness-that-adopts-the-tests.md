---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The project is a small command-line app (`src/shelfnote.py`, commands checkout, return, overdue,
export) with a test suite run by `python3 -m pytest tests/`, and no project surfaces. A
verification harness is one command-line tool reading one recipe per thing it checks; a setup
should adopt what already checks the project rather than add a second runner, and should not
mark a recipe ask-first when running it costs nothing — running a local CLI or its tests is free.

**First, list** what the reply offers about verification, and what it says the context file
will gain about it.

**Then judge.** PASS only if all of these hold:

- It offers one verification harness — one tool or command — not several verification surfaces.
- Its recipes or scenarios run the existing test command or the app's commands; it does not
  propose a second test runner or framework beside pytest.
- What it would seed includes a way to list the recipes or show the tool's help, and at least one
  recipe that runs with the tools already there.
- It offers one context-file bullet about verification, saying when to run it or naming the
  command.
- It does not mark the app's recipes ask-first, and it does not propose CI or anything else the
  project has no current need for, such as a browser driver or a container.

FAIL otherwise.
