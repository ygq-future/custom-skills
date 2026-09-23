---
name: impl
description: "Implement a piece of work based on a spec or set of tickets with TDD, code review, and post-implementation convergence. Leaves changes uncommitted for manual user acceptance."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use /code-review to review the work.

After code review, use /post-impl-checklist to run post-implementation quality convergence and cleanup.

Report the findings and outcomes from both /code-review and /post-impl-checklist clearly to the user.

Do NOT commit your work automatically. Leave all changes uncommitted in the working tree for user inspection and manual acceptance. Present a concise summary of changes, review outcomes, and verification results.
