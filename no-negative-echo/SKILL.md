---
name: no-negative-echo
description: Prevents rejected, superseded, or corrected ideas from leaking into final-facing project language after the implementation has already converged on the accepted result. Use this skill whenever a task has gone through corrections, reversals, removed approaches, or “don’t do X” feedback and the agent is about to write or revise titles, filenames, code comments, test names, commit messages, PR titles/descriptions, changelogs, release notes, handoffs, delivery notes, or similar durable project history. Also use it as a final hygiene pass before committing or handing off work after requirements changed mid-conversation.
compatibility: Requires access to the current task/conversation context and, when checking repository artifacts, permission to read the relevant files or git diff/history being prepared.
metadata:
  version: "1.0.0"
---

# No Negative Echo

Keep the final artifact about what the project **is**, not about mistakes, rejected drafts, or corrections that happened while getting there.

The central rule is simple:

> Write durable project language from the final accepted state. Treat rejected alternatives as constraints, not as material to echo back into the artifact.

A correction such as “do not use a service; run two normal processes instead” may be essential while implementing the change. Once the implementation follows the accepted architecture, do not turn that correction into names such as `non-service-mode`, comments such as `// intentionally not using a service`, or a commit title such as `switch to two processes (no service)` unless the distinction remains intrinsically important to users or maintainers.

## What counts as a negative echo

A negative echo is durable wording that exists mainly because an earlier draft was wrong, rejected, or superseded.

Common forms:

- `X (without Y)` when `Y` is merely a discarded conversation branch.
- “Unlike the old/rejected approach...” in code comments that only need to explain current logic.
- Test names such as `does_not_use_legacy_strategy` when the real behavior can be named positively.
- Commit or PR text that narrates the correction process instead of the delivered change.
- Release notes mentioning an option that never shipped.
- Handoff notes that promote discarded implementation ideas into current architecture terminology.
- Filenames, flags, identifiers, or configuration keys coined as the negation of an abandoned design.

Negative wording by itself is not automatically a negative echo. `not_found`, `non_empty`, `denylist`, `no-cache`, or a test that verifies an explicit prohibition can be perfectly valid. The question is whether the wording is part of the **final domain** or merely residue from the conversation.

## Workflow

### 1. Establish the accepted-state vocabulary

Before writing durable text, identify the final accepted facts:

- What behavior now exists?
- What architecture or implementation was chosen?
- What user-visible capability was delivered?
- What names already belong to the domain?
- Which constraints remain genuinely important after the conversation is forgotten?

Prefer nouns and verbs that describe those facts directly.

### 2. Identify discarded conversation residue

Look back at corrections, reversals, and rejected proposals only to understand what must **not** leak into the final wording.

Typical markers include:

- “不要 / 别 / 不再 / 改成 / 放弃 / 去掉 / 不是 / 不需要”
- “instead of / no longer / do not / remove / abandon / switch away from / not X”
- earlier proposals that were subsequently superseded

Do not automatically copy these phrases into project artifacts.

### 3. Generate from the accepted state, not by editing the rejected sentence

Do not start from:

`Implement dashboard without the discarded service architecture`

and merely shorten it.

Regenerate from the accepted facts:

`Implement dual-process monitoring dashboard`

This matters because sentence-level editing often leaves semantic residue even after obvious negative words are removed.

### 4. Scan every durable surface

When relevant to the task, inspect all of these surfaces before finalizing:

- document/page/feature titles
- filenames and directory names
- symbols, identifiers, flags, config keys
- code comments and docstrings
- test suite, test case, fixture, and snapshot names
- commit subject and body
- branch name if being proposed
- PR/MR title and description
- changelog and release notes
- implementation summary / delivery notes
- handoff notes intended to guide a fresh agent

Do not limit the check to source code. Negative echo often survives in the outer delivery layer after the implementation itself is correct.

### 5. Classify suspicious wording before changing it

For each phrase that references an omitted, rejected, previous, legacy, alternative, or forbidden approach, ask:

1. **Would this phrase still make sense to a maintainer who never saw the conversation?**
2. **Does the distinction describe a real, persistent domain concept?**
3. **Would removing the rejected alternative make the text less precise or unsafe?**

If the answers are `no / no / no`, remove or rewrite the phrase.

