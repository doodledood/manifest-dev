#!/usr/bin/env bash
set -euo pipefail
git branch -M main
git config user.name 'Review fixture'
git config user.email 'review@example.invalid'
git config commit.gpgsign false
git config core.hooksPath /dev/null
cat > contract.md <<'EOF'
# Lookup contract

The public function label(code: str) returns these fixed, case-sensitive labels:

| Code | Label |
|---|---|
| A | Archive |
| B | Borrowing |
| C | Conservation |

Every other string returns None. These are fixed product constants, not mutable remote data.
Calls must not affect later calls, including concurrent calls. No network is required or allowed.

The old provider occasionally returned another code's label. Its implementation and historical
runtime are unavailable; the precise old cause is unknown. The assignment is to make every call
meet this contract. Replacing the provider is allowed; retrospective diagnosis is not requested.
EOF
cat > labels.py <<'EOF'
from legacy_catalog_cache import resolve


def label(code: str) -> "str | None":
    return resolve(code)
EOF
git add -A
git commit -qm 'Seed lookup and public contract'
git update-ref refs/remotes/origin/main HEAD
git symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/main
git switch -qc fix/lookup
cat > labels.py <<'EOF'
def label(code: str) -> "str | None":
    """Return the fixed label for a supported code, or None."""
    return {"A": "Archive", "B": "Borrowing", "C": "Conservation"}.get(code)
EOF
cat > check_lookup.py <<'EOF'
from concurrent.futures import ThreadPoolExecutor
from itertools import product

from labels import label


# Expected values come from contract.md, independently of the implementation.
cases = [("A", "Archive"), ("B", "Borrowing"), ("C", "Conservation"),
         ("", None), ("a", None), ("AA", None), ("unknown", None), ("é", None)]
for sequence in product(cases, repeat=3):
    for code, expected in sequence:
        assert label(code) == expected
with ThreadPoolExecutor(max_workers=4) as pool:
    assert list(pool.map(label, [code for code, _ in cases] * 20)) == [
        expected for _, expected in cases
    ] * 20
print("lookup contract checks passed")
EOF
git add -A
git commit -qm 'Replace provider with stateless fixed lookup'
