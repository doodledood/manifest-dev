#!/usr/bin/env bash
# The review-explained-page project, made harder to review: the five added sentences are short, and
# docs/review-round-1.md ends with a re-test in which six customers read the page and then said
# correctly what each element meant. The review-design recipe's explained-retested scenario reviews
# the page as it stands.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
. "$(dirname "${BASH_SOURCE[0]}")/../review-explained-page/scaffold.sh" retested
