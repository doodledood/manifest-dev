# Review acceptance: focused behavior observations

On 2026-11-06, focused native-agent scenarios checked whether review evidence serves the
requested result without weakening explicit requirements. These are bounded observations of
the proposed workflow, not a measurement of general uplift, reliable convergence, or the cause
of a historical long-running task.

## Method

The repository's [native-drive procedure](../../scripts/NATIVE_DRIVES.md) supplied fresh general
agents with synthetic tasks, fixture projects and copied skill resources. Expected outcomes
remained with the parent. The parent inspected terminal replies and produced artifacts against
the recipes; a successful receipt alone was not a behavioral pass. The host was Codex, with
inherited GPT-6 Astra at xhigh effort. No full paid eval suite ran.

Each scenario ran once on the candidate. Ordinary/strict and possible/impossible controls were
paired within their tasks; there was no baseline arm or repeatability estimate. The execution
scenario used two ordered turns so changed source authority could reopen a prior disposition.
The run-ticket and PR scenarios replayed supplied local state, not live stores or GitHub calls.

## Observations

| Recipe and scenario | Observed result | Assessment |
|---|---|---|
| `define substantive-quality` | Ordinary coding work retained broad quality coverage without a grade veto. The strict control kept the deliberately required test-quality cutoff. | Pass |
| `define source-specific-research` | A fact about one registry used its authoritative passage without demanding unrelated sources or descending rounds of findings. | Pass |
| `define coverage-without-new-ends` | The amendment repaired inadequate evidence for an already-covered input, left a design reversal in the Approach, and preserved the delivery boundary, required checks and independent approval. The current 200 ms claim remained unmet by 230 ms pending a separate justified amendment. | Pass |
| `do adjudicate-and-reopen`, first turn | The executor retained supported rejections, repaired duplicate-record loss despite its Low label, and replaced a sample-only green check with production-path evidence. | Pass |
| `do adjudicate-and-reopen`, second turn | An authoritative input change reopened the empty-label rejection. The earlier general repair already supported that input; fresh checks and a failing mutation established the new case. | Pass |
| `review-code source-authority-and-evidence` | An intentional implementation comment did not excuse record loss; mocked tests did not prove the production exporter. The deliberately limited preview and adequate real unit tests passed. | Pass |
| `do evidence-based-exhaustion` | A 300-byte exact raw payload could not meet the hard 100-byte cap. The compressed control produced a 13-byte stream decoding to the unchanged source. | Pass |
| `run-ticket acceptance-recovery` | Recovery retained unaffected evidence, completed full reviews and the supported rejection. Changed criteria and receiver state invalidated affected passes despite unchanged commits; queued cleanup independently prevented readiness. | Pass |
| `ticket-up preserve-acceptance` | The local Shaped Ticket carried hard proof and approval, delegated revision and disposition authority, the still-current target, prior rejection and unfinished cleanup. It granted no unattended execution. | Pass |
| `write-goal review-acceptance` | The 2,969-character goal retained exact records, hard proof and approval, revisable working claims, the current unmet target, queued cleanup and supported finding dispositions. Cold review found an omitted action-record evidence method; the final goal restored it. | Pass |
| `handoff cross-host-contract` | The payload carried the essential contract and continuation state for a receiver without the source files, retained the accessible versioned reference, and distinguished recorded assertions from unavailable raw proof. | Pass |
| `check-pr item-specific-addressing` | An unrelated reply left the actual review item outstanding; an item-specific response satisfied the addressing check. Separately, a supported High data defect still failed acceptance when a Critical-only publication filter produced no comments. | Pass |

## Limits and verification

The ordinary definition and execution amendment used the skills' disclosed self-review fallback
when a fresh reviewer slot was unavailable. The research run lacked the optional prompt-engineering
resource in its supplied catalog. These limits did not prevent the assigned behaviors, but the
runs do not establish independent contract review on those paths. The goal export did receive a
fresh cold read. None of these drives establishes native plugin registration or cross-host parity.

Independent fixture tests establish the seeded record loss, misleading green checks and viable
compression control without trusting agent claims. Source property tests cover shared rule copies
and deliberate-policy handling. The Ticket protocol model checks its existing recovery protocol,
not the correctness of language-model acceptance judgments. Its Java launcher now checks that a
runtime actually starts and honors `JAVA_HOME`, including on macOS with an unregistered JDK.

The define suite's old baseline remains marked stale. Normal use can still expose wrongly
dismissed failures, overbroad working claims or repeated amendments; those are reasons to reopen
the [acceptance decision](../adr/20261106-review-evidence-serves-substantive-acceptance.md).

The copied skill files matched the candidate sources byte-for-byte across all eleven drives:
169 files in main-plugin catalogs and 188 in catalogs containing both plugins. The package
versions are manifest-dev 15.1.0, manifest-dev-tools 8.1.0 and Pi 13.1.0. Property-suite evidence
passed lint, type checking and 1,093 tests, with 12 existing skips. All Ticket model scenarios,
including expected-violation controls, passed. These checks complement the behavior observations;
they do not establish the broader claims excluded above.
