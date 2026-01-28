# Slack Message: Claude Code Devs Channel

---

Hey team—

Sharing something that's helped me significantly with Claude Code—might be useful for your workflows too.

**The problem it solves:**

After years of AI workflows, I kept hitting the same wall: Claude would "finish" but leave edge cases or subtle issues I'd spend hours debugging. The core issue wasn't Claude—it was how I was framing tasks.

**What changed:**

Instead of specifying implementation steps, I started defining acceptance criteria first: what would make me actually accept this code as done? Then let Claude implement toward those criteria with flexibility, and verify automatically.

This surfaces latent criteria I'd miss ("should there be rate limiting?") and catches issues before I review.

**The flow:**
- `/define <task>` — Claude interviews you about what you want, surfaces latent criteria
- `/do <manifest>` — Claude implements toward the criteria
- `/verify` — Automated checks against each AC
- Fix loop until done

Try `/define <something you're working on>` and see what the interview surfaces—it's often the most valuable part.

Happy to answer questions or hear feedback if you try it.

**Links:**
```bash
claude plugins add github.com/doodledood/manifest-dev
claude plugins install manifest-dev@manifest-dev-marketplace
```

Full writeup: [BLOG_URL]

Repo: https://github.com/doodledood/manifest-dev
