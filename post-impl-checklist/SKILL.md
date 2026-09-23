---
name: post-impl-checklist
description: "USER-INITIATED OR POST-TASK CONVERGENCE. Execute a final code quality convergence and cleanup audit after a feature, refactor, or bug fix is functionally complete and before handing off for acceptance or committing. Detects and safely eliminates duplicate business rules, verified dead code, invalidated legacy paths, write-only internal state/parameters, premature abstractions, redundant operations, and contract drift introduced or exposed by the change. Focuses strictly on minimal necessary cleanup grounded in concrete references, callers, and test evidence without expanding scope into general refactoring."
---

# Post-Implementation Quality Checklist

Post-implementation code quality convergence and cleanup audit.

Run this skill **after** functional implementation is complete and tests pass, but **before** presenting the work for user acceptance or finalizing the commit.

---

## 1. Positioning & Boundaries

This skill is a **cleanup and convergence audit**, not a general-purpose reviewer or quality gate.

| Review Type | Core Purpose | Out of Scope for This Skill |
| :--- | :--- | :--- |
| **Bug / Security Review** (`/review`) | Finding functional defects, security vulnerabilities, edge-case regressions, performance bottlenecks. | Not replacing vulnerability scanning or deep bug hunting. |
| **Spec / Compliance Review** | Verifying alignment with PRD, user stories, acceptance criteria, or architectural guidelines. | Not re-evaluating business requirements. |
| **Automated Quality Gate** (`lint` / `test`) | Syntax validation, formatting, type checking, unit test execution. | Not replacing CI/pre-commit toolchains. |
| **Post-Implementation Checklist (This Skill)** | **Pruning verified residues, invalidated paths, unused internal state, accidental rule duplicates, and contract drift within the task boundary.** | **Strictly bounded to the delta and its immediate blast radius; prohibits unrequested wide refactoring.** |

---

## 2. Core Principles

1. **Evidence over intuition**: Every finding must be grounded in an exact file, symbol, caller trace, data flow, or test failure. "Might be unused" is not a finding; prove 0 references and absence of runtime entry points.
2. **No forced changes**: Passing the checklist does not require making changes. If the current implementation is justified by distinct semantics, ownership, change drivers, or runtime constraints, leave it unchanged. Do not refactor merely to eliminate superficial similarity, reduce line count, or satisfy a checklist item.
3. **Minimal necessary convergence**: Fix only concrete defects directly introduced, invalidated, or exposed by this change. Do not embark on unrelated "good-to-have" refactors.
4. **Proportional caller & entry point tracing**: For any symbol modified or considered for pruning, trace callers and potential dynamic bindings proportionally to the symbol's visibility and direct blast radius.
5. **Authoritative Single Source of Truth (SSOT)**: Every business rule, policy decision, and authoritative state must have a clear, unique source of truth. Derived, cached, replicated, or presentation states are valid as long as they are explicitly non-authoritative and their synchronization/invalidation model is sound. Focus on eliminating split business rules rather than mechanically deduplicating state copies.
6. **Distinguish internal state from boundary contracts**: Prune dead internal fields, local variables, and private parameters aggressively; preserve boundary contracts (public APIs, IPC/RPC schemas, serialization formats, configuration keys, database schemas) unless their contract deprecation is explicitly part of the task.
7. **Clean cutover**: When new logic fully supersedes older internal logic, completely prune the dead paths, callsites, and imports within the change boundary.

---

## 3. Seven-Dimensional Audit Checklist

Execute each dimension as a concrete inspection action over the changed files and their immediate blast radius.

### Dimension 1: Duplicate Business Rules & Invariant Divergence
- [ ] **Action**: Search the codebase for existing implementations of the business rules, invariants, status mappings, or core domain calculations introduced in this change.
- [ ] **Trigger Conditions**:
  - The exact same business rule, validation logic, or authoritative enum mapping is implemented in multiple places (e.g., duplicate validation rules written independently in frontend and backend).
  - An existing canonical utility or domain service already handles this exact business operation.
- [ ] **Safety Rule**: **Superficial structural similarity is NOT code duplication.** If two pieces of code look alike but represent different domain concepts or will change for different business reasons, keep them separate. Only consolidate when the underlying rule, invariant, and lifecycle reason are identical.
- [ ] **Remedy**: Route calls to the canonical source of truth, or make one implementation authoritative while the other derives from it.

