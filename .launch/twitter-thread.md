# X/Twitter Thread: Manifest-Driven Development

---

## Tweet 1 (Hook)
Stop asking "how do I get the AI to code this properly?"

Start asking "what would make me accept this PR?"

That one shift changed everything about how I work with AI agents.

Thread 🧵

---

## Tweet 2
After years of AI workflows, I kept hitting the same wall:

AI generates code → looks reasonable → ship it → hours later debugging something obvious

The problem wasn't the AI. It was how I was framing tasks.

---

## Tweet 3
Rigid step-by-step plans break when reality gets messy.

The AI starts using `any` types and `@ts-ignore` to satisfy instructions while violating the spirit.

The fix: define acceptance criteria, not implementation steps.

---

## Tweet 4
Specify WHAT the output must do.
Let the AI figure out HOW.
Then verify it hit the bar.

This is manifest-driven development:
- /define → surfaces latent criteria
- /do → AI implements with flexibility
- /verify → automated checks
- Fix loop until done

---

## Tweet 5
Why it works:

- LLMs are goal-oriented (RL training)—acceptance criteria play to their strength
- External manifest survives context drift
- Verify-fix loop catches issues before you see them
- Invest in define, then fire and forget

---

## Tweet 6
What actually changed for me:

- First pass lands closer to done
- I trust the output (know what was checked)
- Can parallelize (define next while current executes)
- Process compounds—encode misses as new criteria

---

## Tweet 7 (CTA)
[VISUAL PLACEHOLDER: GIF showing /define interview in terminal]

I packaged this as a Claude Code plugin. Deeper dive + worked example:

[BLOG_URL]

Code: github.com/doodledood/manifest-dev

---

*Note: Author to add terminal GIF before posting*
