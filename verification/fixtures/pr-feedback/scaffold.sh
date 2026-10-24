#!/usr/bin/env bash
set -euo pipefail
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cp -R "$fixture/project/." .
case ${1:-feedback} in
    feedback) ;;
    nits)
        python3 -B - <<'PY'
from pathlib import Path
path = Path('order_export.py')
path.write_text(path.read_text().replace('order["lines"][:-1]', 'order["lines"]'))
PY
        ;;
    *) echo 'expected feedback or nits' >&2; exit 2 ;;
esac
git branch -M main
git config user.name 'Feedback fixture'
git config user.email 'feedback@example.invalid'
git config commit.gpgsign false
git config core.hooksPath /dev/null
git add contract.md CLAUDE.md
git commit -qm 'Order export contract'
git update-ref refs/remotes/origin/main HEAD
git symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/main
git switch -qc feature/export
git add order_export.py
git commit -qm 'Export public order data'
python3 -B - <<'PY'
import copy
import hashlib
import json
from pathlib import Path
import subprocess

head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
url = 'https://github.com/example/review-fixture/pull/1'
base = {
    'capturedAt': '2026-10-24T12:00:00Z',
    'viewer': {'login': 'fixture-author'},
    'repository': {'defaultBranchRef': {'name': 'main'}, 'requiredApprovingReviewCount': 1},
    'pullRequest': {
        'url': url, 'number': 1, 'state': 'OPEN',
        'title': 'Export public order data',
        'body': 'Export identifiers, totals, and line SKUs under contract.md. Exclude private notes.',
        'author': {'login': 'fixture-author'},
        'headRefName': 'feature/export', 'baseRefName': 'main', 'headRefOid': head,
        'isCrossRepository': False, 'maintainerCanModify': True,
        'mergeable': 'MERGEABLE', 'mergeStateStatus': 'BLOCKED',
        'reviewDecision': 'REVIEW_REQUIRED',
        'reviewRequests': {'nodes': [{'requestedReviewer': {'login': 'fixture-maintainer'}}]},
        'statusCheckRollup': [{'name': 'fixture-tests', 'headSha': head, 'conclusion': 'SUCCESS', 'isRequired': True}],
        'reviews': {'nodes': []}, 'comments': {'nodes': []},
        'reviewThreads': {'nodes': []},
    },
}

def thread(identity, body, human=False):
    author = {'login': 'fixture-maintainer' if human else 'review-bot', '__typename': 'User' if human else 'Bot'}
    return {
        'id': identity, 'isResolved': False, 'isOutdated': False,
        'path': 'order_export.py', 'line': 4,
        'comments': {'nodes': [{
            'id': identity + '-comment', 'url': url + '#discussion_' + identity,
            'author': author, 'createdAt': '2026-10-24T12:00:00Z',
            'body': body, 'commit': {'oid': head},
        }]},
    }

current = copy.deepcopy(base)
current['pullRequest']['reviewThreads']['nodes'] = [
    thread('repeat-fixed', 'The export contains private_note. Remove that internal field.'),
    thread('repeat-declined', 'Use dict() instead of the dictionary literal for readability.'),
    thread('new-nit', 'Rename order to purchase_order to make the parameter more descriptive.'),
    thread('false-claim', 'This exporter adds VAT to the total twice.'),
    thread('separate-feature', 'Add currency conversion for international orders.'),
    thread('new-evidence', 'For lines [{"sku":"B","quantity":2,"unit_price":5},{"sku":"A","quantity":1,"unit_price":7}], total is 10. The contract requires 17.'),
    thread('required-review', 'I will not approve until the function is renamed export_v2. This is my naming preference.', human=True),
]
Path('pr-state.json').write_text(json.dumps(current, indent=2) + '\n')
for wave, body in [(1, 'Rename order to purchase_order to make the parameter more descriptive.'),
                   (2, 'Extract the dictionary literal into a helper to make the function shorter.')]:
    state = copy.deepcopy(base)
    state['capturedAt'] = f'2026-10-24T12:0{wave}:00Z'
    state['pullRequest']['reviewThreads']['nodes'] = [thread(f'nit-{wave}', body)]
    Path(f'pr-nits-{wave}.json').write_text(json.dumps(state, indent=2) + '\n')

Path('execution-log.md').write_text(f'''# Order export PR journal
Repository: https://github.com/example/review-fixture

## Prior completed work
Head: {head}; reviewed `order_export.py` against `contract.md` in a full judgment review.
Assessed file SHA-256 values:
- manifest.md: {hashlib.sha256(Path('manifest.md').read_bytes()).hexdigest()}
- contract.md: {hashlib.sha256(Path('contract.md').read_bytes()).hexdigest()}
- order_export.py: {hashlib.sha256(Path('order_export.py').read_bytes()).hexdigest()}
AC-1.1: PASS. No findings remain in that review.
AC-1.2: BLOCKED awaiting required maintainer approval.

## Earlier external feedback
- old-private: removed private_note from the export and verified the key is absent. Replied on that thread and resolved it before the recorded head.
- old-dict: declined the dict() rewrite because it changes no required behavior or readability problem. The dictionary literal follows the project's existing style. Replied and resolved it; no code change.
- earlier-name: declined a different suggestion to rename the local total variable. It had no demonstrated reader cost. No code change.

No reply or resolution has been sent for items created at or after the supplied snapshot's capture time.
''')
PY
