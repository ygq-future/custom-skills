---
name: impl
description: "Implement a feature, requirement, or bug fix from context discussion, diagnosis findings, or specs, with adaptive testing, review, and post-implementation convergence. Leaves changes uncommitted."
disable-model-invocation: true
---

Implement the requested work based on the most direct source of truth available:
1. **Context consensus**: Decisions, plans, or requirements agreed upon in the ongoing conversation.
2. **Diagnosis findings**: Root causes, failure states, and reproduction paths identified by `/skill:diagnosing-bugs` or previous debugging in the session.
3. **Formal specs/tickets**: Explicitly provided files, issues, or requirements.

Do not ask for external tickets/specs if the scope and acceptance criteria are already established in context.

### Execution Workflow

Adapt the workflow based on the nature of the task:

- **For Bug Fixes**:
  1. Treat the identified root cause, failure state, and reproduction path from context/diagnosis as ground truth—do not re-diagnose or re-verify the failure.
  2. Apply the targeted fix directly to the affected paths.
  3. Verify against the previously failing condition to confirm the fix, and run relevant tests to ensure no regression.

- **For Features / Enhancements**:
  1. Confirm seams, inputs/outputs, and edge cases before editing.
  2. Use /tdd where appropriate at core behavioral seams.
  3. Run relevant typechecks and targeted tests during implementation; run the full test suite when nearing completion.

### Review and Convergence

1. Once implementation is functionally complete and verified, use /code-review to evaluate standards and correctness.
2. After code review, use /post-impl-checklist for convergence (eliminating dead code, contract drift, and redundant logic).
3. Report findings, test results, and residual risks concisely.

### Delivery Constraints

- Do NOT commit changes automatically. Leave all changes uncommitted in the working tree for user inspection and manual acceptance.
- Present a clear summary of modified files, verification evidence, and review conclusions.
