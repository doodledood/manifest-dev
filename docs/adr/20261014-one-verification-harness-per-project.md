# ADR: One verification harness per project — a self-describing CLI reading recipe files, with ask-first runs

## Status
Accepted

## Area
define / do

## Decided by
The user

## Context
20261013-runs-build-and-maintain-a-project-verification-surface gave each artifact a surface in its own form — a harness and feature map for a product, an eval suite for prompts, a reader-task list for documents — and 20261014-the-feature-map-is-a-navigation-contract-over-what-users-invoke added a feature map over anything users invoke. A project could then carry three verification concepts, each with its own folder, statuses kept by hand, test and context-file bullet. In this repository that was 25 map entries, 17 reader tasks, a drive script, two tests and two bullets, kept current across several review rounds; readers asked what the map's "commands" and reader tasks even were. An agent outside this workflow found no single place to learn how to check its work. Separately, some checks cost money, time or shared resources, and nothing told an agent which ones to ask about.

## Decision
- A project keeps one verification harness: a command-line tool whose `--help` tells anyone everything about verifying the project. Its subcommands — `list`, `help`, `drive` (with `walk` and `eval`), `judge`, `doctor`, `check` — are the contract; setup-project ships a working standard-library implementation projects copy and adapt.
- Every check is a recipe: a Markdown data file the tool reads, naming what it covers, how a user reaches it, scenarios (an exact command and what it proves), and traps. Features, skills, document walks and eval suites are all recipes; the feature map and the reader-task list stop being separate concepts.
- Recipes delegate to the project's existing commands, so there is still one way to check each thing. Eval suites stay a measurement; an eval recipe only starts them.
- Statuses are worked out from committed evidence and the git history of what a recipe covers, not kept by hand.
- A recipe whose run costs something a person should weigh — money or quota, long run time, shared environments, effects outside the repository — carries an `ask-first` mark with its reason. By default the tool refuses it without `--yes`, given when a person ran it or agreed; the user sets that default at setup and can change it. The mark follows cost, not kind: a local browser or CLI drive is free.
- The context file carries one verification bullet, written for any reader with or without this workflow: the command, when to run it, and to ask before ask-first recipes.
- setup-project upgrades an existing project by the surfaces version it records, through one guide per older version that goes straight to the newest, moving an existing surface, map and reader tasks into recipes with their content and evidence.

## Alternatives Considered
- **Keep the feature map as its own concept beside the harness**: two places to look and two things to keep current; the map's useful content — reach, drive steps, proof, traps — is exactly a recipe's.
- **A skill as the unit, the way pstack's verification skill holds its map and helper scripts**: works only on hosts that load skills, and an agent outside the workflow never finds it.
- **Recipes as code inside the tool**: stronger per-recipe checks, but harder for an agent to add one and nothing to read outside the code; the tool already turns a recipe's command and proof into evidence.
- **A form per artifact, as before**: three ways to verify, and a reader has to learn which applies first.
- **Marking only model-using runs**: misses the slow company-wide suite and the deploy; cost has more than one kind.

## Consequences

### Positive
- One command for every agent and person; nothing to learn from a README one hop away.
- Statuses cannot drift from evidence, and `verify check` holds recipe structure with the project's tests.
- Costly checks are visible and gated by default, without blocking free ones.

### Negative
- Every project carries a small Python tool, or writes its own to the same contract.
- Too many ask-first marks would stop agents verifying on their own; setup offers a cheap scoped variant beside a costly recipe to prevent that.
- Each new surfaces version updates every upgrade guide.

## Enforced by
partly — `tests/test_verify.py` holds this repository's harness: every recipe parses and names only existing paths, every user-invocable skill has a recipe, the shipped tool and this repository's copy are identical, ask-first recipes are refused without `--yes`, and statuses follow evidence. `tests/test_setup_project_versions.py` (`test_one_upgrade_guide_per_older_version_each_to_the_newest`, `test_latest_version_matches_what_setup_project_emits`) holds the guides and the shipped harness. Whether a recipe is marked when its run is costly stays judgment.

## Source
- Related: Supersedes 20261014-the-feature-map-is-a-navigation-contract-over-what-users-invoke; amends 20261013-runs-build-and-maintain-a-project-verification-surface
