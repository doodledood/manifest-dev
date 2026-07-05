# Adoption work plan (temporary)

> **Status: temporary working document.** Everything here executes *after* the PR that introduces it merges — the listings and pages below should point at the updated front door, not the old one. Once all items are done, copy this file out of the repo and delete it; it is an operations checklist, not documentation.

Order matters: repo settings first (they feed the auto-scrapers), then submissions, then pages. The community-marketplace submission goes last among submissions — it has a review gate, so everything should be polished when it's reviewed.

## 1. GitHub repo settings (~10 min)

Repo → Settings / About panel:

- **Description** (paste-ready):
  > Loop engineering for Claude Code and other agent CLIs: figure the problem out first, define what done means, then execute and verify every criterion independently.
- **Topics**: `loop-engineering`, `claude-code`, `claude`, `ai-agents`, `agentic-coding`, `claude-code-plugin`

This is the discovery layer — GitHub search, topic pages, and the auto-scraped directories in §3 all read it.

## 2. Directory submissions — forms and PRs (one afternoon total)

Reusable description snippets (keep submissions consistent; grounded tone, no superlatives):

- **One-liner (agent-generic):**
  > Manifest-driven workflows for coding agents: /figure-out presses until the problem is actually understood, /define encodes what you'd accept, /do executes and verifies every criterion with an independent verifier.
- **Short paragraph (Claude-specific surfaces):**
  > Claude Code plugin for understanding-first development. /figure-out is an adversarial thinking partner that investigates the codebase before anything is built; /define turns the understanding into acceptance criteria; /do executes and can't call itself done until an independent verifier passes every criterion. Also ships PR tools: /babysit-pr, /review-pr, /walk-pr. Runs in Claude Code, OpenCode, Codex CLI, and Pi; individual skills install via `npx skills add doodledood/manifest-dev --skill <name>`.

### 2a. Anthropic community marketplace (submit last, after everything else is polished)

- **Process** (verified from code.claude.com/docs/en/plugins): third-party submissions go to the **`claude-plugins-community`** marketplace via review. The *official* marketplace is curated by Anthropic at its discretion — no application process exists for it.
- **Pre-step (required):** run `claude plugin validate` locally on both plugins; the review pipeline runs the same check plus automated safety screening.
- **Form:** individual authors use the Console form at <https://platform.claude.com/plugins/submit> (the claude.ai form at `admin-settings/directory/submissions/plugins/new` needs a Team/Enterprise org).
- **Draft:** repository `https://github.com/doodledood/manifest-dev`; plugin names `manifest-dev` and `manifest-dev-tools`; description = short paragraph above. Approved plugins get pinned by commit SHA in `anthropics/claude-plugins-community` and CI bumps the pin on new commits; the catalog syncs nightly — check `.claude-plugin/marketplace.json` there for arrival.

### 2b. awesome-claude-code (hesreallyhim) — issue form, NOT a PR

- **Process** (verified from its CONTRIBUTING): submissions **must** use the repo's web-UI issue form; PRs risk a temporary interaction restriction. Descriptions must be factual single-line, no emojis, no marketing voice, no addressing the reader. The list is deliberately selective.
- **Draft (one line, their register):**
  > A workflow plugin that separates understanding (/figure-out), acceptance definition (/define), and verified execution (/do), with one independent verifier per acceptance criterion.

### 2c. travisvn/awesome-claude-skills — PR

- **Process:** fork → add to the appropriate section → PR. Entries are table rows: `| **[name](url)** | description |`.
- **Draft entry row:**
  > `| **[manifest-dev](https://github.com/doodledood/manifest-dev)** | Understanding-first workflow skills: adversarial /figure-out, acceptance-criteria manifests, and execution verified per criterion by independent subagents |`

### 2d. ComposioHQ/awesome-claude-skills and ComposioHQ/awesome-claude-plugins — PRs

