#!/usr/bin/env bash
# The self-repair-harvested scenario of verification/recipes/do.md: a run resumed after its build,
# whose first version of add_tax returned a float, failed the tests, and was repaired. No gate has
# been evaluated yet.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cp -R "$fixture/project/." .
git config user.name 'Self-repair fixture'
git config user.email 'self-repair@example.invalid'
git config commit.gpgsign false
git config core.hooksPath /dev/null
git add .
git commit -qm 'Money helpers'
python3 -B - <<'PY'
from pathlib import Path
money = Path('money.py')
money.write_text(money.read_text() + '''

def add_tax(cents, rate_percent):
    """Return cents with tax added."""
    return round(cents * (1 + rate_percent / 100), 2)
''')
tests = Path('test_money.py')
tests.write_text(tests.read_text().replace(
    'from money import apply_discount, line_total',
    'from money import add_tax, apply_discount, line_total',
).replace('''

if __name__''', '''
    def test_add_tax_rounds_half_up(self):
        self.assertEqual(add_tax(999, 8), 1079)

    def test_add_tax_whole_amount(self):
        self.assertEqual(add_tax(1000, 8), 1080)


if __name__'''))
PY
git commit -qam 'Add add_tax'
first=$(git rev-parse --short HEAD)
python3 -B - <<'PY'
from pathlib import Path
money = Path('money.py')
money.write_text(money.read_text().replace(
    '''    """Return cents with tax added."""
    return round(cents * (1 + rate_percent / 100), 2)''',
    '''    """Return cents with tax added, rounded half up to a whole cent."""
    return (cents * (100 + rate_percent) + 50) // 100''',
))
PY
git commit -qam 'Round add_tax to whole cents'
repair=$(git rev-parse --short HEAD)
cat > execution-log.md <<LOG
# Tax-inclusive prices execution
Repository: local scratch project

## Run initialized
Manifest: ./manifest.md. One Deliverable, \`add_tax\`.

## Build
- $first Add add_tax. First version: \`return round(cents * (1 + rate_percent / 100), 2)\`.
- \`python3 -m unittest -q\` failed: test_add_tax_rounds_half_up, \`AssertionError: 1078.92 != 1079\`.
- Dead end: float arithmetic on cents; add_tax returned a float with fractions of a cent.
- $repair Round add_tax to whole cents: \`(cents * (100 + rate_percent) + 50) // 100\`.
  \`python3 -m unittest -q\`: 4 tests, OK.

## Build done
Deliverable 1 is built at $repair. No gate has been evaluated yet.
LOG
