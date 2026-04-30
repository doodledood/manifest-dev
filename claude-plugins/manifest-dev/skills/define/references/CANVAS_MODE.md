# Canvas Mode — Shared Understanding Canvas

This file is loaded only when `--canvas` is active and the host environment supports it. It owns the operational specification of the Shared Understanding Canvas — what to generate, when to update it, how to open it, and how to handle failures. SKILL.md owns the suppression logic (when this file is loaded vs not); this file does not re-evaluate those conditions.

## Why a canvas exists

/define produces two artifacts that serve two readers:

- The **Manifest** (`/tmp/manifest-{ts}.md`) is dense, structured, machine-readable. It exists for `/do`, `/verify`, and downstream agents. It is precise but cognitively expensive for a human to read end-to-end.
- The **Canvas** (`/tmp/canvas-{ts}.html`) is the human-facing reflection of that same shared understanding. It absorbs the translation work the agent does natively on formal structure — so the user reviews by *looking* at a layered visual surface rather than by *parsing* hundreds of lines of YAML.

Both artifacts encode the same understanding. The manifest is the source of truth; the canvas is the comprehension instrument.

## Principles

The canvas earns its keep by reducing the cognitive cost of grasping what's being built. Three principles guide every generation and update:

1. **Comprehension over completeness.** Optimize for "the user grasps the shape in 30 seconds" before "every detail is on screen." A canvas where every AC is visible but nothing reads beats nothing — but a canvas where the user instantly sees the high-level intent, the pieces, and how they relate beats both. Density is the enemy.

2. **Layered reveal.** The architecture, intent, and high-level flow are immediate — visible without interaction. Detail (individual ACs, invariants, decision rationale, edge cases) is one expand/click/tab away. The user is never blocked from drilling in, but is never overwhelmed on first read either.

3. **Visual where flow exists, prose where it doesn't.** Diagrams carry meaning faster than words for relationships, sequences, before/after states, and dependencies. Reach for diagrams in those cases. Use prose for declarative content (intent, rationale, scope notes) where flow doesn't apply. Don't substitute a bullet list where a picture would carry the meaning more cheaply.

## Format requirements

- **File:** A single self-contained `.html` file at `/tmp/canvas-{ts}.html`, where `{ts}` is the same timestamp as the manifest (`/tmp/manifest-{ts}.md`) and discovery log (`/tmp/define-discovery-{ts}.md`). Linkable as a triplet.
- **Styling:** Tailwind CSS via CDN (`<script src="https://cdn.tailwindcss.com"></script>`). Tailwind degrades gracefully — if the CDN is unreachable, the page is still readable as semantic HTML.
- **Diagrams:** mermaid via CDN (`<script type="module">import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true });</script>`). Use mermaid blocks (`<pre class="mermaid">...</pre>`) for flowcharts, sequence diagrams, dependency graphs.
- **Auto-reload:** Embed JavaScript that detects when the source file has changed and refreshes the visible content. The mechanism is the agent's choice (JS polling against a version-stamped fragment, fetch + DOM diff, `<meta http-equiv="refresh">`, etc.) — pick what works in the target browser. The principle: page must auto-reload when the file changes, and SHOULD preserve scroll position and expand/collapse state when feasible. The mechanism is chosen ONCE at generation time per /define session and embedded in the file; it does not change mid-interview.
- **Self-contained:** No external assets beyond the two CDN scripts above. No local server is started. The file opens via `file://`.

## Update cadence

The canvas regenerates after each **meaningful event** — defined as anything that changes the substance of the manifest or the user's understanding of the work. Specifically:

- Each interview-cluster checkpoint (when the agent synthesizes its current understanding back to the user)
- Each coverage-goal resolution (Domain Understanding, Reference Class, Failure Modes, Positive Dependencies, Process Self-Audit)
- Each addition or modification of an AC, INV, PG, ASM, R, or T
- Each Approach-section update (Architecture, Execution Order, Risk Areas, Trade-offs)
- Each scope-guard or trade-off lock-in

The canvas does **not** regenerate after every agent turn or every tool call. Per-turn updates are noise — the user's mental picture should change in step with the manifest's substance, not every time the agent thinks. If a cluster of small changes lands together, regenerate once at the end of the cluster.

## Auto-open

On first canvas creation, open it in the user's default browser via the first available of:

```
xdg-open /tmp/canvas-{ts}.html    # Linux
open /tmp/canvas-{ts}.html        # macOS
start /tmp/canvas-{ts}.html       # Windows / WSL
```

Detect via `command -v xdg-open || command -v open || command -v start` and use the first one that exists. Subsequent updates (regenerations) do **not** re-open — the embedded auto-reload mechanism in the already-open tab handles refresh.

If the launcher command fails (e.g., no display), print the path to the user (`Canvas: file:///tmp/canvas-{ts}.html`) and continue with the normal /define flow. Auto-open failure is never a blocker.

## Failure handling

Any canvas-related operation failure is non-blocking. The canvas is supplementary; the manifest is load-bearing. Specifically:

