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

That one question changes everything.

**Why it matters:**

When you define what done looks like, two things happen:

1. The interview surfaces latent criteria—stuff you'd reject code for but wouldn't think to specify. "Should there be rate limiting?" (Yes—I'd reject a PR without it, but I wouldn't have said it upfront.)

2. Claude has flexibility to adapt. You're not micromanaging the path. You're defining the destination.

When you specify *how* to implement, you end up micromanaging. Rigid plans break when reality gets messy. Claude starts using `any` types and `@ts-ignore` to satisfy your instructions while violating the spirit.

**What this looks like in practice:**

Instead of detailed implementation steps, I define:
- What the output must do and must NOT do (acceptance criteria)
- Constraints that must never be violated (invariants)
- How to verify each criterion (automated checks)

Then I let Claude implement toward those criteria. The verify-fix loop is automated—what fails gets fixed, what passes is locked in.

If you know spec-driven development, this is a cousin—adapted for LLMs. Key difference: the manifest is ephemeral. It drives one task, then the code is truth. No spec maintenance.

**What it doesn't fix:**

- Won't help for one-off quick tasks (overkill)
- Requires upfront investment in defining criteria
- Verification is only as good as your criteria—garbage in, garbage out

**What actually changed for me:**

- First pass lands closer to done
- I trust the output (I know what was checked)
- I can fire and forget during execution because I invested in the define phase
- The process compounds—encode what I miss as new criteria

I eventually packaged this workflow as a Claude Code plugin. Two commands: `/define` (AI interviews you, surfaces criteria) and `/do` (AI implements, verifies, fixes—until done).

Blog post with full approach + worked example: aviramk.dev/scrolly/manifest-driven-development

Claude Code plugin: https://github.com/doodledood/manifest-dev
