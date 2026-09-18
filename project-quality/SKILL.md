---
name: project-quality
description: "USER-INITIATED ONLY. NEVER invoke, activate, or apply this skill unless the user explicitly names project-quality and requests its use for the current task, or manually invokes it through the client. Generic quality/setup requests, inferred intent, and another skill or agent are NOT authorization. Once explicitly requested, establish, audit, complete, or maintain a cross-stack quality system with compiler/IDE diagnostics, a unified Quality Gate, and Git/CI integration. Does not replace implementation, code review, or test design."
disable-model-invocation: true
---

# Project Quality

## Invocation policy

**Only the user may initiate this skill.** This rule applies to OMP, Claude Code, Gemini CLI, Codex, and clients that ignore invocation metadata.

- Start only after the user manually selects/invokes this skill, or explicitly asks to use `project-quality` for the current task. Use the client's supported invocation syntax; naming it in an explicit natural-language request also expresses permission to use it.
- Never self-select, activate, load additional references, or execute this workflow merely because quality work seems useful. A generic request to initialize a project, improve quality, fix warnings, implement code, or run checks does not authorize this skill. Neither an agent's plan nor a reference from another skill, initializer, repository instruction, or subagent substitutes for the user's explicit request.
- Merely mentioning, comparing, editing, or reviewing this skill is not a request to execute its project-quality workflow. If its body is loaded without the required authorization, stop this workflow and continue the user's actual task. Do not prompt for permission just to expand that task.
- Explicit authorization remains valid while completing that same task; do not ask again on every step or continuation. A later unrelated task requires its own explicit invocation. Respect cancellation and any narrower scope such as audit-only.
- Running a project's established Quality Gate under its existing agent instructions is ordinary project work and does not invoke this skill. Keep that self-check behavior active without automatically reopening quality-system setup.

`disable-model-invocation: true` supports Claude Code and OMP's model-discovery filtering. Codex uses the accompanying `agents/openai.yaml` policy. For clients without an equivalent supported control, including the inspected Gemini CLI version, the description and this policy provide the instruction-level fallback; they are not a client-enforced access barrier.

Establish a capability-based quality contract and one executable project entrypoint. Aim for maximum useful coverage with minimum redundant tooling.

**Build success != clean diagnostics.** Account for compiler, language-server, IDE, and official analyzer diagnostics separately from producing a build artifact.

## Workflow

### 1. Inspect before changing

Read repository instructions and existing contributor/agent quality documentation. Identify languages, frameworks, build systems, package managers, pinned SDK/tool versions, modules, generated sources, supported operating systems, and CI providers. Inspect actual scripts, task graphs, rule severities, exclusions, baselines, hooks, and CI invocations; a dependency's presence is not evidence that its checks run.

Choose the mode from the request and repository:

- **Audit only:** perform discovery, capability mapping, safe existing checks, and reporting. Do not install tools or edit source, configuration, hooks, or project documentation; present proposed changes in the report. Inspect commands for mutations before executing them.
- **New project:** establish the applicable contract with a small coherent toolchain, gate, Git integration, and CI where the hosting context is known.
- **Existing project:** capture current findings as evidence first (not as an accepted suppression baseline), then reuse and strengthen working infrastructure. Check duplicate rules, conflicting formatters, stale configuration, skipped files/tasks, and local/CI drift before proposing replacement.

After explicit invocation, carry out the scoped setup, repair, or upgrade request. A user's invocation with no additional arguments means audit and fill justified infrastructure gaps. Preserve user choices and avoid unrelated source changes or tool migrations. If the repository is empty and its stack cannot be inferred, ask for the intended stack before choosing dependencies; do not scaffold a business application.

### 2. Load the contract and relevant profiles

Always read [quality-contract.md](references/quality-contract.md). Read [git-quality.md](references/git-quality.md) when auditing or configuring Git/CI integration. Load only matching language profiles and framework overlays:

| Repository signals | Reference |
| --- | --- |
| JavaScript/TypeScript manifests and source | [javascript-typescript.md](references/javascript-typescript.md) |
| React, including Next.js; add to JS/TS | [react.md](references/react.md) |
| Go modules/workspaces | [go.md](references/go.md) |
| Cargo packages/workspaces | [rust.md](references/rust.md) |
| JVM Kotlin/Java; Gradle or Maven | [kotlin-java.md](references/kotlin-java.md) |
| Android Gradle plugin; add to JVM | [android.md](references/android.md) |
| Python source/pyproject | [python.md](references/python.md) |
| .NET solutions/projects | [dotnet.md](references/dotnet.md) |
| C/C++, CMake or native build files | [cpp.md](references/cpp.md) |

Compose profiles per module in mixed repositories. A framework overlay adds capabilities; it does not establish another competing gate. For other stacks, research the installed version's official diagnostics and map them to the same contract. A new profile should contain detection details, capability choices, CLI/IDE gaps, version caveats, and official sources; add one routing row here.

### 3. Map capabilities before choosing tools

