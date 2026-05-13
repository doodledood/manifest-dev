# Canvas Mode — Walk-PR Review Canvas

Loaded when `/walk-pr --canvas` is passed. This file owns the canvas behavior — when to fire, when to suppress, what to generate, how to keep it live, how to fail safely.

## Purpose

The user reads the chat as you walk each sub-changeset; the canvas is the visual side-channel that surfaces the **shape of the whole review at a glance** plus drill-in to any sub-changeset's before/after side-by-side. Categorized overview always visible; verbatim quotes, section mapping, and trade-offs live behind progressive disclosure (`<details>` expanders, tabs). The chat carries the conversation; the canvas carries the structure.

## Activation gate

Evaluate **immediately** when `--canvas` is set, before opening the first sub-changeset. If any condition holds, skip canvas behavior; continue /walk-pr normally (first match wins; conditions 1–2 silent, condition 3 prints one warning):

1. **Trivial diff** — single file, < 50 net lines changed. Canvas is overhead for a 30-second review. Silent skip.
2. **Non-local medium** — the user isn't at a host with browser access. Silent skip.
3. **No graphical-browser launcher** — none of `xdg-open`, `open`, `start` on PATH. Print: `--canvas requires a desktop environment with a graphical browser; skipping artifact generation`. Skip.

If none match: generate the initial canvas at `/tmp/walk-pr-canvas-{ts}.html` (`{ts}` = invocation timestamp), auto-open it, proceed with the walkthrough and regenerate per cadence below.

## Lifecycle

Live during the walkthrough. Updates after each sub-changeset is walked (or after a decision is captured in amendment-capture mode). Freezes when the user signals the walkthrough is complete or invokes `/do` to apply amendments.

First render is a minimal shell: PR title / diff scope banner, the categorized overview (sub-changesets with sizes and recommended order, each collapsed by default), an "Walkthrough in progress" affordance.

## Format

- **File:** single self-contained `.html` at `/tmp/walk-pr-canvas-{ts}.html`.
- **Styling:** Tailwind via CDN (`<script src="https://cdn.tailwindcss.com"></script>`). Degrades to semantic HTML if CDN unreachable.
- **Diagrams** (when useful): mermaid via CDN (`<script type="module">import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true });</script>`). Use `<pre class="mermaid">...</pre>` blocks for architectural diagrams when the change involves component flow.
- **Auto-reload:** embed JS that refreshes when the source file changes. Should preserve scroll position and expand/collapse state when feasible. Mechanism chosen once per session.
- **Self-contained:** no external assets beyond the two CDN scripts. Opens via `file://`. No local server.

## Update cadence

Regenerate after each **meaningful event**:

- A sub-changeset is opened (its expander auto-expands; status changes to "in review")
- A sub-changeset is closed (user thoughts captured, status changes to "reviewed" or "amendment captured")
- A decision is captured in amendment-capture mode
- The user's response to a probe lands a recommendation acceptance / change / new probe

Do NOT regenerate per agent turn. After auto-reload, call `mermaid.run()` to re-initialize diagrams.

## Auto-open

On first canvas creation: detect via `command -v xdg-open || command -v open || command -v start`. Use first available. Launcher failure → print path (`Canvas: file:///tmp/walk-pr-canvas-{ts}.html`), continue normally.

## Failure handling

Any canvas-related failure is **non-blocking**. Canvas is supplementary; the chat walkthrough is load-bearing. File write fails → warn once, continue. Browser launcher fails → print path, continue. Mermaid syntax error → emit as-is, continue. Any other failure → warn once, continue.

## What the surface must enable

Test: **at a glance, can the user grasp the shape of the whole review and the state of each sub-changeset without scrolling?**

Visible by default:
- **Review intent** — what PR/diff is being walked (PR number/URL or diff range, total stat).
- **Categorized overview** — sub-changesets with size + status badges (queued / in review / reviewed / decision-captured / pending). Recommended walk order indicated.
- **Current focus** — which sub-changeset is open right now, highlighted.

Behind progressive disclosure (per sub-changeset card):
- **Before / after side-by-side panels** — verbatim quotes from the original file and the new file (or per file in the sub-changeset), in two columns. Code blocks rendered with monospace + syntax-aware coloring where the file type permits.
- **Section-by-section mapping** — a table or list mapping original sections → new sections, with the verdict (survived / cut / moved-to-X) and the cut justification.
- **Net change** — lines, ratio, and a small bar visualizing the reduction.
- **Architectural probes** — open questions surfaced during walkthrough as a collapsed list, each one expandable to show the user's response and the resulting decision.
- **Captured amendments** (when amendment-capture mode is on) — each amendment as a numbered entry showing the change and the manifest path it was recorded to.

## Visual richness — what lands as comprehension-friendly

- **Sub-changeset cards** with status pills (`queued` slate, `in review` amber, `reviewed` emerald, `decision-captured` indigo). Click expands.
- **Side-by-side panels** for before/after — `grid grid-cols-2 gap-4`. Header row labels each side. Code rendered with light syntax styling — keep it readable, not flashy.
- **Mapping table** with three columns: Original → Verdict → New location. Color-code verdicts (survived green, cut gray, moved blue). Short cut-justification in a fourth column or as a tooltip on hover.
- **Net change bar** — small inline visualization (`<div class="h-2 bg-emerald-200 rounded">` width-proportional). Big reductions are visually arresting; trivial changes barely register.

## Anti-patterns

- **Wall of diff.** Don't dump the entire patch as monolithic text. Side-by-side panels per file inside the sub-changeset card; everything else collapsed.
- **Per-turn regeneration.** Updates fire after meaningful events, not every tool call.
- **Schema vocabulary on surface.** No "Acceptance Criteria", "Global Invariants" labels — those belong in manifests, not here. Talk about *what changed* and *why* in user vocabulary.
- **Re-skinned chat.** If the canvas reads as the same content the chat just said with different fonts, it has failed. Different role: chat = conversation, canvas = structure-at-a-glance + drill-in. The canvas surfaces the *map*; the chat carries the *decisions*.
- **Status-pill explosion.** Pills only on sub-changeset cards (the navigation surface). Don't sprinkle them on every detail row inside.
- **Diagram for nothing.** Mermaid only when the change involves component flow / architecture that's clearer drawn. A prose-heavy refactor doesn't need a diagram.

## Amendment-capture mode interaction

When `/walk-pr --amend <manifest-path>` is in effect, the canvas adds a footer section "Captured amendments" — a running list of decisions made during the walkthrough, each linkable to the corresponding manifest amendment block. The user can scan this footer at any time to see what /do will apply when the walkthrough closes. If the footer is empty, hide it; don't surface scaffolding.
