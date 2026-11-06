# Definition: Readable labels and exact fees

## 1. Intent
- **Outcome:** Labels remain readable and fee calculations preserve exact integer cents.
- **Outcome evidence:** Inspect the finished artifacts and exercise the uses stated below.
- **Problem:** The page needs readable labels and the fee calculation must keep exact integer cents.
- **Appetite:** The existing label function and integer fee calculation, with their check.
- **Out of bounds:** INV-G1.

## 3. Global Invariants

### INV-G1 — Keep the accepted contract and check

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Do not change this Manifest or check.py, and make no network calls. Label spacing is presentation only: the contract requires readable text, with no exact spacing or Unicode-normalization promise.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

## 6. Deliverables

### Deliverable 1: Readable labels and exact fees

#### AC-1.1 — Labels remain readable

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Activate review-code with dimension=change-intent on label in display.py against this Manifest, using caller acceptance policy no Medium-or-higher findings. The label shows the supplied text readably. Exact whitespace normalization is not required.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

#### AC-1.2 — Fee calculations preserve integer cents

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

For nonnegative integer cents and fee, with fee no greater than cents, net_after_fee in display.py returns cents minus fee. Read the code and activate review-code with dimension=code-bugs to evaluate the result against this promise using caller acceptance policy no Medium-or-higher findings.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Judgment gate.

#### AC-1.3 — The unchanged check passes

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

Run python3 check.py. It exits zero.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.
