# Canvas Mode — Walk-PR Review Canvas

Loaded when `/walk-pr --canvas` is passed. The canvas **is** the walkthrough — every surface (PR primer, per-SC behavior summary + verification probe, expanded depth with boundary view, topics, per-file diff affordances, per-topic comment input) lives in the HTML artifact, generated **once, upfront, with the full walk content**. The user navigates self-paced via local JS; chat reconnects only at the end, when the user pastes back a single bundled review result. After the walkthrough closes, the artifact is redundant.

## Reader model

The reviewer **lives in the repo** (knows the modules, idioms, naming conventions) but has **zero context on this PR**. Calibrate explanations accordingly: codebase vocabulary is shared ground and doesn't need re-explaining; PR-specific framing has to be surfaced. Probes, boundary views, and recommendations name files, functions, and modules by their real codebase identifiers, not by invented abstractions.

**Codebase fluency ≠ PR fluency.** Codebase vocabulary (modules, idioms, naming conventions present before this PR) remains shared ground per above. Vocabulary introduced by *this PR* — new types, new modes, new modules, new domain terms — is **not** shared ground. The PR primer (see below) is the only place that vocabulary gets introduced; downstream SC summaries, boundary views, and topics use it without re-explanation. Treat a freshly-coined PR term used in an SC summary without a prior primer entry as a contract violation.

## Activation gate

Evaluate **immediately** when `--canvas` is set, before opening the first sub-changeset. If any condition holds, skip canvas behavior and fall back to chat-only /walk-pr (first match wins; conditions 1–2 silent, condition 3 prints one warning):

1. **Trivial diff** — canvas setup cost (file write + render + browser open + auto-reload plumbing) exceeds the review's information need. Rough threshold: single file with tens of net lines changed.
2. **Non-local medium** — the user isn't at a host with browser access.
3. **No graphical-browser launcher** — none of `xdg-open`, `open`, `start` on PATH. Print: `--canvas requires a desktop environment with a graphical browser; skipping artifact generation`.

If none match: generate the canvas at `/tmp/walk-pr-canvas-{ts}.html` (`{ts}` = invocation timestamp), auto-open it, proceed.

## Cognitive-load contract

The canvas rations what the user sees at any moment. Four rules govern visibility:

1. **Card surface always visible per SC.** Every SC shows its title, size, status pill (`queued` slate, `in review` amber, `reviewed` emerald), one-sentence **behavior summary** (user terms), and one-sentence **verification probe** (concrete observable — a check the reviewer could run paired with an observable outcome). This is the always-visible skim surface across all SCs.
2. **One SC in focus, depth on demand.** Each SC's depth content (boundary view, topics, per-file diffs) collapses behind a single **per-SC depth expand**. Exactly one SC has its depth expanded at a time (the in-focus SC); others have it collapsed — card surface still visible. Reviewers skim behavior + verify across SCs and expand depth only on SCs that need it. (The prior progressive-disclosure rule on per-topic detail bodies — `<details>` closed by default, attached to the in-focus topic — still applies inside the expanded depth.)
3. **One review topic in view.** Inside the in-focus sub-changeset's expanded depth, exactly one topic (probe / trade-off / recommendation) is highlighted with its comment textarea visible. Prior topics collapse to a one-line preview of what the user typed (read from the textarea). Future topics show their headline only, dimmed. At generation, the first topic of the first sub-changeset is marked in-focus; local JS advances the marker as the user clicks "next topic" or marks a sub-changeset reviewed.
4. **No content duplication.** Walkthrough content lives in the canvas — not echoed in chat. Chat stays empty during the walk and receives only the final bundled paste.

Pacing is local — the canvas advances via JS (expand/collapse, "next topic", "mark reviewed") as the user works through it. There's no agent-side state to track until paste-back.

## PR primer

Above the categorized overview, before any sub-changeset card: introduce the PR to a reviewer who has codebase fluency but zero PR context.

