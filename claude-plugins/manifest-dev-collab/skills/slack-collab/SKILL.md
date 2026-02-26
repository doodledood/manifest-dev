---
name: slack-collab
description: 'Orchestrate team collaboration on define/do workflows through Slack. A Python script drives phases deterministically; Claude handles intelligent work. Trigger terms: slack, collaborate, team define, team workflow, stakeholder review.'
---

# /slack-collab - Collaborative Define/Do via Slack

Launch the Python orchestrator that drives a full define → do → PR → review → QA → done workflow with your team through Slack.

`$ARGUMENTS` = task description (what to build/change), or `--resume <state-file-path>` to resume a crashed session.

## What to Do

Run the orchestrator script in the background. The script lives at `scripts/slack-collab-orchestrator.py` relative to this plugin's root directory (one level up from `SKILL.md`'s location: `${CLAUDE_PLUGIN_ROOT}/../scripts/`).

**New workflow:** Run the script with the task description as the argument. Use `run_in_background` so the user gets control back immediately.

**Resume a crashed workflow:** If `$ARGUMENTS` starts with `--resume`, run the script with `--resume <state-file-path>` instead of a task description.

After launching, tell the user:
- The workflow has started and is running in the background.
- They should follow along in the Slack channel that will be created.
- If the process crashes, they can resume with: `/slack-collab --resume /tmp/collab-state-<id>.json`
- The state file path will be in the script's stderr output.

If `$ARGUMENTS` is empty, ask what they want to build or change, then launch the script with their answer.
