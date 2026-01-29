# LinkedIn Post: Manifest-Driven Development

---

## Post Body

We're asking AI the wrong question.

Instead of "how do I get the AI to code this properly?"

Ask: "What would make me accept this PR in full?"

That reframe changes everything.

After years of AI workflows, I kept hitting the same wall: AI generates code, it looks reasonable, I ship it—then hours later I'm debugging something that should have been obvious.

The problem wasn't the AI. It was how I framed tasks.

Rigid implementation plans break when reality gets messy. Acceptance criteria don't—they define the destination, not the path.

I call this manifest-driven development:

→ Define: LLM interviews you, surfaces latent criteria you'd reject code for but wouldn't think to specify
→ Do: AI implements toward those criteria with flexibility
→ Verify: Automated checks against every criterion
→ Fix: What fails gets fixed. What passes is locked.

What changed for me:
• First pass lands closer to done
• I trust the output (I know what was checked)
• Process compounds—encode what I miss as new criteria

Not because it removes AI limitations—but because it works with them.

I wrote up the full approach with a worked example.

---

## First Comment

Full writeup with worked example and the Claude Code plugin:

aviramk.dev/scrolly/manifest-driven-development

Repo: github.com/doodledood/manifest-dev
