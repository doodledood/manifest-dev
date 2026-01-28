# Definition: Launch Content Strategy for manifest-dev

## 1. Intent & Context

- **Goal:** Launch manifest-dev publicly with high-signal content across blog, social media, and internal channels. Introduce "manifest-driven development" as a concept, position this repo as the Claude Code implementation.

- **Mental Model:**
  - Blog is the anchor — comprehensive position piece ("manifesto")
  - Social posts are self-contained but link to blog for depth
  - Each platform has different norms; content adapts to context
  - Anti-hype voice is the brand differentiator
  - "Structured vibe coding" framing for r/vibecoding (evolution, not replacement)

## 2. Approach

- **Architecture:**
  - All artifacts are markdown files in `.launch/`
  - Blog draws from RAW_DUMP.md as ideological backbone
  - Platform research informs each post's format/tone
  - Schedule document coordinates the rollout

- **Execution Order:**
  - D8 (Schedule) → D1 (Blog) → D2-D7 (Social/Slack)
  - Rationale: Schedule first to understand timing constraints. Blog is the anchor all posts reference. Social posts can be parallelized after blog draft exists.

- **Risk Areas:**
  - [R-1] Content reads as AI-generated despite anti-slop intent | Detect: Subagent review for generic/filler language
  - [R-2] r/vibecoding dismisses as preachy/anti-vibe-coding | Detect: Framing check for "evolution not replacement" stance
  - [R-3] Slack message feels self-promotional rather than helpful | Detect: Subagent review for value-first framing
  - [R-4] SEO term "manifest-driven development" not prominent enough | Detect: Grep for term frequency in blog

- **Trade-offs:**
  - [T-1] Depth vs Brevity → Prefer depth for blog, brevity for social (blog is the deep dive)
  - [T-2] Tool-specific vs Concept-general → Prefer concept-general for intro, tool-specific for CTA
  - [T-3] Personal story vs Technical explanation → Prefer personal story as hook, technical as body
  - [T-4] Polished vs Authentic → Prefer authentic (matches RAW_DUMP.md voice)

## 3. Global Invariants (The Constitution)

- [INV-G1] **Anti-hype voice**: No superlatives ("revolutionary", "game-changing", "magic", "10x"). Language must match CUSTOMER.md messaging guidelines.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Review the content for hype language. Flag any instances of: revolutionary, game-changing, magic, 10x, best, ultimate, perfect, incredible, amazing. Also flag marketing-speak, vague claims without evidence, or excessive enthusiasm. Return PASS if clean, FAIL with specific violations if found."
  ```

- [INV-G2] **High signal**: Every sentence must earn its place. No filler, padding, or redundant statements.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Review the content for filler or low-signal content. Flag: redundant sentences, unnecessary qualifiers, padding phrases ('it's worth noting that', 'as we all know'), or content that could be cut without losing meaning. Return PASS if dense and high-signal, FAIL with specific examples if filler found."
  ```

