#!/usr/bin/env bash
set -euo pipefail
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
mkdir -p sources
cp "$fixture"/sources/* sources/