**Always present.** A one-paragraph problem statement in workflow vocabulary — what user-facing problem this PR solves, what workflow it serves. Codebase identifiers are allowed only when they *are* the user vocabulary (a service name the reviewer would search for); typed signatures and field names belong downstream.

**Conditional slots — render only when load-bearing, skip when empty (no placeholders):**

- **Concept glossary** when the PR introduces vocabulary downstream content will use. One-line definitions at *workflow level* — what the concept means in the system's behavior, not the type signature. Example: *"Live fallback: when replay can't find a frozen fact, it calls the live business service and notes which fact was missing."* (Not: *"`LiveFallbackHandle` is a record with `access: ExternalServiceAccess` and `recordLiveFallback: (key: FrozenDependencyKey) => void`."*) The type signature lives downstream in the boundary view.

- **Component sketch** (mermaid) when the change involves component flow or data path that's clearer drawn than described. One diagram, not many.

- **Reading hint** when sub-changesets differ in importance and one is the highest-signal entry point. One sentence pointing the reviewer at where to look first.

Goal: a reviewer leaves the primer knowing what to expect when they hit new terms in SC summaries, boundary views, or topics downstream. The primer **introduces** concepts; downstream content **uses** them.

## Interaction model

**One-shot generation.** At creation, the agent embeds **every** sub-changeset, **every** review topic, and the full walk content (PR primer, per-SC behavior summary + verification probe, expanded depth with boundary view, topics, per-file diff `<details>` affordances) into the HTML. No per-topic Copy buttons, no anchor-format paste-back, no canvas regeneration mid-walk — those were artifacts of a per-turn design the user never actually used.

Each topic renders as a two-part structure (see "Topic shape and progressive disclosure" below):

- A visible **headline** — concrete framing of the concern plus the recommended call.
- A collapsible **detail body** (`<details>`, closed by default) for rationale, topic-level code excerpts, and alternatives considered. The in-focus topic only — prior topics keep their one-line preview, future topics keep their dimmed headline.
- A `<textarea>` for the user's comment. State persists across canvas reloads (e.g. `localStorage` keyed by topic id) so the user doesn't lose work.

At the bottom of the canvas, a single **Copy as prompt** button writes the consolidated review result to the clipboard as one structured block — per sub-changeset, per topic: the anchor (file + line range or PR-level) plus the user's textarea content (or `(captured, no comment)` if empty). The user pastes this block into chat; the agent reads it and proceeds with the end-of-walk handoff.

Clipboard write uses `navigator.clipboard.writeText` with a `document.execCommand('copy')` fallback for sandboxed `file://` cases. On any clipboard failure, pre-select the bundled string in a visible read-only `<pre>` so the user can copy manually.

## Boundary view (inside the per-SC expand)

When the reviewer expands an SC's depth, the first content is a **boundary view** of the change — the shape of what shifted at module-boundary altitude.

Goal: give the reviewer the structural picture of the SC's change — what new or changed types exist, what signatures shifted at module edges, what dependency edges changed, what guarantees moved — without forcing them to parse diff hunks. A senior reviewer would mentally synthesize this from the diff; the boundary view does that synthesis once, explicitly, so the diff is verification rather than orientation.

Shape: ≤3 short paragraphs, freeform prose, load-bearing pieces only. No exhaustive enumeration — do not list every type / file / call site touched. If a touch is mechanical (a name change propagated through 8 import sites), name it once at the right altitude; do not inventory it.

The boundary view replaces the previously-canonical "ground the user" prose and "survived / cut / moved" paragraph as the SC's structural exposition. Line-level inventory moves to the per-file diff affordance below.

After the boundary view, topic blocks follow — one in focus, others previewed or dimmed per Cognitive-load contract rule 3.

## Diff as evidence (inside the per-SC expand)

Diff hunks render as **per-file** on-demand affordances — one native `<details>` per touched file in the SC, closed by default, opened by the reviewer when they want to verify a boundary-view claim against the actual code change.

Diff is not the default exposition. Reviewers who want verbatim ground truth have it one click away per file; reviewers who trust the boundary view skim past.

