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

Here's the thing: modern LLMs are trained to be goal-oriented. They're remarkably good at satisfying stated criteria. The bottleneck isn't capability anymore—it's clarity on what done looks like, and how to reliably verify it.

Rigid implementation plans break when reality gets messy. They force the AI to follow your path even when a better one exists. Acceptance criteria don't—they define the destination, not the route.

I call this manifest-driven development:

→ Define: AI interviews you, surfaces latent criteria you'd reject code for but wouldn't think to specify
→ Do: AI implements, verifies against criteria, fixes failures—until every criterion passes

Two commands. The verify-fix loop is internal. You define the bar; AI iterates until it clears.

If this sounds like spec-driven development—it is, adapted for LLMs. Key differences: manifests are ephemeral (no maintenance), the interview surfaces criteria you wouldn't write yourself, and verification is automated. Same DNA, different context.

What this enables:
• First pass lands closer to done
• Trust the output (you know what was checked)
• Fire and forget—invest in defining, not babysitting

Full approach + worked example in comments.

---

## First Comment

Full approach with worked example:

aviramk.dev/scrolly/manifest-driven-development

Claude Code plugin: github.com/doodledood/manifest-dev
