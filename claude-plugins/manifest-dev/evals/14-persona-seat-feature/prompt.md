---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 12
---
use the figure-out skill for this. i'm afk, dont ask me anything - work it out and come back with what you land on.

we're adding a CSV export of the missing-ingredients list to Pantry. figure out what the export
needs - the columns, the file naming, where the file lands, and how it gets triggered from the
recipe screen. i want to hand this straight to define.

what exists today:

- recipes are stored with structured ingredient lines (`name`, `quantity`, `unit`, `note`).
- on a recipe screen the cook can tick each ingredient as "have" or leave it unticked; unticked
  is treated as missing. ticks are remembered per ingredient name across recipes.
- there is no shopping list feature yet and no integration with any list or grocery app.
- the app is phone-only. there is no web or desktop client.

the project's north star, so you have it:

```
## Who it's for
Home cooks with no technical background, cooking weeknight dinners for a family, usually with
the phone propped on the counter and one hand free, often already mid-recipe when they discover
something is missing. Not for: professional kitchens, meal-prep optimizers, or people who enjoy
configuring apps.
— hypothesis 2026-09

## Promise
Open the app mid-recipe and know in one glance what you have and what you're missing.
— hypothesis 2026-09

## Never
- Ask the cook to set up anything before they can cook.
— ruled 2026-09
```

(write any notes or logs you keep into the current directory rather than your home directory)
