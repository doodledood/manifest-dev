# Slack Message: Broader Engineering Channel

---

Hey all—

Sharing an approach that's helped me get better first-pass output from AI coding tools.

**The reframe:**

Stop asking "how do I get the AI to code this properly?"
Start asking "what would make me accept this PR?"

Modern LLMs are goal-oriented—they're good at satisfying stated criteria. The bottleneck isn't capability, it's clarity on what done looks like and how to verify it.

Instead of implementation instructions, define acceptance criteria. Then let the AI implement toward those criteria.

**The workflow:**

1. **Define** — AI interviews you, surfaces latent criteria you'd reject code for but wouldn't specify upfront
2. **Do** — AI implements, verifies against criteria, fixes failures—until every criterion passes

The verify-fix loop is automated. You define the bar; AI iterates until it clears.

**Why it helps:**

The define phase catches stuff you'd miss. The verification catches issues before you review. The approach works with the way LLMs actually work—they're goal-oriented from training, so giving clear success criteria plays to their strength.

**Tool-agnostic:**

The concept applies to any AI coding tool—Claude Code, Cursor, Copilot, etc. The workflow is what matters, not the specific tool.

**If you want to try it:**

I packaged it as a Claude Code plugin: https://github.com/doodledood/manifest-dev

Full writeup with worked example: aviramk.dev/scrolly/manifest-driven-development
