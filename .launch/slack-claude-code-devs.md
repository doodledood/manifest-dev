# Slack Message: Claude Code Devs Channel

---

Hey team—

Been working on something I think might be useful for your Claude Code workflows.

**What it is:**

A plugin called `manifest-dev` that adds a structured workflow on top of Claude Code. The core idea: instead of going straight to implementation, you define acceptance criteria first, then let Claude implement toward those criteria, then verify automatically.

**The flow:**
- `/define <task>` — Claude interviews you about what you want, surfaces latent criteria
- `/do <manifest>` — Claude implements toward the criteria
- `/verify` — Automated checks against each AC
- Fix loop until done

**Why I built it:**

I kept hitting the same problem—Claude would "finish" but leave edge cases or subtle issues I'd spend hours debugging. Defining acceptance criteria upfront and verifying against them automatically reduced that friction significantly.

**How to try it:**

```bash
claude plugins add github.com/doodledood/manifest-dev
claude plugins install manifest-dev@manifest-dev-marketplace
```

Then run `/define <something you're working on>` and see what the interview surfaces.

Wrote up the full thinking behind it: [BLOG_URL]

Repo: https://github.com/doodledood/manifest-dev

Happy to answer questions or hear feedback if you try it.
