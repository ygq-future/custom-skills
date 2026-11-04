# Examples and Boundary Cases

Consult this reference when a phrase contains negative wording, historical contrast, or comparison and it is unclear whether it is conversational residue or legitimate domain context.

## 1. Clear Negative Echo vs. Accepted-State Wording

| Surface | Scenario | Conversational Residue (Avoid) | Accepted-State Wording (Prefer) | Why |
| :--- | :--- | :--- | :--- | :--- |
| **Title** | Proposed embedded DB → corrected to JSON files | `Settings persistence (no embedded database)` | `Settings persistence` / `JSON settings persistence` | Rejected DB is not part of product vocabulary. |
| **Commit** | Rejected service design → split into 2 processes | `refactor: replace wrong service design with two processes` | `refactor: separate collector and UI processes` | Repository history tracks resulting boundary, not chat corrections. |
| **Comment** | Decided against polling in favor of events | `// Do not use polling here; we decided against it.` | `// Subscribe to change notifications so updates stay event-driven.` | Documents current invariant and engineering rationale. |
| **Test** | Kept settings page, dropped old dialog draft | `test_does_not_open_old_settings_dialog` | `test_opens_settings_page` | Old dialog is not an active contract. |

## 2. Legitimate Negative or Historical Language (Keep)

- **Security requirement**: `rejects_unsigned_plugins` — rejection is the observable required behavior.
- **Regression test**: `test_rejects_duplicate_invoice_number` (when a shipped version previously allowed duplicates) — enforces a durable domain invariant.
- **Migration release note**: `Removed support for config schema v1; migrate to v2 before upgrading` — users actually depended on v1.
- **Compatibility comment**: `// Keep CRLF normalization for files produced by v1 Windows clients` — explains surprising code for clients that still exist.
- **Architecture Decision Record (ADR)**: Explicitly comparing options and recording why Option B was rejected — decision history is the document's purpose.

## 3. Borderline Terms

- **`legacy`**: Valid when a legacy interface/path still exists in the system; residue when referring to an unshipped idea discarded in chat.
- **`fallback`**: Valid when runtime genuinely has primary + secondary paths; residue when the "fallback" became the sole accepted design.
- **`new`**: Ages poorly in durable identifiers (`newSettingsPage`); use the actual feature name unless contrasting with a still-present old version.
- **`no-X` / `non-X` / `without-X`**: Justified only if `X` is a real product/runtime axis users or maintainers must distinguish; otherwise name the chosen architecture.
