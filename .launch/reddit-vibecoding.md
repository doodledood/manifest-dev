# Reddit Post: r/vibecoding

---

## Title

What years of AI coding taught me: you can keep the vibe and still ship clean code

---

## Body

I love vibe coding. That flow state where you're riffing with the AI, ideas becoming code in real-time—it's genuinely fun. I don't want to lose that.

But after years of AI workflows, I kept running into the same problem: the initial session feels productive, then I'd spend hours afterward debugging edge cases, fixing inconsistencies, or realizing the AI "finished" with critical pieces half-done.

So I tried asking a different question. Not "how should AI implement this?" but "what would make me actually ship this?"

That one shift kept the vibe but added a finish line.

**What I changed:**

Before a session, I now spend 10-15 minutes defining acceptance criteria. Not implementation steps. Not "write function X that does Y." Just: what does success look like? What would I reject in a PR review?

Then I let the AI vibe toward those criteria. It still has flexibility. I'm not micromanaging the implementation. But now there's a bar.

The verify-fix loop runs automatically. When something fails, it gets fixed. What passes is locked in.

**What surprised me:**

The upfront definition phase actually surfaces stuff I'd miss. "Oh right, I should rate limit this." "Oh right, I'd be annoyed if error messages weren't consistent." Those latent criteria come out of the process, not my initial thinking.

And the automated verification catches cleanup before I even look at the code. The fix loop handles the debugging I used to do manually.

**Tradeoffs:**

- Takes longer on the first pass. You're investing upfront instead of during cleanup.
- Overkill for truly quick throwaway tasks.
- You still need to define good criteria—bad criteria = bad output.

**Where this fits:**

This isn't "stop vibe coding." It's structured vibe coding. The creative exploration is still there. You're just defining the destination first so you don't wander forever.

I eventually packaged this workflow as a Claude Code plugin (though the concept works with any AI tool). Two commands: `/define` and `/do`. That's it.

Blog post with more detail + worked example: aviramk.dev/scrolly/manifest-driven-development

Claude Code plugin: https://github.com/doodledood/manifest-dev
