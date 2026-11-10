---
name: post-impl-checklist
description: "USER-INITIATED OR POST-TASK CONVERGENCE. Execute a final 7-dimensional code quality convergence and cleanup audit after a feature, refactor, or bug fix is functionally complete and before handoff or commit. Eliminates duplicate business rules, verified dead code, invalidated legacy paths, write-only internal state/parameters, premature abstractions, redundant operations, and contract drift within the task boundary."
---

# Post-Implementation Quality Checklist

Run this convergence audit **after** functional implementation and tests pass, **before** user handoff or commit. It prunes verified residues and drift strictly within the task delta and its immediate blast radius—never expand into unrequested wide refactoring.

## 1. Core Rules

1. **Establish boundary, never guess**: Determine the exact task diff from the active working tree (staged + unstaged) or an explicit branch merge-base (`git merge-base <target> HEAD`). Never blindly assume `HEAD~1` unless proven.
2. **Concrete evidence over intuition**: Every finding requires exact `file:line`, caller trace, or local Language Server (LSP) CLI / analyzer output. Never refactor merely to reduce lines or force changes when code is already clean.
3. **LSP CLI diagnostic evidence**: Do not rely solely on basic compile checks (`go build`, `cargo check`, bundler transpilation) or lightweight navigation tools that only surface blocking errors. When a local language-server CLI exists (e.g., `gopls check -severity=hint`, `pyright`/`basedpyright`, `cargo clippy --all-targets`, `vue-tsc`/`svelte-check`, `clang-tidy`/`clangd --check`), run it on modified files to capture IDE-grade `warning`/`info`/`hint` diagnostics (unused parameters, dead helpers, invalid struct/annotation tags, redundant allocations, deprecated APIs).
4. **Fix, Keep, or Defer**:
   - **In-scope & low-risk**: Fix immediately in-place and re-verify.
   - **Justified by semantics or contract**: Keep unchanged.
   - **Pre-existing debt or high cross-module risk**: Do not touch; record under `Deferred / Out of Scope`.

## 2. Seven-Dimensional Audit Checklist

Inspect all added, modified, or superseded symbols within the established diff:

1. **Dimension 1: Duplicate Business Rules & Invariant Divergence**
   - **Audit**: Check if newly written business rules, validations, enum mappings, or domain calculations duplicate an existing canonical implementation.
   - **Guardrail**: Superficial structural similarity is NOT duplication. Consolidate into a Single Source of Truth (SSOT) only when the domain concept, invariant, and lifecycle change driver are identical.
2. **Dimension 2: Write-Only State & Parameters (Internal vs. Contract)**
   - **Audit**: Trace downstream reads for every new/modified struct field, property, state variable, or function parameter. Remove purely internal state/parameters that are written but never read (or rename unused interface-bound parameters to `_`).
   - **Guardrail (Contract Exemption)**: NEVER delete fields/parameters belonging to public/exported APIs, IPC/RPC/HTTP wire schemas, DB/serialization formats, config contracts, or generated/plugin interfaces.
3. **Dimension 3: Dead Code & Orphaned Paths (Proportional Runtime Check)**
   - **Audit**: For helpers, types, branches, or imports bypassed/superseded by this change, verify no live callers remain and delete them.
   - **Guardrail**: Keep caller checks proportional to visibility. Private/file-local symbols only need local scope verification; exported/public symbols require targeted checks for runtime entry points (DI, routes, events, reflection, framework bindings) before deletion.
4. **Dimension 4: Redundant State & Unnecessary Operations**
   - **Audit**: Replace stored state that can be synchronously derived from authoritative state; remove duplicate writes/dispatches/I/O, redundant allocations (e.g., `[]byte(fmt.Sprintf(...))`), no-op defensive checks on verified non-null internal contracts, and dead retries.
   - **Guardrail**: Preserve intentional caches, memoized selectors, or decoupled UI presentation states justified by performance or architecture.
5. **Dimension 5: Premature Abstraction & Patchwork Complexity**
   - **Audit**: Inline single-use interfaces, wrappers, or factories introduced solely for this task that lack domain/architectural value; flatten stacked conditional patches (`if (a && !b && c)`) into cohesive domain logic.
   - **Guardrail**: Retain single-implementation abstractions when they express a real domain boundary, decouple third-party I/O, provide a required test seam, or mark a concrete planned extension point.
6. **Dimension 6: Contract & Source of Truth Drift**
   - **Audit**: Verify modified models, RPC/API payloads, event schemas, struct/serialization tags (e.g., `omitempty` vs. `omitzero`), and error shapes against downstream consumers, mocks, and bindings.
   - **Guardrail**: Enforce producer-consumer compatibility, not artificial structural symmetry (optional fields, asymmetric projections, and forward-compatible schemas are valid).
7. **Dimension 7: Behavioral Convergence & Path Cleanliness**
   - **Audit**: Ensure new logic cuts over cleanly without leaving superseded logic running in parallel as a silent fallback; strip all temporary debug logs, flags, and transitional scaffolding.

## 3. Verification & Output Report

After applying any in-place cleanups, re-run targeted tests, local LSP CLI checks on modified files, and the repository's Quality Gate (and `Post-Edit Sync` if applicable) to confirm zero regressions and clean diagnostics.

Always output findings in this exact structure (omit speculative or cosmetic remarks):

```markdown
## Post-Implementation Quality Convergence Report

### Confirmed Findings & Applied Cleanups
- **[Dimension N: <Name>]** `path/to/file:line`
  - **Issue**: <Verified dead code, duplicate rule, write-only parameter/state, or contract drift>
  - **Evidence**: <Caller trace, local LSP CLI diagnostic (`warning`/`info`/`hint`), or analyzer proof>
  - **Action Taken**: <Deleted / Consolidated / Simplified in-place>

### No Issue Found
- **[Dimension N: <Name>]**: Checked <inspected symbols/files>, confirmed <active consumption / unified SSOT / valid contract / clean cutover>.

### Deferred / Out of Scope
- **Finding**: <Pre-existing debt or broad refactor item (`file:line`)> — <Reason deferred & suggested follow-up>

### Verification
- **Checks executed**: <Commands / LSP CLI / test suite / Quality Gate run>
- **Result**: <Pass / Exit code 0 / Diagnostics clean>
```
