# ADR: Taste is checked at each user's call, followed only where it bears, and captured from explained reversals

## Status
Accepted; narrowed by 20261031-do-takes-a-reaction-to-a-draft-as-direction-not-a-lock: an explained reaction to a disposable draft is not a reversal to capture as Taste unless the person states it as reaching beyond that draft

## Area
figure-out

## Decided by
The user

## Context
A Taste entry is a ratified steering preference that rides in a memory file. Until now an entry was used passively: it sat in context and the model was trusted to weigh it. Entries were captured only in interactive figure-out, from a preference that recurred or that the user stated as a standing way of working. A single correction did not qualify.

A backtest over 101 recorded decisions asked whether the owner's stated reasons carry to later calls. Six owner preferences were held passively in the system prompt, and they changed nothing. With them, 66 of 101 agreed with the owner, against 67 without. The agent named a preference in 3 of 69 runs. This matches a user's report that agents do not follow Taste. An explicit check of the preferences at each call helped where one clearly bore on the call: 8 better and 1 worse than the agent alone. It hurt where none did: 1 better and 7 worse. The harm came mostly from stretching one broad preference over unrelated calls. Where a narrow preference bore, it pointed to the owner's pick 9 of 11 times, against 7 for the agent alone. The broad one did no better than the agent alone: 32 against 33 of 46. Following a preference only where it clearly bears would at best lift agreement on the owner's calls from about 57% to about 67%.

The moment that best shows a preference is often a reversal: the user overturns an agent's call and says why, frequently while shaping a fix in `/define`. That moment was lost.

## Decision
**Use.** At each user's call — the shared definition in `20261012-unattended-runs-flag-the-users-calls-by-disagreement-not-confidence` — the run checks the user's Taste entries. It follows an entry only where it clearly bears: the entry speaks to this kind of call, and following it would change the choice. A general lean that would tilt almost any call, such as lower cost, does not bear on its own. Otherwise the run decides on the evidence. Wherever the call is reported, the run names what decided it: the entry, or that none applied. In interactive figure-out, a user's call that an entry settles is decided and cited, not asked.

**Capture.** A single reversal of an agent's call qualifies when the user states the reason. The drafted entry is built on that reason, never an inferred one, and its preference text names the kind of call it covers; boundary form stays three parts. The offer asks whether the entry is standing or for this case only. A later reversal of a call an entry decided is a clash, re-ratified under the existing curation rule. figure-out's Taste reference keeps the full rules. `/define` and `/do` each carry a short copy. `/define` offers while the user is present. `/do` never waits, so it carries the drafted entry in its terminal report for the user's yes. No unattended run asks the user anything about an entry while it runs. Only the user's explicit yes to the exact text writes an entry.

## Alternatives Considered
- **Keep passive use**: the backtest showed passive preferences changed nothing.
- **Check every call against every entry**: this applied broad entries to calls they do not bear on, which was the measured harm.
- **Capture only recurring or stated preferences**: this loses the reversal, the moment where the user's reason is most concrete.
- **Infer the reason behind a reversal**: an inferred reason can only be obeyed, not weighed, and it stops the pushback that would correct it.

## Consequences

### Positive
- Entries now change decisions where they bear, which passive use did not.
- A reversal the user explains can become standing context with one yes.
- Each entry names its kind of call, which keeps it from stretching.

### Negative
- The measured ceiling is modest: about 57% to about 67% agreement on the owner's calls.
- Older entries name no kind of call and read broader than intended until re-ratified.
- Reversal offers add interruptions; the existing bar that an offer repay its interruption still applies.

## Enforced by
partly — `tests/test_shared_blocks.py` (`test_block_is_verbatim_in_each_file[users-call]`, `test_block_lives_only_in_declared_files[users-call]`) fails when a skill that states the user's-call block drops or alters its per-call Taste check; capturing entries from explained reversals stays judgment.

## Source
- Session: figure-out investigation with a backtest over recorded decisions; aggregate figures only.
- Amends 20260719-taste-persists-by-offer-and-ratify: offer-and-ratify stands; the earned-entry bar widens to explained reversals, and passive use becomes a per-call check.
- Related: 20260810-universal-discipline-belongs-in-the-prompt
- Amends 20260905-investigation-messages-do-not-require-acknowledgment: figure-out still yields for a concrete contribution only the user can supply, and a user's call that a Taste entry settles is now decided and cited instead of asked.
