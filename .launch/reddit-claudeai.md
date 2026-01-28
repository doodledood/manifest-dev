# Reddit Post: r/ClaudeAI

---

## Title

I built a Claude Code plugin after getting frustrated with how I was using AI agents—here's what changed

---

## Body

After weeks of using Claude Code for production work, I kept running into the same problem: I'd give it a task, it'd generate reasonable-looking code, and then I'd spend hours debugging edge cases or realizing it "finished" with critical pieces missing.

The issue wasn't Claude. The issue was me—I was framing tasks wrong.

**The reframe that worked:**

Instead of thinking "how do I get Claude to implement this properly?", I started asking "what would make me accept this PR in full?"

That shift led me to build a workflow I call manifest-driven development:

1. **Define** — Claude interviews you about what you want. Not just what you say, but the latent criteria you'd reject a PR for but wouldn't think to specify upfront. (Things like "did you add rate limiting?" or "is error handling consistent?")

2. **Manifest** — The output is a structured document: deliverables, acceptance criteria, global invariants, verification methods.

3. **Do** — Claude implements toward the acceptance criteria with flexibility on the how.

4. **Verify** — Automated checks run against every criterion. What fails gets flagged specifically.

5. **Fix loop** — Failed criteria get fixed. What passes is locked in. Loop until done.

**Why it helped me:**

- The interview surfaces stuff I'd miss. Latent criteria come out of the conversation, not my upfront thinking.
- Verification catches issues before I review. The fix loop handles cleanup.
- I can trust the output more—not because Claude is perfect, but because I know what was checked.
- I can fire and forget during execution because I invested in the define phase.

**What it doesn't fix:**

- Won't help if you're doing one-off quick tasks (overkill)
- Requires upfront investment in the define phase
- Verification is only as good as your criteria—garbage in, garbage out

I packaged this as a Claude Code plugin. Blog post with the full approach + worked example: [BLOG_URL]

Repo: https://github.com/doodledood/manifest-dev

Curious if others have tried similar structured approaches. What's worked for you?
