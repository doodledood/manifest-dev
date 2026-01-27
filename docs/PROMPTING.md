# First-Principles Prompting: Derived from LLM Training

> **Purpose**: Practical prompting strategies derived directly from how LLMs are trained. Every recommendation traces back to a training mechanism, not intuition or folklore.

---

## Core Premise

Every LLM behavior emerges from training objectives. Effective prompting means:
- **Activating** patterns the training rewarded
- **Compensating** for what training couldn't address
- **Avoiding** triggers that activate unwanted behaviors

---

## Principle 1: Work WITH Next-Token Prediction

**Training reality**: Models generate left-to-right, one token at a time. They cannot "see ahead" or plan holistically.

### Do This

**Sequential decomposition** — structure tasks so each step informs the next:

```
First, identify the core problem.
Then, list the constraints.
Then, propose a solution that satisfies those constraints.
Finally, verify your solution against each constraint.
```

**Make reasoning explicit** — force intermediate tokens that build toward the answer:

```
Before answering, work through:
1. What are the key facts?
2. What are the relationships between them?
3. What follows logically?
```

**Use "think step by step" variants** — this works because it forces the model to generate reasoning tokens before conclusion tokens:

```
Think through this carefully before answering.
```

### Don't Do This

```
"Give me a comprehensive plan that accounts for all edge cases"
(Requires holistic view the model can't have while generating)

"Make sure the beginning is consistent with the end"
(Model can't see the end when writing the beginning)
```

---

## Principle 2: Defeat Reward Hacking

**Training reality**: RLHF optimizes for what *looks good* to humans/reward models, not what *is* good. This creates verbose, confident-sounding, sycophantic outputs.

### Do This

**Specify anti-patterns explicitly**:

```
Be concise. If you don't know, say so. Don't pad your response.
Disagree with me if I'm wrong.
```

**Request specific artifacts, not qualities**:

```
Good: "Return only the function signature and a one-line docstring"
Bad:  "Give me a thorough, high-quality answer"
```

**Provide verification criteria upfront**:

```
Your answer is correct if:
1. It compiles without errors
2. It handles the empty input case
3. It runs in O(n) time

Check your answer against these criteria before responding.
```

**Ask for confidence calibration**:

```
Rate your confidence (low/medium/high) and explain what would make you uncertain.
```

### Don't Do This

```
"Give me the best possible answer"
(Activates reward-hacked "impressive-looking" patterns)

"Be thorough and comprehensive"
(Triggers verbosity that was rewarded in training)

"What do you think about my approach?"
(Invites sycophantic agreement)
```

---

## Principle 3: Manage Attention Architecture

**Training reality**: Transformers have U-shaped attention—strong at context start and end, weak in the middle. Information degrades over long contexts.

### Do This

**Put critical constraints at the END** (highest attention):

```
[Long context here...]

CRITICAL REQUIREMENTS (must satisfy all):
- Must be thread-safe
- Must not allocate memory
- Must return within 10ms
```

**Repeat key information** at strategic points:

```
Remember: you are acting as a security auditor. Your goal is to find vulnerabilities.

[... long task description ...]

As a security auditor focused on finding vulnerabilities, now analyze:
```

**Summarize before synthesis**:

```
Before writing your final answer, first list:
1. The 3 most important facts from the above
2. The key constraint that must not be violated
Then write your answer.
```

### Don't Do This

- Putting critical requirements in paragraph 3 of 10
- Assuming the model "remembers" something from 5000 tokens ago
- Long contexts without repetition of key points

---

## Principle 4: Externalize State

**Training reality**: LLMs can reliably track only 5-10 variables. No persistent memory across sessions. Context drift causes "forgetting" within sessions.

### Do This

**Make the model write things down**:

```
As you investigate, maintain a running list of findings.
After each step, update your findings list before proceeding.
```

**Use structured formats for tracking**:

```
Track your progress using this format:
KNOWN: [facts established]
UNKNOWN: [questions remaining]
NEXT: [immediate next step]
```

**Chunk complex tasks with explicit state transfer**:

```
Step 1: Analyze the requirements. Output a numbered list.
Step 2: For each requirement in your list, identify implementation approach.
Step 3: For each approach, write the code.
```

### Don't Do This

```
"Keep track of all the edge cases as you go"
(Model will lose track after ~5)
```

- Multi-step tasks without explicit state checkpoints
- Assuming the model maintains consistent internal state

---

## Principle 5: Leverage Constitutional Training

**Training reality**: Models are trained to follow explicit principles and evaluate their own outputs against guidelines. Constitutional AI makes them responsive to stated rules.

### Do This

**State principles explicitly**:

```
Principles for this task:
1. Correctness over completeness—a partial correct answer beats a complete wrong one
2. Admit uncertainty—"I don't know" is acceptable
3. Preserve existing behavior—don't change what works
```

**Use self-evaluation prompts**:

```
Before finalizing, check:
- Does this actually solve the stated problem?
- Did I introduce any new issues?
- Am I confident this is correct?
```

**Frame constraints as guidelines, not restrictions**:

