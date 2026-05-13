# Complete Output Format

Output the manifest path and stop. Substitute placeholders before printing:
- `{timestamp}` → the manifest filename's timestamp.
- `<dir>` → the current project directory in slug form (path separators → `-`, e.g., `-home-user-manifest-dev` for `/home/user/manifest-dev`).
- `${CLAUDE_SESSION_ID}` → the env value.

```text
Manifest complete: /tmp/manifest-{timestamp}.md
Session: ~/.claude/projects/<dir>/${CLAUDE_SESSION_ID}.jsonl

To execute: /do /tmp/manifest-{timestamp}.md
```

## Summary for Approval (precedes Complete)

Before emitting `Manifest complete:`, digest the manifest into a scannable summary the user approves at a glance. Plain language. **No manifest codes** (D1, AC-1.1, INV-G3), **no YAML**, **no structured-document vocabulary** ("acceptance criteria", "global invariants"). Default shape:

- **The plan** — one-line headline of what's being done and why.
- **What I'll build** — work items grouped naturally; don't enumerate every sub-task.
- **Guardrails** — invariants as plain rules.
- **How I'll verify** — brief description of verification approach.

Include an ASCII architecture diagram when the task has multiple components with inter-component flow.

**Test:** if it reads like a compressed manifest (codes, YAML, structured labels dressed up as prose; enumerated criteria; abstractions hiding content), rewrite. If it reads like something you'd say to a colleague, it's right.

After presenting, wait:
- *Approval* ("looks good", "approved") → emit Complete.
- *Feedback* ("also add X", "change Y") → revise manifest, re-present summary. Do not implement.
- *Explicit /do invocation* → /define is done; /do takes over.
- *Decline* ("scrap this", "cancel") → exit silently without writing the manifest.
