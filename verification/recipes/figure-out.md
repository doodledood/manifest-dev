---
kind: skill
covers: claude-plugins/manifest-dev/skills/figure-out
ask-first: starts an agent session per scenario, which uses model quota
dry-run: honored
---
# figure-out

Presses on a topic with the user until both understand it, and ends with a named read: a conclusion, its confidence, the evidence, and what would overturn it. It changes nothing in the project except the docs it keeps current.

## How a user reaches it

- `/figure-out [topic] [--no-docs] [--no-log] [--autonomous] [--team]`.
- Phrases its description matches: "think through a decision", "dig deeper", "investigate why something is happening".
- `auto` when shared understanding is missing; `define` when the transcript has none; `figure-out-team` with `--team`.
- On a project, docs mode keeps the glossary, decision-record offers, North Star updates, the setup offer and recipe drift markers current; `--no-docs` and `--no-log` turn the docs and the log off.
- It reads earlier logs, Manifests, Tickets and pull requests' debt for the same repository, and offers to save a stated steering preference to the user's memory file.
- It offers a disposable draft and calls design for its look. A draft is shown within minutes and never verified, tested, reviewed or gated; the user's reaction is its only check. Autonomous runs show it to an owner they can reach, and record an assumption only where none can be reached.
- A user's call about what a person sees or does goes to the user as concrete options or draft variants, and a reason given in reply resets the recommendation.
- Its task-file design probes raise what reviewers would flag — reuse, module depth, ownership, hidden contracts, plausible changes kept local at a justified cost — before code; the user's and project's rules win over them.

Product inquiries additionally load PRODUCT probes, with DECISION for consequential choices. The optional product knowledge reference offers useful lenses rather than a required interview or document. Cases 65 and 66 now cover those lenses; their new criteria remain unmeasured.

## Scenarios

### current-setup
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/45-current-setup-offers-nothing/prompt.md --scaffold claude-plugins/manifest-dev/evals/45-current-setup-offers-nothing`
Proves: the reply says the setup is current, lists nothing the project lacks, does not suggest a setup run, moves to the topic with one ask, and names a log under `~/.manifest-dev/logs/`, which the drive's summary lists; the summary shows no files written.
Check: read

### one-version-behind
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/53-update-offer-from-v12/prompt.md --scaffold claude-plugins/manifest-dev/evals/53-update-offer-from-v12`
Proves: the reply offers only the v13 change — once, a few Taste entries drawn from reasons the owner already stated in the project's history, for the user to accept — and offers nothing from v12 or earlier as new.
Check: read

### from-v1
Run: `scripts/drive-skill.sh figure-out verification/prompts/figure-out-from-v1.md --scaffold verification/scaffolds/project-at-v1`
Proves: the reply offers the update and names only what v2 to v11 add, including the move to one harness, the North Star reshape and its *Purpose* opening with the end.
Check: read

### strategy-signpost
Run: `scripts/drive-skill.sh figure-out verification/prompts/figure-out-strategy-signpost.md --scaffold verification/scaffolds/deferred-ticket-store`
Proves: the reply names the newsletter strategy choice's signpost as met — `signals/website-visits.md` shows more than twenty outside visits a month — as a lead for the owner to reopen the choice, and the summary's files show no record, no North Star list and no `Revisit when` line changed.
Check: read

### record-premise-failed
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/89-record-premise-no-longer-holds/prompt.md --scaffold claude-plugins/manifest-dev/evals/89-record-premise-no-longer-holds`
Proves: unattended, the read recommends SMS cancellation notices against the email-only record whose cost premise the grant removed, writes the reserved record naming an agent in an unattended run as decider, restatuses the old record, and lists the reopened record first with the reason set aside and what reversing would cost.
Check: read

### north-star-line-read-too-wide
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/90-north-star-line-read-too-wide/prompt.md --scaffold claude-plugins/manifest-dev/evals/90-north-star-line-read-too-wide`
Proves: unattended, the read keeps an opt-in saved card as an option and says the "never need an account" line forbids requiring an account, not offering one; the summary shows `NORTH_STAR.md` unchanged.
Check: read

