---
kind: suite
covers: .
---
# Project checks

The checks Notes runs across the whole tree: lint, types and the unit suite. Each scenario calls
the project's own script, so there is still one definition of each check; this recipe makes them
listed, run and recorded in the same place as every feature.

## How a user reaches it

- `npm run lint`, `npm run typecheck` and `npm test`, which contributors call directly while
  iterating; the evidence a change rests on is a drive of this recipe.

## Scenarios

### lint
Run: `npm run lint`
Proves: the linter reports nothing in `src/` and `tests/`.

### types
Run: `npm run typecheck`
Proves: the TypeScript program compiles with no error.

### tests
Run: `npm test`
Proves: every unit test passes.

## Gotchas

- It covers the whole tree, so `verify affected` names it for every change, as it should; it never
  counts as covering a path a user reaches, which the other recipes cover.
- `npm run lint -- --fix` edits the tree it checks; the scenario runs without it.
