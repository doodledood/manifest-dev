---
tags: [figure-out-multi-turn]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill for this.

this repo is Sift, our internal pull-request review bot for about 30 engineers. the team agreed on the next version:

1. every PR gets a second model pass that double-checks the first pass's findings before they're posted.
2. a nightly scan of the whole repo that posts a digest of findings to our #eng slack channel.
3. an inline fix suggestion under each finding.

help me figure out how to build it: where the second pass sits in the pipeline, how the nightly scan batches the repo, and how we test the fix suggestions.
<!-- next turn -->
before the pipeline, on the second pass: what does an engineer actually get from it? today people merge about 10 minutes after the review lands. the second pass adds about 4 minutes to every PR and doubles the model bill, for findings the first pass mostly has already. i'd want to see it catch something the first pass misses before we pay that on every PR.
<!-- next turn -->
same question for the nightly scan: who reads that digest, and what do they do with it? it's the whole repo every night, a lot of compute, and one more slack message people learn to skip.
<!-- next turn -->
ok, that's my time for today. name the read.
