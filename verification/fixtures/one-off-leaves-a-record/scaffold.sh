#!/usr/bin/env bash
# The one-off-leaves-a-record scenario of verification/recipes/do.md: a run resumed after its build,
# whose first order_shipping_cents gave free shipping from 51 units, failed its test at 50, and was
# repaired. pulls/3.md records a repair of a different kind on the same file. No gate has been
# evaluated yet.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cp -R "$fixture/project/." .
git config user.name 'One-off fixture'
git config user.email 'one-off@example.invalid'
git config commit.gpgsign false
git config core.hooksPath /dev/null
git add .
git commit -qm 'Shipping charges'
python3 -B - <<'PY'
from pathlib import Path
shipping = Path('shipping.py')
shipping.write_text(shipping.read_text() + '''

def order_shipping_cents(units, grams):
    """Return the shipping charge for an order; large orders ship free."""
    if units > 50:
        return 0
    return shipping_cents(grams)
''')
tests = Path('test_shipping.py')
tests.write_text(tests.read_text().replace(
    'from shipping import carrier_weight_kg, shipping_cents',
    'from shipping import carrier_weight_kg, order_shipping_cents, shipping_cents',
).replace('''

if __name__''', '''
    def test_49_units_pay_shipping(self):
        self.assertEqual(order_shipping_cents(49, 2500), shipping_cents(2500))

    def test_50_units_ship_free(self):
        self.assertEqual(order_shipping_cents(50, 2500), 0)


if __name__'''))
PY
git commit -qam 'Add order_shipping_cents'
first=$(git rev-parse --short HEAD)
sed -i 's/if units > 50:/if units >= 50:/' shipping.py
git commit -qam 'Ship free from 50 units'
repair=$(git rev-parse --short HEAD)
cat > execution-log.md <<LOG
# Free shipping execution
Repository: local scratch project

## Run initialized
Manifest: ./manifest.md. One Deliverable, \`order_shipping_cents\`.

## Build
- $first Add order_shipping_cents. First version tested \`if units > 50\`.
- \`python3 -m unittest -q\` failed: test_50_units_ship_free, \`AssertionError: 855 != 0\`.
- Dead end: the threshold excluded 50 units, which the Manifest includes.
- $repair Ship free from 50 units: \`if units >= 50\`. \`python3 -m unittest -q\`: 4 tests, OK.

## Build done
Deliverable 1 is built at $repair. No gate has been evaluated yet.
LOG
