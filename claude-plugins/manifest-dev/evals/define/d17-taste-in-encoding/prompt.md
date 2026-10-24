---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
append_system_prompt: |
  The user's preference file (./preferences.md, loaded in this session) contains:

  ## Taste

  - For anything customers see, ship it behind a switch I can turn off without a deploy — a bad customer-facing change at 6am cannot wait for a release; yield for changes with no customer-visible effect.
  - Don't over-engineer — fewer gates and less ceremony; yield when money or customer data is at stake.
---
use the define skill for this.

our bakery's pre-order site is adding pickup slots: when you pre-order, you pick a 30-minute
pickup window instead of "any time after 7am". each window holds at most 20 orders. pre-orders
are paid online at checkout through our existing payment step, which this change has to touch to
attach the slot to the order. we'll also start emailing a reminder the evening before pickup with
the chosen window. some customers already hold pre-orders placed before this launch.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
