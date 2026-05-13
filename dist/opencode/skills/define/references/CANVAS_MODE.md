# Canvas Mode — Shared Understanding Canvas

You are reading this file because the user passed `--canvas` to /define. SKILL.md only does the flag check and routes here; **this file owns the entire canvas behavior** — when to fire, when to suppress, what to generate, how to keep it live, how to fail safely, when to stop.

## Why this exists — shared-understanding alignment

`/define` produces two artifacts that serve two readers.

The **Manifest** (`/tmp/manifest-{ts}.md`) is the formal downstream encoding of the shared understanding the interview produced. It exists for `/do`, `/verify`, and downstream agents — dense, structured, machine-readable. Precise, and necessarily formal.

The **Canvas** (`/tmp/canvas-{ts}.html`) is the human-facing reflection of that same understanding, expressed in the **ideas and decisions** the manifest formally encodes — in plain language, visual where possible, scanned at a glance.

**The canvas's job is alignment.** The user is engaged in the chat interview — that's where their attention sits. The canvas is the visual side-channel they glance at to spot *"wait, that's not what I meant"* on the high-level shape: the intent, the flow, the scope. Misalignment caught early during the interview is cheap; the same misalignment surfacing later — during /do, in PR review, after a feature ships — is expensive. Helping the user catch it at a glance is what the canvas is for.

This framing is load-bearing. The principles, the surface contract, the visual richness, and the anti-patterns below all subordinate to it. **Manifest formalism — IDs like AC-1.1 or INV-G3, schema section names like "Acceptance Criteria" or "Global Invariants", YAML verify blocks, the Mode/Interview/Medium metadata line — belongs in the manifest, not the canvas.** The canvas re-expresses the same ideas in plain language, surface and expanders alike. Formalism is forbidden anywhere on the canvas; it never enables alignment, only friction.

## Principles

The canvas earns its keep by reducing the cognitive cost of grasping what's being built. Three principles guide every generation and update — each in service of the alignment job above:

1. **Comprehension over completeness.** Optimize for "the user grasps the shape in 30 seconds" before "every detail is on screen." A canvas where every acceptance detail is visible but nothing reads beats nothing — but a canvas where the user instantly sees the intent, the pieces, and how they relate beats both. Density is the enemy of misalignment-spotting.

2. **Layered reveal.** The intent, the high-level flow, and the scope are immediate — visible without interaction. Detail (acceptance specifics, invariants, decision rationale, edge cases) is one expand/click/tab away. The user is never blocked from drilling in, but is never overwhelmed on first read either.

3. **Visual where flow exists, prose where it doesn't.** Diagrams carry meaning faster than words for relationships, sequences, before/after states, and dependencies. Reach for diagrams in those cases. Use prose for declarative content (intent, rationale, scope notes) where flow doesn't apply. Don't substitute a bullet list where a picture would carry the meaning more cheaply — and conversely, don't force a diagram where there's no genuine relationship to draw.

## Activation gate

Evaluate **immediately** — before Domain Guidance and the interview begin. The canvas tab must be open and ready before the user starts answering questions. If any of the following hold, skip canvas behavior entirely and continue /define normally (first match wins; conditions 1–3 are silent, condition 4 prints one warning):

1. **Amendment mode is active.** Canvas is fresh-/define-only. Amendment is "active" via three paths: (a) literal `--amend` was passed, (b) Session-Default Detection resolved to amendment ("Related" branch — note: "Truly unrelated" and "Prior manifest unreadable" branches proceed FRESH and DO get a canvas), or (c) input arguments referenced a specific `/tmp/manifest-*.md` path that will be amended. Silent skip. Edge case: when "Related" fires, control diverts to AMENDMENT_MODE.md and this gate may not be re-evaluated explicitly — outcome is incidentally correct because amendment flow contains no canvas-generation step.

2. **`--interview autonomous`** (transitively covers `/auto` — `/auto` always passes `--interview autonomous` to /define; no separate `/auto` check needed). The canvas's value is live human review; without a human reviewer, it's wasted tokens. Silent skip.

3. **Resolved `--medium` is anything other than `local`.** Anticipatory: only `local` is currently supported and the Input section halts on non-local mediums at parse time, so this is dormant in practice. Generalizes to any future medium where the user lacks host-browser access (e.g., `--medium slack`). Silent skip.

4. **No graphical-browser launcher available** — none of `xdg-open`, `open`, or `start` is on PATH. Print one line: `--canvas requires a desktop environment with a graphical browser; skipping artifact generation`. Then skip.

If none match, the canvas is genuinely active: generate the initial canvas at `/tmp/canvas-{ts}.html` (same `{ts}` as the manifest), auto-open it, then proceed with the rest of /define and regenerate per the cadence below. At the Summary for Approval step, append one line to the chat summary: `Canvas: file:///tmp/canvas-{ts}.html` — but only if the canvas file was actually written (skip the line if any write failed; pointing the user at a non-existent file is worse than no link).

## Lifecycle

Canvas is generated and updated only during /define's interview phase. It freezes at user approval. `/do` never touches the canvas — no regeneration, extension, or annotation by `/do` or any downstream skill. The first render is intentionally a minimal shell (see Update cadence below).

## Format requirements