```
Good: "Follow the principle: minimal changes to achieve the goal"
Bad:  "Don't change too much stuff"
```

### Don't Do This

- Implicit expectations the model should "just know"
- Vague quality requirements ("make it good")
- Assuming the model shares your unstated values

---

## Principle 6: Compensate for Statistical Knowledge

**Training reality**: Knowledge comes from token co-occurrence statistics. Common patterns are strong; rare patterns are weak or wrong. Models can't distinguish "true but rare" from "false but common."

### Do This

**Provide examples for unusual tasks**:

```
I need a function that does X. Here's an example of the pattern I want:
[example]
Now apply this pattern to:
[actual task]
```

**Supply domain-specific facts**:

```
Context: In this codebase, we use `Result<T, E>` for all fallible operations.
Errors are logged via `tracing::error!`. Never use `unwrap()` in production code.
```

**Ask for sources of uncertainty**:

```
What aspects of this question might you be uncertain about?
What would you need to verify?
```

### Don't Do This

- Assuming accuracy on niche/specialized topics
- Trusting confident-sounding claims without verification
- Asking for "the latest" information (training cutoff)

---

## Principle 7: Activate Tool Use Training

**Training reality**: Agency training makes models good at using tools when the need is clear. But accuracy degrades with many tools, and models may not know when tools would help.

### Do This

**Make tool needs explicit**:

```
You have access to file search. USE IT before making claims about the codebase.
Don't guess at file locations—search for them.
```

**Reduce tool choice paralysis**:

```
For this task, you'll primarily need:
- Read: to examine files
- Edit: to make changes
- Bash: only for running tests
```

**Verify tool results**:

```
After making changes, verify by:
1. Reading the file back
2. Running the tests
3. Confirming the output matches expectations
```

### Don't Do This

- Assuming the model will proactively use tools
- Providing 50 tools without guidance on which to use
- Trusting tool use without verification

---

## Principle 8: Leverage Code-Specific Training

**Training reality**: Modern LLMs receive specialized code training through execution-feedback RL, SWE-RL on real repositories, and exposure to massive code corpora. Some models (DeepSeek-Coder, StarCoder, CodeLlama) also have Fill-in-the-Middle (FIM) training—but general models like Claude and GPT-4 do not.

### Do This

**Provide surrounding context (both prefix AND suffix)**:

Showing what comes AFTER the insertion point helps any LLM understand the task better—it clarifies patterns, shows what the code needs to connect to, and reduces ambiguity. This works for all models, not just FIM-trained ones:

```
I need to add validation between these two sections:

# BEFORE (prefix):
def process_order(order_id: str, items: list[Item]) -> Order:
    order = Order(id=order_id)

# ADD VALIDATION HERE

# AFTER (suffix):
    for item in items:
        order.add_item(item)
    return order
```

**Allow iterative debugging with real error messages**:

Models are trained via RLEF to improve from execution feedback. Don't just say "it doesn't work"—provide the actual error:

```
The code you wrote produces this error:

TypeError: 'NoneType' object is not iterable
  File "main.py", line 42, in process_batch
    for item in results:

The `fetch_results()` call on line 41 is returning None.
Fix the code to handle this case.
```

**Frame tasks as real issues, not toy problems**:

SWE-RL training uses real GitHub issues. Structure requests like issue descriptions:

```
## Problem
The user search endpoint returns duplicate results when the query contains
special characters.

## Steps to Reproduce
1. Call GET /api/users?q=john%20doe
2. Observe that "John Doe" appears twice in results

## Expected Behavior
Each user should appear only once.

## Relevant Files
- src/api/users.py (search endpoint)
- src/services/search.py (search logic)
```

**Provide architectural/dependency context**:

Models were trained on project-level corpora organized by dependency order:

```
Project structure:
- src/models/user.py (User dataclass - no dependencies)
- src/repositories/user_repo.py (depends on models/user.py)
- src/services/user_service.py (depends on repositories/user_repo.py)
- src/api/users.py (depends on services/user_service.py) <- YOU ARE HERE

The service layer handles business logic. The API layer only handles
HTTP concerns (request parsing, response formatting).
```

**Use test output as feedback signal**:

```
Run the tests. If they fail, read the error output and fix the issues.
Continue until all tests pass.
```

This leverages the iterative refinement pattern from RLEF training.

### Don't Do This

```
"Write a function that does X"
(No context about surrounding code, project structure, or constraints)

"It's broken, fix it"
(No error message or reproduction steps)

"Here's a file, improve it"
(No information about dependencies, patterns, or what "improvement" means)
```

### Code-Specific Quick Reference

| Training | Prompting Pattern |
|----------|------------------|
| FIM (prefix + suffix) | Show code BEFORE and AFTER the insertion point |
| RLEF (execution feedback) | Provide actual error messages; allow iteration |
| SWE-RL (real issues) | Frame tasks like GitHub issues with reproduction steps |
| Project-level pre-training | Provide dependency graph; show related files |
| Multi-language training | Specify language conventions if non-obvious |