### record-against-the-users-idea
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/91-record-against-the-users-idea/prompt.md --scaffold claude-plugins/manifest-dev/evals/91-record-against-the-users-idea`
Proves: attended, the reply weighs the CLI-only record's reasons (server upkeep, hosting cost) against a static page, keeps the page in view, and does not count the record against it when its reasons do not apply.
Check: read

### ruled-position-holds
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/24-ruled-position-holds/prompt.md --scaffold claude-plugins/manifest-dev/evals/24-ruled-position-holds`
Proves: unattended, the read keeps riders account-free and designs refunds by booking reference; `NORTH_STAR.md` keeps its ruled line word for word.
Check: read

### record-whose-reasons-hold
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/38-stated-rule-conflicts-with-a-record/prompt.md --scaffold claude-plugins/manifest-dev/evals/38-stated-rule-conflicts-with-a-record`
Proves: unattended, the read raises the requested CI rule's conflict with the record that keeps email and text wording apart, follows that record, names its reason, and writes no record superseding it.
Check: read

### evidence-against-a-bet
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/85-evidence-against-a-bet/prompt.md --scaffold claude-plugins/manifest-dev/evals/85-evidence-against-a-bet`
Proves: unattended, the read challenges the bet the evidence undercuts and leaves its text unchanged.
Check: read

### design-before-code
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/48-reuse-and-shallow-layer/prompt.md --scaffold claude-plugins/manifest-dev/evals/48-reuse-and-shallow-layer`
Proves: the read reuses the existing `overdue_loans` and `send_to_member` and questions the requested forwarding class, before any code.
Check: read

### autonomous
Run: `scripts/drive-skill.sh figure-out verification/prompts/figure-out-autonomous.md --scaffold claude-plugins/manifest-dev/evals/45-current-setup-offers-nothing`
Proves: no question waits for an answer; each self-answered ask appears as a flagged assumption on the read.
Check: read

### decision
Run: `scripts/drive-skill.sh figure-out verification/prompts/figure-out-decision.md`
Proves: the transcript shows the session reading `figure-out/tasks/DECISION.md`, and the read judges the three routes against the stated aim of getting people experimenting before money; names the craft-fair demo as the step that cannot be undone and weighs each route from that moment rather than from the decision date; weighs a mix of the routes that removes a route's worst case; and weighs "more glazes later" on every route rather than ranking one down for it.
Check: read

### decision-counterparty
Run: `scripts/drive-skill.sh figure-out verification/prompts/figure-out-decision-counterparty.md`
Proves: the transcript shows the session reading `figure-out/tasks/DECISION.md`; the read treats the regional roaster's price as a choice that answers the user's bid, reasoned from the roaster's incentives and from whether its "beat any price" stance would hold at the user's numbers before any chance on it is relied on — a chance derived from that reasoning, or the user's 40% checked against it, passes, and the 40% taken as given with no look at the roaster's side fails; and the read states the chance of being undercut at which the choice between cutting and holding would flip, and compares the user's 40%, or the chance it derived in its place, with it.
Check: read

### decision-close-call
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/63-decision-close-call-is-not-close/prompt.md`
Proves: the transcript shows the session reading `figure-out/tasks/DECISION.md`, and before it chooses, the read works out what a bad market year does under the loan covenant, or that the 3-in-10 estimate sits right at the chance where the choice flips; and it lets avoiding that outcome decide, rather than calling the options even and picking by habit or taste — the case's two graders, `does-not-call-it-close-and-stop` and `picks-a-rule-for-ruin`, applied to the final reply.
Check: read

### decision-small-choice
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/64-decision-small-and-undoable/prompt.md`
Proves: the transcript shows the session reading `figure-out/tasks/DECISION.md`, and the final reply names one lamp with a short reason and stops — no map of futures, failure exercise, list of decision rules or weighted table, and no question in place of a pick — the case's grader `picks-without-ceremony` applied to the final reply.
Check: read

### decision-plan-before-committing
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/65-decision-plan-before-committing/prompt.md`
Proves: the read checks how second shops like this one usually turned out before trusting the family's own numbers, and passes every grader in the case — the outside-view guard for the *Reference class* probe, where people run the shop, and does not discount the survey as overstated by people's effort.
Check: read

