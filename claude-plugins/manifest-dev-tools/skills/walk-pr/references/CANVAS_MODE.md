# Canvas Mode — Walk-PR Review Canvas

Loaded when `/walk-pr --canvas` is passed. The canvas **is** the walkthrough — every surface (verbatim quotes, section mapping, trade-offs, probes, recommendations, per-topic comment input) lives in the HTML artifact, generated **once, upfront, with the full walk content**. The user navigates self-paced via local JS; chat reconnects only at the end, when the user pastes back a single bundled review result. After the walkthrough closes, the artifact is redundant.

## Activation gate

Evaluate **immediately** when `--canvas` is set, before opening the first sub-changeset. If any condition holds, skip canvas behavior and fall back to chat-only /walk-pr (first match wins; conditions 1–2 silent, condition 3 prints one warning):

1. **Trivial diff** — canvas setup cost (file write + render + browser open + auto-reload plumbing) exceeds the review's information need. Rough threshold: single file with tens of net lines changed.
2. **Non-local medium** — the user isn't at a host with browser access.
3. **No graphical-browser launcher** — none of `xdg-open`, `open`, `start` on PATH. Print: `--canvas requires a desktop environment with a graphical browser; skipping artifact generation`.

If none match: generate the canvas at `/tmp/walk-pr-canvas-{ts}.html` (`{ts}` = invocation timestamp), auto-open it, proceed.

## Cognitive-load contract

The canvas rations what the user sees at any moment. Three rules govern visibility:

1. **One sub-changeset in focus.** Exactly one expanded; others show title + size + status pill (`queued` slate, `in review` amber, `reviewed` emerald), collapsed.
2. **One review topic in view.** Inside the in-focus sub-changeset, exactly one topic (probe / trade-off / recommendation) is highlighted with its comment textarea visible. Prior topics collapse to a one-line preview of what the user typed (read from the textarea). Future topics show titles only, dimmed.
3. **No content duplication.** Walkthrough content lives in the canvas — not echoed in chat. Chat stays empty during the walk and receives only the final bundled paste.

Pacing is local — the canvas advances via JS (expand/collapse, "next topic", "mark reviewed") as the user works through it. There's no agent-side state to track until paste-back.

## Interaction model

**One-shot generation.** At creation, the agent embeds **every** sub-changeset, **every** review topic, and the full walk content (verbatim quotes, mappings, trade-offs, probes, recommendations) into the HTML. No per-topic Copy buttons, no anchor-format paste-back, no canvas regeneration mid-walk — those were artifacts of a per-turn design the user never actually used.

Each topic renders:
- A short statement (probe / trade-off / recommendation text, plus the recommended call where applicable).
- A `<textarea>` for the user's comment. State persists across canvas reloads (e.g. `localStorage` keyed by topic id) so the user doesn't lose work.

At the bottom of the canvas, a single **Copy as prompt** button writes the consolidated review result to the clipboard as one structured block — per sub-changeset, per topic: the anchor (file + line range or PR-level) plus the user's textarea content (or `(captured, no comment)` if empty). The user pastes this block into chat; the agent reads it and proceeds with the end-of-walk handoff.

Clipboard write uses `navigator.clipboard.writeText` with a `document.execCommand('copy')` fallback for sandboxed `file://` cases. On any clipboard failure, pre-select the bundled string in a visible read-only `<pre>` so the user can copy manually.

## Format

- **File:** single self-contained `.html` at `/tmp/walk-pr-canvas-{ts}.html`.
- **Styling:** Tailwind via CDN (`<script src="https://cdn.tailwindcss.com"></script>`). Degrades to semantic HTML if unreachable.
- **Diagrams** (when useful): mermaid via CDN. Use `<pre class="mermaid">...</pre>` only when the change involves component flow that's clearer drawn.
- **Auto-reload:** embed JS that refreshes if the source file changes. Preserve scroll position, expand/collapse state, and textarea contents across reloads (`localStorage`).
- **Self-contained:** no external assets beyond the small set of CDN scripts (Tailwind, mermaid, diff renderer, syntax-highlighter — see below). Opens via `file://`. No local server.

