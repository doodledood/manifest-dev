# PLANNING Task Guidance

Encoding a decomposition read into a durable decision map — an effort too large for one deliberation, worked as decisions over time. The deliverable is the map itself; the work its decisions eventually spawn gets its own manifests.

## Quality Gates

| Aspect | Threshold |
|--------|-----------|
| Map as index | The map file gists and links; each decision's detail lives in exactly one place — its own file. The map restates nothing it can point to |
| Frontier legibility | Every decision file carries a status and names what blocks it; the open-and-unblocked set is readable from the map alone, without opening each decision file |
| Fog and scope sections | The map carries a not-yet-specified section (in-scope ground not yet statable as decisions, held un-sliced) and an out-of-scope section (ground consciously ruled beyond the destination, each ruling with its why) |
| Seeded working rules | The map body states its own resolution protocol — record the answer in the decision file, update its status, graduate newly-statable fog into new decision files, re-wire blocking — so any later session inherits the process from the artifact rather than from memory |
| Destination named | The map opens with what reaching its end looks like, in a line or two every future session orients to before picking a decision |

## Defaults

*Domain best practices for this task type.*

- **Local markdown first** — The map is markdown files (one map + one per decision) at a location the manifest names; an external venue (GitHub issues, a tracker) is a per-manifest encoding choice made explicitly, never assumed
- **Decisions resolve by deliberation, not here** — Each mapped decision is later worked in its own session against its decision file; the map manifest only creates the map
- **Resolution hands off to execution** — A decision whose answer implies build work gets its own define/do cycle; the map records the decision and its status, never the execution
