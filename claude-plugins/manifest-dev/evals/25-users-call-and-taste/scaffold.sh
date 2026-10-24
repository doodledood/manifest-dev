#!/usr/bin/env bash
set -euo pipefail
cat > preferences.md <<'EOF'
## Taste

- When choosing a messaging vendor (SMS, email, push), prefer one we already pay for over a new contract — every new vendor means another data-processing review and another bill to watch; yield when the existing vendor cannot deliver the channel at all.
- Keep builds small — the plainest version that does the job beats a clever one; yield when the plain version would mislead a customer.
EOF