- [INV-G3] **All artifacts in .launch/**: Every deliverable file must be created in `/home/user/manifest-dev/.launch/`
  ```yaml
  verify:
    method: bash
    command: "ls /home/user/manifest-dev/.launch/*.md | wc -l"
  ```

- [INV-G4] **RAW_DUMP.md as source**: Blog must incorporate key ideas from RAW_DUMP.md (mindset shift, verify-fix loop, LLM goal-orientation, latent criteria, fire-and-forget parallelism)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Compare the blog post against the RAW_DUMP.md ideas. Verify that these concepts appear: (1) mindset shift from 'how to implement' to 'what would make me accept this PR', (2) verify-fix loop, (3) LLMs are goal-oriented from RL training, (4) surfacing latent criteria, (5) fire-and-forget after define investment. Return PASS if all concepts present, FAIL listing missing concepts."
  ```

- [INV-G5] **Self-contained social posts**: Each social post must deliver value even without clicking the blog link.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Review the social post. Ask: Does a reader who never clicks the link still learn something valuable? Is there an insight, lesson, or actionable takeaway in the post itself? Return PASS if self-contained value exists, FAIL if the post is just a teaser."
  ```

## 4. Process Guidance (Non-Verifiable)

- [PG-1] Write in author's authentic voice — direct, opinionated, like the RAW_DUMP.md reads
- [PG-2] Reference team experience generally ("after weeks of production use") but no confidential specifics
- [PG-3] For Reddit: lead with value/story, include link in body (user preference over comments-only research finding)
- [PG-4] For LinkedIn: use line breaks for scannability, keep hook under 200 chars
- [PG-5] For X/Twitter: include note about visuals (GIF of terminal) — author will add separately
- [PG-6] Slack messages should feel helpful to recipients, not self-promotional
- [PG-7] Use research-validated posting times: Twitter Tue-Thu 9-11 AM EST, LinkedIn 8-9 AM or 2-3 PM EST

## 5. Known Assumptions

- [ASM-1] Author's X handle exists and can be referenced | Default: @aviramk or similar | Impact if wrong: Update CTA in posts
- [ASM-2] Slack culture is receptive to personal project sharing | Default: Frame as genuinely helpful | Impact if wrong: May need to soften or skip
- [ASM-3] Blog will be hosted at aviramk.com/blog or similar | Default: Use placeholder [BLOG_URL] | Impact if wrong: Update links before publishing
- [ASM-4] GitHub repo URL is github.com/doodledood/manifest-dev | Default: Use this URL | Impact if wrong: Update all references

## 6. Deliverables (The Work)

### Deliverable 1: Blog Post

**File:** `.launch/blog-post.md`

**Description:** Manifesto-style blog post introducing manifest-driven development. Broad concept introduction → Claude Code implementation → CTA to try it.

**Structure:**
1. Hook: The problem (vibe coding hangover, AI output you can't trust, hype fatigue)
2. Insight: The mindset shift ("what would make me accept this PR")
3. Framework: Manifest-driven development (define → do → verify loop)
4. Why it works: Grounded in how LLMs actually work
5. Worked example: What /define actually produces
6. Try it: This repo as the implementation, install instructions
7. CTA: Install → Star → Follow

**Acceptance Criteria:**

- [AC-1.1] Blog follows the 7-section structure above
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Verify the blog post contains all 7 sections: (1) Hook with problem statement, (2) Mindset shift insight, (3) Framework explanation, (4) Why it works / LLM grounding, (5) Worked /define example, (6) Try it / installation, (7) CTA. Return PASS if all present, FAIL listing missing sections."
  ```

- [AC-1.2] Blog includes a worked /define example with hypothetical task (e.g., "add user auth") showing manifest output
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Verify the blog post includes a worked /define example. The example should show: (1) A hypothetical task being defined (e.g., 'add user authentication'), (2) Key interview questions or the define process, (3) Sample manifest output (deliverables, ACs, invariants). Return PASS if example is complete and illustrative, FAIL if superficial or missing components."
  ```

- [AC-1.3] "Manifest-driven development" term appears at least 5 times (SEO)
  ```yaml
  verify:
    method: bash
    command: "grep -ci 'manifest-driven' /home/user/manifest-dev/.launch/blog-post.md"
  ```

- [AC-1.4] Blog includes clear installation instructions for the plugin
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Verify the blog post includes installation instructions. Should reference: (1) how to add the marketplace, (2) how to install the plugin, (3) how to invoke /define. Return PASS if installation path is clear, FAIL if missing or unclear."
  ```

- [AC-1.5] Blog ends with prioritized CTA (install → star → follow)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Check the blog ending. Does it include CTAs in priority order: (1) install/try the plugin, (2) star the repo, (3) follow on X/Twitter? Return PASS if CTAs present in roughly this priority, FAIL if missing or wrong order."
  ```

---

### Deliverable 2: X/Twitter Thread

**File:** `.launch/twitter-thread.md`

**Description:** 5-7 tweet thread introducing manifest-driven development. Self-contained value, links to blog for depth.

**Format requirements (from research):**
- Hook with specific numbers or unexpected result
- Visual placeholder noted (author adds GIF)
- Link in final tweet or bio reference (avoid algorithm penalty)
- Single clear CTA at end

**Acceptance Criteria:**

- [AC-2.1] Thread is 5-7 tweets
  ```yaml
  verify:
    method: bash
    command: "grep -c '^---$\\|^Tweet [0-9]' /home/user/manifest-dev/.launch/twitter-thread.md || grep -c '^[0-9]\\.' /home/user/manifest-dev/.launch/twitter-thread.md"
  ```

- [AC-2.2] First tweet is a compelling hook (under 280 chars, specific or contrarian)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Review the first tweet of the thread. Is it: (1) Under 280 characters, (2) Contains a hook (specific number, surprising claim, or contrarian insight), (3) Not a generic announcement? Return PASS if compelling hook, FAIL with reason if weak."
  ```

- [AC-2.3] Thread includes placeholder/note for visual (GIF of terminal)
  ```yaml
  verify:
    method: bash
    command: "grep -ci 'gif\\|visual\\|screenshot\\|video\\|image' /home/user/manifest-dev/.launch/twitter-thread.md"
  ```

- [AC-2.4] Link placement follows best practice (end of thread or bio reference)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Check link placement in the Twitter thread. The blog/repo link should appear in the final tweet or as a 'link in bio' reference, NOT in the opening tweets. Return PASS if link at end, FAIL if link appears too early."
  ```

- [AC-2.5] All tweets are under 280 characters
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Check each tweet in the thread. Verify every tweet is under 280 characters. Return PASS if all tweets fit, FAIL listing any tweets that exceed the limit with their character count."
  ```

---

### Deliverable 3: LinkedIn Post

**File:** `.launch/linkedin-post.md`

**Description:** Medium-length post for mixed audience (devs + managers). Self-contained, links to blog in first comment.

**Format requirements (from research):**
- 1,200-1,500 characters
- Hook under 200 chars (before "See More" cutoff)
- Line breaks for scannability
- 3-5 hashtags at bottom
- Note: link goes in first comment (include as separate section)

**Acceptance Criteria:**

- [AC-3.1] Post is 1,000-1,600 characters (with some flexibility)
  ```yaml
  verify:
    method: bash
    command: "wc -c < /home/user/manifest-dev/.launch/linkedin-post.md | awk '{if ($1 >= 800 && $1 <= 2000) print \"PASS\"; else print \"FAIL: \" $1 \" chars\"}'"
  ```

- [AC-3.2] First paragraph is under 200 characters (pre-fold hook)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Check the LinkedIn post's first paragraph (before first blank line). Is it under 200 characters? This is the 'hook' that appears before 'See More'. Return PASS if under 200 chars, FAIL with char count if over."
  ```

- [AC-3.3] Post uses line breaks for scannability (not wall of text)
  ```yaml
  verify:
    method: bash
    command: "grep -c '^$' /home/user/manifest-dev/.launch/linkedin-post.md | awk '{if ($1 >= 3) print \"PASS\"; else print \"FAIL: only \" $1 \" blank lines\"}'"
  ```

- [AC-3.4] Includes 3-5 hashtags at bottom
  ```yaml
  verify:
    method: bash
    command: "grep -o '#[A-Za-z]\\+' /home/user/manifest-dev/.launch/linkedin-post.md | wc -l | awk '{if ($1 >= 3 && $1 <= 6) print \"PASS\"; else print \"FAIL: \" $1 \" hashtags\"}'"
  ```

- [AC-3.5] Includes separate "First Comment" section with blog link
  ```yaml
  verify:
    method: bash
    command: "grep -ci 'first comment\\|comment:' /home/user/manifest-dev/.launch/linkedin-post.md"
  ```

- [AC-3.6] Works for dual audience (devs AND managers)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Review the LinkedIn post for dual-audience appeal. Does it: (1) Include technical substance that developers respect, AND (2) Include outcome/benefit language that managers understand (quality, reliability, shipping confidence)? Return PASS if both audiences served, FAIL if too technical or too fluffy."
  ```

---

### Deliverable 4: Reddit Post for r/ClaudeAI

**File:** `.launch/reddit-claudeai.md`

**Description:** Problem-first story for r/ClaudeAI. Transparent "I built this" framing with value upfront.

**Format requirements (from research):**
- Title: Personal narrative + honest framing
- Body: Value even without clicking link
- Link: Include repo/blog link in body (user preference)
- No marketing-speak

**Acceptance Criteria:**

- [AC-4.1] Title follows "I [verb] X because Y" or similar personal narrative pattern
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Review the Reddit post title. Does it follow a personal narrative pattern like 'I built X because Y' or 'After X months of Y, here's what worked'? Return PASS if personal/authentic, FAIL if it sounds like a product announcement."
  ```

- [AC-4.2] Body provides technical insight/value independent of the repo
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Review the Reddit post body. Does it provide genuine technical insight or lessons learned that a reader benefits from even if they never click the repo link? Return PASS if standalone value exists, FAIL if it's just a sales pitch."
  ```

- [AC-4.3] Includes repo/blog link in the body
  ```yaml
  verify:
    method: bash
    command: "grep -ciE 'github\\.com|blog|http' /home/user/manifest-dev/.launch/reddit-claudeai.md"
  ```

- [AC-4.4] No marketing-speak or feature-list style
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Check the Reddit post for marketing-speak. Flag: feature lists without context, superlatives, promotional language, or corporate tone. Return PASS if authentic dev voice, FAIL with examples if marketing-speak detected."
  ```

---

### Deliverable 5: Reddit Post for r/vibecoding

**File:** `.launch/reddit-vibecoding.md`

**Description:** Custom post for r/vibecoding with "structured vibe coding" angle. Evolution, not replacement. Experience-based framing.

**Format requirements (from research):**
- Angle: "Structured vibe coding" not "anti-vibe coding"
- Title: "How I stopped [pain] with [approach]" pattern
- Tone: Humble, honest about tradeoffs
- DO NOT be preachy or dismissive of vibe coding

**Acceptance Criteria:**

- [AC-5.1] Framed as evolution/improvement, not rejection of vibe coding
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Review the r/vibecoding post. Is it framed as 'structured vibe coding' or 'adding structure to vibe coding' rather than 'vibe coding is bad'? Does it acknowledge vibe coding's benefits (speed, flow) before introducing structure? Return PASS if respectful/evolutionary, FAIL if dismissive or preachy."
  ```

- [AC-5.2] Title follows experience-based pattern ("How I stopped X with Y" or similar)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Check the Reddit post title. Does it follow an experience-based pattern like 'How I stopped [pain]' or 'What 3 months of [X] taught me'? Return PASS if experience-based, FAIL if it sounds like an announcement."
  ```

- [AC-5.3] Honest about tradeoffs (not presented as silver bullet)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Does the post acknowledge any tradeoffs, limitations, or situations where the approach might not fit? Return PASS if honest about limitations, FAIL if presented as perfect solution."
  ```

- [AC-5.4] Distinct from r/ClaudeAI post (not just copy-paste)
  ```yaml
  verify:
    method: bash
    command: "diff /home/user/manifest-dev/.launch/reddit-claudeai.md /home/user/manifest-dev/.launch/reddit-vibecoding.md | wc -l | awk '{if ($1 > 20) print \"PASS\"; else print \"FAIL: too similar\"}'"
  ```

- [AC-5.5] Uses "structured vibe coding" framing or similar evolutionary language
  ```yaml
  verify:
    method: bash
    command: "grep -ciE 'structured.*vibe|vibe.*structure|add.*structure|more structure' /home/user/manifest-dev/.launch/reddit-vibecoding.md"
  ```

---

### Deliverable 6: Slack Message (Claude Code Devs Channel)

**File:** `.launch/slack-claude-code-devs.md`

**Description:** Internal message for Claude Code devs channel. Audience already uses Claude Code. Focus on the plugin and workflow.

**Acceptance Criteria:**

- [AC-6.1] Concise and scannable (under 500 words)
  ```yaml
  verify:
    method: bash
    command: "wc -w < /home/user/manifest-dev/.launch/slack-claude-code-devs.md | awk '{if ($1 <= 500) print \"PASS\"; else print \"FAIL: \" $1 \" words\"}'"
  ```

- [AC-6.2] Includes clear "what this is" and "how to try it"
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Review the Slack message. Does it clearly answer: (1) What is this? (2) Why should I care? (3) How do I try it? Return PASS if all three are clear, FAIL listing what's missing."
  ```

- [AC-6.3] Links to blog post for full context
  ```yaml
  verify:
    method: bash
    command: "grep -ci 'blog\\|post\\|article\\|wrote\\|details' /home/user/manifest-dev/.launch/slack-claude-code-devs.md"
  ```

- [AC-6.4] Feels helpful rather than self-promotional
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Review the Slack message tone. Does it feel like genuinely sharing something useful with colleagues, or does it feel like self-promotion? Return PASS if helpful tone, FAIL if promotional."
  ```

---

### Deliverable 7: Slack Message (Broader Engineering Channel)

**File:** `.launch/slack-engineering-broad.md`

**Description:** Message for broader engineering channel (mixed tools - Claude Code, Cursor, etc.). Present manifest-driven development as tool-agnostic concept.

**Acceptance Criteria:**

- [AC-7.1] Presents manifest-driven development as concept (not Claude Code-specific)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Review the Slack message. Does it present manifest-driven development as a general concept applicable to various AI coding tools (not just Claude Code)? Return PASS if tool-agnostic framing, FAIL if too Claude Code-specific."
  ```

- [AC-7.2] Acknowledges other tools exist (Cursor, etc.)
  ```yaml
  verify:
    method: bash
    command: "grep -ci 'cursor\\|copilot\\|other tool\\|any tool' /home/user/manifest-dev/.launch/slack-engineering-broad.md"
  ```

- [AC-7.3] Concise (under 400 words)
  ```yaml
  verify:
    method: bash
    command: "wc -w < /home/user/manifest-dev/.launch/slack-engineering-broad.md | awk '{if ($1 <= 400) print \"PASS\"; else print \"FAIL: \" $1 \" words\"}'"
  ```

- [AC-7.4] Distinct from Claude Code devs message
  ```yaml
  verify:
    method: bash
    command: "diff /home/user/manifest-dev/.launch/slack-claude-code-devs.md /home/user/manifest-dev/.launch/slack-engineering-broad.md | wc -l | awk '{if ($1 > 15) print \"PASS\"; else print \"FAIL: too similar\"}'"
  ```

---

### Deliverable 8: Launch Schedule

**File:** `.launch/launch-schedule.md`

**Description:** Timing and sequencing document for the multi-platform rollout.

**Acceptance Criteria:**

- [AC-8.1] Includes specific days and times for each platform
  ```yaml
  verify:
    method: bash
    command: "grep -cE 'Day [0-9]|Monday|Tuesday|Wednesday|Thursday|AM|PM|EST' /home/user/manifest-dev/.launch/launch-schedule.md | awk '{if ($1 >= 5) print \"PASS\"; else print \"FAIL: not enough schedule details\"}'"
  ```

- [AC-8.2] Covers all 7 content deliverables
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Verify the schedule covers timing for: (1) Blog, (2) Twitter/X, (3) LinkedIn, (4) Reddit r/ClaudeAI, (5) Reddit r/vibecoding, (6) Slack Claude Code devs, (7) Slack broader engineering. Return PASS if all covered, FAIL listing missing items."
  ```

- [AC-8.3] Includes rationale for timing choices
  ```yaml
  verify:
    method: bash
    command: "grep -ci 'because\\|rationale\\|reason\\|why' /home/user/manifest-dev/.launch/launch-schedule.md"
  ```