- File write fails (disk full, permissions): print one warning (`Canvas write failed: <reason>`), continue /define normally.
- Browser launcher fails: print the file path, continue /define normally.
- Mermaid syntax error in generated content: emit the canvas as-is (mermaid blocks render an error in the page itself), continue /define normally.
- **All other canvas failures** — including partial/mid-generation errors, malformed content, model errors during HTML generation, or any unanticipated condition: warn once, continue. Never raise into the /define workflow.

The user's manifest workflow is never blocked by a canvas failure.

## Illustrative content menu

Consider including any of the following in the canvas when they serve the task. **None are required.** The agent picks what fits — a small bug-fix manifest may need only Intent + Deliverable Cards; a multi-component refactor may use most of the menu. The principle is comprehension, not coverage.

- **High-level intent banner** — one or two sentences capturing what's being built and why. Always near the top.
- **Process flows (before / after)** — when the change modifies existing behavior, a side-by-side flow showing what happens today vs what will happen. Mermaid `flowchart` or `sequenceDiagram` works well.
- **Mental model diagram** — how the user should think about the system after the change. Components, their roles, how they relate. Often a simple boxes-and-arrows diagram.
- **Component / dependency relationships** — for changes spanning multiple files or services, show what depends on what. Prevents the user from missing an affected consumer.
- **Deliverable cards with AC checkpoints** — each deliverable as a visual card; ACs as collapsible items underneath. The user sees deliverables at a glance and expands for detail.
- **Decision tree / trade-off comparison** — when the interview surfaced branching choices, show the options considered and which path was taken. Exposes assumptions for review.
- **"What changes" callouts** — for amendments or modifications to existing code, highlight what's being added, removed, or replaced. Often a colored diff-style block.
- **Risk panel** — surfaces R-* with detection criteria. A quick "what could go wrong, how would we know."
- **Scope-out list** — explicit "this is NOT in scope" items. Prevents the user from assuming the manifest covers more than it does.

The menu is a starting point — if the task suggests a content type not listed (e.g., a state machine for a stateful workflow), include it. Conversely, if a listed type doesn't serve the task, omit it.

## What "visual richness" looks like

Below are illustrative fragments showing the kind of visual structure that lands as comprehension-friendly. **These are examples of what richness looks like, not required structures.** The agent's canvas may use these patterns or invent its own; the goal is grasp-ability, not template conformance.

### Example: high-level flow as mermaid

```html
<section class="my-8">
  <h2 class="text-xl font-semibold mb-4">How --canvas fits into /define</h2>
  <pre class="mermaid">
flowchart LR
  U[User runs /define --canvas] --> C{Env supports?}
  C -->|Yes| G[Generate canvas]
  C -->|No| W[Warn and skip]
  G --> O[Auto-open in browser]
  O --> I[Interview proceeds]
  I -->|Each meaningful event| R[Regenerate canvas]
  R --> I
  I -->|Approval| F[Canvas frozen]
  </pre>
</section>
```

### Example: deliverable card with collapsible ACs

```html
<details class="border rounded-lg p-4 my-3 bg-slate-50">
  <summary class="font-semibold cursor-pointer">D1 — Create CANVAS_MODE.md</summary>
  <ul class="mt-3 space-y-2 text-sm text-slate-700">
    <li>AC-1.1: Intro frames canvas as comprehension instrument</li>
    <li>AC-1.2: Three principles (comprehension, layered reveal, visual-where-flow)</li>
    <li>AC-1.3: Illustrative content menu, framed as suggestions</li>
    <li>...</li>
  </ul>
</details>
```

### Example: side-by-side before/after

```html
<div class="grid grid-cols-2 gap-4 my-6">
  <div class="border-l-4 border-slate-400 pl-4">
    <h3 class="font-semibold">Today</h3>
    <p>/define produces only the manifest. Users review by reading 800 lines of YAML.</p>
  </div>
  <div class="border-l-4 border-emerald-500 pl-4">
    <h3 class="font-semibold">With --canvas</h3>
    <p>/define produces manifest + visual canvas. Users review by looking and clicking to drill in.</p>
  </div>
</div>
```

These patterns share a property: they expose structure visually before any text is read. A user scanning quickly grasps "there are deliverables," "this is the flow," "this is the difference" before deciding where to drill in.

## Style notes

- Default to a calm palette (slate / neutral grays for chrome, an accent color for highlights). Avoid loud styling that distracts from content.
- Use whitespace generously. Cramped layouts increase cognitive cost — the opposite of the canvas's purpose.
- Headings establish hierarchy; bold for emphasis within paragraphs. Avoid heavy use of all-caps or italics.
- For long content sections, prefer collapsible (`<details>`) over walls of text.
- Re-render mermaid after auto-reload updates content (`mermaid.run()` or equivalent) — diagrams need re-initialization when the DOM changes.

## Anti-patterns

- **Re-skinned manifest.** If the canvas reads as the same content as the manifest with different fonts, it has failed. The canvas should look and feel different — visual where the manifest is textual.
- **Tidy-outline syndrome.** Headers, bullets, more headers, more bullets. The canvas should reach for diagrams, cards, panels, side-by-side comparisons, expand/collapse — not just prettier prose.
- **Wall of ACs.** Listing every AC inline at the top level defeats layered reveal. Cards with collapsible details are nearly always better.
- **Per-turn regeneration.** Updates fire after meaningful events, not after every tool call. Constant page flicker undermines the "live alongside understanding" feel.
