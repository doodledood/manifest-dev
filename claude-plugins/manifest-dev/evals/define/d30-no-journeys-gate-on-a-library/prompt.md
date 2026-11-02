---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 1
---
use the define skill for this.

`tidyurls` is our small python library that normalizes URLs: it lowercases the host, drops default ports and sorts query parameters. other teams call it from their own code; it has no interface of its own. add an option, `keep_query_order=True`, that leaves the query parameters in their original order, because one team signs URLs and sorting breaks the signature. the default stays as it is.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything. write the spec to ./manifest.md in the current directory, not your home directory.
