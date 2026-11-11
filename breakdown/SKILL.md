---
name: breakdown
description: "USER-INITIATED ONLY. Break a large feature or wide refactor in one step into dependency-ordered vertical slices with acceptance criteria, saved under docs/tasks/ or GitHub Issues."
disable-model-invocation: true
---

# Breakdown

One-step decomposition of a large feature or cross-cutting refactor directly into actionable, dependency-ordered slices with verifiable Acceptance Criteria—without intermediate spec-to-ticket ceremony.

## 1. Slicing Rules

1. **Explore seams first**: Inspect the codebase to understand existing modules, public interfaces (seams), schemas, and test patterns. Note any prerequisite prefactoring ("make the change easy, then make the easy change").
2. **Vertical tracer-bullet slices (Default)**:
   - Each slice cuts a narrow, end-to-end path across all needed layers (data/schema → domain logic → API/IPC → UI → seam tests). Never split horizontally by layer ("all DB tables", then "all APIs", then "all UI").
   - Every completed slice must leave the build green and be independently verifiable.
   - Size each slice to fit comfortably within a single focused agent session.
3. **Expand–Migrate–Contract (Exception for wide mechanical refactors)**:
   - When renaming/retyping a shared contract breaks dozens of call sites simultaneously, sequence as: (1) **Expand** (introduce new alongside old), (2) **Migrate** (batched by package/module, blocked by Expand), (3) **Contract** (delete old path once callers reach zero, blocked by all Migrate slices).
4. **Explicit dependency graph**: Every slice declares `Blocked by` (`None` if ready immediately, or exact upstream slice IDs). Keep edges minimal so independent slices can run in parallel.
5. **Concrete Acceptance Criteria**: Every slice carries `- [ ]` checkboxes stating observable behavior, edge cases, and verification expectations. Avoid hardcoding volatile line numbers or large code dumps.

## 2. Interactive Confirmation

Before writing any files or creating issues, present a compact numbered blueprint in chat:
- **Slice `<NN>` — `<Title>`** (`Blocked by: None | <IDs>`)
  - **Delivers**: End-to-end user/caller capability
  - **Acceptance Criteria**: Key `- [ ]` items
- Ask the user to confirm: (1) slice granularity & `Blocked by` edges, and (2) target destination (**Local `docs/` file** vs. **GitHub Issues**), defaulting to existing repo convention if obvious.

## 3. Publishing Targets

Once approved:

- **Local Markdown (`docs/tasks/<feature-slug>.md`)**:
  - Never create hidden dot-folders (`.xxx`) at the repository root. Place task files under `docs/tasks/<feature-slug>.md` (or an existing `docs/` planning subdirectory used by the repo).
  - Include a brief `# Overview & Context` header (problem, core architectural/seam decisions, out-of-scope boundaries) followed by ordered `## Slice <NN>: <Title>` sections containing `Status: pending`, `Blocked by`, `What to build`, and `- [ ]` Acceptance Criteria checkboxes.
- **GitHub Issues (`gh issue create`)**:
  - Verify `gh repo view` works. Publish slices in dependency order so downstream issues reference real `#<number>` blockers.
  - Each issue body includes: `## Context & Scope`, `## What to Build`, `## Blocked By` (`None` or `#<id>`), and `## Acceptance Criteria` (`- [ ] ...`).
