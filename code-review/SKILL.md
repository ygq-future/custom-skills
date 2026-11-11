---
name: code-review
description: "Two-axis parallel review (Spec/AC conformance + Repo standards & design smells) over uncommitted working-tree changes or branch diffs."
---

# Code Review

Independent two-axis review using two parallel read-only subagents with clean context windows so spec verification and code-standards inspection never mask each other.

## 1. Establish Diff & Spec Inputs

1. **Resolve the diff target**:
   - **Working-tree mode (default after `impl`)**: Capture tracked staged + unstaged changes (`git diff HEAD`) plus any newly added untracked project files (`git status --porcelain`).
   - **Branch / commit mode**: When given a base ref (`main`, tag, SHA, PR), confirm `git rev-parse <base>` and capture `git diff <base>...HEAD` + `git log <base>..HEAD --oneline` (combining uncommitted edits if present).
   - Halt immediately if the diff is empty.
2. **Locate the Spec / Acceptance Criteria** (in priority order):
   - Explicit GitHub Issue (`gh issue view <N>`) or local task file (`docs/tasks/...`) referenced in prompt/branch/commits.
   - Requirements and decisions agreed upon in the active conversation.
   - If neither exists (pure exploratory refactor or external branch review), run the **Standards & Design** subagent only and note `Spec axis skipped (no spec source)`.
3. **Locate repo standards**: Collect `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, `GLOSSARY.md`, and relevant `docs/adr/` files if present.

## 2. Dispatch Parallel Review Subagents

Spawn two read-only subagents concurrently (skipping anything automated formatters/compilers already enforce):

### Subagent A — Spec & Acceptance Criteria
Provide the diff access command/files and exact Spec/AC text. Instruct it to report concisely (<400 words) with `file:line` citations:
- **Missing or partial requirements**: Every requested behavior or `- [ ]` Acceptance Criterion not fully satisfied or lacking behavioral test coverage where expected.
- **Scope creep**: Unrequested features, config knobs, or behavioral changes outside the agreed scope.
- **Logic & edge-case defects**: Requirements that appear implemented but fail boundary, error, concurrency, or state-transition invariants.

### Subagent B — Standards & Design Smells
Provide the diff access command/files, repo standard docs, and the smell baseline below. Documented repo rules override baseline heuristics; distinguish **Hard Violations** (broken repo rules/invariants) from **Design Judgments**:
- **Shallow Pass-Through / Middle Man**: Thin wrappers or interfaces whose surface is as complex as their body (fails the deletion test; 1-implementation interface without a real boundary or test seam).
- **Leaky Seam / Feature Envy**: Logic reaching into another module's internals instead of operating behind a cohesive deep interface.
- **Shotgun Surgery / Divergent Change**: One rule split across scattered files, or one file mixing unrelated responsibilities.
- **Speculative Generality**: Hooks, flags, or abstractions built for hypothetical future needs.
- **Primitive Obsession / Data Clumps**: Raw strings/maps or recurring parameter tuples standing in for a domain type.
- **Artifact Hygiene**: Negative echoes of rejected drafts in names/comments, swallowed errors, bare `unwrap()`/`expect()`, or lint/type suppressions.

## 3. Aggregate Report

Present findings separately under `## Spec & AC` and `## Standards & Design` without merging or cross-ranking them. Close with a two-line verdict stating finding counts and the highest-severity issue per axis. *(When invoked inside `impl`, fix confirmed in-scope findings before running `post-impl`.)*
