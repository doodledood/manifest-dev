# Slack Message: Claude Code Devs Channel

---

Hey team—

Sharing a workflow that's helped me get better first-pass output from AI coding tools.

**The reframe:**

Stop asking "how do I get the AI to implement this properly?"
Start asking "what would make me accept this PR?"

Modern LLMs are goal-oriented—they're good at satisfying stated criteria. The bottleneck isn't capability, it's clarity on what done looks like and how to verify it.

**The flow:**
- `/define <task>` — AI interviews you, surfaces what you'd actually reject a PR for
- `/do` — AI implements, verifies against criteria, fixes failures—until done

Two commands. The rest is automated.

Try `/define <something you're working on>` and see what the interview surfaces—often the most valuable part.

Happy to answer questions if you try it.

**Links:**
```bash
claude plugins add github.com/doodledood/manifest-dev
claude plugins install manifest-dev@manifest-dev-marketplace
```

Full writeup: aviramk.dev/scrolly/manifest-driven-development

Claude Code plugin: https://github.com/doodledood/manifest-dev
