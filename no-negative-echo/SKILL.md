---
name: no-negative-echo
description: Prevents rejected drafts, reversals, and conversational corrections from leaking into durable code and project text. Use after requirements change, approaches are abandoned, or "don't do X / instead of Y" feedback occurs when naming symbols/files/flags/tests or writing comments, docs, commits, PRs, release notes, or handoffs.
compatibility: Requires access to current conversation context and relevant repository files or diffs.
metadata:
  version: "1.1.0"
---

# No Negative Echo

> Write durable project artifacts purely from the **final accepted state**. Treat rejected alternatives and mid-task corrections as constraints, never as material to echo back.

A negative echo is durable code or prose that exists only because an earlier draft or proposal was wrong, rejected, or superseded (e.g., turning "don't use a service; run two processes" into `non_service_mode`, `// intentionally not using a service`, or `feat: switch to two processes (no service)`).

Domain-negative terms (`not_found`, `non_empty`, `denylist`, `no-cache`, `rejects_unsigned_payload`) are **not** negative echoes when the prohibition or absence belongs to the final domain contract.

## 1. Durable Surfaces to Guard

Inspect both code and outer delivery layers:
- **Code & Config**: filenames, directories, symbols, identifiers, CLI flags, config keys, comments, docstrings.
- **Tests**: suite, case, fixture, and snapshot names (name observable behavior or required prohibitions, never discarded proposals).
- **Delivery & History**: document/feature titles, commit subjects/bodies, branch names, PR titles/descriptions, changelogs, release notes, delivery summaries, and agent handoffs.

## 2. Classification Test (Residue vs. Required Context)

When a phrase references an omitted, rejected, previous, legacy, or alternative approach (often triggered by markers like *"不要 / 别 / 不再 / 改成 / 去掉"* or *"instead of / no longer / without / avoid / not X"*), ask:

1. **Stranger test**: Would this make sense to a maintainer who never saw the conversation?
2. **Domain test**: Does the distinction describe a real, persistent domain concept or runtime axis?
3. **Safety/precision test**: Would removing the rejected alternative weaken an invariant or make the text unsafe/ambiguous?

- If **no / no / no** → **Residue**: regenerate from accepted-state facts.
- If **yes** to any → **Keep**: legitimate context includes released-version migration notes, non-obvious compatibility workarounds, security/regression prohibitions, ADRs recording rejected options, live traps in handoffs, or user-requested history.

## 3. Positive Generation & Invariant Preservation

- **Regenerate, don't trim**: Never start from a rejected sentence (`Implement dashboard without the discarded service architecture`) and merely trim words. Generate directly from accepted facts (`Implement dual-process monitoring dashboard`).
- **Name the chosen mechanism**: When removing a negation leaves vague wording, name what *was* selected.
- **Never weaken invariants**: If a negative correction encodes exclusivity, ownership, or authority, state that invariant positively so the rejected design remains impossible under the new wording.

| Conversational Residue | Accepted-State Wording |
| :--- | :--- |
| `番茄炒蛋（没有东坡肉）` | `番茄炒蛋` |
| `add local mode without service` / `feat(ui): use dual-process instead of service` | `add local dual-process mode` / `feat(ui): add dual-process startup flow` |
| `test_no_service_startup` / `does_not_use_first_proposed_parser` | `test_collector_and_ui_startup` / `parses_model_group_with_v2_schema` |
| `// Do not use the service approach here because it was rejected` | `// Keep collector lifetime independent from UI so either process restarts safely` |
| `remove caller-owned projection logic` *(encodes exclusivity)* | `all callers rely exclusively on the shared projection seam` |

## 4. Operating Modes

- **Generation Mode**: Formulate new identifiers, comments, test names, commits, PRs, and handoffs directly from accepted-state vocabulary. In handoffs, state current architecture, invariants, completed behavior, and open risks; mention discarded ideas only if they remain a realistic trap for the next agent.
- **Review Mode**: Flag only actual conversational residue (1. quote phrase → 2. state what discarded context it preserves → 3. provide positive replacement). Leave legitimate domain-negative or historical wording untouched.

## 5. Optional Deterministic Scan & References

- **Literal scan**: When rejected terms are concrete, run `python scripts/scan_echo.py --forbidden "service approach" --forbidden "legacy dialog" path/to/files`, then apply the Section 2 classification test to every match.
- **Boundary examples**: Read `references/examples.md` for borderline cases (`legacy`, `fallback`, `new`, `non-X`).
