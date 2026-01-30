# GIF Recording Script: Full Workflow Demo

## Specs

- **Length**: 45-60 seconds when played (can be sped up 1.5-2x)
- **Resolution**: 1200x800 or similar (readable on mobile)
- **Tool**: asciinema + gif conversion, or native screen recording
- **Font size**: Large enough to read on Twitter/LinkedIn mobile

---

## The Differentiator

**NOT the interview** — "ask me questions" prompts are already trending.

**THE ACTUAL HOOK**: Define criteria once → automated verify-fix loop runs until done → fire and forget.

The GIF must show the *payoff*: you invest upfront, then walk away while it works.

---

## The Task

**Use case**: Adding a CLI flag to an existing tool

Small enough to show full loop in one GIF.

---

## Script

### Act 1: Define (Compressed) — 10-12 sec

Show define is thorough but don't dwell. Speed through.

```
> /define add a --dry-run flag to the deploy command
```

Quick montage (sped up 2-3x):
```
Exploring src/commands/deploy.ts...

Questions:
1. What should --dry-run output? > 1a
2. Should --dry-run run pre-checks? > yes
3. Compatible with --force? > yes

✓ Manifest: /tmp/manifest-123.md
  • 4 acceptance criteria
  • 2 global invariants
  • All automated verification
```

### Act 2: Do — 8-10 sec

This is where "fire and forget" becomes visible.

```
> /do /tmp/manifest-123.md
```

Show it working autonomously (sped up):
```
Implementing --dry-run flag...

✓ Added --dry-run to argument parser
✓ Implemented dry run logic in deploy()
✓ Updated help text

Running verification...
```

### Act 3: Verify-Fix Loop — THE MONEY SHOT — 15-20 sec

This is the differentiator. Show it catching something and fixing it.

```
Verifying against manifest...

✓ AC-1.1: --dry-run outputs summary         PASS
✓ AC-1.2: Pre-checks run in dry-run mode    PASS
✗ AC-1.3: Compatible with --force flag      FAIL
  → --force currently overrides --dry-run

Fixing AC-1.3...
```

Brief pause — let this sink in. Then:

```
Fixed: --dry-run now takes precedence over --force

Re-verifying...

✓ AC-1.1: --dry-run outputs summary         PASS
✓ AC-1.2: Pre-checks run in dry-run mode    PASS
✓ AC-1.3: Compatible with --force flag      PASS
✓ AC-1.4: No deployment in dry-run mode     PASS
✓ INV-G1: Existing flags unchanged          PASS
✓ INV-G2: All tests pass                    PASS

All criteria met. Done.
```

### Act 4: End Card — 3-4 sec

```
manifest-driven development
github.com/doodledood/manifest-dev
```

Or just hold on the "All criteria met. Done." for impact.

---

## Key Moments

1. **Act 1 should feel fast** — "I defined it, moving on." Don't linger on the interview.

2. **Act 3 is the payoff** — The FAIL → fix → PASS sequence shows the system working. This is what no one else has. Slow down here.

3. **The checkmarks at the end** — Visual proof that criteria from Act 1 were actually verified. Connects the loop.

---

## The Story Arc

| Act | Message | Pacing |
|-----|---------|--------|
| 1. Define | "I told it what done looks like" | Fast (compressed) |
| 2. Do | "It's working autonomously" | Medium |
| 3. Verify-Fix | "It caught a bug AND fixed it" | Slow (let it land) |
| 4. Done | "All criteria met" | Hold for impact |

---

## Recording Tips

- **Speed up Act 1 and Act 2** — these are setup
- **Normal speed or slow for Act 3** — this is the hook
- The FAIL → fix → PASS sequence should be readable
- Consider a brief flash/highlight on "FAIL" then "PASS"
- Test on phone screen before finalizing

---

## Alternate Framings

**If 60 sec is too long**, cut Act 1 further:

```
> /define add --dry-run flag

[3 sec montage]

✓ Manifest ready: 4 criteria, all automated
```

Then spend more time on Act 3.

**If you want more drama**, show TWO failures:

```
✗ AC-1.3: Compatible with --force    FAIL
✗ AC-1.4: No deployment occurs       FAIL

Fixing...

[both fixed]

All criteria met.
```

---

## Post-Recording

- Convert to GIF or MP4 (Twitter/LinkedIn both support video)
- Keep under 15MB for Twitter
- The loop should feel satisfying — end on "Done" or fade cleanly