- **File:** A single self-contained `.html` file at `/tmp/canvas-{ts}.html`, where `{ts}` is the same timestamp as the manifest (`/tmp/manifest-{ts}.md`). Linkable as a pair.
- **Styling:** Tailwind CSS via CDN (`<script src="https://cdn.tailwindcss.com"></script>`). Tailwind degrades gracefully — if the CDN is unreachable, the page is still readable as semantic HTML.
- **Diagrams:** mermaid via CDN (`<script type="module">import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs"; mermaid.initialize({ startOnLoad: true });</script>`). Use mermaid blocks (`<pre class="mermaid">...</pre>`) for flowcharts, sequence diagrams, dependency graphs.
- **Auto-reload:** Embed JavaScript that detects when the source file has changed and refreshes the visible content. The mechanism is the agent's choice (JS polling against a version-stamped fragment, fetch + DOM diff, `<meta http-equiv="refresh">`, etc.) — pick what works in the target browser. The principle: page must auto-reload when the file changes, and SHOULD preserve scroll position and expand/collapse state when feasible. The mechanism is chosen ONCE at generation time per /define session and embedded in the file; it does not change mid-interview.
- **Self-contained:** No external assets beyond the two CDN scripts above. No local server is started. The file opens via `file://`.

## Update cadence

**Initial canvas is a minimal shell.** When SKILL.md's Canvas Mode dispatch fires (before Domain Guidance and the interview begin), no deliverables, ACs, or invariants exist yet. The first canvas write is intentionally minimal: an intent banner derived from `$ARGUMENTS`, an "Interview in progress" affordance, and an empty scaffold for the sections that will fill in. The user opens the tab knowing the substance materializes as the interview produces it — not all at once on first render.

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

## What the canvas surface must enable

The user looks at the canvas to spot misalignment. That's the contract on what's visible by default — not a structural template, but an enablement test: **at a glance, can the user detect "that's not what I meant" on the things people most often disagree about?**

People disagree about three things, predictably: **intent** (what we're actually building, and why), **flow** (how the system or process behaves — sequence, branches, before/after), and **scope** (what's in, what's deliberately out). Surface these so they're scannable without scrolling and without expanding anything. Everything else — acceptance specifics, decision rationale, risk drilldowns, edge cases, work-item drill-ins — lives behind progressive disclosure (`<details>` expanders, tabs, click-to-reveal). Detail is one click away, never zero.

The visible-by-default layer:

- **Intent** — what's being built, in plain language. Always immediate.
- **The visual that most exposes misalignment for this task, when one exists.** Common shapes: a flowchart for sequence changes, before/after panels for behavioral changes, an architecture sketch for component-level work, a dependency graph for cross-cutting changes, a state diagram for stateful workflows. The agent picks per task. When the task has no genuine flow — a one-line text fix, a renaming, a copy edit — don't force one. Prose is right where flow doesn't exist (per the third principle).
- **Scope** — what's in, what's deliberately out. Often a callout or a short bordered list.

Once those three surfaces enable misalignment-spotting at a glance, everything else collapses behind progressive disclosure.

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

### Example: collapsible work-item card with details inside

```html
<details class="border rounded-lg p-4 my-3 bg-slate-50">
  <summary class="font-semibold cursor-pointer">Refactor the canvas content rules</summary>
  <ul class="mt-3 space-y-2 text-sm text-slate-700">
    <li>Reframe the canvas as an alignment surface, not a comprehension brochure</li>
    <li>Replace the suggested-content menu with a principle: surface what people disagree about</li>
    <li>Make detail collapsed by default — visible-by-default surface stays scannable</li>
    <li>Strip manifest IDs and schema vocabulary throughout, surface and expanders alike</li>
  </ul>
</details>
```

The summary line names the work in user vocabulary. The details inside are plain-language commitments — not formal acceptance IDs.

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

These patterns share a property: they expose structure visually before any text is read. A user scanning quickly grasps the shape — what's being built, how it flows, what's different — before deciding where to drill in.

## Style notes

- Default to a calm palette (slate / neutral grays for chrome, an accent color for highlights). Avoid loud styling that distracts from content.
- Use whitespace generously. Cramped layouts increase cognitive cost — the opposite of the canvas's purpose.
- Headings establish hierarchy; bold for emphasis within paragraphs. Avoid heavy use of all-caps or italics.
- For long content sections, prefer collapsible (`<details>`) over walls of text.
- Re-render mermaid after auto-reload updates content (`mermaid.run()` or equivalent) — diagrams need re-initialization when the DOM changes.

## Anti-patterns

- **Re-skinned manifest.** If the canvas reads as the same content as the manifest with different fonts, it has failed. The canvas should look and feel different — visual where the manifest is textual.
- **Tidy-outline syndrome.** Headers, bullets, more headers, more bullets. The canvas should reach for diagrams, cards, panels, side-by-side comparisons, expand/collapse — not just prettier prose.
- **Wall of acceptance details.** Listing every acceptance detail inline at the top level defeats layered reveal. Cards with collapsible details are nearly always better.
- **Per-turn regeneration.** Updates fire after meaningful events, not after every tool call. Constant page flicker undermines the "live alongside understanding" feel.
- **Manifest restatement at the surface.** The canvas isn't a digest of the manifest's IDs and schema. If a section reads like a re-formatted invariant or acceptance list, it's the wrong content — re-express the underlying ideas in plain language, or move the detail behind an expander.
- **Schema vocabulary visible.** Canvas section labels should not read as "Acceptance Criteria", "Global Invariants", "Process Guidance", "Risk Areas", or "Trade-offs". Those are manifest-internal categories. The canvas talks about *what we're building*, *how it works*, *what's in and out of scope*, *what could go wrong* — in user vocabulary.
- **Paragraph where a visual would land.** When the content involves relationships, sequence, before/after, dependencies, or branching, prose that *describes* the structure carries less than a diagram that *shows* it. If you find yourself writing more than a few sentences about how things relate, ask whether a diagram would carry it more cheaply.
- **Formalism leaking into expanders.** The scrub applies everywhere on the canvas, not only the visible-by-default surface. Detail behind `<details>` is still on the canvas — still ideas and decisions in plain language, never IDs or schema labels.
