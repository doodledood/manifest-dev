---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 6
---
use the define skill for this.

rename the `getUsr` function to `getUser` across our frontend package — it's a typo from years
ago and it bugs everyone. about 30 call sites, all in `packages/web`. no behavior change. the
package has a typecheck and a test suite.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
