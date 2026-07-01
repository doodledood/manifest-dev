# figure-out: scratch mode

Maintains a rough, domain-native supporting artifact — a design draft, a code prototype, a UI mock — that mirrors the investigation's current understanding. Purpose: ground long or complex sessions in something concrete, and let the user glance at it mid-session to catch "that's not what I meant" before it's load-bearing. This is a mirror of understanding, not a second deliverable: it never gets ahead of the read, and naming the read still ends the skill.

## Override: this write IS the action

The master frame in `SKILL.md` says answers and agreement feed exploration, not action — don't leap to the implied move, not the edit, not even the proposal.

Scratch mode carves out one narrow exception. **Maintaining the scratch artifact is not deferred work — it is the action of this mode.** Write and update it inline as understanding shifts. Do not wait for the user to ask, and do not batch every change to the end of the session.

(The default figure-out posture still applies to everything else — the real deliverable, real project files, any edit outside the sanctioned scratch location. Only writes to the scratch artifact itself carve out, and only inside the boundary below.)

## Content-boundary gate

Before writing to scratch, or when unsure whether an update belongs there, check all three:

- **Directionality** — understanding drives the artifact, never the reverse. Update scratch to reflect what was just settled; never use scratch to push the design somewhere the conversation hasn't gone.
- **Fidelity** — it stays rough and throwaway. Polishing it for its own sake, or making it production-ready, is the tell that this has crossed from supporting understanding into doing the work.
- **Terminal state unchanged** — naming the read still ends the skill. Scratch is input color for `/define`, never itself the deliverable.

If an update would fail any of these, it belongs to execution, not scratch — stop and name the read instead.

## Format

Domain-native, not one fixed template. A tech-design session keeps a rough draft doc with open questions; a coding-shaped session may keep a small prototype; a UI-shaped session may keep an HTML mock. Not limited to a single file — use as many as the domain naturally produces.

Do not force content through `define/references/CANVAS_MODE.md`'s HTML/Tailwind/Mermaid machinery. That machinery exists to re-skin a structured manifest for a stakeholder glance-check; scratch content is heterogeneous by nature and has no common schema to re-render. When the domain itself is visual (a UI mock), producing HTML is the domain's own native format, not a reuse of canvas mode.

## Location

Default to `~/.manifest-dev/scratch/{session-ts}/` (create the dir; `~` = `$HOME` / `%USERPROFILE%`; `{session-ts}` matches the session's log/manifest timestamp where one exists) — out-of-repo, matching the precedent set by the investigation log (`~/.manifest-dev/logs/`) and by `/define`'s manifest and canvas artifacts (`~/.manifest-dev/manifests/`). This keeps scratch from ever being mistaken for a real deliverable, never lands in git by accident, and never pollutes the repo before `/define` locks anything in. Fall back to a writable temp path only when the home directory isn't writable.

**Exception:** when the artifact genuinely needs the project's own build/run tooling to function — a prototype that must import real project modules or dependencies to validate an approach — place it in-repo instead, under an obviously-scratch, gitignored path (not intermixed with real source), so it stays physically unmistakable for deliverable code even while living in the tree. Prefer the out-of-repo default whenever the artifact doesn't require this.

## Lifecycle

**Lazy creation.** Don't scaffold an empty shell at session start. Create the artifact the first time there's actually something worth sketching — a first design element agreed, a first UI direction picked, a first algorithm shape decided.

**Update cadence.** Regenerate or edit after a meaningful shift in understanding — a belief-register update, a new element decided, an open question resolved — not per turn and not per tool call. Batch small changes into one update rather than writing on every micro-step.

## Composition

Scratch mode composes with logging and docs mode without changing their behavior: the investigation log still records the reasoning line, `CONTEXT.md`/ADR captures still happen on their own triggers, and scratch only adds the artifact-mirroring behavior described above. It composes the same way under `--autonomous` and `--team` — the artifact can still ground a long unattended or multi-party session even when no one is glancing at it turn-by-turn.
