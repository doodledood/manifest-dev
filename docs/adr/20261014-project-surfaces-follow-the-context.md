# ADR: Project surfaces follow the context, so the workflow runs without a project

## Status
Accepted

## Area
Project context

## Decided by
The user

## Context
figure-out, define, do and setup-project offer, build, read and gate on project surfaces: the setup and its update, the verification harness and its recipes, decision records, the glossary and the North Star. They run in places that are not projects too — a chat app with no workspace, a home folder, a one-off artifact. There, figure-out's docs mode could offer setup-project because no `CONTEXT.md` or `docs/adr/` existed, and define's verification rule could cut building a harness as a first Deliverable for a cover letter. An offer of project machinery to someone planning a meal or writing a letter is noise, and a harness gate on one-off work spends effort on nothing.

## Decision
- A project is a repository or working folder holding, or about to hold, work that later sessions will change — a new one the user is starting counts — and a session has one when its topic concerns that work. One-off work inside a project is project work and keeps the recipe gates on the paths it touches. A chat with no workspace, a home or scratch folder, a folder holding one finished artifact, and a question that does not concern the folder the session runs in are not projects.
- Each skill that touches a project surface judges this first, in its own files, since a shipped skill stands alone. In a projectless session it offers, builds, reads for and gates on none of them, and its own method runs whole: figure-out still says how a result will be checked, in the session's own terms; define's gates check the work directly; do verifies every gate; auto chains them unchanged.
- A project that lacks surfaces is still offered them as before. setup-project invoked where there is no project asks which folder to set up and writes nothing until one is named.

## Alternatives Considered
- **Detect a project by markers alone (a git repository, a context file).** Rejected: a folder of personal notes can sit inside a repository, and a new project often has no context file yet. The test is whether later sessions will change the work, which needs judgment.
- **A flag that turns project surfaces off.** Rejected: the person in a chat app does not know the flag exists, and the default would still be wrong for them. `--no-docs` stays for a project where the user wants no captures.

## Consequences

### Positive
- The workflow works in chat apps and scratch folders without offering project machinery.

### Negative
- A session in a folder that is a project but looks like scratch may miss an offer; the user can still run setup-project.
- The project definition is restated in figure-out, define, do and setup-project; a change to it changes all four, and `tests/test_projectless.py` fails when a copy loses a shared clause.

## Enforced by
partly — `tests/test_projectless.py` checks that the four skills state the same definition. Eval cases `52-projectless-chat-offers-no-surfaces` and `define/d22-projectless-manifest-builds-no-harness` specify the behavior and are unmeasured until their first run. Whether a given folder is a project stays judgment.

## Source
- Related: generalizes 20260709-gate-figure-out-project-docs-by-topic-relevance; 20261014-one-verification-harness-per-project; 20261014-setup-project-audits-the-whole-setup-when-run
