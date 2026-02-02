# LinkedIn Post: Manifest-Driven Development

---

## Media

**GIF**: Terminal recording of `/define` interview (same asset as Twitter)

---

## Post Body

We're asking AI the wrong question.

Instead of "how do I get the AI to code this properly?"

Ask: "What would make me accept this PR in full?"

That reframe flips where you invest energy—from micromanaging implementation to defining what success looks like.

After years of AI workflows, I kept hitting the same wall: AI generates code, it looks reasonable, I ship it—then hours later I'm debugging something that should have been obvious.

The problem wasn't the AI. It was how I framed tasks.

Rigid implementation plans break when reality gets messy. Acceptance criteria don't—they define the destination, not the path.

I call this manifest-driven development:

→ Define: AI interviews you, surfaces latent criteria you'd reject code for but wouldn't think to specify
→ Do: AI implements, verifies against criteria, fixes failures—until every criterion passes

Two commands. The verify-fix loop is internal. You define the bar; AI iterates until it clears.

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

Claude Code plugin: github.com/doodledood/manifest-dev
