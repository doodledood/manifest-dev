---
tags: [figure-out-plugin-only]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
append_system_prompt: |
  The user's preference file (./preferences.md, loaded in this session) contains:

  ## Taste

  - When naming files and folders, prefer dates in YYYY-MM-DD form — they sort correctly everywhere; yield when a tool requires its own format.
---
use the figure-out skill for this.

[earlier in this conversation]

me: why do our shop's order confirmation pages load so slowly on mobile?

you: Leading read, the HERO-BLOAT pattern: the confirmation page loads the full product carousel bundle (1.4 MB) though it shows no carousel. Rival: the SLOW-TAG path, a third-party tag that blocks rendering. Next probe: the page's network waterfall on a throttled phone.

me: stop using those made-up labels in your messages. just say what you mean. anyway the waterfall shows the carousel bundle is 70% of the load time, so go with that.

you: Understood. The confirmation page loads the product carousel's JavaScript, about 1.4 MB, even though it shows no carousel. The waterfall confirms it is about 70% of the load time. The fix is to stop loading that bundle on the confirmation page.

---

great, thats all i needed