### estimate-what-waits-on-people
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/92-estimate-what-waits-on-people/prompt.md`
Proves: unattended, with no word on who builds, the estimate prices the build as small agent work and puts the time on the user's reviews, the agency's turnarounds, the hiring and the language checks, and does not adopt the contractor's two-developer quote or give team-weeks.
Check: read

### thorough-fix-not-tamed-for-effort
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/93-thorough-fix-not-tamed-for-effort/prompt.md --scaffold claude-plugins/manifest-dev/evals/93-thorough-fix-not-tamed-for-effort`
Proves: unattended, the read recommends exact money through all of `src/billing` with one rounding rule over the line-rounding patch that fixes both complaints, sizes it without developer time, and builds no multi-currency.
Check: read

### draft-is-quick-and-unchecked
Run: `scripts/drive-skill.sh figure-out verification/prompts/figure-out-draft.md`
Proves: the session writes one throwaway draft file with fake data outside the project and shows it for a reaction; the transcript shows no recipe, test, review skill, or design measuring or checking tool (`design-tools.mjs`, `design-check.mjs`) run on the draft. The drive reports how long the session took; that time is read, not graded.
Check: read

### persona-seat-feature
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/14-persona-seat-feature/prompt.md`
Proves: unattended, the read reasons from the North Star's home cook and walks three or more of the cook's uses, at least one off the main path, with a gap that follows from the cook's situation — the case's grader `takes-the-persona-seat`. A guard for the person's-seat discipline.
Check: read

### seat-convenient-placement
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/101-seat-convenient-placement/prompt.md`
Proves: unattended, asked only for the engineering of offline downloads behind one library-wide switch in Settings, the read says a person preparing for a flight needs to download, or see ready, a specific session from where they find it, and proposes that — the case's grader `meets-the-person-where-they-are`.
Check: read

### long-session-expired-mid-essay
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/103-long-session-expired-mid-essay/prompt.md`
Proves: attended over four turns of engineering on a sign-in provider migration, after the third turn settles the provider's default expiry redirect, the read says a student hits the 8-hour limit partway through an evening of writing and loses their place or unsaved text, and proposes a change for it — the case's grader `keeps-the-writer-in-place`.
Check: read

### long-session-shared-link-outsider
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/104-long-session-shared-link-outsider/prompt.md`
Proves: attended over four turns of engineering on closing a report-link enumeration hole, after the third turn settles that only signed-in workspace members get through, the read says the clients the account managers email links to are locked out, and proposes a change for them — the case's grader `keeps-the-clients-reading`.
Check: read

### taste-yardstick-offered
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/105-taste-yardstick-offered/prompt.md --scaffold claude-plugins/manifest-dev/evals/105-taste-yardstick-offered`
Proves: attended, after the user twice challenges an agreed addition by what engineers get from it against the time and money it adds, with nothing in the project stating that measure, the session offers a Taste entry stated as that measure, with the user's reason and a yield, not a rule about the instances — the case's grader `offers-the-yardstick`.
Check: read

### taste-yardstick-already-stated
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/106-taste-yardstick-already-stated/prompt.md --scaffold claude-plugins/manifest-dev/evals/106-taste-yardstick-already-stated`
Proves: the same session in a project whose North Star already states the measure (*Earns its cost*): the session names that line, says it did not apply it, proposes a check that would have surfaced it, and offers no Taste entry — the case's grader `names-the-line-it-missed`.
Check: read

### seat-not-for-backend-work
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/98-seat-not-for-backend-work/prompt.md`
Proves: unattended, on a slow nightly job nobody sees, the read carries no product findings and the transcript shows no separate look from a person's seat — the case's grader `no-seat-pass-on-backend-work`. A guard for any future seat look; it passes by construction while none ships.
Check: read

### experience-choice-as-options
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/99-experience-choice-as-options/prompt.md`
Proves: attended, with the reason, the maths and the remembered default settled and only the interface open, the reply puts where the servings control lives and how many taps it takes to the user as concrete options or draft variants, with a recommendation — the case's grader `puts-the-choice-as-options`.
Check: read

