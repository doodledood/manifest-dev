# ADR: Manifest-aware review-pr instead of a standalone GitHub verification plugin

## Status
Accepted

## Context
The manifest-dev workflow verifies a PR's Acceptance Criteria and Global Invariants **in-session** inside `/do`: before `/done`, `/do` spawns one general-purpose subagent per criterion using its `verify.prompt` verbatim (`skills/do/SKILL.md`). That verification is the *same model* that implemented the change. Correlated blind spots follow: if the implementer misreads a spec while building, a same-model verifier subagent can share the misread. The reviewer-side actor that *could* provide an independent cross-check — `review-pr` — runs a generic `review-code` dimension fleet (bugs, design, simplicity, intent) grounded *against* the manifest but does **not** execute the manifest's Acceptance-Criteria `verify.prompt`s (`skills/review-pr/SKILL.md`). So no independent actor re-verifies the contract.

The triggering idea was a new experimental plugin: a separate verifier session (possibly a different CLI/model) that takes the same manifest, polls the PR for new commits via a deterministic sleep-loop baked into a skill, tracks a last-seen-commit marker, runs the manifest's verifications, and posts PASS/FAIL as PR comments for `/do`/`babysit-pr` to ingest.

Investigation found that nearly all of that machinery already exists and is proven: two sessions coordinating *only* through GitHub state and the Manifest (`skills/babysit-pr/SKILL.md`), `/do` ingesting PR comments as external review input distinct from the manifest's own ACs (`skills/do/SKILL.md`), babysit driving a PR to mergeable (`skills/babysit-pr/SKILL.md`), and webhook-driven wake via `subscribe_pr_activity` (running environments prefer this over `bash sleep` polling for external events). The only genuine gap is that no reviewer-side actor executes the manifest's Acceptance Criteria. The cross-model independence the idea wanted is obtained for free by running the existing reviewer-side skill on a different tool/model.

## Decision
Reviewer-side independent verification of a manifest-dev PR is delivered by making **`review-pr` polymorphic on manifest presence**, not by building a separate GitHub-mediated verifier plugin with its own poller and marker tracking.

- **Manifest present** (`--manifest <path>`): `review-pr` **skips** the generic reviewer fleet and verifies *only* the manifest — running the Acceptance Criteria and Global Invariant `verify.prompt`s against the PR head and posting PASS/FAIL as voice-compliant PR comments (approve when all green). The manifest is the single source of truth for "done."
- **Manifest absent**: `review-pr` runs the existing generic `review-code` reviewer fleet, for an ordinary human/teammate PR with no contract.

Generic code-quality review is **not lost** in manifest mode: it is carried inside the manifest as a Global Invariant whose `verify.prompt` activates the `review-code` skill (a `verify.prompt` can already activate skills, per `skills/do/SKILL.md`). `/define` **already default-injects** this `review-code` Global Invariant through its default gates, so the soundness net is on by default and no `/define` change is required — `review-pr` running the manifest's invariants therefore still runs `review-code`.

Operationally, the desired "execution + independent verification collaborate over GitHub" outcome is then just: `define → do` (babysits to mergeable) plus, on a different tool/model, `review-pr --loop --manifest <path>`. The two coordinate through GitHub state. No new plugin, no sleep-poller, no bespoke marker tracking.

## Alternatives Considered
- **Standalone GitHub-verification-bus plugin**: a dedicated verifier session with a deterministic sleep-loop poller, last-seen-commit marker, and PR-comment PASS/FAIL posting — Rejected. Re-implements (worse) three things already owned: two-session-via-GitHub coordination, `/do`'s external-review-input ingestion, and webhook wake. Adds round-trip latency, a second PR-head checkout, self-comment loop hazards, and a hand-rolled poller that duplicates `subscribe_pr_activity`. Framed as "simplification," it relocates complexity and adds distributed-systems failure modes instead of removing them.
- **Manifest mode runs ACs *and* the generic fleet additively**: Rejected. Reintroduces a second source of truth and noisy duplicate comments on a contract-driven PR. "How much generic review does done require" belongs in the manifest (as an invariant), per-PR, not as an always-on fleet bolted onto AC verification.
- **Manifest mode verifies ACs only, with generic review out of scope entirely**: Rejected. Acceptance Criteria are an *incomplete* specification of "good" — they catch "did we build what we promised" but miss unspecified failure modes (security holes, perf regressions, bugs in code paths no AC enumerated, sound-passing-but-wrong designs). Dropping the soundness net silently ships spec-satisfying-but-unsound code with no independent check. Resolved by encoding `review-code` as a Global Invariant so it runs *as* manifest verification.
- **Keep verification in-session only (status quo)**: Rejected as insufficient for the independence goal. Same-model AC verification carries correlated blind spots; an independent, cross-model reviewer-side check is the value being added.

## Consequences

### Positive
- Independent, optionally cross-model verification of the manifest contract on the PR, with zero new plugin and no bespoke polling — built by composing existing skills.
- Single source of truth: in manifest mode the manifest defines everything verified, including how much generic review "done" requires.
- Fits a faceless, async operating mode — `review-pr --loop --manifest` runs on a separate tool and coordinates only through GitHub state.
- `/define`'s existing default gate keeps the soundness net on by default, so authors don't have to remember to ask for generic review.

### Negative
- `review-pr` gains a mode branch (manifest vs no-manifest), adding conditional behavior to one skill.
- Manifest quality becomes more load-bearing: `/define` injects the `review-code` invariant by default, but a hand-edited or externally-authored manifest that drops it gets manifest-mode review covering only its explicit ACs, with a thinner soundness net.
- The reviewer-side actor must obtain a PR-head checkout to execute AC `verify.prompt`s — real machinery, though no worse than what in-session verification already needs.
- Cross-model AC re-execution may have low marginal value if in-session fresh-context AC subagents already catch most same-model misreads; the durable win then concentrates in the encoded `review-code` invariant rather than AC re-running.

## Source
- Session: `/figure-out` on the experimental "GitHub as the execute/verify collaboration medium" idea (2026-06-19).
- Governs behavior of the `review-pr`, `define`, `do`, and `babysit-pr` skills.
