#!/usr/bin/env bash
set -euo pipefail
fixture=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
bash "$fixture/../pr-feedback/scaffold.sh"
python3 -B - <<'PY'
import copy
import json
from pathlib import Path
state = json.loads(Path('pr-state.json').read_text())
pr = state['pullRequest']
pr['reviewThreads']['nodes'] = []
pr['reviewRequests']['nodes'] = []
pr['reviewDecision'] = 'APPROVED'
pr['mergeStateStatus'] = 'CLEAN'
state['repository']['requiredApprovingReviewCount'] = 0
pr['reviews']['nodes'] = [{'id': 'review-9', 'url': pr['url']+'#pullrequestreview-9', 'state': 'COMMENTED', 'author': {'login': 'reviewer'}, 'submittedAt': '2026-10-24T12:00:00Z', 'body': 'Please document the supported empty-order behavior.'}]
pr['comments']['nodes'] = [{'id': 'reply-10', 'url': pr['url']+'#issuecomment-10', 'author': {'login': 'fixture-author'}, 'createdAt': '2026-10-24T12:01:00Z', 'body': 'The new logo has been added.'}]
Path('unrelated-reply.json').write_text(json.dumps(state, indent=2)+'\n')
addressed=copy.deepcopy(state)
addressed['pullRequest']['comments']['nodes'].append({'id': 'reply-11', 'url': pr['url']+'#issuecomment-11', 'author': {'login': 'fixture-author'}, 'createdAt': '2026-10-24T12:02:00Z', 'body': 'Regarding review-9: empty orders are supported; the exporter returns an empty items list and a zero total. This is now stated in the description. No new behavior is intended.'})
addressed['pullRequest']['body'] += ' Empty orders are supported and produce an empty items list and zero total.'
Path('addressing-reply.json').write_text(json.dumps(addressed, indent=2)+'\n')
PY
