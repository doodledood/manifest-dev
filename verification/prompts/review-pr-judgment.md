Use review-pr to review the local PR described in pr.json. The checkout and git history
are the PR's actual source snapshot. Use the supplied local state instead of GitHub; this
assignment ends before external actions. Save draft review comments, proposed thread actions
and the operator cycle summary in review-initial.md. Do not modify the application. Keep your
continuation state for the next turn. Leave snapshots/ unopened until a later turn names a file.

<!-- next turn -->

The author has now replied: read snapshots/reply-authority.md. Treat any judgment comments
you drafted in the prior turn as posted review-pr threads with the judgment marker and
assess this reply on those threads. Advance the review from this local snapshot; save draft
replies, proposed thread actions and the operator summary in review-authority.md. No remote actions.

<!-- next turn -->

Read snapshots/reply-decision.md for the next reply on that same thread. Advance the local
review, preserving prior drafts as its history. Save draft replies, proposed thread actions
and the operator summary in review-decision.md. No remote actions.

<!-- next turn -->

Read snapshots/reply-late.md. The new PR head is snapshots/late.py in place of recommendations.py;
treat that supplied file as the current head's change and all prior decisions and threads as
retained history. Advance the review again. Save draft comments, proposed thread actions and
the operator summary in review-late.md. No remote actions.