Build the coverage matrix defined in the contract. Distinguish missing coverage from disabled rules, inadequate scope, and an existing tool configured too weakly. Name the additional capability and maintenance cost of every proposed tool.

Prefer, in order: existing effective checks, compiler/build-system capabilities, official framework/analyzer support, then a mature maintained ecosystem tool. **Whenever selecting or recommending a quality library/tool/plugin version, you MUST use Web Search to establish the latest stable release compatible with the project's actual toolchain.** Follow the [mandatory version-selection procedure](references/quality-contract.md#mandatory-web-search-for-version-selection), including primary-source verification and recorded evidence. Model memory, profile examples, and familiarity with an older release are not version-selection evidence. Profiles are starting points, not permanent installation lists. Verify flags and configuration against the selected release; do not fabricate lockfiles or invent support.

Assign one owner for each overlapping rule family/file scope. Multiple tools are justified only by distinct coverage or a documented migration. Avoid adding another runtime solely for hook or commit validation when the existing runtime has a maintainable solution.

### 4. Implement one Quality Gate

For audit-only requests, assess this design and propose any needed changes; do not implement them. The implementation and persistence instructions below apply to setup/repair/upgrade work.

Reuse the existing canonical command where possible, or introduce the smallest entrypoint native to the project (package script, build task, Make/Task target, or repository script). Do not invent native commands such as `go quality` or `cargo quality` without implementing the wrapper/alias.

The full default invocation covers applicable format checks, syntax/type/compiler diagnostics, lint/static analysis, tests, and build/configuration validation. Order cheap checks first unless generation or build dependencies require otherwise. Share task definitions with hooks and CI; avoid maintaining parallel command lists.

Use check-only behavior, pinned tooling, explicit failure propagation, and declared module/target scope as required by the contract. A fast/affected mode can supplement the full gate but must be visibly named and must not become its default. The root interface covers all in-scope modules and exposes explicit CI targets where needed; document the pre-commit and CI responsibilities before wiring them.

Integrate commit validation and hooks using the Git reference. Git event inputs (a proposed message or CI commit range) enter the same quality interface through documented arguments/subtasks; a pre-commit source check cannot validate a message that does not exist yet.

### 5. Verify and persist the project contract

In audit-only mode, record outcomes of safe existing checks and proceed to handoff; do not repair failures or persist files.

Run changed checks, exercise their failure behavior, and run the full gate. Fix infrastructure failures and problems introduced by this task. Classify pre-existing findings using the contract's debt policy; do not mass-refactor unrelated code. After the last fix, rerun the affected checks and full gate before declaring success.

Update the existing project quality document, or use `docs/agents/quality.md` to match the Matt-style project configuration convention. Record the actual command, prerequisites, capability matrix, diagnostic limits, baseline policy, and verification evidence there. Keep executable task definitions authoritative for command composition; the document explains scope and decisions.

Add a concise link and the coding-completion rule below to the project's existing agent instructions, updating in place. Respect its chosen instruction-file layout, including `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`; do not create a parallel instruction file when one already serves the project. If none exists, create a small `AGENTS.md` unless repository conventions specify another location. Initializers may use this skill only when the user explicitly requested `project-quality` for that setup task. They can reference the resulting project contract instead of copying its rules. Persist the Quality Gate command, not an instruction to auto-invoke this skill.

### 6. Handoff

Report the stack, changes, retained tools and any justified replacements, coverage/gaps, exact commands run and outcomes, hook/CI verification state, and the **single command future agents should run**. Distinguish infrastructure configured from gate passing and remote enforcement verified. Missing SDKs, unavailable services, historical failures, or IDE-only gaps are explicit limitations, never a clean pass.

## Agent coding-completion rule

Persist this behavior using the project's concrete command and contract path:

> After modifying code, run checks appropriate to the change before marking the task complete. Before committing, run the full default Quality Gate on the final tree: Implement → Quality Gate → Fix → Quality Gate → Commit. Fix newly introduced diagnostics, including warnings and deprecated API use. Follow the documented historical-debt policy for verified pre-existing findings. If this required gate fails or is unavailable, report the blocker and do not commit or claim completion. Run the commit-message validator with the actual proposed message when it becomes available. Report any separately declared CI-only checks as pending until verified; they remain required for the project's merge/release policy.

Never disable rules, add arbitrary ignores/suppressions, delete tests, or use `--no-verify` to make a failing change pass. Genuine false positives and compatibility constraints require the narrow, documented exception process in the contract, not an ad hoc bypass. This skill does not authorize creating commits by itself.

## Boundaries and completion

Classify findings as **quality infrastructure**, **current-change code**, **historical debt**, or **out of scope**. Fix the first two within the authorized task. Report the others with evidence and a next action; leave business features, broad refactors, comprehensive test design, and code review to their own workflows.

Setup is complete when the applicable contract is recorded, the unified entrypoint actually enforces it, verification passes, Git/CI integration has an honest status, and future agents can discover the command. An audit is complete with an evidence-backed gap report; it need not alter the repository. An incomplete setup can be handed off with blockers, but must not be described as a completed quality system.
