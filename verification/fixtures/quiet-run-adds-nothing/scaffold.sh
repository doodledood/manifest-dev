#!/usr/bin/env bash
# The quiet-run-adds-nothing scenario of verification/recipes/do.md: ordinary work whose only failure
# is the one test-first expects.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cp -R "$fixture/project/." .
