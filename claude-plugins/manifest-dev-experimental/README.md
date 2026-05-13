# manifest-dev-experimental

Radically slim parallel rework of the `manifest-dev` plugin. Same skills, same agents, same hooks — every word in the prompts steers model behavior, nothing scaffolds against failures the model handles fine when given clean posture.

The discipline: trust capability, minimize specification, observe what actually fails, add specific lines back only on real failure. The experimental plugin is the sandbox where that discipline gets tested before promotion.

## Skills

- **`/figure-out`** — relentless probing. Walks every branch of the decision tree (design, diagnostic, commitment, exploratory), tackles the next load-bearing question first, gives recommended answers, returns to dropped threads, explores instead of asking when discoverable.
- **`/define`** — encodes shared understanding into a verifiable Manifest. Auto-invokes `figure-out` when the transcript lacks understanding. Supports `--amend`, `--babysit <pr-url>`, `--platform`, `--canvas`.
- **`/do`** — executes a Manifest deliverable-by-deliverable, invokes `/verify` for criterion checks, default-to-amend on user feedback, escalates blockers via `/escalate`.
- **`/verify`** — spawns verifiers for INV-G* and AC-* in parallel within each phase, routes outcome to `/done` or `/escalate`. Selective with auto-triggered full final gate. Supports `--deferred` for user-triggered deferred-auto criteria.
- **`/done`** — completion summary mirroring manifest hierarchy. Called by `/verify` after full-suite green pass.
- **`/escalate`** — structured escalation: blocking, manual review, self-amendment, proposed amendment, user-requested pause, deferred-auto pending.
- **`/auto`** — chains figure-out → define → do autonomously. Add `--babysit <pr-url>` for PR lifecycle work.

## Differences from the core plugin

- **One mode instead of three.** `--mode efficient|balanced|thorough` and `--interview minimal|autonomous|thorough` are dropped — defaults are quality-first. Trust the verifiers.
- **`figure-out` owns the interview.** `/define`'s epistemic stance, interview style modes, and discovery-question disciplines are gone — they live in `/figure-out`, which `/define` auto-invokes on cold-start.
- **Coverage Goals reframed.** No longer drive the interview; the `manifest-verifier` agent audits the manifest against them post-synthesis.
- **Spirit lives in the slim prompt itself.** No separate rubric files. The slim prompt either steers the load-bearing behavior or it doesn't; reviewers (`change-intent-reviewer`, `prompt-reviewer`) catch regressions.

## Hooks and agents

Hooks (`hooks/`) and reusable agents (`agents/`) are duplicated from the core plugin so this plugin runs standalone. Hook detection via `was_skill_invoked` is plugin-source-agnostic — experimental's skill invocations fire the same hook state machine as the core plugin's.

When both plugins are installed alongside, hooks fire from each independently. Manage your installation accordingly.

## Status

Experimental. Skills produce the same outcomes as the core plugin but with radically slimmer prompts. The plan: use experimental, observe what fails, fix with specific lines (not blanket additions), promote to core when validated.
