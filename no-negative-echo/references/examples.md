# Examples and Boundary Cases

Use this reference when a phrase is ambiguous: it contains negative wording, historical context, or a comparison, but it is not obvious whether it is conversation residue.

## Clear negative echo

### Title

Conversation:

- First proposal: add an embedded database.
- Correction: keep data in flat files.
- Final implementation: JSON files beside the executable.

Bad:

`Settings persistence (no embedded database)`

Better:

`Settings persistence`

More specific when needed:

`JSON settings persistence`

Why: the rejected database is not part of the final product vocabulary.

### Commit

Bad:

`refactor: replace wrong service design with two processes`

Better:

`refactor: separate collector and UI processes`

Why: the repository cares about the resulting process boundary, not the conversational correction.

### Code comment

Bad:

`// Do not use polling here; we decided against it.`

Better:

`// Subscribe to change notifications so updates remain event-driven.`

Why: the second comment documents the current invariant and its engineering reason.

### Test name

Bad:

`test_does_not_open_old_settings_dialog`

Better:

`test_opens_settings_page`

Why: the old dialog is not a current behavior or contract.

## Legitimate negative or historical language

### Security requirement

`rejects_unsigned_plugins`

Keep it. Rejection is the observable required behavior.

### Regression test

A released version previously allowed duplicate invoices and the test exists to prevent recurrence:

`test_rejects_duplicate_invoice_number`

Keep it. This is a durable domain invariant, not conversation history.

### Migration release note

`Removed support for configuration schema v1; migrate to v2 before upgrading.`

Keep it. Users may actually depend on v1, so the removed state is externally relevant.

### Compatibility comment

`// Keep CRLF normalization for files produced by v1 Windows clients.`

Keep it when those clients still exist. Historical context explains otherwise surprising compatibility code.

### Architecture Decision Record

An ADR explicitly compares alternatives and records why option B was rejected.

Keep the rejected alternative. The document's purpose is decision history.

## Borderline cases

### “Legacy”

`legacy` is acceptable when there is a real legacy interface or compatibility path still present in the system. It is residue when it merely refers to an idea discussed and discarded before shipping.

### “Fallback”

`fallback` is acceptable when runtime behavior genuinely has a primary and secondary path. It is residue when the so-called fallback is simply the only accepted design after another proposal was rejected.

### “New”

`new` is often weak durable naming because it ages badly. Prefer the feature's actual name unless comparison with an existing old version is part of the product contract.

### “No-service”, “non-X”, “without-X”

These names are justified only if X is a meaningful product axis users or maintainers must distinguish. If X exists only in the conversation, name the selected architecture instead.

## Review heuristics

A phrase is likely residue when several of these are true:

- It mentions something absent from the final implementation.
- It sounds defensive or corrective.
- It would confuse a new maintainer.
- It depends on chronological words such as “originally,” “instead,” “anymore,” or “now” without a real migration context.
- It names the final solution only by what it is not.
- Removing the rejected concept makes the wording clearer.

A phrase is likely legitimate when several of these are true:

- Users can observe the distinction.
- The old behavior shipped or still exists somewhere.
- The constraint protects security, compatibility, data integrity, or a regression.
- The artifact is explicitly historical (ADR, migration guide, postmortem).
- A future maintainer needs the contrast to avoid a plausible mistake.