### Dimension 2: Write-Only State & Parameters (Internal vs. Contract)
- [ ] **Action**: For every newly added struct field, object property, class member, reactive state, or function parameter, search for its downstream read/consumption points.
- [ ] **Trigger Conditions**:
  - The field or parameter is purely internal to the module/function, is written or assigned, but never read to affect control flow, computation, or presentation.
- [ ] **Safety Rule (Contract Exemption)**:
  - Do **NOT** delete fields or parameters if they belong to:
    - Public / exported APIs;
    - IPC / RPC / HTTP wire contracts;
    - Serialization or database schemas;
    - Configuration file contracts;
    - Generated code or plugin interface requirements;
    - Explicit forward/backward compatibility specifications.
  - Verify external consumption and contract requirements before classifying a boundary field as write-only.
- [ ] **Remedy**: If confirmed as purely internal and unconsumed, remove the field/parameter and adjust immediate callers.

### Dimension 3: Dead Code & Orphaned Paths (Proportional Runtime Awareness)
- [ ] **Action**: For functions, helpers, branches, or types replaced or bypassed by the change, determine whether any live callers or entry points remain.
- [ ] **Trigger Conditions**:
  - An internal helper, private branch, or configuration key has become unreachable solely because the new implementation bypassed it.
- [ ] **Safety Rule (Proportional Runtime-Entry Check)**:
  - Zero static incoming references is a necessary clue, **not a sufficient condition** for deletion.
  - **Runtime-aware, but not exhaustive by default**:
    - For strictly **private/internal symbols**, if the local structure and file-level visibility already prove the absence of callers, do not perform unbounded runtime archaeology across the repository.
    - Only for **exported/public symbols** or code with plausible runtime registration (dependency injection, framework lifecycle, event/route/plugin handler, reflection, generated binding, dynamic dispatch) should targeted runtime-entry checks be performed.
    - Keep checks strictly proportional to the symbol's visibility and direct blast radius; never expand into open-ended discovery across unrelated files.
- [ ] **Remedy**: Once confirmed that no static or dynamic runtime consumer exists, delete the orphaned functions, types, and unused imports.

### Dimension 4: Redundant State & Unnecessary Operations
- [ ] **Action**: Inspect newly added state variables, caches, effect handlers, and lifecycle hooks for redundant persistence or unnecessary operations.
- [ ] **Trigger Conditions**:
  - Storing a state variable that can be trivially and synchronously derived from existing authoritative state on demand.
  - Redundant writes, duplicate event dispatches, duplicate cache invalidations, or repeated disk/network I/O for the same state transition.
  - Excessive defensive programming unsupported by evidence: deep null checks on verified non-nullable internal contracts, retries on permanent fatal errors, or state resets immediately prior to object destruction.
- [ ] **Safety Rule**: Explicitly maintained caches, memoized selectors, or decoupled UI presentation states are acceptable when justified by performance or architecture. Verify whether the state is an unneeded duplicate or a valid non-authoritative projection.
- [ ] **Remedy**: Convert redundant stored state into pure derived values; prune baseless defensive guards and duplicate side effects.

### Dimension 5: Premature Abstraction & Patchwork Complexity
- [ ] **Action**: Review newly introduced interfaces, generic wrappers, factory layers, and branching logic.
- [ ] **Trigger Conditions**:
  - An interface, wrapper, or strategy abstraction was introduced solely for this task, has only one implementation, has no distinct domain semantics, and does not serve as an architectural boundary.
  - A bug fix or feature was implemented by stacking nested conditional patches (`if (isSpecial && !isOld && count > 0)`) rather than updating the domain logic.
- [ ] **Safety Rule**: A single implementation or single callsite alone is **NOT** a reason to inline if the abstraction:
  - Expresses a meaningful domain concept;
  - Decouples an external third-party dependency;
  - Serves as a required test seam;
  - Represents a stable extension point with concrete variation planned.
- [ ] **Remedy**: Only inline when the abstraction adds indirection without architectural, testing, or domain value. Refactor tangled conditional patches into clear, cohesive branch logic.

### Dimension 6: Contract & Source of Truth Drift (Compatibility & Consistency)
- [ ] **Action**: Compare modified models, RPC/API contracts, event schemas, and enum sets against their downstream and cross-boundary consumers.
- [ ] **Trigger Conditions**:
  - An enum value, field nullability, or error shape was altered on the producer side, but consumer mocks, deserializers, or IPC bindings were left with contradictory assumptions.
  - Default values, required constraints, or validation boundaries differ between producer and consumer in an incompatible way.
