# Custom Skills

[English](#english) | [简体中文](#简体中文)

---

<a id="english"></a>

## English

A cohesive, minimal-overhead suite of engineering skills for coding agents (Claude Code, Codex, OpenCode, Oh My Pi), covering the full software lifecycle from Day-0 project bootstrapping, requirement clarification, and vertical slicing to implementation, UI craft, review, convergence, and architectural optimization.

### Skills Matrix

| Skill | Stage | Core Purpose | Invocation |
| :--- | :--- | :--- | :--- |
| [`project-init`](./project-init) | Bootstrap | Bootstrap or standardize an Agent-ready repo: clean `docs/` & single `out/` root, Git/`.github`, root lifecycle, XERJ, Quality Gate, and initial commit. | User-Initiated Only |
| [`clarify`](./clarify) | Alignment | Clarify ambiguous requirements or trade-offs via frontier decision rounds with recommended answers. | Auto / On Demand |
| [`breakdown`](./breakdown) | Planning | Break a large feature or wide refactor in one step into dependency-ordered vertical slices (`docs/tasks/` or GitHub Issues). | User-Initiated Only |
| [`impl`](./impl) | Execution | Implement features, slices, GitHub Issues, or fixes with seam tests, mandatory AC check-off, and adaptive review gates. | Auto / On Demand |
| [`diagnose`](./diagnose) | Debugging | Diagnose hard, flaky, or performance bugs with unknown root causes via a fast headless reproduction loop. | Auto / On Demand |
| [`ui-craft`](./ui-craft) | Frontend / UI | Design, build, polish, or audit UI surfaces with mode-aware aesthetics, complete state matrices, and a11y floor. | Auto / On Demand |
| [`code-review`](./code-review) | Macro Review | Fast two-axis parallel review (Spec/AC conformance + Architecture & repo standards) over pre-packaged diffs. | High-Scope Auto / On Demand |
| [`post-impl`](./post-impl) | Micro Convergence | Final 7-dimensional cleanup audit eliminating dead code, write-only state, duplicate rules, and LSP `hint/info` drift. | Post-Task Gate |
| [`arch-optimize`](./arch-optimize) | Architecture | Audit codebase hotspots to surface shallow modules and leaky seams, then plan module-deepening refactors. | User-Initiated Only |
| [`project-quality`](./project-quality) | Quality Infra | Establish, audit, or maintain a cross-stack quality system with compiler/LSP diagnostics and a unified Quality Gate. | User-Initiated Only |
| [`no-echo`](./no-echo) | Artifact Hygiene | Strip rejected drafts, reversals, and conversational corrections from code, docs, commits, PRs, and handoffs. | Auto / On Demand |

### End-to-End Workflow

1. **Day-0 Bootstrap**: Invoke [`project-init`](./project-init) to scaffold a clean repository (`docs/` Markdown consolidation, single `out/` build/artifact root, `.github/` CI/Release + release-note templates, root-only service lifecycle, XERJ indexing, chained [`project-quality`](./project-quality) gate, and verified initial commit).
2. **Align & Decompose**: Clear requests go straight to [`impl`](./impl). Ambiguous trade-offs trigger [`clarify`](./clarify); multi-session features use [`breakdown`](./breakdown) to emit vertical slices directly to `docs/tasks/<slug>.md` or GitHub Issues.
3. **Execute & Verify**: [`impl`](./impl) enforces behavioral tests at public seams, pairs with [`ui-craft`](./ui-craft) for UI surfaces or [`diagnose`](./diagnose) for elusive bugs, and **checks off `- [x]` Acceptance Criteria** in `docs/tasks/` or GitHub Issues (keeping uncommitted issues open until commit/push).
4. **Scope-Driven Quality Gates** (judged by semantic blast radius, never file count):
   - **Contained scope** (localized fixes, UI tweaks, single-seam features, or mechanical wiring without contract/concurrency/state-machine changes) → [`post-impl`](./post-impl).
   - **High semantic blast radius** (shared API/IPC/DB contract changes, state-machine/concurrency/auth/recovery rewrites even in one file, or non-trivial cross-subsystem coupling) → [`code-review`](./code-review) (pre-packaged 2-subagent fast review) followed by [`post-impl`](./post-impl).
5. **Periodic Maintenance**: Run [`project-quality`](./project-quality) on existing repos to audit/upgrade compiler + LSP CLI gates, and [`arch-optimize`](./arch-optimize) to deepen high-churn shallow modules.

### Repository Layout

```text
custom-skills/
├── project-init/            # Day-0 standard Agent repo bootstrap, single out/ root & root lifecycle
├── clarify/                 # Frontier decision rounds & domain term alignment
├── breakdown/               # One-step vertical slice decomposition (docs/tasks/ or GitHub Issues)
├── impl/                    # Adaptive implementation, seam tests & mandatory AC check-off
├── diagnose/                # Headless reproduction loop & falsifiable bug diagnosis
├── ui-craft/                # Mode-aware UI design, component state floor & headless audit
├── code-review/             # Parallel Spec/AC + Standards/Smells review
├── post-impl/               # 7-dimensional post-task convergence & LSP hint check
├── arch-optimize/           # Deep-module hotspot survey & non-intrusive refactoring plan
├── project-quality/         # Cross-stack unified Quality Gate & LSP CLI parity profiles
└── no-echo/                 # Accepted-state artifact & prose hygiene (zero conversational residue)
```

---

<a id="简体中文"></a>

## 简体中文

面向 Coding Agents（Claude Code、Codex、OpenCode、Oh My Pi 等）的自包含、低噪音工程研发流技能套件，闭环覆盖“Day-0 标准工程初始化 → 需求澄清 → 一步式垂直拆分 → 编码实现与 AC 核销 → UI 精工 → 分级审查与微观收敛 → 架构深潜与质量门禁”。

### 技能清单

| 技能名称 | 阶段定位 | 核心职责 | 触发机制 |
| :--- | :--- | :--- | :--- |
| [`project-init`](./project-init) | 工程初始化 | 一键搭建或标准化 Agent 工程底座：`docs/` 文档归口、单一 `out/` 产物目录、Git/`.github`、根级统一启停、XERJ 索引、质量门禁与基线提交。 | 仅限用户显式调用 |
| [`clarify`](./clarify) | 需求对齐 | 按依赖前沿分轮追问模糊需求与架构权衡，每题附带推荐解。 | 自动匹配 / 按需调用 |
| [`breakdown`](./breakdown) | 任务拆解 | 将大型功能或广域重构一步拆解为带依赖边与验收项的垂直切片（落盘 `docs/tasks/` 或 GitHub Issues）。 | 仅限用户显式调用 |
| [`impl`](./impl) | 编码执行 | 端到端实现功能、切片、Issue 或缺陷修复，内置公共切面测试、强制 AC 打勾核销与分级审查分流。 | 自动匹配 / 按需调用 |
| [`diagnose`](./diagnose) | 疑难排障 | 针对根因未知的复杂/偶发缺陷与性能退化，构建后台最小变红复现环并逐项证伪。 | 自动匹配 / 按需调用 |
| [`ui-craft`](./ui-craft) | 界面设计 | 区分工具态（高密度桌面审美）与展示态，强制交互全状态矩阵、封装原语与无头非侵入验证。 | 自动匹配 / 按需调用 |
| [`code-review`](./code-review) | 宏观审查 | 基于预打包上下文的极速双子代理并行审查（Spec/AC 行为正确性 + 架构边界与规范）。 | 广域变更自动 / 按需 |
| [`post-impl`](./post-impl) | 微观收敛 | 任务收尾 7 维收敛清扫，消除死代码、只写状态、重复业务规则与本地 LSP `hint/info` 异味。 | 任务收尾必跑门禁 |
| [`arch-optimize`](./arch-optimize) | 架构优化 | 扫描代码库高频变更热点，识别浅模块透传与切面泄漏，输出非侵入式模块加深重构方案。 | 仅限用户显式调用 |
| [`project-quality`](./project-quality) | 质量基建 | 建立、审计并维护跨语言统一质量门禁（Quality Gate）与编译器/LSP CLI 诊断对齐体系。 | 仅限用户显式调用 |
| [`no-echo`](./no-echo) | 资产净化 | 清除代码命名、注释、文档、提交、PR 与交接记录中的被否决方案与对话纠偏回声。 | 自动匹配 / 按需调用 |

### 核心研发闭环

1. **Day-0 工程初始化**：新开项目或规范化早期仓库时手动调用 [`project-init`](./project-init)，一次性配齐 `docs/` 文档收拢、单一 `out/` 编译/运行产物目录、`.github/`（`ci.yml` + `release.yml` + `release-note/template.md`）、根级统一服务启停、XERJ 索引与 `AGENTS.md`，并自动串联 [`project-quality`](./project-quality) 跑通首轮门禁后完成首次基线提交。
2. **对齐与拆解**：清晰需求直入 [`impl`](./impl) 开工；存在歧义先经 [`clarify`](./clarify) 决策收敛；跨模块大特性调用 [`breakdown`](./breakdown) 一步生成垂直切片（存放于 `docs/tasks/<slug>.md` 或创建 GitHub Issues，绝不在根目录生成冗余隐藏目录）。
3. **实现与验收核销**：[`impl`](./impl) 在公共接口切面编写行为测试，涉及界面时联动 [`ui-craft`](./ui-craft)，遇到未知根因疑难杂症切换 [`diagnose`](./diagnose)；收尾前**逐条核对并勾选 `- [x]` Acceptance Criteria**（GitHub Issue 在本地未提交状态下先完成勾选与评论留证，待提交推送时再行关单）。
4. **按影响域分流的审查门禁**（依据语义影响半径而非改动文件数）：
   - **收敛影响域**（局部修复、UI 微调、单切面功能或纯机械接线，未触碰共享契约/状态机/并发/安全模型）→ 直接执行 [`post-impl`](./post-impl)。
   - **高语义爆炸半径**（修改公共 API/IPC/DB 契约、重写复杂状态机/并发锁/缓存失效/鉴权恢复逻辑——哪怕仅在单文件内，或产生跨子系统非平凡耦合）→ 先执行预打包极速双轨 [`code-review`](./code-review)，修复问题后再执行 [`post-impl`](./post-impl)。
5. **基建与架构演进**：对存量仓库单独审计/升级编译器与本地 LSP Gate 时手动调用 [`project-quality`](./project-quality)；阶段性手动调用 [`arch-optimize`](./arch-optimize) 对高频热点做深模块重构评估。
