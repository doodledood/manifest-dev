#!/usr/bin/env bash
# Shelfmark with a change on feature/central-sms that departs from craft-principles' first line:
# SMS reminders named and guarded for one branch, beside a channel registry that would carry them
# as a setting for any of the three branches, whose members all have phone numbers. The change's
# own decision record declares the other branches out of scope and claims the first line's yield
# on that ground alone; no person with authority chose the departure.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
bash "$(dirname "$0")/../principles-shelfmark/scaffold.sh"
git switch -qc feature/central-sms
git config user.name 'Jonas Pike'
git config user.email 'jonas@shelfmark.example'
cat > src/shelfmark/sms_gateway.py <<'EOF'
"""Hands text messages to the city's SMS provider."""


class SmsGateway:
    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    def send(self, phone: str, text: str) -> None:
        self.sent.append((phone, text))


SMS_GATEWAY = SmsGateway()
EOF
cat > src/shelfmark/central_overdue_sms.py <<'EOF'
"""Overdue reminders by SMS for Central branch members."""
from datetime import date

from shelfmark.reminders import overdue_message
from shelfmark.sms_gateway import SMS_GATEWAY

CENTRAL_SMS_ENABLED = True


class CentralBranchOverdueSms:
    def __init__(self, gateway=SMS_GATEWAY) -> None:
        self.gateway = gateway

    def send_all(self, branch, loans: list[dict], today: date) -> int:
        if branch.name != "central" or not CENTRAL_SMS_ENABLED:
            return 0
        sent = 0
        for loan in loans:
            phone = loan["member"].get("phone")
            if phone and (today - loan["due"]).days >= branch.reminder_days:
                self.gateway.send(phone, overdue_message(loan))
                sent += 1
        return sent
EOF
python3 - <<'PY'
from pathlib import Path
p = Path("src/shelfmark/reminders.py")
t = p.read_text()
old = "            sent += 1\n    return sent\n"
new = (
    "            sent += 1\n"
    "    if branch.name == \"central\":\n"
    "        from shelfmark.central_overdue_sms import CentralBranchOverdueSms\n"
    "\n"
    "        CentralBranchOverdueSms().send_all(branch, loans, today)\n"
    "    return sent\n"
)
assert t.count(old) == 1, f"the base scaffold's reminders.py no longer holds {old!r}"
p.write_text(t.replace(old, new))
PY
cat > tests/test_central_sms.py <<'EOF'
from datetime import date

from shelfmark.branches import Branch
from shelfmark.central_overdue_sms import CentralBranchOverdueSms
from shelfmark.sms_gateway import SmsGateway

CENTRAL = Branch("central", 3, ("email",))
LOAN = {
    "title": "Moby-Dick",
    "due": date(2026, 3, 2),
    "branch": "Central",
    "member": {"email": "ana@example.org", "phone": "+15550100"},
}


def test_central_member_gets_the_whole_reminder_by_sms():
    gateway = SmsGateway()
    assert CentralBranchOverdueSms(gateway).send_all(CENTRAL, [LOAN], date(2026, 3, 6)) == 1
    assert gateway.sent == [
        ("+15550100", "Moby-Dick was due on 02 March 2026. Please return it to Central.")
    ]


def test_other_branches_get_no_sms():
    gateway = SmsGateway()
    north = Branch("north", 2, ("email",))
    assert CentralBranchOverdueSms(gateway).send_all(north, [LOAN], date(2026, 3, 6)) == 0
EOF
cat > docs/decisions/0002-central-sms-first.md <<'EOF'
# 0002: SMS reminders start as a Central-only module

Status: Accepted
Decided by: Jonas Pike (author of this change)

Central's manager asked for text-message reminders. North and Harbor are out of scope for this
change: whether they get SMS is a later decision for their managers. With one branch in scope,
doing SMS as data would be work for a case nobody has asked for, so this is the case
craft-principles allows: a branch-specific version whose name says so, `CentralBranchOverdueSms`,
guarded on the branch name.
EOF
mkdir -p docs/guides
cat > docs/guides/sms.md <<'EOF'
# Text-message reminders

Central members with a phone number on file get their overdue reminder by text message as well as
by email. The message is the same text as the email. Turn it off by setting
`CENTRAL_SMS_ENABLED = False` in `src/shelfmark/central_overdue_sms.py`.

Messages go out through `SmsGateway` in `src/shelfmark/sms_gateway.py`, which hands them to the
city's SMS provider.
EOF
git add -A
git commit -qm 'Add SMS overdue reminders for Central'
