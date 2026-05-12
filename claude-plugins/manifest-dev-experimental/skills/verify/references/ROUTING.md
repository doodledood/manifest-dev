# Verifier Routing by Method

| Criterion `method:` | Verifier |
|--------------------|----------|
| `bash`, `codebase`, `research` | `criteria-checker` agent |
| `subagent` | the agent named in the criterion's `agent:` field |
| `manual` | `/escalate` (no automated check exists) |
| `deferred-auto` | skipped on normal passes; under `--deferred`, routed by the criterion's `inner_method:` field (required; missing → halt: `Deferred-auto criterion <ID> missing inner_method.`) |
| (none / unrecognized) | `criteria-checker` |

## Deferred-auto verify block

```yaml
verify:
  method: deferred-auto
  inner_method: subagent       # REQUIRED — one of: subagent | bash | codebase | research
  agent: general-purpose       # if inner_method: subagent
  command: "..."               # if inner_method: bash
  prompt: "..."                # if inner_method: subagent or research, or any inner_method that uses a prompt
```

Under `--deferred`, /verify routes the criterion identically to a non-deferred criterion of that `inner_method`.
