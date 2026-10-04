---
max_turns: 20
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write]
model: opus
runs: 3
---
Use the define skill for this. Shared understanding is settled below; this is contract
encoding, not implementation. Keep any files in the current directory. Show the proposed
contract or the unresolved owner decision in your final message so I can review it.

We agreed to a browser archive explorer so researchers can scrub an entire recording and
inspect exact original frames. The owner explicitly requires lossless access to every frame;
no truncation, downsampling, approximate frame substitution, or server. The owner is here
and has not authorized changing those requirements. Here is a draft contract to assess and
finish. These operating bounds are measured facts for the target environment: a recording
has 100 GB of independently encoded frame data; the client has a hard 256 MB working-memory
ceiling; cold network throughput is at most 10 MB/s; the endpoint has 500 ms minimum latency.
No cache is guaranteed at first visit.

# Definition: Archive explorer
## 1. Intent
- **Problem:** Researchers cannot inspect arbitrary frames from archived recordings.
- **Appetite:** One browser viewer over the existing static archive.
- **Out of bounds:** INV-G2
## 2. Initial Approach (Complex Tasks Only)
- **Architecture:** Local decoding of original frames from a static endpoint.
## 3. Global Invariants
### INV-G2 — Preserve archive access
Every original frame remains available losslessly. No truncation, downsampling,
approximate frame substitution, or server.
Deterministic gate.
### INV-G3 — Memory bound
Peak working memory stays under 256 MB in the target client.
Deterministic gate.
## 4. Process Guidance
- [PG-1] Start with the existing static endpoint.
## 5. Known Assumptions
- [ASM-1] Browser codecs support these frames | Default: existing codec | Impact if wrong: change decoder
## 6. Deliverables
### Deliverable 1: Researcher frame explorer
*What it is, and how it is exercised end-to-end:* A researcher opens a recording and scrubs
to arbitrary original frames, inspecting exact frame content.
#### AC-1.1 — Fast cold start and immediate arbitrary seeking
After a cold visit the complete timeline is ready in 100 ms; seeking to any uncached
original frame returns its exact pixels in 10 ms, including over the stated endpoint.
Deterministic gate.

The latency wording was a proposed performance target, not an owner decision. We want the
fastest feasible experience without reducing the lossless/full-timeline feature. Identify
the conflict and propose an honest acceptance boundary for owner decision before handoff.
Do not implement anything.
