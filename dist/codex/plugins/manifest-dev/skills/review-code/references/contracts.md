# Contracts review

Verify, with evidence, that code uses external/internal APIs correctly and that interface changes don't break existing consumers.

For every API call ask: **"Is this correct per the actual contract?"** For every interface change ask: **"Will existing consumers still work?"** This dimension's distinguishing discipline is **evidence** — cite actual API docs or codebase definitions; speculation without documentation or codebase proof is not a finding.

## What to examine

Focus on code that crosses boundaries: API calls, interface definitions, public function signatures, data contracts, serialization formats.

These categories are guidance, not exhaustive. If you find a contract issue that fits this dimension but no listed category, report it — just respect the orthogonality boundaries below.

### Source-of-Truth Discipline

Before accepting hand-built calls, payloads, literals, status names, schemas, config values, or protocol assumptions, look for the authoritative source: generated client, SDK, OpenAPI/Swagger, protobuf/IDL, GraphQL schema, schema file, shared constants/enums, framework config, migration, documented API, or neighboring established module pattern.

Flag when the change duplicates or bypasses an existing authoritative source and creates concrete contract risk: drift, wrong request/response shape, invalid literals, duplicated protocol rules, or breaking consumers. Do not report merely because a generated or shared source exists; report only when bypassing it changes correctness, durability, or consumer compatibility.

### Outbound: API Usage Verification

Verify that code calling external or internal APIs does so correctly per the API's actual contract.

**Request Shape Correctness**
- Required parameters missing or misnamed
- Parameter types or formats that don't match the API specification
- Request body structure that doesn't match the expected schema
- Query parameters vs body parameters placed incorrectly
- Content-Type or Accept headers that don't match what the API expects

**Authentication & Authorization**
- Missing or incorrect authentication headers/tokens
- Wrong auth scheme (Bearer vs Basic vs API key)
- Scopes or permissions insufficient for the endpoint being called
- Token refresh logic that doesn't match the auth provider's contract

**Response Handling Completeness**
- Handling only success responses, ignoring documented error status codes
- Assuming response shape without accounting for documented variations
- Missing handling for rate limit responses (429) when the API documents rate limits
- Not handling pagination when the API returns paginated results
- Assuming response field presence when the API documents it as optional

**API Lifecycle Awareness**
- Using deprecated endpoints or parameters when the API documents replacements
- Using API versions approaching or past end-of-life
- Missing version pinning when the API supports versioning

### Inbound: Consumer Impact Verification

Verify that changes to interfaces, public APIs, or contracts don't break existing consumers.

**Signature & Shape Changes**
- Function parameter changes (added required params, removed params, reordered params) that break existing callers
- Return type changes that consumers depend on
- Removed or renamed exported functions, types, or constants
- Changed field names or types in data structures consumers read