## Rendering and layout adapt to the content

Use the representation that fits each piece of content. This is the second half of the cognitive-load contract — visual rationing controls *how much* the user sees; content-shaped rendering controls *how legibly* it lands.

- **Diffs render as diffs.** Line-level hunks with additions / deletions / context, colored (green / red / muted), not monolithic raw text. Use a CDN-loaded diff library (e.g. `diff2html`) or render server-side as styled `<span>` per line — either is fine; the contract is "looks like a diff, not a `<pre>` dump".
- **Code renders with syntax highlighting.** Highlight.js or Prism via CDN, language inferred from file extension. Applies inside diff hunks where the library supports it, and to any standalone code excerpts in mappings or probes.
- **Layout adapts to the change.** Not every sub-changeset gets the same shape. A move / refactor benefits from side-by-side panels. A pure deletion is a one-line summary, not an empty "after" panel. A config or small data change is a tight grid or table. An architectural shift may warrant a mermaid sketch instead of (or alongside) diffs. Pick the layout that lowers load for *this* change, not a uniform template.

## Lifecycle

Generate once, freeze. The canvas is a fully self-contained snapshot:

- Initial render contains every sub-changeset and every topic; state lives in-browser (expand/collapse, "current topic", persisted textareas).
- Auto-reload fires only if the source file changes — e.g. the user asks the agent to regenerate from scratch. Scroll position, expand/collapse state, and textarea contents are preserved across reloads.
- After auto-reload, call `mermaid.run()` to re-initialize diagrams.

The agent disengages after generating the canvas and re-engages only when the user pastes the bundled review result.

## End-of-walk: paste, draft, post

When the user clicks **Copy as prompt** and pastes the bundle into chat, the agent has the full set of topic responses. It then:

1. Synthesizes review-comment prose from each non-empty textarea — line-anchored where the topic ties to a specific code location, file-level or PR-level otherwise. Captured-no-comment items appear in the plan summary as `captured — no comment` but generate no PR comment.
2. Calls `ExitPlanMode` with the plan-of-comments as the proposed plan.
3. On approval, posts the comments as a single PR review using available GitHub tools (`gh pr review` / `mcp__github__pull_request_review_write` / API).

After posting, the canvas is redundant. Whether and how the PR's author addresses the comments is the manifest workflow's job, not /walk-pr's.

## Failure handling

Any canvas-related failure is **non-blocking**:

- File write fails → warn once, fall back to chat-only walkthrough.
- Browser launcher fails → print path (`Canvas: file:///tmp/walk-pr-canvas-{ts}.html`), continue.
- Clipboard write fails → pre-select the bundled string in a visible block; show a one-line hint.
- Mermaid syntax error → emit as-is, continue.
- PR-post failure → keep the drafted plan, surface the API error inline, offer retry.

## Anti-patterns

- **Chat duplicating canvas content.** Don't restate verbatim quotes, mappings, trade-offs, probes, or topic text in chat. The canvas is the surface; chat only sees the final bundled paste.
- **Mid-walk regeneration.** The canvas is one-shot. Don't update it as the user works through topics — local JS handles pacing.
- **Per-topic Copy buttons or anchor-format paste-back.** Single end-of-walk bundle only. Per-topic round-trips are the failure mode we removed.
- **Wall of diff.** Don't dump entire patches as monolithic `<pre>` text. Render diffs as proper line-level hunks per file inside the in-focus card; everything else collapsed.
- **Uniform layout template.** Forcing every sub-changeset into side-by-side panels regardless of what the change actually is — empty "after" columns for deletions, grids of identical lines for renames, etc. Match the layout to the change.
- **Status-pill explosion.** Pills only on sub-changeset cards (the navigation surface).
- **Diagram for nothing.** Mermaid only when component flow is at stake.
- **Internal vocabulary on surface.** Talk about *what changed* and *why* in user vocabulary; no leaked internal labels (schema names, anchor formats in headings, etc.).
