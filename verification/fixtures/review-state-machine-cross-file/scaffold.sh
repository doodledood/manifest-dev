#!/usr/bin/env bash
set -euo pipefail
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cp "$fixture"/{README.md,store.py,payments.py,shipping.py,delivery.py,refunds.py} .
git branch -M main
git config user.name 'Orders fixture'
git config user.email 'orders@example.invalid'
git config commit.gpgsign false
git config core.hooksPath /dev/null
git add .
git commit -qm 'Order service: pay, ship, deliver, nightly refunds'
git switch -qc feature/cancel
cat > cancel.py <<'PY'
import store


def cancel(order_id: str) -> bool:
    """Let a customer cancel an order that has not reached them yet."""
    order = store.get(order_id)
    if order["status"] == "delivered":
        return False
    order["cancelled"] = True
    return True
PY
git add cancel.py
git commit -qm 'Let customers cancel an order before delivery'
