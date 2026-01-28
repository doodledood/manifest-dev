# Manifest-Driven Development: What I Learned After Years of AI Workflows

Here's what I've learned after years of building with AI coding agents: the problem isn't the AI. The problem is how we're framing what we want.

We keep asking "how do I get the LLM to implement this feature properly?" when we should be asking "what would make me accept this PR in full?"

That reframe changes everything.

---

## The Vibe Coding Hangover

If you've spent any time with AI coding tools in the past year, you know the pattern. You give the agent a task. It generates code. The code looks reasonable. You ship it. Two days later you're debugging something that should have been obvious—or worse, you're realizing the AI "finished" but left critical pieces incomplete.

This is the vibe coding hangover. We got excited about the speed. We ignored the cleanup cost.

The frustrating part: the tools are getting smarter. Claude, GPT, the latest models—they can genuinely code. But we're throwing them into deep water without defining what "done" actually means.

---

## The Mindset Shift

Here's the insight that changed how I work with AI agents:

**Stop thinking about how to make the AI implement correctly. Start defining what would make you accept the output.**

This isn't just semantic wordplay. It's a fundamental shift in where you invest your energy.

When you ask "how should the LLM do this?", you end up micromanaging the implementation. You write detailed plans. You specify function names and types. You try to puppeteer the AI through every step. And the moment something unexpected happens—which it always does—the rigid plan breaks down. The AI starts using `any` types, adding `// @ts-ignore` comments, bending reality to satisfy the letter of your instructions while violating the spirit.

When you ask "what would make me accept this?", you define success criteria. You specify what the output must do and must not do—not how it must be built. You encode your quality standards as verifiable acceptance criteria. Then you let the AI figure out the implementation—and you verify whether it hit the bar.

This is manifest-driven development.

---

## The Framework

Manifest-driven development separates three concerns:

1. **WHAT** needs to be built (deliverables with acceptance criteria)
2. **CONSTRAINTS** that must never be violated (global invariants)
3. **HOW** to verify each criterion (automated checks)

The workflow:

```
/define → Interview → Manifest → /do → Execute → /verify → Fix loop → /done
```

**Define**: An LLM interviews you to surface what you actually want. Not just what you say you want—your latent criteria. The stuff you'd reject in a PR but wouldn't think to specify upfront.

**Do**: The AI implements toward the acceptance criteria. It has flexibility on the how. It doesn't have flexibility on the what.

**Verify**: Automated checks run against every criterion. Failing checks get specific—they say exactly what's wrong.

**Fix**: The AI fixes what failed. Only what failed. It doesn't restart. It doesn't touch passing criteria.

The loop continues until everything passes—or until a blocker requires human intervention.

---

## Why This Works (The LLM Science)

LLMs aren't general reasoners. They're goal-oriented pattern matchers trained through reinforcement learning. This has implications for how we should work with them.

**They're trained on goals, not processes.** RL during training made them fundamentally goal-oriented. When you give clear acceptance criteria, you're playing to their strength. When you give rigid step-by-step plans, you're fighting their nature.

**They can't hold all the nuances.** Neither can you. Some implementation details only surface once you're deep in the code. A rigid plan can't account for unknowns. Acceptance criteria can—because they define the destination, not the path.

**They suffer from context drift.** Long sessions cause "context rot"—the model loses track of earlier instructions. Manifest-driven development compensates for this with external state (the manifest file) and verification that catches drift before it ships.

**They don't know when they're wrong.** LLMs can't express genuine uncertainty. They'll confidently produce broken code. The verify-fix loop doesn't rely on the AI knowing it failed—it relies on automated checks catching failures.

This isn't a hack around LLM limitations. It's a design that treats those limitations as first principles.

---

## What /define Actually Produces

Here's a real example. Imagine you want to add user authentication to a web app. You invoke `/define`:

```
/define add user authentication
```

The interview begins. The AI asks questions:

> What authentication method? (password, OAuth, magic link?)
> What user attributes do you need to store?
> Do you have an existing users table or starting fresh?
> Password requirements?
> Session handling—JWT, server sessions, something else?
> What should happen when auth fails? Redirects? Error messages?

You answer. The AI probes deeper on areas where your answers were vague. It surfaces latent criteria you didn't think to mention—"should there be rate limiting on login attempts?" (Yes, you'd reject a PR without it, but you wouldn't have specified it.)

The output is a manifest:

````markdown
# Definition: User Authentication

## 1. Intent & Context
- **Goal:** Add password-based authentication to existing Express app
  with JWT sessions. Users can register, log in, and log out.

