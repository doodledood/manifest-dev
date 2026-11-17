#!/usr/bin/env bash
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
bash "$fixture/../pr-feedback/scaffold.sh" nits
