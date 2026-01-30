# GIF Recording Script: `/define` Demo

## Specs

- **Length**: 30-45 seconds when played (can be sped up 1.5-2x)
- **Resolution**: 1200x800 or similar (readable on mobile)
- **Tool**: asciinema + gif conversion, or native screen recording
- **Font size**: Large enough to read on Twitter/LinkedIn mobile

---

## The Task

**Use case**: Adding a CLI flag to an existing tool

This is relatable (every dev has done it) and small enough to show the full flow quickly.

---

## Script

### Frame 1: Invocation (2-3 sec)

```
$ claude

> /define add a --dry-run flag to the deploy command
```

### Frame 2: Claude Explores (3-4 sec)

Show Claude's thinking briefly:

```
I'll explore the existing deploy command to understand the current
structure before we define criteria...

Reading src/commands/deploy.ts...
Found: deploy command with --env and --force flags
```

### Frame 3: First Interview Question (5-6 sec)

```
A few questions to nail down the requirements:

1. What should --dry-run output?
   a) Just "would deploy X" summary (Recommended)
   b) Full diff of what would change
   c) Both, controlled by verbosity flag

2. Should --dry-run be compatible with --force?
   a) Yes, allow it (Recommended - no harm in dry run)
   b) No, error if both provided
```

### Frame 4: User Response (2 sec)

```
> 1a, and good catch on the --force thing - 2a
```

### Frame 5: Latent Criteria Discovery — THE AHA MOMENT (6-8 sec)

This is the hook. Show Claude surfacing something non-obvious:

```
One thing that often gets missed with --dry-run flags:

If the deploy command has side effects before the actual deploy
(like fetching latest config or validating credentials), should
--dry-run:

   a) Skip ALL side effects (pure dry run)
   b) Run pre-checks but skip the deploy (Recommended - catches
      config errors early)
   c) Let me check what side effects exist first

This matters because users often expect --dry-run to catch
problems, not just print what would happen.
```

### Frame 6: User Responds (2 sec)

```
> Didn't think of that. 2b - run pre-checks.
```

### Frame 7: Manifest Output (5-6 sec)

Show the manifest being written with key acceptance criteria visible:

```
Writing manifest...

✓ Manifest complete: /tmp/manifest-1706612345.md

Deliverable: --dry-run flag for deploy command

Acceptance Criteria:
• AC-1.1: --dry-run outputs "Would deploy: {summary}"
• AC-1.2: --dry-run runs pre-deploy validation (config, creds)
• AC-1.3: --dry-run is compatible with --force flag
• AC-1.4: No actual deployment occurs when --dry-run is set

Global Invariants:
• INV-G1: Existing --env and --force flags unchanged
• INV-G2: All tests pass

To execute: /do /tmp/manifest-1706612345.md
```

### Frame 8: End Card (2-3 sec)

```
>

```

Hold on empty prompt briefly, or fade to:

```
manifest-driven development
github.com/doodledood/manifest-dev
```

---

## Key Moments to Nail

1. **Frame 5 is the money shot** — Claude surfacing the pre-check insight is the differentiator. This is "latent criteria" in action. Time it so viewers can read it.

2. **Keep user responses short** — Shows the user isn't doing heavy lifting.

3. **The manifest output** — Proves the interview produced something concrete and actionable.

---

## Recording Tips

- **Speed up exploration/typing**, slow down on Frame 5 (the insight)
- If using asciinema: record at normal speed, then use `asciinema-edit` to adjust timing
- Consider a subtle highlight/flash when the insight appears
- Test on phone screen before finalizing — must be readable

---

## Alternate Hooks (A/B Test)

If you want to test different tasks:

**Alt A: Bug fix**
```
/define fix: users see stale data after logout/login
```
Insight: "Should we also invalidate cached API responses, or just local state?"

**Alt B: API endpoint**
```
/define add DELETE /users/:id endpoint
```
Insight: "Should deletion be hard delete or soft delete? What about audit trail requirements?"

---

## Post-Recording

- Convert to GIF or MP4 (Twitter/LinkedIn both support video)
- Keep under 15MB for Twitter
- Add subtle loop or fade at end
