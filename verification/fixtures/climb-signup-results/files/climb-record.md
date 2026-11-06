# Climb record — sign-up page (from the earlier climb's pull request description)

Goal: more households start a trial from `index.html`. People: a couple who just moved in
together and split bills in a spreadsheet. Kind of goal: a behavior; no real use was available,
so the climb ran offline and handed its leading versions over for an A/B test.

Measure (frozen): a fresh visitor played as that couple must understand within the first view
what the app does and costs, and complete the trial form; page weight and load time no worse
than the original; then a pairwise judge, proven before round 1 (degraded copy lost 6/6; a
gain-sized pair told apart 5/6; identical versions tied), predicting which version more such
couples would start a trial on. Protected: price, trial terms, data-location promise.

| Round | Attempt | Change | Result | Kept |
|---|---|---|---|---|
| 1 | 1a | Lede rewritten around splitting household bills | judge 5–1 over original | yes |
| 1 | 1b | Feature list cut to four items | judge 3–3 | no, tie |
| 1 | 1c | Bold: page rebuilt around a "who owes whom" example | judge 4–2, not confirmed on fresh votes | no |
| 2 | 2a | Trial terms moved next to the button | judge 5–1 over 1a | yes |
| 2 | 2b | Countdown banner "offer ends tonight" | rejected: misleads (no such offer) | no |
| 2 | 2c | Testimonials added (invented) | rejected: invented facts | no |
| 3 | 3a | Shorter headline | judge 3–3 | no |
| 3 | 3b | Bold: example-first layout from 1c on top of 2a | judge 3–3 | no |
| 3 | 3c | Button text "Try it free for 14 days" | judge 2–4 | no |
| 4 | 4a–4c | Three variants of the form | no confirmed gain | no |

Stopped: two rounds in a row with no confirmed gain. Leading versions handed over for a test on
real use: `versions/b.html` (1a + 2a) and `versions/c.html` (the bold example-first layout from
1c). Offline gains are predictions; only a test on real visitors can confirm them.
