---
name: code-review
description: "Fast two-axis parallel review (Spec/AC conformance + Architecture & repo standards) over pre-packaged working-tree or branch diffs."
---

# Code Review

Fast, independent two-axis review using two parallel read-only subagents with clean context windows—structured so subagents inspect pre-captured context directly instead of re-discovering the repository from scratch.

## 1. Pre-Package Review Bundle (Parent Agent Responsibility)

Before spawning subagents, the parent agent **MUST** assemble the review bundle once so subagents start immediately:

1. **Capture the diff once**:
   - **Working-tree mode (default after `impl`)**: Capture tracked staged + unstaged changes (`git diff HEAD`) plus newly added untracked project files (`git status --porcelain`).
   - **Branch / commit mode**: Confirm `git rev-parse <base>` and capture `git diff <base>...HEAD` + `git log <base>..HEAD --oneline` (plus uncommitted edits if present).
   - Halt immediately if the diff is empty. Pass small/medium diffs inline in the subagent context; for large diffs, write the captured diff once to an OS temp file (outside the repo) and pass that path, deleting the temp file after aggregation.
2. **Bundle Spec / Acceptance Criteria** (in priority order):
   - Inline the exact GitHub Issue body (`gh issue view <N>`), `docs/tasks/...` slice text, or active conversation requirements.
   - If no spec source exists (pure exploratory refactor or external branch review), skip Subagent A and note `Spec axis skipped (no spec source)`.
3. **Bundle Repo Standards**: Locate `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, `GLOSSARY.md`, and relevant `docs/adr/` paths once and pass their key rules (or exact paths) to Subagent B.

## 2. Dispatch Fast Parallel Subagents

Spawn both read-only subagents concurrently (prefer lightweight `reviewer` / read-only subagent profiles when supported), enforcing **three mandatory speed & scope guardrails** in every subagent prompt:
- **Zero Command Execution**: NEVER run `test`, `build`, `lint`, `lsp`, `git`, or index commands—compilation, tests, and static analyzers are owned by the parent workflow.
- **Bounded Exploration ($\le 5$ targeted reads/lookups)**: Evaluate the provided diff first. Read surrounding lines or direct callers **only** when an invariant or contract cannot be verified from the diff hunks alone; never perform open-ended repository archaeology.
- **No Overlap with `post-impl`**: Skip formatting, unused parameters/imports, dead private helpers, language modernization hints, and wording echoes—those belong to LSP + `post-impl`.

### Subagent A — Spec & Behavioral Correctness
Inspect the provided diff against the inline Spec/AC and report concisely (<350 words) with `file:line` citations:
- **Missing or partial requirements**: Requested behaviors or `- [ ]` Acceptance Criteria not satisfied or missing seam-level behavioral tests.
- **Scope creep**: Unrequested features, config knobs, or behavioral side effects outside agreed scope.
- **Logic, state & concurrency defects**: Bugs in boundary conditions, state transitions, locking/races, caching/invalidation, error recovery, or security invariants.

### Subagent B — Architecture & Repo Standards
Inspect the provided diff against repo standards and architectural boundaries (<350 words, `file:line` citations; documented repo rules override heuristics; separate **Hard Violations** from **Design Judgments**):
- **Documented Standard Breaches**: Direct violations of `AGENTS.md` / `CONTRIBUTING.md` / ADR invariants (error handling, bare `unwrap()`/`expect()`, swallowed errors, forbidden suppressions, layer rules).
- **Shallow Pass-Through / Speculative Seam**: Indirection layers, wrappers, or single-implementation interfaces whose surface is as complex as their body without a real boundary or test seam.
- **Leaky Seam / Responsibility Split**: Logic reaching into another module's private state, one rule scattered across unrelated modules (Shotgun Surgery), or unrelated concerns tangled together (Divergent Change).

## 3. Aggregate & Clean Up

Remove any temporary diff file, then present findings separately under `## Spec & Correctness` and `## Architecture & Standards` without cross-ranking them. Close with a two-line verdict stating finding counts and highest-severity issue per axis. *(When invoked inside `impl`, fix confirmed in-scope findings before running `post-impl`.)*