Open/closed state of per-file diff `<details>` is preserved across reloads via the existing expand/collapse state bucket — same mechanism as topic-detail bodies. Diff rendering itself follows "Rendering and layout adapt to the content" (line-level hunks with colored additions/deletions/context, syntax highlighting where the library supports it).

## Topic shape and progressive disclosure

**Headline shape.** Each topic's visible headline is **two declarative sentences**:

1. A concrete framing of the concern in **codebase vocabulary** — which file, function, or module is at issue and what the concern is. One declarative sentence.
2. The **recommended call** — what to do about it. One declarative sentence.

No nested clauses, no embedded justification, no narrated reasoning ("I'm wondering whether...", "It seems that..."). If a topic can't fit this shape, it's two topics, or it isn't load-bearing enough to be one.

**Progressive disclosure for detail.** Everything past the headline — rationale, topic-level code excerpts, alternatives considered, trade-off depth — lives in a collapsible `<details>` body **closed by default**, attached to the *in-focus* topic only. Prior topics keep their existing one-line preview (textarea content) per the Cognitive-load contract; future topics keep their dimmed headline. Sub-changeset diff hunks render as per-file on-demand affordances per the "Diff as evidence" section above — they are not embedded inline in topic detail bodies.

Open/closed state of the topic-detail `<details>` is preserved across reloads via the existing **expand/collapse state** bucket that the Lifecycle section already covers — no new `localStorage` keys are introduced. Native `<details>` open/close *is* expand/collapse state by natural reading.

## Format

- **File:** single self-contained `.html` at `/tmp/walk-pr-canvas-{ts}.html`.
- **Styling:** Tailwind via CDN (`<script src="https://cdn.tailwindcss.com"></script>`). Degrades to semantic HTML if unreachable.
- **Diagrams** (when useful): mermaid via CDN. Use `<pre class="mermaid">...</pre>` only when the change involves component flow that's clearer drawn.
- **Auto-reload:** embed JS that refreshes if the source file changes. Preserve scroll position, expand/collapse state, and textarea contents across reloads (`localStorage`).
- **Self-contained:** no external assets beyond the small set of CDN scripts (Tailwind, mermaid, diff renderer, syntax-highlighter — see below). Opens via `file://`. No local server.

## Rendering and layout adapt to the content

Use the representation that fits each piece of content. This is the second half of the cognitive-load contract — visual rationing controls *how much* the user sees; content-shaped rendering controls *how legibly* it lands.

- **Diffs render as diffs.** Line-level hunks with additions / deletions / context, colored (green / red / muted), not monolithic raw text. Use a CDN-loaded diff library (e.g. `diff2html`) or render server-side as styled `<span>` per line — either is fine; the contract is "looks like a diff, not a `<pre>` dump".
- **Code renders with syntax highlighting.** Highlight.js or Prism via CDN, language inferred from file extension. Applies inside diff hunks where the library supports it, and to any standalone code excerpts in boundary views or topic detail bodies.
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
2. Presents the plan-of-comments through the harness's approval/planning mechanism.
3. On approval, posts the comments as a single PR review using the available GitHub review mechanism.

After posting, the canvas is redundant. Whether and how the PR's author addresses the comments is the manifest workflow's job, not /walk-pr's.

## Failure handling

Any canvas-related failure is **non-blocking**:

- File write fails → warn once, fall back to chat-only walkthrough.
- Browser launcher fails → print path (`Canvas: file:///tmp/walk-pr-canvas-{ts}.html`), continue.
- Clipboard write fails → pre-select the bundled string in a visible block; show a one-line hint.
- Mermaid syntax error → emit as-is, continue.
- PR-post failure → keep the drafted plan, surface the API error inline, offer retry.

## Anti-patterns

