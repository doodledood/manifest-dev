#!/usr/bin/env bash
# The environment-fact-lands scenario of verification/recipes/do.md. Two facts a run learns only by
# failing: report.py needs STOCK_DB set when run by hand, in every environment, and nothing says so;
# check.sh calls the sqlite3 command, which some machines lack. Read the recipe's trap first.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cp -R "$fixture/project/." .
