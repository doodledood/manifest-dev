---
name: re-pitch
description: "Stop and re-pitch the last message — it didn't land. Re-explains with the context the reader was missing, in plain words, cutting every line that isn't value while keeping every fact that is. Use when the user says wait what, I'm lost, that didn't land, what do you mean, or asks for a re-explanation in plain English."
argument-hint: '[what lost you]'
user-invocable: true
---

The last message didn't land. Re-pitch it — don't defend it, don't shrink it into a summary, don't repeat it louder. Explain it again as if for the first time, better.

- Start from the context the reader was missing: what question this answers and why it matters now, before the answer itself.
- Plain words, short sentences. A term of art earns its place only where the reader meets it in what they receive — the manifest they get, the read you name. Everything else gets dropped or grounded in one line, the vocabulary these prompts use on themselves included.
- Attention is sparse. Assume a reader who skims and bails the moment a sentence pays nothing: lead with the point, and cut every line that doesn't carry value — preamble, restated context they already hold, hedges, transitions that only fill space. Losing them a second time is the failure mode.
- Invoke the `manifest-dev:chat-surface` skill with: `text` — it owns which form carries each point.
- Cut noise, not value. A re-pitch that drops load-bearing facts to get shorter has also failed: if the original carried ten facts that matter, the re-pitch carries ten — shorter comes from stripping the dead prose around them, never from stripping them.
- When the argument names what lost the reader, aim the re-pitch there first; otherwise re-pitch the whole message.
