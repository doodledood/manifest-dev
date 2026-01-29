# Slack Message: Broader Engineering Channel

---

Hey all—

Wanted to share an approach I've been using for AI-assisted coding that's helped reduce the "AI generated it but now I'm debugging for hours" problem.

**The core idea:**

After years of AI workflows, I found the issue wasn't the AI—it was how I was framing tasks.

Instead of giving the AI implementation instructions, define acceptance criteria—what would make you actually accept the output as done. Then let the AI implement toward those criteria, and verify automatically.

The workflow:

1. **Define** — AI interviews you, surfaces latent criteria you'd reject code for but wouldn't specify upfront
2. **Do** — AI implements with flexibility on the how
3. **Verify** — Automated checks against each criterion
4. **Fix** — What fails gets fixed, what passes is locked in

**Why it helps:**

The define phase catches stuff you'd miss. The verification catches issues before you review. The approach works with the way LLMs actually work—they're goal-oriented from training, so giving clear success criteria plays to their strength.

**Tool-agnostic:**

The concept applies to any AI coding tool—Claude Code, Cursor, Copilot, etc. The workflow is what matters, not the specific tool.

**If you want to try it:**

I packaged it as a Claude Code plugin: https://github.com/doodledood/manifest-dev

Full writeup with worked example: aviramk.dev/blog/manifest-driven-development
