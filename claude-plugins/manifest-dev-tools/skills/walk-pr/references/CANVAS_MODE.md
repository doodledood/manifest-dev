# Canvas Mode — Walk-PR Review Canvas

Loaded when `/walk-pr --canvas` is passed. In this mode the canvas **is** the walkthrough — every walkthrough surface (verbatim quotes, section mapping, trade-offs, probes, recommendations, per-topic comment input) lives in the HTML artifact, and chat acts as paste-transport. The user reads the canvas, types a comment in the awaiting topic's textarea, clicks **Copy as prompt** to copy an anchored string, pastes it into chat. The agent processes the response, regenerates the HTML, the canvas advances. After the walkthrough closes, the artifact is redundant.

## Activation gate

Evaluate **immediately** when `--canvas` is set, before opening the first sub-changeset. If any condition holds, skip canvas behavior and fall back to chat-only /walk-pr (first match wins; conditions 1–2 silent, condition 3 prints one warning):

1. **Trivial diff** — single file, < 50 net lines changed. Canvas is overhead for a 30-second review.
2. **Non-local medium** — the user isn't at a host with browser access.
3. **No graphical-browser launcher** — none of `xdg-open`, `open`, `start` on PATH. Print: `--canvas requires a desktop environment with a graphical browser; skipping artifact generation`.

If none match: generate the initial canvas at `/tmp/walk-pr-canvas-{ts}.html` (`{ts}` = invocation timestamp), auto-open it, proceed.

## Cognitive-load contract

The canvas rations what the user sees at any moment. Three rules govern visibility:

1. **One sub-changeset in focus.** Exactly one expanded; others show title + size + status pill (`queued` slate, `in review` amber, `reviewed` emerald), collapsed.
2. **One review topic awaiting input.** Inside the in-focus sub-changeset, exactly one topic (probe / trade-off / recommendation) is highlighted with its comment textarea visible and a *Copy as prompt* button. Prior topics show collapsed with a one-line summary of what the user said. Future topics show titles only, dimmed.
3. **No content duplication.** Walkthrough content lives in the canvas — not echoed in chat. Chat carries only the user's pasted responses and the agent's short coordination acknowledgments.

This is the visual fix for the "throw everything on screen, ask at the end" failure mode. Agent pacing alone doesn't solve it — what's expanded shapes load regardless of what chat says.

## Interaction model

Each *awaiting* topic renders:
- A short statement of the topic (probe / trade-off / recommendation text, plus the recommended call where applicable).
- A `<textarea>` for the user's comment.
- A **Copy as prompt** button that writes an anchored string to the clipboard, formatted as:

  ```
  [walk-pr / sub-changeset "<short title>" / <kind>: "<short topic title>"]

  <textarea content, or `(captured, no comment)` if empty>
  ```

The user pastes the string into chat. The agent recognizes the anchor prefix, identifies which topic the response addresses, treats non-empty content as a **comment candidate** and empty content as **captured, no comment**, regenerates the canvas with that topic captured and the next one promoted to awaiting. When the user replies in chat without the anchor, the agent maps the response to the currently-awaiting topic by context — anchor recognition is permissive, not strict.

Clipboard write uses `navigator.clipboard.writeText` with a `document.execCommand('copy')` fallback for sandboxed `file://` cases. Any clipboard failure pre-selects the anchored string in a visible read-only `<pre>` so the user can copy manually.

## Format

- **File:** single self-contained `.html` at `/tmp/walk-pr-canvas-{ts}.html`.
- **Styling:** Tailwind via CDN (`<script src="https://cdn.tailwindcss.com"></script>`). Degrades to semantic HTML if unreachable.
- **Diagrams** (when useful): mermaid via CDN. Use `<pre class="mermaid">...</pre>` only when the change involves component flow that's clearer drawn.
- **Auto-reload:** embed JS that refreshes when the source file changes. Preserve scroll position and the expand/collapse state of non-focused sub-changeset cards across reloads.
- **Self-contained:** no external assets beyond the two CDN scripts. Opens via `file://`. No local server.

## Lifecycle

Live during the walkthrough, freezes when the walkthrough closes. Regenerate after each **meaningful event**, not every agent turn:

- A sub-changeset opens (its card expands; status → "in review"; its first review topic becomes awaiting).
- The user's pasted response lands (current topic captures the response and collapses with a one-line summary; next topic becomes awaiting; or, if topics exhausted, the sub-changeset → "reviewed" and the next one opens).
- All sub-changesets are reviewed → render the **end-of-walk plan section** (see below).

After auto-reload, call `mermaid.run()` to re-initialize diagrams.

## End-of-walk: plan-of-comments

When all sub-changesets are reviewed, the canvas adds a final section: **Comments to post.** Each entry shows:
- Which sub-changeset / topic it came from.
- The anchor — file + line range where the topic ties to a specific code location, file-level or PR-level otherwise.
- A drafted comment body (the agent synthesizes review-comment prose from the user's textarea content).
- Captured-no-comment items list separately, dimmed, as `captured — no comment`.

The agent then calls `ExitPlanMode` with the plan-of-comments as the proposed plan. On approval, the agent posts the comments as a single PR review using available GitHub tools (`gh pr review` / `mcp__github__pull_request_review_write` / API). On success, the canvas section flips to `posted` with links to the live PR comments — at which point the artifact is redundant. Whether and how the PR's author addresses the comments is the manifest workflow's job, not /walk-pr's.

## Failure handling

Any canvas-related failure is **non-blocking**. The canvas is the primary surface in this mode, but failures fall back gracefully:

- File write fails → warn once, fall back to chat-only walkthrough.
- Browser launcher fails → print path (`Canvas: file:///tmp/walk-pr-canvas-{ts}.html`), continue.
- Clipboard write fails → pre-select the anchored string in a visible block; show a one-line hint.
- Mermaid syntax error → emit as-is, continue.
- PR-post failure at end of walk → keep the plan section, surface the API error inline, offer retry.

## Anti-patterns

- **Chat duplicating canvas content.** Don't restate verbatim quotes, mappings, trade-offs, probes, or topic text in chat. The canvas is the surface; chat is paste-transport.
- **Per-turn regeneration.** Updates fire on meaningful events, not every tool call.
- **Wall of diff.** Don't dump the entire patch as monolithic text. Before/after side-by-side panels per file inside the in-focus card; everything else collapsed.
- **Status-pill explosion.** Pills only on sub-changeset cards (the navigation surface).
- **Diagram for nothing.** Mermaid only when component flow is at stake.
- **Schema vocabulary on surface.** Talk about *what changed* and *why* in user vocabulary; no manifest schema labels.
