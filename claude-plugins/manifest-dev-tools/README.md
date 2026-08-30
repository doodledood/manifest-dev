# manifest-dev-tools

Tools that sit alongside the workflow: pull requests, prompts, teaching, and handoff.

```bash
/plugin install manifest-dev-tools@manifest-dev
```

## Pull requests

Three skills cover the two sides of a review:

| Skill | What it does |
|-------|--------------|
| `/review-pr` | Reviews a pull request on its own and posts the findings under your account, advancing existing threads rather than repeating them. |
| `/babysit-pr` | The author's side: tends a pull request through checks, review threads, and mergeability. Never presses merge. |
| `/walk-pr` | Walks a large diff with you, one piece at a time. |

## Prompts

One writes prompts, the other reviews them:

| Skill | What it does |
|-------|--------------|
| `/prompt-engineering` | Writes, revises, or discusses a prompt — a system prompt, a skill, or an agent. |
| `review-prompt` | Reviews a prompt against those principles and reports what it finds without editing anything. |

## People and sessions

These carry context across a boundary:

| Skill | What it does |
|-------|--------------|
| `/handoff` | Packages what a session established so a fresh agent can carry on without re-deriving it. |
| `/teach-me` | Teaches a body of work — this session, a pull request, a decision record, any topic — and checks you've got it before moving on. |
| `/eli5` | Explains any topic from zero, as an HTML page of big pictures and few words. |

`/review-pr` and `/babysit-pr` can run on the same pull request at once: one applies review pressure, the other drives it toward mergeable.