## 3. Global Invariants (The Constitution)
- [INV-G1] Passwords never stored in plaintext
  ```yaml
  verify:
    method: bash
    command: "grep -r 'password' src/ | grep -v 'hashedPassword' | grep -v '.test.'"
  ```
- [INV-G2] All auth endpoints rate-limited (max 5 attempts/minute)
- [INV-G3] JWT secrets from env variable, not hardcoded
  ```yaml
  verify:
    method: bash
    command: "grep -r 'JWT_SECRET\\|process.env' src/routes/auth.ts"
  ```

## 6. Deliverables (The Work)

### Deliverable 1: User Model & Migration
**Acceptance Criteria:**
- [AC-1.1] User model has id, email, hashedPassword, createdAt
  ```yaml
  verify:
    method: bash
    command: "grep -E 'id|email|hashedPassword|createdAt' src/models/user.ts"
  ```
- [AC-1.2] Email has unique constraint
- [AC-1.3] Migration creates users table with indexes

### Deliverable 2: Auth Endpoints
**Acceptance Criteria:**
- [AC-2.1] POST /register creates user, returns 201
- [AC-2.2] POST /login validates credentials, returns JWT
- [AC-2.3] Invalid credentials return 401, not 500
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Check auth routes for proper error handling. 401 for auth failures, not 500."
  ```
````

Every criterion has a verification method—bash commands, grep checks, or LLM-as-judge prompts. The manifest also includes sections for Approach (execution order, risks, trade-offs), Process Guidance (non-verifiable constraints), and Known Assumptions.

Now `/do` executes against this manifest. The AI implements with flexibility. `/verify` checks every criterion. What fails gets fixed. What passes is locked in.

---

## The Big Shift

Here's what changes when you adopt this approach:

**Your first pass lands closer to done.** Verification catches issues before you see them. The fix loop handles cleanup automatically.

**You can trust the output.** Not because the AI is infallible, but because every acceptance criterion has been verified. You know what was checked.

**You can parallelize.** While one manifest is executing, you can define the next. The define phase is where your judgment matters. The do-verify-fix phase runs on its own.

**You stop chasing hype.** The workflow is grounded in how LLMs actually work. It's not magic. It's engineering.

**You stay connected to your codebase.** The define phase forces involvement—you can't write acceptance criteria without understanding what you want. When the code comes back, you're reviewing against criteria you thought through, not parsing AI-generated code cold. This combats the atrophy problem where heavy AI assistance means losing touch with your own code.

**Your process compounds.** When a PR passes verification but reviewers still find issues, encode those as new review agents or CLAUDE.md guidelines. Next time, the system catches what you missed. The process gets smarter with use.

**It's dead simple to use.** All the complexity lives in the implementation—you never see it. Run `/define`, answer the interview questions, run `/do`, go grab coffee. That's it. No prompt engineering. No babysitting. Just follow along.

**Resist the urge to intervene.** It won't nail everything on the first pass—that's expected. The verify-fix loop exists precisely for this. You invested in define; now let the loop run. It rarely gets there in a straight line, but it gets there.

The goal isn't perfect output on the first try. It's reducing friction to get there. Fewer iterations. Less debugging. More shipping.

---

## Try It

Manifest-driven development isn't the final answer. But after years of iterating on AI workflows, it's the most reliable approach I've found to ship quality code with AI agents. Not because it removes the AI's limitations—but because it works with them.

I packaged this as a Claude Code plugin. The workflow:

```bash
# Start a define session
/define <what you want to build>

# After manifest is ready, execute
/do <manifest-path>

# Verify and fix until done
/verify
```

**Pro tip**: Run `/do` in a fresh session after `/define` completes—or at minimum, `/compact` before starting execution. Long define sessions accumulate context that can cause drift during implementation. The manifest is your external state; the session doesn't need to remember the conversation that produced it.

The plugin includes:
- **/define**: Interview-driven manifest creation
- **/do**: Execution with verification loops
- **/verify**: Automated acceptance criteria checks
- **Specialized reviewers**: Agents for maintainability, testability, bugs, coverage

It's opinionated by design. The workflow is structured so you can invest heavily in the define phase, then fire and forget during execution. You're not babysitting the AI—you're verifying its output against criteria you defined upfront.

If this resonates, try `/define` on your next task and see what the interview surfaces.

---

**Get Started**

```bash
claude plugins add github.com/doodledood/manifest-dev
claude plugins install manifest-dev@manifest-dev-marketplace
```

Repo: [github.com/doodledood/manifest-dev](https://github.com/doodledood/manifest-dev)

I share what I'm learning as I build this at [@aviramk](https://twitter.com/aviramk)

*[BLOG_URL] — I write about building with AI agents, first-principles workflows, and what actually works.*