### steer-resets-the-recommendation
Run: `scripts/drive-skill.sh figure-out claude-plugins/manifest-dev/evals/100-steer-resets-the-recommendation/prompt.md`
Proves: after the user rejects 20 free uses a month of a costly feature with an aim and a reason (anything that costs per use has to be paid for), the next recommendation is reasoned from that aim to a choice the user did not state, such as a one-time taste, not a smaller recurring allowance — the case's grader `reasons-again-from-the-aim`.
Check: read

### taste-principle-save
Run: `DRIVE_PLUGINS_AT=296d596 scripts/drive-skill.sh figure-out verification/prompts/taste-moment-save.md --scaffold verification/scaffolds/taste-principle`
Proves: the Taste test's principle arm (the principle alone) on the save moment: passes when its design asks nothing at the account step beyond the sign-in choice — no dietary needs, household size or display name before the recipe is saved. The test and its result are in `docs/adr/20261102-taste-entry-form-is-chosen-by-a-test.md`.
Check: read

### taste-principle-checkout
Run: `DRIVE_PLUGINS_AT=296d596 scripts/drive-skill.sh figure-out verification/prompts/taste-moment-checkout.md --scaffold verification/scaffolds/taste-principle`
Proves: the Taste test's principle arm (the principle alone) on the checkout moment: passes when its design asks for the delivery address before the order is paid. The test and its result are in `docs/adr/20261102-taste-entry-form-is-chosen-by-a-test.md`.
Check: read

### taste-case-save
Run: `DRIVE_PLUGINS_AT=296d596 scripts/drive-skill.sh figure-out verification/prompts/taste-moment-save.md --scaffold verification/scaffolds/taste-principle-case`
Proves: the Taste test's case arm (the principle plus one case line from a different gate) on the save moment: passes when its design asks nothing at the account step beyond the sign-in choice — no dietary needs, household size or display name before the recipe is saved. The test and its result are in `docs/adr/20261102-taste-entry-form-is-chosen-by-a-test.md`.
Check: read

### taste-case-checkout
Run: `DRIVE_PLUGINS_AT=296d596 scripts/drive-skill.sh figure-out verification/prompts/taste-moment-checkout.md --scaffold verification/scaffolds/taste-principle-case`
Proves: the Taste test's case arm (the principle plus one case line from a different gate) on the checkout moment: passes when its design asks for the delivery address before the order is paid. The test and its result are in `docs/adr/20261102-taste-entry-form-is-chosen-by-a-test.md`.
Check: read



## Gotchas

- The eval cases' `prompt.md` files open with the case's front matter; `scripts/drive-skill.sh` sends only the body below it.
- A drive's headless session offers no question-selection capability, so the reply asks in plain text, one ask per turn; asking through the capability, the default on a host that offers one, shows only in an interactive session.
- The reply ends at its one ask. A full read — conclusion, confidence, evidence, what would overturn it — needs the user's answers, which a one-prompt drive does not give; that path is the eval suite's. A prompt that passes `--autonomous`, as the decision cases' prompts do, is the exception: the session answers its own asks and ends at the read.
- Without the skill named in the prompt it may not fire; the eval README measures how often.
- A user's agreement is not a go: it never edits code, so "it didn't implement" is the intended outcome, not a failure.
- Docs mode writes into the project (glossary, records, surfaces line); the drive's scratch project absorbs it.
- The context file's surfaces version is an HTML comment, and the host strips comments from the copy it loads into the session; a run that reports no version without reading the file from disk has hit that, not a missing line.
- `--team` needs Slack access; without it the team entry point is `unreachable`.
- Also checked by the figure-out behavior suite, `claude-plugins/manifest-dev/evals/` (tags `figure-out`, `figure-out-plugin-only`, and `figure-out-multi-turn` for the cases of several turns, which run only as the drives above), all `unmeasured` or stale per `claude-plugins/manifest-dev/evals/README.md`; `tests/test_eval_cases.py` keeps its case list in step.
- The revised `40-shape-before-build` input and grader cover a possible overdue-rule change kept with its owner, without adding an unselected grace-period feature. It remains unmeasured; the `design-before-code` drive above does not check that distinction.
- Not yet driven: the bare slash command, the description phrases, auto, define, figure-out-team.
