# Reddit Post: r/vibecoding

---

## Title

What years of AI coding taught me: you can keep the vibe and still ship clean code

---

## Body

I love vibe coding. That flow state where you're riffing with the AI, ideas becoming code in real-time—it's genuinely fun. I don't want to lose that.

But after years of AI workflows, I kept running into the same problem: the initial session feels productive, then I'd spend hours afterward debugging edge cases, fixing inconsistencies, or realizing the AI "finished" with critical pieces half-done.

So I tried something different. Not replacing the vibe—adding structure around it.

**What I changed:**

Before a session, I now spend 10-15 minutes on what I call "defining the acceptance criteria." Basically: what would make me actually accept this code as done?

Not implementation steps. Not "write function X that does Y." Just: what does success look like? What would I reject in a PR review?

Then I let the AI vibe toward those criteria. It still has flexibility. I'm not micromanaging the implementation. But now there's a bar.

And—this is the key part—I verify against that bar automatically. When something fails, I fix just that thing and check again.

**What surprised me:**

The upfront definition phase actually surfaces stuff I'd miss. "Oh right, I should rate limit this." "Oh right, I'd be annoyed if error messages weren't consistent." Those latent criteria come out of the process, not my initial thinking.

And the verification catches cleanup before I even look at the code. The fix loop handles the debugging I used to do manually.

**Tradeoffs:**

- Takes longer on the first pass. You're investing upfront instead of during cleanup.
- Overkill for truly quick throwaway tasks.
- You still need to define good criteria—bad criteria = bad output.

**Where this fits:**

This isn't "stop vibe coding." It's structured vibe coding. The creative exploration is still there. You're just defining the destination first so you don't wander forever.

Curious what structures others have layered on top of vibe coding. What's helped you keep the flow without drowning in cleanup?

I eventually packaged this workflow as a Claude Code plugin (though the concept works with any AI tool). Blog post with more detail + worked example: [BLOG_URL]

Repo: https://github.com/doodledood/manifest-dev