- **Chat duplicating canvas content.** Don't restate the PR primer, per-SC behavior summary or verification probe, boundary view, topic text, or per-file diff content in chat. The canvas is the surface; chat only sees the final bundled paste.
- **Mid-walk regeneration.** The canvas is one-shot. Don't update it as the user works through topics — local JS handles pacing.
- **Per-topic Copy buttons or anchor-format paste-back.** Single end-of-walk bundle only. Per-topic round-trips are the failure mode we removed.
- **Wall of diff.** Don't dump entire patches as monolithic `<pre>` text. Render diffs as proper line-level hunks inside the per-file `<details>` affordances described in the "Diff as evidence" section.
- **Uniform layout template.** Forcing every sub-changeset into side-by-side panels regardless of what the change actually is — empty "after" columns for deletions, grids of identical lines for renames, etc. Match the layout to the change.
- **Status-pill explosion.** Pills only on sub-changeset cards (the navigation surface).
- **Diagram for nothing.** Mermaid only when component flow is at stake.
- **Internal vocabulary on surface.** Talk about *what changed* and *why* in user vocabulary; no leaked internal labels (schema names, anchor formats in headings, etc.).
- **Narrated reasoning in the topic headline.** The headline carries the reasoning out loud — "I'm wondering whether the new `flushBuffer()` call inside `handleClose()` could end up racing the `onDisconnect` callback if the socket closes mid-write, since the buffer might still be referenced by the pending write promise and we don't currently guard against that case — should we add a check?" Headline shape instead: "`handleClose()` calls `flushBuffer()` without guarding the pending-write promise that still holds the buffer. Add a guard before `flushBuffer()` runs, or document why the race is safe." The trace, the alternatives weighed, the rationale — all belong in the collapsible detail body, not in the visible line.
- **Headline restates the body.** The two-line headline summarises what the `<details>` body says, instead of standing alone as the concrete framing. The detail body adds rationale, evidence, alternatives — it doesn't unpack a generic headline.
- **Detail dumped in the headline.** Inline code excerpts, multi-line enumerations, or alternative-comparison tables render alongside the two headline sentences instead of inside `<details>`. These break the two-sentence shape visually even when "short" — the most tempting things to inline because they feel atomic. Collapse them anyway.
- **Invented abstraction in place of codebase vocabulary.** The headline names "the propagation manager" when the repo calls it `notifier`, or refers to "the auth pipeline" when no such concept exists in this codebase. Reader model: name things using identifiers the reviewer already knows.
- **Line-level diff as default depth.** Rendering diff hunks as visible-by-default content in the SC card surface, or as a single SC-level monolithic diff block inside the expand. Diff is per-file, on-demand, *evidence* — not exposition. Reviewers trust the boundary view by default and open per-file diffs only when they want to verify a specific claim.
- **Prose grounding mixing problem + change + mechanism.** Per-SC prose that interleaves what the system does today, what was broken, and what the fix mechanism is into one block. Three mental models in one paragraph force the reviewer to hold all three simultaneously. The new model separates them: behavior summary names the user-facing change (visible); verification probe names how to confirm it (visible); boundary view names the structural shift (inside expand); per-file diff shows the lines (deeper).
- **Boundary view listing every type / file / call site.** Boundary view paragraphs that read like an inventory — "six PVP-related types: `ToolContextParams`, `PromptValueProviderExecutionContext`, …" — recreate the BOOM at boundary altitude. Name the structural shift once, at the right altitude; if a change propagates mechanically through N call sites, say so once and do not enumerate.
- **Type-signature-level primer glossary.** A primer glossary entry that reads as the literal type or constructor: "`LiveFallbackHandle` is a record with `access: ExternalServiceAccess` and `recordLiveFallback: (key) => void`." Workflow-level instead: "Live fallback: when replay can't find a frozen fact, it calls the live business service and notes which fact was missing." The type signature belongs in the boundary view, not the orientation layer.
- **Primer introducing while evaluating.** A primer paragraph that introduces a new concept and, in the same sentence or paragraph, asks the reviewer to evaluate whether it's the right design. Introduction and evaluation must be separated: the primer establishes vocabulary; topics carry the evaluation. A reviewer can't judge a design they haven't yet been oriented on.
