---
name: post-impl
description: "Execute a final 7-dimensional code quality convergence and cleanup audit after implementation and tests pass, before handoff or commit."
---

# Post-Implementation Quality Checklist

Run this convergence audit **after** functional implementation and tests pass, **before** user handoff or commit. It prunes verified residues and drift strictly within the task delta and its immediate blast radius—never expand into unrequested wide refactoring.

## 1. Mandatory Pre-Audit Step: Establish Diff & Run Incremental LSP Scan

Before inspecting the 7 dimensions, you **MUST** execute these two concrete actions (never skip or rely on prior compile/test passes):

1. **Pin changed code files**: Resolve the exact task diff from the active working tree (`git status --porcelain` / `git diff --name-only HEAD`) or an explicit branch merge-base (`git merge-base <target> HEAD`). Never blindly assume `HEAD~1`.
2. **Execute an Incremental LSP Diagnostic Scan (`warning` / `info` / `hint`) on every modified source file**:
   - **Basic compile checks (`go build`, `cargo check`, `tsc` transpile) DO NOT satisfy this gate**—they miss unused parameters, modernize/syntax-sugar idioms, no-op struct tags, deprecated calls, and redundant allocations.
   - **Execution cascade (run at least one real tool call)**:
     1. **Agent-mounted LSP diagnostics tool** (if available in the host): Run per-file `diagnostics` (and `code_actions` for modernize/quick-fix hints) explicitly against the changed file paths—note that workspace-wide `file: "*"` often falls back to shallow build errors, so target the modified files or pair with the CLI below.
     2. **Local Language Server / Analyzer CLI** (probe `PATH`, toolchain bins like `GOPATH/bin` or `~/.cargo/bin`, and editor-managed language dirs such as `%LOCALAPPDATA%/Zed/languages` or `~/.local/share/zed/languages`—note that Zed's running LSP process is stdio-bound to Zed, so invoke the local binary directly):
        - **Go**: `gopls check -severity=hint <changed.go...>`
        - **Rust**: `cargo clippy --all-targets -- -W clippy::pedantic` (scoped to touched crates/files) or `rust-analyzer diagnostics`
        - **TS/JS/Frameworks**: `tsc --noEmit` / `vue-tsc --noEmit` / `svelte-check` + local linter (`oxlint` / `eslint`) on changed files
        - **Python**: `basedpyright` / `pyright` / `ruff check` on changed files
        - **C/C++**: `clang-tidy` / `clangd --check=<file>` on changed files
   - Treat every in-scope `warning`/`info`/`hint` emitted on modified lines/symbols as concrete evidence for Dimensions 2, 3, 4, and 6.

## 2. Seven-Dimensional Audit Checklist

Every finding requires exact `file:line`, caller trace, or LSP/analyzer proof. Fix in-scope low-risk issues immediately in-place; keep code justified by semantics/contracts; defer pre-existing out-of-scope debt:

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
   - **Audit**: Replace stored state synchronously derivable from authoritative state; apply language/LSP modernization idioms and remove duplicate writes/I/O, redundant allocations (e.g., `[]byte(fmt.Sprintf(...))` → `fmt.Appendf`), no-op guards on verified non-null internal contracts, and dead retries.
   - **Guardrail**: Preserve intentional caches, memoized selectors, or decoupled UI presentation states justified by performance or architecture.
5. **Dimension 5: Premature Abstraction & Patchwork Complexity**
   - **Audit**: Inline single-use interfaces, wrappers, or factories introduced solely for this task without domain/architectural value; flatten stacked conditional patches (`if (a && !b && c)`) into cohesive domain logic.
   - **Guardrail**: Retain single-implementation abstractions when they express a real domain boundary, decouple third-party I/O, provide a required test seam, or mark a concrete planned extension point.
6. **Dimension 6: Contract & Source of Truth Drift**
   - **Audit**: Verify modified models, RPC/API payloads, event schemas, struct/serialization tags (e.g., `omitempty` vs. `omitzero` on `time.Time`/structs), and error shapes against downstream consumers, mocks, and bindings.
   - **Guardrail**: Enforce producer-consumer compatibility, not artificial structural symmetry (optional fields, asymmetric projections, and forward-compatible schemas are valid).
7. **Dimension 7: Behavioral Convergence & Path Cleanliness**
   - **Audit**: Ensure new logic cuts over cleanly without leaving superseded logic running in parallel as a silent fallback; strip all temporary debug logs, flags, transitional scaffolding, and conversational negative echoes in names/comments/docs.

## 3. Verification & Output Report

After applying any in-place cleanups, re-run targeted tests, the incremental LSP scan on modified files, and the repository's Quality Gate (plus `Post-Edit Sync` if applicable) to confirm zero regressions and clean diagnostics.

Always output findings in this exact structure—**`LSP Incremental Scan` MUST record the exact tool/command executed and finding count** (or state `N/A (non-code files only)`):

```markdown
## Post-Implementation Quality Convergence Report

### Confirmed Findings & Applied Cleanups
- **[Dimension N: <Name>]** `path/to/file:line`
  - **Issue**: <Verified dead code, duplicate rule, write-only parameter/state, unmodernized idiom, or contract drift>
  - **Evidence**: <LSP diagnostic (`warning`/`info`/`hint`), caller trace, or analyzer output>
  - **Action Taken**: <Deleted / Consolidated / Modernized / Simplified in-place>

### No Issue Found
- **[Dimension N: <Name>]**: Checked <inspected symbols/files>, confirmed <active consumption / unified SSOT / valid contract / clean cutover>.

### Deferred / Out of Scope
- **Finding**: <Pre-existing debt or broad refactor item (`file:line`)> — <Reason deferred & suggested follow-up>

### Verification
- **LSP Incremental Scan**: <Exact LSP tool call or CLI command run on changed files + warning/info/hint count>
- **Quality & Tests**: <Test suite / Quality Gate / Post-Edit Sync commands run + pass status>
```
