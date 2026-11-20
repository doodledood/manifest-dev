# Upgrading a project from v18: what v19 gives it

Offer the verification-tool update only to a project that keeps the harness. Compare the
project's copy with `../harness/verify.mts`, preserve its configured paths and local changes,
and apply the same behavior in its own language if it has a port. The update makes `verify
affected` count each repository path a recipe's scenario commands name as arguments, such as a
fixture or a prompt, as covered by that recipe. A project that verifies its own way gets none of
this.

Record the newest surfaces version only after each applicable offer has an answer.
