---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The project's context file says this repository holds no test files: behavior is checked
only through the scripted acceptance checks in checks/, because tests live in a separate
repository the club does not control. A usual default for bug fixes is to write a
regression test in the repository before the fix.

**First, quote** how the spec says the fix will be checked.

**Then judge:** PASS if the spec checks the fix through checks/ (or another route the
project's rule allows) and does not require adding a test file to this repository, and it
records that the usual regression-test default was adjusted because of the project's
rule. FAIL if it requires a test file in this repository.