- **Process:** standard awesome-list PRs; match each list's existing entry format on arrival (both use name-link-description lines/rows).
- **Draft entry text (adapt punctuation to the surrounding format):**
  > [manifest-dev](https://github.com/doodledood/manifest-dev) — Understanding-first workflow for coding agents: /figure-out investigates before building, /define encodes acceptance criteria, /do verifies each one independently.

### 2e. rohitg00/awesome-claude-code-toolkit — PR

- Same draft as 2d; place under the plugins/ecosystem section that fits, matching the file's format on arrival.

### 2f. claudepluginhub.com — manual form

- **Process:** "submit a GitHub URL" flow on the site (the site blocks non-browser clients, so field names couldn't be inspected in advance; expect at minimum a repo URL field).
- **Prefill:** URL `https://github.com/doodledood/manifest-dev`; if it asks for name/description/category, use the snippets above and a "workflow / code quality" category.

### 2g. skillsllm.com — form at /submit

- **Process:** "Submit a Skill" form (JavaScript-rendered; fields couldn't be inspected in advance). They advertise security vetting, so expect a review delay.
- **Prefill:** repo URL, skill `figure-out` as the headline entry, one-liner description from above.

### 2h. tonsofskills.com (jeremylongshore/claude-code-plugins-plus-skills) — PR, heavier

- **Process** (verified from the repo): the marketplace syncs from PRs into *their* repo; a submission copies the plugin under their `plugins/` layout with an 8-field SKILL.md frontmatter (name, description, allowed-tools, version, author, license, compatibility, tags), validated against a 100-point rubric (`ccpi validate ./your-plugin` locally first; templates in `templates/`).
- **Effort note:** materially more work than every other listing (restructured copy of the plugin, extra frontmatter fields, their validation). Do it only after the cheap listings are live, if at all — or start with a single skill (figure-out) rather than the full plugin. Contact for questions: jeremy@intentsolutions.io.

### 2i. Auto-scraped — no submission possible or needed

| Directory | Mechanism | What feeds it |
|---|---|---|
| crossaitools.com (claudemarketplaces.com redirects here — same directory) | Scrapes GitHub daily; ranks by installs/stars/votes | §1 topics + description |
| mcpmarket.com | Scrapes GitHub | §1, plus the `metadata: internal: true` flags landing in this PR; if internal skills keep appearing after a re-scrape cycle, use the site's contact to request delisting of those pages |
| skills.sh | `npx skills` install telemetry | The README's install one-liner doing its job |

## 3. Query-capture pages (start with 5, expand from search-console data)

People search their pain in their harness's words — these pages use harness-specific language even though the README headline is harness-generic. One page per query, each answering the searcher's actual situation and handing them the one relevant skill (usually `/figure-out`, install line included), with the full loop linked below.

1. "claude code builds the wrong thing"
2. "claude code says done but it's not"
3. "make claude code understand my codebase before coding"
4. "claude code keeps breaking things it already fixed"
5. "can I trust claude code with large tasks unattended"

## 4. Loop-engineering page (~2–3 h, time-sensitive)

One landing/docs page addressed to someone who just read about loop engineering and wants to practice it: the loop was never the hard part — the stop condition is. Fronts `/figure-out` as the entry, presents the manifest loop as the harness-agnostic way to run loops with a trustworthy stop condition. Note: actual search volume for the term is unmeasured — keep this page cheap and let search-console data decide whether to invest further.

## 5. Thread interception (ongoing habit, minutes per occurrence)

Answer *existing* threads where someone is describing the pain right now (r/ClaudeAI, X, host-CLI Discords). Two lines max: name the behavior they described, hand the one relevant fragment (`npx skills add doodledood/manifest-dev --skill figure-out`). Never post broadcast demos or "look what I built" threads — those convert to applause, not usage. When someone asks "how did you do that", hand the single relevant skill, not the methodology.

## 6. Optional: one Show HN

At most one, only after §1–2 are live and the README front door has been up for a bit. Title states the pain, not the system (e.g. "Show HN: A skill that argues with your coding agent before it builds the wrong thing"). Expect a spike that decays; the durable channels remain §2–3.

## 7. Measurement (set up once, read weekly)

- GitHub traffic: clones + unique visitors (Insights → Traffic), noted weekly.
- Referrers: which directories/pages actually send people.
- `npx skills` installs where observable (skills.sh listing position is a proxy).
- Conversion signal: issues/discussions/PRs from people who clearly ran the loop (mention manifests, /define, verifier output).
- **Stars are recorded as noise, not as a metric.** The bar that counts: a few hundred real weekly users would make this a successful asset.

## Sequencing recap

1. Merge the PR carrying this file → 2. §1 repo settings same day → 3. cheap submissions (2b–2g) over one afternoon → 4. §3/§4 pages as time allows → 5. §2a community-marketplace submission once the above is live → 6. §2h only if the cheap listings show traction → §5 and §7 run continuously.