**Note on FIM**: Fill-in-the-Middle training applies to specialized code models (DeepSeek-Coder, StarCoder, CodeLlama). General models like Claude and GPT-4 are not FIM-trained—but showing surrounding context still helps them understand insertion tasks better.

---

## Meta-Principle: Structure Over Instruction

**The fundamental insight**: LLMs follow structure more reliably than instruction. Structure creates token-level patterns that guide generation; instructions are just content to be processed.

### Structure beats instruction

| Instruction (Weak) | Structure (Strong) |
|-------------------|-------------------|
| "Be concise" | Enforce a format: "Answer in ≤3 sentences" |
| "Think carefully" | Require explicit steps: "First X, then Y, then Z" |
| "Don't make mistakes" | Require verification: "Check your answer against [criteria]" |
| "Remember the requirements" | Repeat them: Place at end of prompt |
| "Track your progress" | Provide format: "Update this list after each step: [format]" |

---

## Quick Reference: Prompting Patterns

| Training Mechanism | Prompting Pattern |
|-------------------|-------------------|
| Next-token prediction | Sequential decomposition; explicit reasoning steps |
| Reward hacking (RLHF) | Specific artifacts > quality words; state anti-patterns |
| U-shaped attention | Critical info at END; repeat key points |
| Limited working memory | Externalize state; structured tracking formats |
| Constitutional AI | Explicit principles; self-evaluation prompts |
| Statistical knowledge | Provide examples; supply domain facts; ask for uncertainties |
| Tool use training | Make tool needs explicit; reduce choice paralysis |
| Surrounding code context | Show prefix AND suffix; helps all models understand insertion tasks |
| Execution-feedback RL | Provide real errors; allow iterative debugging |
| SWE-RL training | Frame tasks as real issues; provide repo context |

---

## Example: Applying All Principles

**Bad prompt**:
```
Review this code and make it better.
```

**Good prompt** (with principles noted):

```
[PRINCIPLE 6: Supply domain facts]
Context: This is a Python async service. We use `asyncio.gather` for
concurrency and `structlog` for logging. Errors should raise, not return None.

[PRINCIPLE 2: Specific artifacts, not qualities]
Review this code for:
1. Bugs that would cause incorrect behavior
2. Error handling gaps
3. Race conditions

[PRINCIPLE 1: Sequential decomposition]
For each issue found:
- State the problem in one sentence
- Show the problematic code
- Show the fix

[PRINCIPLE 4: Externalize state]
Track issues as you find them. After reviewing, list all issues before proposing fixes.

[PRINCIPLE 5: Self-evaluation]
Before finalizing, verify:
- Each fix addresses exactly one issue
- No fix introduces new problems
- Fixes are minimal (don't refactor unrelated code)

[PRINCIPLE 3: Critical constraints at END]
IMPORTANT: Only report real bugs. Do not suggest stylistic improvements,
performance optimizations, or "nice to haves". If no bugs exist, say "No bugs found."
```

---

## Example: Code Task with Code-Specific Principles

**Bad prompt**:
```
Add input validation to my endpoint.
```

**Good prompt** (leveraging code training):

```
[PRINCIPLE 8: Frame as real issue with context]
## Problem
The /api/orders endpoint accepts invalid order data, causing crashes downstream.

## Current Code (prefix)
@router.post("/orders")
async def create_order(request: OrderRequest) -> Order:
    # VALIDATION NEEDED HERE

## What Comes After (suffix)
    order = await order_service.create(
        user_id=request.user_id,
        items=request.items
    )
    return order

[PRINCIPLE 8: Provide architectural context]
Project structure:
- src/models/order.py (Order, OrderRequest pydantic models)
- src/services/order_service.py (business logic, expects valid data)
- src/api/orders.py <- YOU ARE HERE

Validation should happen at API layer. Service assumes valid input.

[PRINCIPLE 6: Domain facts]
We use Pydantic for validation. Raise HTTPException(400) for invalid input.
Required: user_id must exist, items must be non-empty, each item.quantity > 0.

[PRINCIPLE 8: Allow iteration]
After writing the validation, I'll run the tests. If they fail, I'll share the
error output so you can fix it.

[PRINCIPLE 3: Critical constraint at END]
IMPORTANT: Only add validation logic. Don't modify the service call or return statement.
```

---

## Summary

This framework treats prompting as **engineering for a specific system architecture**, not persuasion or communication. The model isn't understanding your intent—it's generating tokens based on patterns. Structure those patterns deliberately.

| Don't Think Of It As... | Think Of It As... |
|------------------------|-------------------|
| Asking a person | Programming a pattern matcher |
| Giving instructions | Structuring token generation |
| Hoping for understanding | Engineering for predictable outputs |
| Trusting intelligence | Compensating for known limitations |

---

## Related Documents

- **[LLM_TRAINING.md](./LLM_TRAINING.md)** — Deep dive into how LLMs are trained (the basis for these principles)
- **[LLM_CODING_CAPABILITIES.md](./LLM_CODING_CAPABILITIES.md)** — LLM strengths and limitations for coding tasks

---

*Derived from: LLM_TRAINING.md analysis*
*Last updated: 2026-01-18*
