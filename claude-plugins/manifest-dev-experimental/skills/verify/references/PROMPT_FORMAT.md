# Verifier Prompt Format

Pass each verifier exactly three sections, **in this order, each on its own line**:

1. **Cross-repo prefix** (ONLY when the manifest declares `Repos:`) — verbatim string from `../../define/references/MULTI_REPO.md` §e (single source of truth). Single-repo manifests skip this line entirely.
2. **Optional context line** (ONLY when at least one of manifest / discovery log / execution log path exists) — format: `Optional context — manifest: <path>, discovery log: <path>, execution log: <path>`. Include only paths that exist. Informational, not directive.
3. **Criterion content** — the criterion's manifest data: ID, description, verification method, and the verify block's `command:` or `prompt:` field **verbatim**. If `prompt:` is absent (e.g., bash criteria with only `command:`), pass the criterion's description as the agent prompt instead. Add file scope when the criterion targets specific files.

## Never add framing to criterion content

- Severity thresholds ("only report medium+ issues", "focus on critical findings")
- Implementation context ("the code was refactored to...", "this was implemented by...")
- Opinions or expectations ("this should pass", "this is likely fine")
- Leading language ("verify this important constraint", "carefully check this critical rule")
- Task summaries ("check that the auth module correctly handles...")
- Suggested outcomes ("confirm that X works correctly")
- Interpretations of manifest intent ("the goal is to...", "this change is about...")

The verify block's `prompt:` is manifest-authored — pass it verbatim. The cross-repo prefix is the one prescribed exception, because it's manifest-driven (derived from `Repos:`), not orchestrator opinion. The optional context line is raw references, not framing — it provides access to source material without steering the agent's analysis.
