# Changelog

All notable changes to the manifest-dev plugin.

Format: `[manifest-dev] vX.Y.Z` - Brief description

## [Unreleased]

- Graduated from doodledood/claude-code-plugins as standalone marketplace repo

## History (as vibe-experimental)

- [manifest-dev] v0.27.2 - /define: Refine BLOG.md with blog-specific interview probes, voice compliance and anti-slop quality gates, blog-specific risks/trade-offs, and process guidance for voice docs and outline-first drafting
- [manifest-dev] v0.27.1 - /define: Refine RESEARCH.md with research-specific interview probes, source authority hierarchy, decomposition architecture patterns, research risks/trade-offs
- [manifest-dev] v0.27.0 - /define: Add RESEARCH.md and BLOG.md task types; all task files follow lean pattern (quality gates + AC patterns only)
- [manifest-dev] v0.26.5 - /define: Default to opus model for general-purpose subagent verification
- [manifest-dev] v0.26.4 - /define: Probe user for ways to make criterion automatable before accepting manual fallback
- [manifest-dev] v0.26.3 - /define: Automate quality gates, strengthen verification constraint
- [manifest-dev] v0.26.2 - /define: Neutralize coding-specific terminology in universal constraints
- [manifest-dev] v0.26.1 - /define: Move AskUserQuestion 4-option limit to main skill constraint
- [manifest-dev] v0.26.0 - /define: Make domain-agnostic with conditional task resources
- [manifest-dev] v0.25.3 - /define: Add space-splitting prioritization to Efficient principle
- [manifest-dev] v0.25.2 - /define: Add question quality gate and batch related questions constraint
- [manifest-dev] v0.25.1 - /define: Promote "Mark a recommended option" to standalone constraint
- [manifest-dev] v0.25.0 - /define + manifest-verifier: Known Assumptions (ASM-*) manifest section
- [manifest-dev] v0.24.8 - /do: Add "Verify fixes first" principle
- [manifest-dev] v0.24.7 - /verify: Enforce all criteria verified in single parallel launch
- [manifest-dev] v0.24.6 - Reviewers: Standardize git diff commands
- [manifest-dev] v0.24.5 - manifest-verifier: Principles-based gap detection; /define: Explicit convergence criteria
- [manifest-dev] v0.24.4 - Stop hook: Allow stops on API errors
- [manifest-dev] v0.24.3 - /define, /do: Surface logging discipline as first constraint
- [manifest-dev] v0.24.2 - /define: Simplify e2e verification probing
- [manifest-dev] v0.24.1 - /define: Add probing for input artifacts, e2e verification, AskUserQuestion limit
- [manifest-dev] v0.24.0 - Add Approach section to manifest schema (architecture, execution order, risks, trade-offs)
- [manifest-dev] v0.23.8 - /verify: Optimize via auto-optimize-prompt (46% line reduction)
- [manifest-dev] v0.23.7 - /do: Optimize via auto-optimize-prompt (53% line reduction)
- [manifest-dev] v0.23.6 - manifest-verifier: Optimize via auto-optimize-prompt
- [manifest-dev] v0.23.5 - /define: Optimize via auto-optimize-prompt
- [manifest-dev] v0.23.4 - Replace hardcoded tool names with natural language
- [manifest-dev] v0.23.3 - Tighten convergence constraint in /define
- [manifest-dev] v0.23.2 - Add "Domain-grounded" principle to /define
- [manifest-dev] v0.23.1 - Add structural example to Non-Functional AC type
- [manifest-dev] v0.23.0 - Add Process Guidance (PG-*) section to manifest schema
- [manifest-dev] v0.22.0 - Improve /define and manifest-verifier constraint encoding
- [manifest-dev] v0.21.1 - Add latent criteria gap detection to manifest-verifier
- [manifest-dev] v0.21.0 - Add manifest-verifier agent to /define workflow
- [manifest-dev] v0.20.3 - Add "Efficient" principle to /define
- [manifest-dev] v0.20.2 - Refine /define for better interview quality
- [manifest-dev] v0.20.1 - Add verification preference constraint to /define
- [manifest-dev] v0.20.0 - Sync reviewers from vibe-workflow v2.17.0
- [manifest-dev] v0.19.0 - /define: Restructure around 3 core principles (Verifiable, Validated, Complete)
- [manifest-dev] v0.18.0 - Decision-making improvements (Annie Duke inspired)
- [manifest-dev] v0.17.0 - Strengthen todo discipline and goal motivation
- [manifest-dev] v0.16.0 - /define: ACs are observable behaviors, explicitly surface edge cases
- [manifest-dev] v0.15.1 - /define: Filter quality gates through project preferences
- [manifest-dev] v0.15.0 - Optimize /define per prompting principles
- [manifest-dev] v0.13.0 - Restructure all skills from rigid phases to goal-oriented
- [manifest-dev] v0.12.1 - Fix outdated content in /define skill
- [manifest-dev] v0.12.0 - Proactive interview + consolidated Global Invariants
- [manifest-dev] v0.11.0 - Major refactor: Manifest-based two-level architecture
- [manifest-dev] v0.10.2 - Simplified /verify: single parallel launch
- [manifest-dev] v0.10.1 - Subagent verification uses natural language prompts
- [manifest-dev] v0.10.0 - Removed define-verifier, improved interview flow
- [manifest-dev] v0.9.0 - Techniques are starting points, not checklists
- [manifest-dev] v0.8.0 - Terminology: "definition-driven" framing, context handling
- [manifest-dev] v0.7.0 - Unified criteria prefix to AC-*
- [manifest-dev] v0.6.0 - /verify three-phase execution for better parallelism
- [manifest-dev] v0.5.3 - /define: Flexible adversarial examples, quality gate improvements
- [manifest-dev] v0.5.2 - claude-md-adherence-reviewer focuses on outcome rules only
- [manifest-dev] v0.5.1 - claude-md-adherence-reviewer checks context before reading files
- [manifest-dev] v0.5.0 - Auto-detect project quality gates from CLAUDE.md
- [manifest-dev] v0.3.2 - Parallel verification via criteria-checker agents
- [manifest-dev] v0.3.1 - Trust LLM to work toward criteria
- [manifest-dev] v0.3.0 - Rename skills: /spec -> /define, /implement -> /do
- [manifest-dev] v0.2.0 - Implement verification-first workflow system
