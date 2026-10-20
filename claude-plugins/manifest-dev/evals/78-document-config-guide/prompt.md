---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

i want one doc that teaches new devs how our billing service's config works and also lists every option. my plan for it:

1. clone the repo, copy `config/local.example.yaml` to `config/local.yaml`
2. set your tenant shard and database url
3. run `make dev` and hit `/health`
4. a full table of all 46 config keys, each with its default value and what it does
5. a line saying startup takes under 2 seconds with defaults

the defaults all live in `config/defaults.yaml`, which someone changes most sprints. the README already has a shorter table of the 20 keys people touch most, with their defaults. "tenant shard" is explained in the architecture doc on our internal wiki, which most new devs don't open in their first month. the 2 seconds is how it felt last time i ran it. figure out how this doc should be put together before i write it. i'm afk — work it out and come back with your read, how sure you are, and what it rests on.