**Behavioral Contract Changes**
- Changed function behavior that callers depend on (different return value for same input, different side effects)
- Modified error behavior (throwing where it didn't before, changing error types, suppressing errors that callers catch)
- Changed ordering guarantees, uniqueness guarantees, or other implicit contracts

**Serialization & Protocol Changes**
- Changed JSON/XML/protobuf field names or types in wire formats
- Modified API response shapes that downstream services parse
- Changed event payload structures that subscribers consume
- Database schema changes that affect other services reading the same data

## Evidence requirement

**Every finding MUST cite evidence.** Evidence-based verification, not speculation, is what this dimension is for.

**Acceptable evidence sources:**
- **API documentation** — fetched via shell_command (e.g. curl) from official docs, API reference pages, or OpenAPI/Swagger specs
- **Internal API definitions** — read from the codebase (route handlers, controller definitions, generated clients, SDKs, type exports, shared constants/enums, protobuf/GraphQL schemas)
- **Consumer code** — actual callers found via codebase search that depend on the contract
- **Test expectations** — existing tests that assert specific contract behavior

**Evidence workflow:**
1. Identify API calls or interface changes in the diff.
2. Look for the authoritative source of truth before judging handwritten code: generated client, SDK, schema, shared constants, docs, or established neighboring pattern.
3. For outbound: locate the API documentation (shell_command fetch for external, codebase read for internal).
4. For inbound: search the codebase for consumers of the changed interface.
5. Compare the code against the evidence.
6. Report only verified mismatches.

**When evidence is unavailable:** If you cannot find documentation for an external API (shell_command fetch fails, no docs URL discoverable), or cannot locate consumers of an internal interface, note the gap in the report's **Unverified** section but do NOT fabricate API behavior or assume consumer existence.

## Tool usage

Use **shell_command** (e.g. curl) to pull external API documentation, reference pages, and OpenAPI/Swagger specs as evidence; fall back to **web_search** to discover a docs URL when none is referenced in the project. Before resorting to web search, try the project's existing documentation references (config files, comments with URLs). For internal APIs, search the codebase for route definitions, type exports, and function signatures.

## Actionability filter

Before reporting, a finding must pass ALL of these. If it fails ANY, drop it entirely.

1. **In scope** — Diff-based review (default): only report contract issues introduced or affected by this change; pre-existing contract violations are out of scope. Explicit-path review (caller specified paths): pre-existing contract issues are valid findings.
2. **Evidence-backed** — Cite the specific documentation, API definition, or consumer code that establishes the contract. No speculation.
3. **Concrete mismatch** — Identify the specific parameter, field, status code, or behavior that doesn't match the contract. "This API call might be wrong" is not a finding.
4. **Not intentional** — If code, comments, or commit messages show the author deliberately deviated (e.g., "ignoring pagination for now — single-page results guaranteed"), it's not a finding.
5. **Matches codebase patterns** — If the codebase consistently uses an API a particular way and the documentation is ambiguous, follow the established pattern rather than flagging it.
6. **Worth flagging** — Trivial mismatches (optional header that makes no difference, extra parameter that's ignored) aren't worth reporting unless they cause observable issues.

## Out of scope (orthogonality)

Do NOT report on — these belong to other dimensions:
- **Intent-behavior divergence** (does the change achieve its goal?) → the change-intent dimension
- **Mechanical code defects** (race conditions, resource leaks, null handling) → the code-bugs dimension
- **Type system improvements** (better type definitions, narrower types) → the type-safety dimension
- **Code organization** (DRY, coupling, consistency) → the code-maintainability dimension
- **Over-engineering / complexity** → the code-simplicity dimension
- **Design fitness** (wrong approach, reinvented wheels) → the code-design dimension
- **Test coverage gaps** → the test-quality dimension
- **Documentation accuracy** → the docs dimension
- **Context file compliance** → the context-file-adherence dimension

**Key distinctions from neighboring dimensions:**
- **code-bugs** asks: "Will this code crash or produce wrong output?" (runtime defects). This dimension asks: "Does this code match the API's documented contract?"
- **change-intent** asks: "Does the change achieve its goal?" (intent analysis). This dimension asks: "Are the specific API interactions correct per documentation?"
- **type-safety** asks: "Does the type system catch errors?" (compile-time). This dimension asks: "Does the runtime API usage match the documented contract?"
- **code-design** asks: "Is this the right approach?" (architecture). This dimension asks: "Is the interface shape correct for its consumers?"

**Rule of thumb:** If the issue is a **general code defect**, it's code-bugs. If it's whether the **overall logic works**, it's change-intent. If it's whether a **specific API call matches its documentation** or a **specific interface change breaks consumers**, it's this dimension.

## Severity calibration

Severity reflects how broken the contract interaction is:

- **Critical** — Contract violation that WILL cause runtime failure on every invocation. Examples: required parameter missing, wrong HTTP method, auth scheme completely wrong, response parsed with wrong structure causing data loss, consumer calling a removed function.
- **High** — Contract violation that will fail for common cases. Examples: missing error handling for documented error codes that occur regularly, pagination not handled when results commonly exceed one page, breaking change to an interface used by multiple consumers without migration.
- **Medium** — Contract violation that fails in edge cases or degrades behavior. Examples: missing handling for rare error codes, optional pagination parameters omitted (works but suboptimal), deprecated endpoint still functional but scheduled for removal, single consumer affected by an interface change.
- **Low** — Minor contract deviations with minimal practical impact. Examples: using a deprecated parameter that still works, not setting optional headers that would improve behavior, extra fields sent that are silently ignored.

**Calibration check**: Critical contract violations should be relatively rare — they represent fundamental misuse. If you're marking multiple issues Critical, verify each truly causes failure on every invocation.

## Reporting notes (dimension-specific)

Beyond the shared report skeleton, for this dimension:
- Tag each finding with **Direction** (Outbound | Inbound) and the detection **Category**.
- Include an **Evidence Source** (URL, file path, or description of the documentation used) and an **Evidence** excerpt (the relevant snippet from API docs or consumer code) for every finding.
- State the **Contract** (what the documentation/definition says) vs the **Actual** (what the code does).
- Add an **Unverified (Evidence Unavailable)** section listing API calls or interface changes where documentation could not be found — note what was attempted (URLs tried, searches performed) so the developer can supply documentation. Count unverified items in the summary.
- Every Critical/High violation MUST have specific file:line references, evidence citations, and concrete fix suggestions.

## Guidelines / gotchas

- **Evidence first**: Always locate documentation or consumer code before asserting a violation. If you can't find evidence, it's not a finding — it's an "Unverified" item.
- **Search thoroughly**: For internal APIs, search the codebase for route definitions, type exports, and function signatures. For external APIs, try the project's existing documentation references before web search.
- **Respect versioning**: API behavior may differ by version. Verify which version the code targets before comparing against documentation.
- **Consider migration context**: If the change is part of a documented migration (v1 → v2, deprecating an endpoint), evaluate against the target state, not the current state.
- **Outbound takes priority**: When time-constrained, prioritize outbound (API usage) over inbound (consumer impact) — outbound violations cause immediate runtime failures while inbound violations may have delayed impact.
