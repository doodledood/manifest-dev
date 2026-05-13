---
name: walk-pr
description: 'Walk through a PR or large diff together, one sub-changeset at a time. Verbatim quotes from both sides, section-by-section mapping of what survived / cut / moved, honest trade-offs with a recommended call, pause between groups for input. Optional --amend captures decisions to a manifest for later /do; --canvas presents the review as a live HTML side-channel. Use when reviewing a substantive PR collaboratively or walking a large refactor. Triggers: walk pr, walk diff, walk me through, pr walkthrough, review collaboratively, review this change with me.'
user-invocable: true
---

Walk the user through a PR or large diff **one sub-changeset at a time** — a group of files that makes sense together. Open with a categorized overview (load-bearing changes vs copies / data, recommended order biggest-signal-first); skip on trivial diffs. For each sub-changeset: show **verbatim quotes from both sides** — never paraphrased — map section-by-section what survived / cut / moved with each cut justified, report net change, pause for the user's thoughts. Probe architectural questions, not just mechanical change. Recommend a call with each trade-off; the user decides. Hold positions under pushback when evidence still supports them.

**Modes.** `--amend <manifest-path>` (or chat-derived *"amend as we go"*) records each decision as an amendment block in the manifest instead of editing files in place — apply at the end via /do. `--canvas` loads `references/CANVAS_MODE.md` for a live HTML side-channel where the chat carries the conversation and the canvas carries the structure-at-a-glance. **Input** = PR number, PR URL, diff range, or nothing (infer current branch's PR via `gh pr view`, falling back to `origin/main..HEAD`).
