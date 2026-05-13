# Canvas Mode — Shared Understanding Canvas

Loaded when `/define` is invoked with `--canvas`. This file owns canvas behavior — when to fire, when to suppress, what to generate, how to keep it live, how to fail safely.

## Purpose

The user reads the chat; the canvas is the visual side-channel they glance at to spot *"that's not what I meant"* on the high-level shape: intent, flow, scope. Misalignment caught during the interview is cheap; the same misalignment surfacing during /do or after a feature ships is expensive. The canvas re-expresses the manifest's ideas in plain language — **never** schema vocabulary, never AC/INV-G/PG IDs.

## Activation gate

Evaluate **immediately** — before Domain Guidance and the interview begin. If any condition holds, skip canvas behavior; continue /define normally (first match wins; conditions 1–3 silent, condition 4 prints one warning):

1. **Amendment mode active.** Canvas is fresh-/define-only. Active via: literal amendment trigger from chat/transcript, Session-Default Detection resolved to "Related", or input args reference a `/tmp/manifest-*.md` path.
2. **Invoked autonomously** (e.g., `--autonomous`, `/auto`). No human reviewer in the loop → canvas is wasted tokens.
3. **Non-local medium.** Only `local` supported currently; non-local skip is anticipatory.
4. **No graphical-browser launcher** — none of `xdg-open`, `open`, `start` on PATH. Print: `--canvas requires a desktop environment with a graphical browser; skipping artifact generation`. Skip.

If none match: generate the initial canvas at `/tmp/canvas-{ts}.html` (same `{ts}` as the manifest), auto-open it, proceed with /define and regenerate per cadence. At the Summary for Approval step, append one line to the chat summary: `Canvas: file:///tmp/canvas-{ts}.html` — only if the file was successfully written.

## Lifecycle

Generated and updated only during /define's interview phase. Freezes at user approval. `/do` never touches the canvas. First render is a minimal shell (intent banner + "Interview in progress" affordance + empty scaffold).

## Format

- **File:** single self-contained `.html` at `/tmp/canvas-{ts}.html`. Linkable as a triplet with manifest + discovery log.
- **Styling:** Tailwind via CDN (`<script src="https://cdn.tailwindcss.com"></script>`). Degrades to semantic HTML if CDN unreachable.
- **Diagrams:** mermaid via CDN (`<script type="module">import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true });</script>`). Use `<pre class="mermaid">...</pre>` blocks.
- **Auto-reload:** embed JS that refreshes when the source file changes. Mechanism is agent's choice (JS polling, fetch + DOM diff, `<meta http-equiv="refresh">`). Should preserve scroll position and expand/collapse state when feasible. Mechanism chosen once per session.
- **Self-contained:** no external assets beyond the two CDN scripts. Opens via `file://`. No local server.

## Update cadence

Regenerate after each **meaningful event** — anything that changes the substance of the manifest or the user's understanding:

- Interview-cluster checkpoints (agent synthesizes back to user)
- Coverage-goal resolutions
- AC / INV / PG / ASM / R / T additions or modifications
- Approach-section updates (Architecture / Execution Order / Risk Areas / Trade-offs)
- Scope-guard or trade-off lock-ins

Cluster of small changes → regenerate once at the end. Do NOT regenerate per agent turn or per tool call. After auto-reload, call `mermaid.run()` or equivalent to re-initialize diagrams.

## Auto-open

On first canvas creation: detect via `command -v xdg-open || command -v open || command -v start`. Use first available:

```
xdg-open /tmp/canvas-{ts}.html    # Linux
open /tmp/canvas-{ts}.html        # macOS
start /tmp/canvas-{ts}.html       # Windows / WSL
```

Subsequent updates do NOT re-open — auto-reload handles refresh. Launcher failure → print path (`Canvas: file:///tmp/canvas-{ts}.html`), continue normally.

## Failure handling

Any canvas-related failure is **non-blocking**. The canvas is supplementary; the manifest is load-bearing. File write fails → warn once (`Canvas write failed: <reason>`), continue. Browser launcher fails → print path, continue. Mermaid syntax error → emit as-is (page renders the error inline), continue. Any other failure → warn once, continue. Never raise into the /define workflow.

## What the surface must enable

The user looks at the canvas to spot misalignment. Test: **at a glance, can the user detect "that's not what I meant" on the things people most often disagree about?**

People disagree predictably about three things:
- **Intent** — what's being built, in plain language. Always immediate.
- **Flow** — sequence, branches, before/after, dependencies. The visual that most exposes misalignment for *this* task: flowchart for sequence changes, before/after panels for behavioral changes, architecture sketch for component-level work, dependency graph for cross-cutting, state diagram for stateful workflows. Pick per task. When task has no genuine flow (one-line text fix, rename, copy edit), don't force one — prose is right.
- **Scope** — what's in, what's deliberately out. Callout or short bordered list.

Everything else (acceptance specifics, decision rationale, risk drilldowns, edge cases, work-item drill-ins) lives behind progressive disclosure (`<details>` expanders, tabs, click-to-reveal). Detail is one click away, never zero.

## Anti-patterns

- **Re-skinned manifest.** If the canvas reads as the same content with different fonts, it has failed. Different look-and-feel: visual where the manifest is textual.
- **Tidy-outline syndrome.** Headers + bullets + more headers + more bullets is just prettier prose. Reach for diagrams, cards, panels, side-by-side comparisons, expand/collapse.
- **Wall of acceptance details.** Cards with collapsible details beat inline at top level.
- **Per-turn regeneration.** Updates fire after meaningful events, not every tool call.
- **Schema vocabulary on surface.** No "Acceptance Criteria", "Global Invariants", "Process Guidance", "Risk Areas", "Trade-offs" labels. Talk about *what we're building*, *how it works*, *what's in/out of scope*, *what could go wrong* — in user vocabulary.
- **Formalism in expanders.** Scrub applies everywhere on the canvas, not just the visible-by-default surface. Detail behind `<details>` is still ideas in plain language, never IDs or schema labels.
- **Paragraph where a visual would land.** Relationships, sequence, before/after, dependencies, branching → diagram. If you find yourself writing more than a few sentences about how things relate, a diagram would carry it more cheaply.
