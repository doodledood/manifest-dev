---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 6
---
use the define skill for this.

our public api docs are a mess — about 40 markdown pages under docs/api/, one per endpoint
group, written by different people over four years. make them excellent: every statement
accurate, nothing missing, consistent style throughout.

what we have: an openapi spec generated from the code on every build (that's the source of
truth for endpoints, params, responses). a short style guide in docs/STYLE.md (sentence-case
headings, second person, one example request + response per endpoint). the people who read
these are external developers integrating for the first time.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
