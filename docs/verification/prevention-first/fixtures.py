import json
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
if root.exists():
    raise SystemExit(
        "Choose a new output directory; fixtures never overwrite an existing run"
    )
root.mkdir(parents=True)
owner = (
    "sent = []\n\ndef send(quantity):\n    sent.append(quantity)\n    return quantity\n"
)
callers = "from owner import send\n\ndef web(quantity):\n    return send(quantity)\n\ndef batch(quantity):\n    return send(quantity)\n"
guarded = 'from owner import send\n\ndef web(quantity):\n    if quantity <= 0:\n        raise ValueError("quantity must be positive")\n    return send(quantity)\n\ndef batch(quantity):\n    if quantity <= 0:\n        raise ValueError("quantity must be positive")\n    return send(quantity)\n'
protected = owner.replace(
    "    sent.append(quantity)",
    '    if quantity <= 0:\n        raise ValueError("quantity must be positive")\n    sent.append(quantity)',
)
base = {"owner.py": owner, "callers.py": callers}
spec = "The application ships orders with positive quantities. Zero/negative quantities must never be shipped. send is the supported shipping operation. The reported defect was web(-1) appending a negative shipment. Review the repair. Both tracked callers are in application scope unless an explicit exclusion says otherwise."
cases = []


def add(n, before, after, context, dim="defect-class"):
    p = root / f"case{n:02d}"
    p.mkdir(exist_ok=True)

    def git(*args):
        return subprocess.check_output(
            ["git", "-C", str(p), *args], stderr=subprocess.STDOUT, text=True
        ).strip()

    git("init", "-q", "-b", "main")
    git("config", "user.name", "Evaluation")
    git("config", "user.email", "eval@example.invalid")
    for name, text in before.items():
        (p / name).write_text(text)
    git("add", ".")
    git("commit", "-qm", "baseline")
    sha = git("rev-parse", "HEAD")
    for name, text in after.items():
        (p / name).write_text(text)
    git("add", ".")
    git("commit", "-qm", "reviewed change")
    cases.append(
        {
            "id": p.name,
            "path": str(p),
            "base": sha,
            "head": git("rev-parse", "HEAD"),
            "dimension": dim,
            "context": context,
        }
    )


add(1, base, {"callers.py": guarded}, spec)
helper = 'from owner import send\n\ndef checked_send(quantity):\n    if quantity <= 0:\n        raise ValueError("quantity must be positive")\n    return send(quantity)\n'
add(
    2,
    base,
    {
        "helpers.py": helper,
        "callers.py": callers.replace(
            "from owner import send", "from helpers import checked_send as send"
        ),
    },
    spec
    + " Author says the shared helper prevents the defect class; owner.send stays public and supported.",
)
add(3, base, {"owner.py": protected}, spec)
add(
    4,
    base,
    {"owner.py": protected},
    spec
    + " Review the maintainability of this repair, which adds three lines and removes no lines. It moves the obligation from callers to the only operation that ships.",
    "code-maintainability",
)
b5 = {
    **base,
    "credits.py": "credits = []\n\ndef adjust(quantity):\n    credits.append(quantity)\n    return quantity\n",
}
add(
    5,
    b5,
    {"owner.py": protected},
    spec
    + " credits.adjust records account adjustments; negative quantities there are valid refunds and do not ship orders.",
)
add(
    6,
    base,
    {"callers.py": guarded},
    spec
    + " Explicit owner constraint: only callers.py may change in this maintenance release. owner.py is a frozen external SDK compatibility surface; current application callers must reject invalid quantities. Changing the shared API is forbidden. The author records future-caller exposure and includes regression checks for both application entry points.",
)
add(
    7,
    base,
    {
        "callers.py": guarded.replace(
            'def batch(quantity):\n    if quantity <= 0:\n        raise ValueError("quantity must be positive")\n    return send(quantity)',
            "def batch(quantity):\n    return send(quantity)",
        )
    },
    spec
    + " Author says batch is out of scope because the initial plan only named web; both are active supported entry points. No owner exclusion exists.",
)
add(
    8,
    {"owner.py": owner, "callers.py": guarded, "README.md": "# Orders\n"},
    {"README.md": "# Order shipping\n"},
    "Review only the supplied base..head range. An earlier repair guarded callers but left owner.send permissive. This range changes only a README heading; no defect is repaired here.",
)
add(
    9,
    base,
    {"callers.py": guarded},
    spec
    + " The product also loads user-supplied shipping plugins unavailable in this checkout. The task requires accounting for all supported shipment paths. No plugin inventory or access is available; author marks the unenumerated region closed as out of scope.",
)
add(
    10,
    base,
    {"callers.py": guarded},
    spec
    + " Binding task outcome: the supported owner.send operation itself must reject invalid quantities, including new callers. Explicit permission limit: owner.py cannot be changed and the API cannot be replaced. There is no approved alternate owner. The current caller patch is the only authorized code edit.",
)
feature_base = 'events = []\n\ndef alpha(value):\n    result = value + 1\n    events.append(("alpha", result))\n    return result\n\ndef beta(value):\n    result = value * 2\n    events.append(("beta", result))\n    return result\n'
feature_new = (
    feature_base
    + '\ndef gamma(value):\n    result = value - 1\n    events.append(("gamma", result))\n    return result\n'
)
add(
    11,
    {"processors.py": feature_base},
    {"processors.py": feature_new},
    "New feature: add gamma processor. Every processor must record its successful result in events. More processors are planned. Entry points currently own both the transformation and event recording; a dispatcher could own event recording once. Author deliberately copied existing code to keep this diff short. A dispatcher would add lines but eliminate independently maintained recording obligations. No explicit owner exclusion forbids it. Judge maintainability; no bug is reported.",
    "code-maintainability",
)
(root / "cases.json").write_text(json.dumps(cases, indent=2) + "\n")

# Supplemental scope/coverage cases were added after the first paired run.
one = dict(cases[0])
one["id"] = "case12"
one[
    "context"
] += " Author disposition: owner.send is named out of scope because no current application caller omits the new checks and the planned patch named only callers.py. This is an implementation rationale, not an owner exclusion or permission limit."
two = dict(cases[2])
two["id"] = "case13"
two[
    "context"
] += " A required deployment integration loads third-party shipment plugins from an external registry. They can use separate shipping transports. No registry inventory, plugin source or runtime access is available in this review. The binding task requires verifying remediation of the demonstrated nonpositive-shipment mechanism across those integrations as well. Author calls the unenumerated plugin region closed because it cannot be searched."
(root / "supplemental-cases.json").write_text(json.dumps([one, two], indent=2) + "\n")
