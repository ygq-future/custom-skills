---
name: impl
description: "Implement features, slices, GitHub Issues, or bug fixes end-to-end with seam-level behavioral tests, mandatory Acceptance Criteria check-off, and adaptive review gates."
---

# Implement

End-to-end implementation workflow from conversation consensus, `docs/tasks/` slices, GitHub Issues, or verified root causes.

## 1. Establish Scope & Acceptance Criteria

1. **Resolve the source of truth**:
   - **GitHub Issue (`#<N>`) or Local Slice (`docs/tasks/<slug>.md`)**: Fetch/read the full entry upfront (`gh issue view <N>` or `read`), verify `Blocked by` prerequisites are satisfied, and copy every `- [ ]` Acceptance Criterion into the active task tracker (`todo`) so none are missed.
   - **Verified Diagnosis**: Treat root cause and reproduction steps from `diagnose` or context as established—do not re-diagnose. *(If a bug's root cause is still unknown or flaky, run `diagnose` first.)*
   - **Conversation Consensus**: Do not demand external specs/issues when scope is already clear in chat.
2. **Act or Clarify**:
   - **Clear scope**: State target seams briefly and implement end-to-end without pausing for "OK".
   - **Ambiguous / high-blast-radius trade-offs**: Run `clarify` before editing.
   - **UI / frontend changes**: Apply `ui-craft` alongside this workflow.

## 2. Implementation & Seam Testing

- **Vertical execution**: Implement narrow, cohesive paths across schema, domain logic, and callers; run typechecks and targeted tests continuously.
- **Test at public seams**: Write permanent behavioral tests strictly against public module interfaces (seams), asserting observable outcomes with independent expected literals.
- **Testing anti-patterns (Forbidden)**:
  - Never mock private internal collaborators or test private helper functions directly;
  - Never write tautological assertions that recompute expected values using the same formula as production code;
  - Delete obsolete implementation-coupled tests superseded by a clean cutover.

## 3. Mandatory Acceptance Criteria Check-Off & Tracker Sync

Before running final convergence gates, verify **every** `- [ ]` Acceptance Criterion item-by-item against concrete test runs or `file:line` evidence:

- **Local Task File (`docs/tasks/<slug>.md`)**: Edit the file to check off verified items (`- [ ]` → `- [x]`) and update the slice's `Status` (`completed` once all items pass).
- **GitHub Issue (`#<N>`)**:
  1. Update the issue body (`gh issue edit <N> --body-file ...`) to check off verified `- [x]` Acceptance Criteria, and post a brief evidence summary via `gh issue comment <N>`.
  2. **Closure rule**: Because code remains uncommitted locally by default, **keep the issue open** after checking off `- [x]` and note that it is ready to close upon commit/push—only run `gh issue close <N>` immediately when committing/pushing or when the user explicitly instructed to close the issue in this turn.

## 4. Adaptive Review & Convergence Gate

1. Run full relevant tests, an **incremental LSP diagnostic scan** (`warning`/`info`/`hint` via host LSP `diagnostics` on changed files and/or local LSP CLI such as `gopls check -severity=hint`, `pyright`, `cargo clippy --all-targets`), the repository's unified Quality Gate (if configured), and XERJ `Post-Edit Sync` (when declared in `AGENTS.md`).
2. **Choose Review Tier by Semantic Change Scope & Blast Radius** (never judge by file count—a 10-file mechanical wiring change can be low-risk while a single-file state/concurrency rewrite is high-risk):
   - **Lightweight Tier (`post-impl` only)**: Contained behavioral scope—localized bug fixes, UI refinements, single-seam features, or mechanical wiring with straightforward control flow and **zero** changes to shared contracts, core domain invariants, concurrency/lifecycle semantics, or persistence/security models.
   - **Full Dual-Axis Tier (`code-review` → `post-impl`)**: Mandatory when the change (a) alters public APIs, IPC/RPC wire protocols, DB/storage schemas, or shared domain contracts; (b) rewrites complex control flow, state machines, concurrency/locking, caching/invalidation, auth/security, or error-recovery paths (even within a single file); (c) couples multiple subsystems with non-trivial behavioral interactions; or (d) is explicitly requested by the user. Fix confirmed in-scope `code-review` findings first, then execute `post-impl`.

## 5. Delivery

- **Never auto-commit or push**: Keep all changes uncommitted in the working tree unless explicitly instructed.
- Present a concise handoff: modified files, Acceptance Criteria check-off status (when applicable), verification outputs, and the `Post-Implementation Quality Convergence Report`.
