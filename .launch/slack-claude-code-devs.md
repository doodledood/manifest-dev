# Slack Message: Claude Code Devs Channel

---

Hey team—

Sharing something that's helped me significantly with Claude Code—might be useful for your workflows too.

**The problem it solves:**

After years of AI workflows, I kept hitting the same wall: Claude would "finish" but leave edge cases or subtle issues I'd spend hours debugging. The core issue wasn't Claude—it was how I was framing tasks.

**What changed:**

I stopped asking "how do I get Claude to implement this properly?" and started asking "what would make me accept this PR?"

That reframe changes everything. Instead of specifying implementation steps, I define acceptance criteria first. Then let Claude implement toward those criteria—the verify-fix loop is automated.

**The flow:**
- `/define <task>` — Claude interviews you, surfaces what you'd actually reject a PR for
- `/do` — Claude implements, verifies against criteria, fixes failures—until done

Two commands. The rest is automated.

Try `/define <something you're working on>` and see what the interview surfaces—it's often the most valuable part.

Happy to answer questions or hear feedback if you try it.

**Links:**
```bash
claude plugins add github.com/doodledood/manifest-dev
claude plugins install manifest-dev@manifest-dev-marketplace
```

Full writeup: aviramk.dev/scrolly/manifest-driven-development

Claude Code plugin: https://github.com/doodledood/manifest-dev
