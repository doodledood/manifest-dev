# X/Twitter Thread: Manifest-Driven Development

---

## Tweet 1 (Hook)
After weeks of shipping production code with AI agents, here's the one change that actually worked:

Stop asking "how do I get the AI to code this properly?"

Start asking "what would make me accept this PR?"

Thread 🧵

---

## Tweet 2
The problem with AI coding isn't the AI—it's how we frame tasks.

Rigid step-by-step plans break when reality is messy. The AI starts using `any` types and `@ts-ignore` to satisfy your instructions while violating the spirit.

---

## Tweet 3
The fix: define acceptance criteria, not implementation steps.

Specify WHAT the output must do.
Let the AI figure out HOW.
Then verify it hit the bar.

This is manifest-driven development.

---

## Tweet 4
The workflow:

/define → LLM interviews you → surfaces latent criteria you'd reject a PR for but didn't specify

/do → AI implements with flexibility

/verify → automated checks against every criterion

Fix loop until all pass.

---

## Tweet 5
Why it works:

- LLMs are goal-oriented (from RL training)—acceptance criteria play to their strength
- External manifest survives context drift
- Verify-fix loop catches issues before you see them
- You invest in define, then fire and forget

---

## Tweet 6
[VISUAL PLACEHOLDER: GIF showing /define interview in terminal]

I built this as a Claude Code plugin.

Try it: `/define <your next task>`

The interview alone surfaces stuff you'd miss.

---

## Tweet 7 (CTA)
Wrote a deeper dive on the approach + worked example:

[BLOG_URL]

Code: github.com/doodledood/manifest-dev

If you're tired of debugging AI output and want something grounded, give it a look.

---

*Note: Author to add terminal GIF before posting*
