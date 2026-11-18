---
name: code-principles
description: 'Code principles for manifest-dev: how its maintainer wants the repository code — tests, scripts, the verify tool and the code skills ship — written and changed, and why. Use before planning, designing, building or reviewing code in this project.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- When the code a change must build on resists it, a separate step reshapes that code first without changing its behavior, held by tests, as part of what the change owes, and the change follows — work layered on a tangle inherits the tangle, and a step that changes no behavior is easy to review. Yields when that code is not expected to change again.
- A module offers a small interface over a substantial job — callers have little to learn and much to gain, and a later change touches one place instead of several. Yields for a module whose job is to expose a whole interface it does not own, such as a client for an outside service.
- Shared logic works only from what it is handed, the clock included, and hands back what it makes, while effects happen at the entry point that asked for them — such code behaves identically in tests and replays, where an effect would fire for no one. Yields where the effect is itself the behavior being shared.
- A test drives behavior through the interface its callers use — a test that still passes once the behavior is gone proves nothing. Yields for a unit that has no caller-facing interface yet, which is tested at its own edge.
- A test's expected values are written out, not derived the way the code derives them — a test that computes its answer as the code does repeats the code's mistakes. Yields where an independent reference implementation serves as the oracle.
- A bug fix comes with a test seen to fail on the code before the fix, and that failing run is shown with the change — the failing run is the evidence that the cause was understood. Yields when no automated test can reproduce the bug; then it is reproduced in a real run, and that run is shown.

Before calling code work done, check it against these principles from a fresh start — a new
session, or a reviewer who did not do the work. Fix what departs unless the person chose the
departure, and check again only after a fix, until a check finds none. Name each departure kept,
with the principle and why.
