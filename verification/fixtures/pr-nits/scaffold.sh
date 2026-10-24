#!/usr/bin/env bash
set -euo pipefail
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
bash "$fixture/../pr-feedback/scaffold.sh" nits
