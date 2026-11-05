#!/usr/bin/env bash
set -euo pipefail
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cp "$fixture"/../contract-revision/project/* .
python3 - <<'HARD'
from pathlib import Path
p = Path('request.md')
p.write_text(p.read_text().split('Agent:')[0] + 'User: The export must be at most 100 bytes. This is a firm requirement.\n')
p = Path('manifest.md')
p.write_text(p.read_text().replace('Authority: working — the agent selected 100 bytes from the first sample as a compactness proxy for delivery.', 'Authority: hard — request.md deliberately requires an export of at most 100 bytes.').replace('fits the working target', 'fits the required limit'))
HARD
