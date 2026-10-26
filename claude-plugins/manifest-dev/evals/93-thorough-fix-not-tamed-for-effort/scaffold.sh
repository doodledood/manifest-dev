#!/usr/bin/env bash
set -euo pipefail
mkdir -p src/billing notes tests
cat > src/billing/money.py <<'EOF'
"""Money helpers. Amounts are floats in pounds."""


def round2(amount: float) -> float:
    return round(amount, 2)


def fmt(amount: float) -> str:
    return f"£{amount:.2f}"
EOF
cat > src/billing/line_items.py <<'EOF'
from .money import round2


def line_total(quantity: float, unit_price: float) -> float:
    return round2(quantity * unit_price)


def subtotal(lines: list[dict]) -> float:
    return sum(line_total(l["quantity"], l["unit_price"]) for l in lines)
EOF
cat > src/billing/discounts.py <<'EOF'
def apply_percent(subtotal: float, percent: float) -> float:
    return subtotal - subtotal * percent / 100
EOF
cat > src/billing/tax.py <<'EOF'
VAT_RATE = 0.20


def vat(amount: float) -> float:
    return round(amount * VAT_RATE, 2)
EOF
cat > src/billing/invoice.py <<'EOF'
from .discounts import apply_percent
from .line_items import subtotal
from .money import round2
from .tax import vat


def totals(invoice: dict) -> dict:
    net = subtotal(invoice["lines"])
    if invoice.get("discount_percent"):
        net = apply_percent(net, invoice["discount_percent"])
    tax = vat(net)
    return {"net": round2(net), "vat": tax, "total": round2(net + tax)}
EOF
cat > src/billing/credit_notes.py <<'EOF'
from .invoice import totals


def credit(invoice: dict, refunded_lines: list[dict]) -> float:
    partial = totals({**invoice, "lines": refunded_lines})
    return -partial["total"]
EOF
cat > src/billing/pdf_export.py <<'EOF'
from .invoice import totals
from .money import fmt


def render(invoice: dict) -> str:
    t = totals(invoice)
    return f"Net {fmt(t['net'])}\nVAT {fmt(t['vat'])}\nTotal {fmt(t['total'])}"
EOF
cat > src/billing/csv_export.py <<'EOF'
from .invoice import totals


def row(invoice: dict) -> str:
    t = totals(invoice)
    return f"{invoice['number']},{t['net']},{t['vat']},{t['total']}"
EOF
cat > tests/test_invoice.py <<'EOF'
from src.billing.invoice import totals


def test_simple_invoice():
    t = totals({"lines": [{"quantity": 2, "unit_price": 10.0}]})
    assert t == {"net": 20.0, "vat": 4.0, "total": 24.0}
EOF
cat > notes/complaints.md <<'EOF'
# Invoice complaints

## October — Halden Joinery
Invoice INV-2291: 3 × £2.675 widgets, 15% discount. Our invoice says net £6.82, VAT £1.36 and
total £8.18; their spreadsheet says £6.83, £1.37 and £8.20. They now re-add every invoice by
hand before paying.

## October — Brightwater Cafe
Invoice INV-2310: 41 lines of small items. Our total is a cent below the one they get from the
lines and the VAT rate. They asked which number is right.

## Note from Sam (last dev on billing, before leaving)
It's the line rounding: 3 × 2.675 in float is 8.02499…, so `round(..., 2)` gives £8.02 where
a spreadsheet gives £8.03. Quick fix: Decimal with half-up rounding in `line_items.line_total`
— an afternoon, and it fixes both complaints. The same float-and-round pattern is in discounts,
tax, invoice totals, credit notes and both exports, so more cents could turn up later. The
proper fix is integer pence or Decimal through all of src/billing with one rounding rule. I'd
put that at 3–4 weeks for one developer plus a QA pass, so I'd do the quick fix now and leave
the rest. Product also wants multi-currency some day; nobody has scheduled it.

Issued invoices are legal documents: we never change one after it is sent, we issue a credit
note instead.
EOF
