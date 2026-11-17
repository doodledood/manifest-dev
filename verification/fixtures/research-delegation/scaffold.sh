#!/usr/bin/env bash
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
mkdir -p sources
cp "$fixture"/sources/* sources/
