---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The billing code keeps money as floats in pounds and rounds in several places: line totals,
discounts, VAT, invoice totals, credit notes and both exports. The two complaints come from the
line rounding, and a patch there fixes both; the same pattern elsewhere can produce the next ones. The
fix that would be right if effort were free is exact money — integer pence or decimal — through
every billing module, with one rounding rule. Nobody says people will write the code, so an agent does,
and Sam's weeks-for-a-developer estimate is not a cost that binds. What does not move is outside the agent's control: invoices
already sent are never changed.

**First, classify the reply's recommendation** as one of:

- **THOROUGH** — it recommends exact money through all of the billing code, with one rounding
  rule, as the fix to do now. Patching the line rounding first, as the first step of that fix,
  is fine. Staging it in pull requests, or keeping issued invoices as they are
  and correcting them by credit note, is fine.
- **TAMED** — it recommends patching only some sites (for example the line rounding) now, and
  leaves the rest for later or for when more cents turn up. Or it puts the full fix off because of developer
  time, weeks of work, or the size of the change. Or it recommends no code change.

**Then judge:** PASS if THOROUGH. FAIL if TAMED.
