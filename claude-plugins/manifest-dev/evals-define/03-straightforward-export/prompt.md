---
max_turns: 20
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write]
model: opus
runs: 3
---
Use the define skill for this. Shared understanding is settled below; this is contract
encoding, not implementation. Keep any files in the current directory. After your digest, reproduce any Manifest you write **verbatim** in your final
message, including all gate bodies. If an owner decision blocks completion, show the
unresolved decision and keep the contract visibly pending. This lets me review the
actual contract rather than a summary or path.

We have settled the feature: on the existing recipe screen, add Export missing ingredients.
It downloads a UTF-8 CSV with the columns name, quantity, unit in that order; one row per
unticked ingredient, preserving recipe order. Quote commas, quotes, and newlines correctly.
Use the existing ingredient data and download helper. The screen already stores the ticked
state; change neither that storage nor the recipe model. Empty lists export the header only.
The recipe owner confirmed the existing button style. No shopping-list feature or integrations.

The pain is retyping missing ingredients into a spreadsheet. The appetite is one small
export path. The existing project gates are its unit tests and lint, both executable locally.
No consequential choice is left open; I authorize this contract and am AFK. Write a complete
Manifest for execution, retaining all agreed behavior and bounds. Do not implement it.
