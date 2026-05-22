---
name: review-pr
description: 'Autonomous PR review that posts high-signal, human-voiced comments under your account. Use when reviewing someone else''s PR (or your own manifest-driven PR) and you want a precision-tuned review you can walk away from. Triggers: review pr, autonomous review, post pr review, autoreview, loop review, watch pr review.'
argument-hint: '[pr-url] [--manifest <path>] [--bundle <urls>] [--loop]'
user-invocable: true
---

High-signal autonomous PR review posted under your account. A review you'd put your name on — precision over coverage.

**Inputs.** `pr-url` from the arg or the current branch's upstream PR. `--manifest <path>` opts into grounding against the author's intent; the skill does not auto-discover from any folder convention. `--bundle <urls>` plus PR-description linked-PR parsing (`Depends on #N`, `Stack:`, `Co-changes:`, GitHub PR URLs) provides cross-PR context for coupled changes.

**Reviewer fleet.** Spawn in parallel. Always-on: `change-intent-reviewer`, `code-bugs-reviewer`, `code-design-reviewer`, `code-maintainability-reviewer`, `code-simplicity-reviewer`, `context-file-adherence-reviewer`. Add when the diff fits: `type-safety-reviewer` on typed code; `test-quality-reviewer` and `code-testability-reviewer` on source; `contracts-reviewer` on API surfaces; `operational-readiness-reviewer` on CI/infra/env/migrations/workers/queues/secrets; `docs-reviewer` and `prose-value-reviewer` on prose; `prompt-reviewer` (with `prompt-token-efficiency-verifier`, `prompt-compression-verifier`) on prompts/skills/agents. Forward the manifest to every spawned reviewer when present.

**Narrow-lens reviewers.** Reviewer agents never receive PR conversation, linked-PR diffs, or linked-PR conversation. That context flows only to the holistic pass — narrow lens is what keeps each reviewer precise.

**Holistic coherence pass.** Collect findings from the fleet, drop Low severity, and spawn one subagent with what remains plus:

- PR history: recent review/conversation comments, all unresolved threads, the author's recent commit messages on the branch, the PR description.
- Bundle context for each linked PR: diff, description, top-level conversation. No inline review comments from linked PRs.
- The manifest if present.
- Any truncation the caller did, carried forward.

The subagent:

- **Prunes** findings already raised by another reviewer in the existing PR conversation, already discussed/conceded by the author, contradicting manifest intent, contradicted by the author's prior explanation in a comment / commit message / PR-description note, or piling on an active thread.
- **Dedupes** across reviewers: merge into one comment when same file + overlapping line range + same underlying concern.
- **Anchors** each surviving finding to exactly one of inline file:line (default), file-level (whole-file concern), or PR-level (cross-cutting, no specific anchor).
- **Rewrites** every comment body and any drafted reply in the voice profile below.
- **Omits a summary header by default** — adds one only when there's a real overall take the per-comment list misses (one short sentence, voice-compliant, no boilerplate).

Returns: comments to post (anchor + voice-compliant body), summary header text if any, truncation notes, and a brief dropped-findings tally with dominant reasons.

**Voice.** Each comment is one thought: state the problem, point to evidence inline (file:line, short code excerpt when load-bearing), suggest the fix. Direct, concrete, no softeners.

Never in a posted body, header, or thread reply: severity labels (`[High]`, `⚠️`, `Critical:`); emoji of any kind; em-dash rhetorical flourishes ("It's not just X — it's Y" / "not just A, but B"); softeners ("I think", "I recommend", "It seems", "Perhaps consider"); opener boilerplate ("Great PR!", "Nice change, but..."); "at the location above" / "as mentioned" (always name file:line inline); AI disclosure footer.

Structural defaults: prose, not bullets, for a single suggestion; no markdown headers or bold-the-takeaway when the comment is one thought. Headers and bullets are fine when a comment genuinely covers multiple distinct thoughts or parallel items.

Target voice: *"Empty input skips the null check — `if (input?.value)` at `parser.ts:42` short-circuits before the parse at `parser.ts:47`, so `{}` reaches `parse()` without the guard. Tighten to `if (input?.value != null)`, or move the `parse()` call inside the existing branch."*

**Posting.** When the holistic pass returns comments to post, present the plan for user approval (comments + anchors, what was loaded as context, any truncation, dropped-findings tally). On approval, submit a single GitHub PR review with decision `comment` — all comments batched atomically.

**Zero comments to post.** When the holistic pass returns nothing, skip plan presentation and ask via AskUserQuestion: `"Looks good to me. Post as approval on the PR?"`. Approve → submit decision `approve` with body `Looks good to me.`; decline → take no PR action. No PR action otherwise.

**Gotchas.**

- The only path to decision `approve` is the user-confirmed lgtm prompt above. Never submit `approve` automatically anywhere else.
- Never submit decision `request_changes` — this skill does not algorithmically block merges.
- Never add an AI disclosure footer to a comment, summary, or reply. There is no flag for one.
- Never forward PR conversation or bundle context to a reviewer agent. Only the holistic pass may see that context.
- Never re-raise a finding the holistic pass pruned in this run. When running under `--loop`, never re-raise in a later iteration something already in our own prior posted comments — dedupe via PR history.

**`--loop`.** Load `references/LOOP.md`.
