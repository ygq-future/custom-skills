---
name: no-echo
description: "Strip rejected drafts, reversals, and conversational corrections from identifiers, comments, tests, docs, commits, PRs, release notes, and handoffs."
---

# No Echo

Write and review durable artifacts—code identifiers, flags, comments, test names, docs, specs, commits, PRs, release notes, and handoffs—purely from the **final accepted state**, never as a reaction to discarded drafts or mid-conversation corrections.

## 1. Residue vs. Legitimate Context (3-Question Filter)

When text or naming contains contrast/negation markers (*"instead of / without / no longer / avoid / 不要 / 去掉 / 改用"*), ask:
1. **Stranger test**: Does it make sense to a reader who never saw the chat history?
2. **Domain test**: Does it name a real runtime/product axis (`no-cache`, `non_empty`, `denylist`, `rejects_unsigned_plugin`)?
3. **Invariant/history test**: Would removing it weaken an exclusivity invariant or erase real shipped history (released-version migration notes, compatibility workarounds for live clients, or ADR option comparisons)?

- **All three "No" → Conversational Residue**: Regenerate from scratch using accepted-state facts (never merely trim words from a rejected sentence).
- **Any "Yes" → Keep**: Preserve genuine security prohibitions, regression invariants, migration docs, and ADRs; state ownership/exclusivity invariants positively where clearer.

## 2. Borderline Terms & Rewrite Patterns

- **`legacy` / `fallback`**: Valid only when both old/new or primary/secondary paths actively coexist at runtime; residue if the rejected path was never shipped or was fully deleted.
- **`new` (`newSettingsPage`)**: Residue unless contrasting with a still-live old surface; name the actual domain concept.
- **`no-X` / `non-X` / `without-X`**: Valid only when `X` is a real user/runtime mode; never echo a rejected proposal (`dual_process_mode`, not `no_service_mode`).

| Surface | Conversational Residue (Rewrite) | Accepted-State Wording |
| :--- | :--- | :--- |
| **Commit / PR** | `feat(ui): use dual-process instead of service` | `feat(ui): add dual-process collector and UI startup` |
| **Comment** | `// Do not use polling here; we decided against it` | `// Subscribe to change events so updates stay push-driven` |
| **Test / Title** | `test_does_not_open_old_dialog` / `Settings (no SQLite)` | `test_opens_settings_page` / `JSON settings persistence` |

## 3. Execution Modes

- **Generation Mode**: Author new names, prose, commits, PRs, docs, and handoffs directly in accepted-state domain language (mentioning discarded ideas in handoffs only if they pose an active trap).
- **Review Mode**: Scan the target diff or document, flag only verified conversational residue (*quote → discarded context leaked → positive replacement*), and leave valid domain/historical language untouched.
