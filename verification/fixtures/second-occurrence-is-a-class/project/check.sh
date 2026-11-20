#!/usr/bin/env bash
# Run the tests in the C locale, with no UTF-8 default, as the servers do.
set -euo pipefail
cd "$(dirname "$0")"
PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 LC_ALL=C python3 -m unittest -q
