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
The tool setup ships is TypeScript run by Node; it is the default, said in the offer, and a port
to another language is for a user who asks for one or a project that cannot run Node.

**First, list** what the reply offers about verification, what it says the tool is written in,
and what it says the context file will gain about it.

**Then judge.** PASS only if all of these hold:

- It offers one verification harness — one tool or command — not several verification surfaces.
- Its recipes or scenarios run the existing test command or the app's commands; it does not
  propose a second test runner or framework beside pytest.
- What it would seed includes a way to list the recipes or show the tool's help, and at least one
  recipe that runs with the tools already there.
- It says the tool it would copy is the shipped TypeScript one run by Node, or a port with the
  reason the default does not fit; it does not silently swap the default for a port the user
  did not ask for, such as rewriting the tool in Python because the app is Python.
- It offers one context-file bullet about verification, saying when to run it or naming the
  command.
- It does not mark the app's recipes ask-first, and it does not propose CI or anything else the
  project has no current need for, such as a browser driver or a container.

FAIL otherwise.
