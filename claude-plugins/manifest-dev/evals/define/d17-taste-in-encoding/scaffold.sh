#!/usr/bin/env bash
set -euo pipefail
cat > preferences.md <<'EOF'
## Taste

- For anything customers see, ship it behind a switch I can turn off without a deploy — a bad customer-facing change at 6am cannot wait for a release; yield for changes with no customer-visible effect.
- Don't over-engineer — fewer gates and less ceremony; yield when money or customer data is at stake.
EOF
