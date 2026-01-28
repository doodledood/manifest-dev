# Reddit Post: r/ClaudeAI

---

## Title

The mindset shift that fixed how I work with AI agents (after years of trying different approaches)

---

## Body

After years of building with AI coding tools, I kept hitting the same wall: Claude generates code, it looks reasonable, I ship it—then hours later I'm debugging something that should have been obvious. Or worse, realizing it "finished" with critical pieces missing.

The issue wasn't Claude. It was me—I was asking the wrong question.

**The shift:**

I stopped asking "how do I get Claude to implement this properly?"

I started asking "what would make me accept this PR in full?"

That reframe changes where you invest your energy.

**Why it matters:**

When you specify *how* to implement, you end up micromanaging. Rigid plans break when reality gets messy. Claude starts using `any` types and `@ts-ignore` to satisfy your instructions while violating the spirit.

When you define *what success looks like*, Claude has flexibility to adapt. You're defining the destination, not the path.

**What this looks like in practice:**

Instead of detailed implementation steps, I define:
- What the output must do and must NOT do (acceptance criteria)
- Constraints that must never be violated (invariants)
- How to verify each criterion (automated checks)

Then I let Claude implement toward those criteria. A verify-fix loop handles cleanup. What fails gets fixed. What passes is locked in.

**The key insight:**

The interview phase surfaces stuff I'd miss. "Should there be rate limiting?" (Yes—I'd reject a PR without it, but I wouldn't have specified it.) Those latent criteria come out of the conversation, not my upfront thinking.

**What it doesn't fix:**

- Won't help for one-off quick tasks (overkill)
- Requires upfront investment in defining criteria
- Verification is only as good as your criteria—garbage in, garbage out

**What actually changed for me:**

- First pass lands closer to done
- I trust the output (I know what was checked)
- I can fire and forget during execution because I invested in the define phase
- The process compounds—encode what I miss as new criteria

I eventually packaged this workflow as a Claude Code plugin. Blog post with full approach + worked example: [BLOG_URL]

Repo: https://github.com/doodledood/manifest-dev