If the distinction is genuinely required, keep it. Examples include:

- migration notes describing behavior that users actually had in a released version
- compatibility code whose reason would otherwise be mysterious
- security constraints where the prohibited behavior is itself part of the requirement
- regression tests whose purpose is explicitly to prevent a previously shipped bug
- ADRs or design documents whose job is to record rejected alternatives
- user-requested historical explanations

### 6. Rewrite positively

Prefer these transformations:

| Residual wording | Accepted-state wording |
| --- | --- |
| `番茄炒蛋（没有东坡肉）` | `番茄炒蛋` |
| `add local mode without service` | `add local dual-process mode` |
| `test_no_service_startup` | `test_collector_and_ui_startup` |
| `remove old parser and use v2 parser` | `adopt v2 parser` |
| `new settings page, not legacy dialog` | `new settings page` |
| `fix implementation to avoid rejected cache path` | `route reads through the canonical cache path` |

When a positive replacement would be vague, name the selected mechanism rather than the rejected one.

Do not weaken a requirement while removing negative echo. If the rejected wording encodes a durable invariant such as exclusivity, ownership, or authority, preserve that invariant in accepted-state terms.

For example:

- `remove caller-owned projection logic` → `all callers rely exclusively on the shared projection`
- `do not duplicate projection rules in response handlers` → `projection-rule coverage is owned by the shared projection seam`

A rewrite is too weak if the rejected implementation could still exist while technically satisfying the new wording.

### 7. Perform a final outside-the-conversation test

Read the candidate text as if you had never seen the chat.

Ask:

- Does any phrase raise the question “why are they telling me this?”
- Does it introduce a concept that does not exist in the final system?
- Does it sound like a rebuttal, apology, correction log, or self-defense?
- Is the wording centered on the delivered result?

If the artifact only makes sense with knowledge of the conversation, rewrite it.

## Git-specific guidance

For commit and PR language, describe the delta that matters to the repository.

Prefer:

- `feat(ui): add dual-process startup flow`
- `refactor(parser): centralize model-group parsing`
- `fix(layout): keep capsule anchored during DPI changes`

Avoid conversation-shaped subjects such as:

- `feat(ui): use dual-process startup instead of service`
- `fix(parser): remove the bad approach`
- `refactor: no longer use the originally planned controller`

The commit body may explain motivation when useful, but it should explain the repository-level reason, not replay the dialogue.

## Comments and tests

Comments should explain current invariants, non-obvious reasons, contracts, or constraints. They should not memorialize temporary misunderstandings.

Prefer:

```text
Keep the collector lifetime independent from the UI so either process can restart safely.
```

Avoid:

```text
We don't use the service approach here because that idea was rejected earlier.
```

Tests should name observable behavior or a durable invariant. A negative test name is fine when the **absence itself is the requirement**. For example, `rejects_unsigned_payload` is meaningful; `does_not_use_the_first_proposed_parser` is conversation residue.

## Handoffs

A handoff should reconstruct the current project state for a fresh agent.

Include:

- accepted architecture and invariants
- completed behavior
- current interfaces and seams
- unresolved work
- known risks and verification status

Do not include discarded alternatives merely to say they are not being used. Include them only when they remain a live trap, compatibility concern, migration constraint, or explicit decision record that a future agent could realistically violate.

## Operating mode

Use this skill in either mode:

### Generation mode

When creating a new title, commit, PR, comment, test name, release note, or handoff, generate directly from accepted-state vocabulary.

### Review mode

When reviewing existing changes, flag only actual conversation residue. For each issue:

1. quote or identify the suspicious phrase,
2. explain what discarded context it unnecessarily preserves,
3. give a positive replacement,
4. leave legitimate historical or domain-negative language unchanged.

Keep review findings concise. Do not create new negative echo while explaining the old one.

## Optional deterministic scan

If the rejected terms are concrete and repository files are available, use `scripts/scan_echo.py` as a supplemental grep-like pass:

```bash
python scripts/scan_echo.py \
  --forbidden "service approach" \
  --forbidden "legacy dialog" \
  path/to/files
```

The script finds literal residue only. It cannot decide whether a match is semantically justified, so always apply the classification test above before changing anything.

For more nuanced examples and boundary cases, read `references/examples.md`.
