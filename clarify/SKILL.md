---
name: clarify
description: "Clarify ambiguous requirements, trade-offs, or plans via dependency-ordered decision rounds with recommended answers before coding."
---

# Clarify

Align on ambiguous requirements, architectural trade-offs, or underspecified ideas before writing code.

## 1. Core Discipline

1. **Facts are yours; decisions are the user's**: Inspect the codebase, configs, and docs first (using indexed search, LSP, or read-only exploration subagents). Never ask the user a factual question the repository or local toolchain can answer.
2. **Walk the decision tree by frontier**: Map open decisions and their dependencies. Ask only the current **frontier**—questions whose prerequisites are already settled—in a single compact round. Defer dependent follow-up questions to the next round once answers reshape the tree.
3. **Always lead with a recommendation**: Every question MUST include a concrete recommended choice grounded in repo conventions and simplicity, phrased so a brief confirmation ("yes" / "go with recommendations") resolves the entire round.
4. **Domain language hygiene**: Cross-check user terms against existing code and any `GLOSSARY.md` / `docs/adr/`. Call out contradictions or overloaded terms immediately. Update `GLOSSARY.md` or offer a concise ADR under `docs/adr/` **only** when the repo already maintains them or when an irreversible, non-obvious architectural trade-off genuinely warrants recording—never create empty boilerplate files.

## 2. Round Format

Keep each round tight (typically 2–4 frontier questions; skip anything obvious):

```markdown
1. **<Decision title>**: <1–3 sentences stating the real trade-off and blast radius>
   - **Recommended**: <Concrete option and one-line rationale>
   - **Alternatives**: <Brief viable alternatives, if any>
```

*(When the host environment provides a native structured questionnaire tool, you may present the frontier there with recommended defaults preselected.)*

## 3. Exit Criteria

Stop interviewing as soon as the decision frontier is empty and acceptance boundaries are clear:
- **Small / medium scope**: Summarize settled seams and constraints in 3–5 bullets, then ask to proceed with `impl` (or proceed directly if the user already authorized implementation).
- **Large multi-slice scope**: Offer to run `breakdown` to split the agreed design into vertical slices.