- [ ] **Safety Rule (Compatibility over Symmetry)**:
  - Do **NOT** enforce artificial structural symmetry. Asymmetric responsibilities, optional fields, forward/backward-compatible schema evolutions, versioned protocols, and consumers ignoring unknown fields are valid designs.
  - The focus is solely on whether producer and consumer have compatible and consistent understandings of the authoritative contract, not whether their types or schemas are identical mirrors.
- [ ] **Remedy**: Ensure cross-boundary contracts and consumers remain compatible with the intended contract and do not make contradictory assumptions.

### Dimension 7: Behavioral Convergence & Path Cleanliness
- [ ] **Action**: Check whether the old implementation and new implementation unintentionally run in parallel or leave confusing fallbacks.
- [ ] **Trigger Conditions**:
  - The new logic was added, but the old logic still executes as an unneeded, silent fallback path.
  - Temporary debugging flags, exploratory prints, or transitional test hooks remain in the diff.
- [ ] **Remedy**: Cut over cleanly: route all traffic through the validated path and prune transitional scaffolding.

---

## 4. Execution Workflow

```
[1. Establish Review Boundary] ────> [2. Proportional Trace & Entry Check] ────> [3. Minimal Convergence] ────> [4. Verify & Report]
```

### Step 1: Establish Review Boundary (Established, Not Guessed)
1. **The review boundary must be established, not guessed**:
   - Prefer an explicitly specified target base, PR target, or branch merge-base (`git merge-base <target-branch> HEAD`).
   - Combine with relevant staged and unstaged working tree changes.
   - Do **NOT** assume `HEAD~1` merely for convenience. Use `HEAD~1` only when the active workflow or explicit user instruction proves that the single previous commit exactly delineates the task scope.
   - If the task boundary cannot be reliably established, explicitly note the boundary ambiguity and request confirmation of the review target rather than arbitrarily widening or narrowing the inspection window.
2. Confirm the selected diff accurately represents the scope of the current task.
3. List all added/modified symbols, exports, parameters, and configuration keys within this scope.

### Step 2: Proportional Trace & Entry Point Cross-Check
1. For every modified or superseded symbol, check callers proportionally:
   - For internal/private symbols: verify absence of callers in immediate file/module scope.
   - For exported/public or dynamic symbols: verify against potential runtime registrations (DI, routes, events, framework bindings).
2. For every newly added field or parameter, verify downstream consumption while distinguishing internal data from boundary contracts.
3. For newly added logic, search for existing canonical implementations of the same business rule.

### Step 3: Minimal Convergence (Fix, Defer, or Justify Keep)
- **Direct Cleanup**: If an issue is directly within the task diff, has verified evidence (no callers, no runtime entry points, purely internal), and carries low risk, **fix it immediately in-place**.
- **Justified Keep**: If a piece of code looks similar or single-use but is justified by domain semantics, boundary contracts, or change drivers, **leave it unchanged**.
- **Deferred / Out of Scope**: If an issue involves pre-existing technical debt, broad architectural restructuring, or high cross-module risk, **do not touch**. Document it as a deferred item with evidence.

### Step 4: Verification & Re-check
1. Re-run targeted unit/integration tests covering the cleaned areas.
2. Confirm compiler diagnostics, linter warnings, and type checks remain clean after any pruning.

---

## 5. Output Report Format

Always present findings in this structured format. **Never report speculative, unevidenced, or purely cosmetic complaints.**

```markdown
## Post-Implementation Quality Convergence Report

### Confirmed Findings & Applied Cleanups
- **[Dimension Name]** `path/to/file:line`
  - **Issue**: <Concrete description of verified dead code, duplicate business rule, or unused internal state>
  - **Evidence**: <LSP check, verified absence of runtime entry points/dynamic callers, or call graph proof>
  - **Action Taken**: <Deleted / Consolidated / Simplified in-place>

### No Issue Found
- **[Dimension Name]**: Checked <inspected symbols/paths>, confirmed <active consumption / unified SSOT / valid boundary contract / clean cutover>.

### Deferred / Out of Scope
- **Finding**: <Pre-existing debt or broad architectural improvement>
- **Reason**: <Why it exceeds current task scope and risk of touching it now>
- **Suggested Follow-up**: <Clear proposal for future dedicated task>

### Verification
- **Checks executed**: <Command / test suite / type checker run>
- **Result**: <Pass / Exit code 0 / Diagnostics clean>
```
