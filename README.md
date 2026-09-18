# Custom Skills

[English](#english) | [简体中文](#简体中文)

---

<a id="english"></a>

## English

A curated collection of production-grade agent skills tailored for coding agents (such as Claude Code, Codex, and Oh My Pi), managed seamlessly via [Skills Manager](https://github.com/xingkongliang/skills-manager).

### Skills Matrix

| Skill | Category | Core Purpose | Invocation |
| :--- | :--- | :--- | :--- |
| [`project-quality`](./project-quality) | Quality Assurance & Tooling | Establishes, audits, and maintains a cross-stack quality system with a single unified Quality Gate. | User-Initiated Only |
| [`no-negative-echo`](./no-negative-echo) | Artifact Hygiene & Communication | Prevents rejected drafts, reversals, and conversational corrections from leaking into durable project artifacts. | Automatic / On Demand |

---

### In-Depth Skill Profiles

#### 1. [`project-quality`](./project-quality)
*Cross-Stack Engineering Quality System & Unified Quality Gate*

Designed to enforce consistent code health and prevent local/CI drift across diverse tech stacks without introducing bloat.

- **Unified Quality Gate**: Establishes a single, canonical entrypoint (e.g. `pnpm quality`, `make quality`, `cargo check` pipelines) that chains formatting, syntax/compiler diagnostics, linters, tests, and build validation in an efficient fail-fast order.
- **Multi-Stack Profiles**: Includes ready-to-use profiles covering JavaScript/TypeScript, React/Next.js, Go, Rust, Kotlin/Java, Android, Python, .NET, and C/C++.
- **Compiler & IDE Diagnostic Parity**: Adheres to the principle that *build success != clean diagnostics*, mapping official compiler and language-server checks directly to the project contract.
- **Git & CI Integration**: Wires pre-commit hooks, commit-message validation, and CI checks to share the same underlying task definitions.
- **User-Initiated Only (`disable-model-invocation: true`)**: Strict invocation policy preventing autonomous or unsolicited system takeovers; activates solely when explicitly requested by the user.
- **Pragmatic Debt Management**: Distinguishes between infrastructure gaps, current changeset issues, and historical debt—avoiding uncontrolled, out-of-scope refactoring or sweeping suppressions.

#### 2. [`no-negative-echo`](./no-negative-echo)
*Artifact Hygiene: Eradicating Conversational Residue from Durable History*

Ensures that final project artifacts reflect what the system **is**, rather than the messy trail of mistakes, rejected alternatives, or mid-turn corrections encountered during development.

- **Accepted-State Wording**: Eliminates conversational residue (e.g., `feature_without_service`, `// don't use old approach`) from commit subjects, PR descriptions, file/symbol names, test names, release notes, and agent handoff documents.
- **Dual Operating Modes**:
  - **Generation Mode**: Formulates new names, comments, and commit messages directly using positive, accepted-state domain vocabulary.
  - **Review Mode**: Inspects prepared git diffs or documentation as a final hygiene pass to pinpoint and rewrite unintentional negative echoes.
- **Semantic & Invariant Preservation**: Distinguishes incidental conversational residue from genuine domain prohibitions (e.g., security constraints, ADR historical context, or exclusive ownership rules), ensuring architectural guarantees remain strict and unambiguous.
- **Deterministic Scanning**: Ships with a lightweight helper script (`scripts/scan_echo.py`) for literal regex-based sweeps of forbidden phrases.

---

### Installation & Usage

#### Via Skills Manager (Recommended)

Install skills individually using their Git subpaths:

```bash
# Install project-quality
skills-manager-cli skills install https://github.com/ygq-future/custom-skills/tree/main/project-quality

# Install no-negative-echo
skills-manager-cli skills install https://github.com/ygq-future/custom-skills/tree/main/no-negative-echo
```

#### Manual Installation

Clone the repository and copy the target skill folder into your agent's configured skills directory:

```bash
git clone https://github.com/ygq-future/custom-skills.git
cp -r custom-skills/project-quality ~/.local/share/skills/  # Adjust path to your agent setup
cp -r custom-skills/no-negative-echo ~/.local/share/skills/
```

---

### Repository Layout

```text
custom-skills/
├── project-quality/             # Quality gate & tooling system skill
│   ├── SKILL.md                 # Core skill instructions & invocation policy
│   ├── agents/openai.yaml       # Client invocation config (Codex, etc.)
│   ├── assets/prettier/         # Shared quality configurations
│   └── references/              # Language and ecosystem quality profiles
└── no-negative-echo/            # Artifact hygiene & anti-residue skill
    ├── SKILL.md                 # Core instructions & rewriting principles
    ├── references/examples.md   # Concrete before/after rewrite cases
    ├── scripts/scan_echo.py     # Deterministic literal residue scanner
    └── evals/evals.json         # Evaluation scenarios & benchmarks
```

---

<a id="简体中文"></a>

## 简体中文

本仓库收集并维护面向 Coding Agents（如 Claude Code、Codex、Oh My Pi 等）的高质量定制化 Agent 技能（Skills），支持通过 [Skills Manager](https://github.com/xingkongliang/skills-manager) 统一管理与按需分发。

### 技能清单

| 技能名称 | 领域分类 | 核心功能定位 | 触发机制 |
| :--- | :--- | :--- | :--- |
| [`project-quality`](./project-quality) | 工程质量与研发基建 | 建立、审计并维护跨技术栈的工程质量体系与统一质量门禁（Quality Gate）。 | 仅限用户显式调用 |
| [`no-negative-echo`](./no-negative-echo) | 交付物规范与信息净化 | 彻底清除沟通过程中的否定修正、反悔草案与对话残留，保持项目资产纯净。 | 自动匹配 / 按需触发 |

---

### 技能深度解析

#### 1. [`project-quality`](./project-quality)
*跨技术栈工程质量系统与统一质量门禁*

针对多语言多技术栈工程，建立标准统一、轻量且具备可执行性的工程质量保障体系，杜绝本地环境与 CI 规则漂移。

- **统一质量门禁 (Unified Quality Gate)**：提炼单一规范入口（如 `pnpm quality`、`make quality`、`cargo check` 组合等），将格式规范检查、语法及编译器诊断、代码分析（Linter）、单元测试与构建校验按成本从低到高串联执行，遇错即停。
- **多语言生态全覆盖 (Multi-Stack Profiles)**：深度支持 JavaScript/TypeScript、React/Next.js、Go、Rust、Kotlin/Java、Android、Python、.NET 以及 C/C++ 等主流技术栈的官方推荐诊断套件。
- **编译器与 IDE 诊断对齐**：坚持“编译通过并不等于诊断通过”，全面纳管编译器警告、语言服务器（LSP）与官方静态分析器诊断信息。
- **Git 与 CI 闭环集成**：统一配置 pre-commit 钩子、commit-message 提交规范及 CI 工作流，共用底层任务定义，避免维护多套重复脚本。
- **严格的用户主动触发策略 (`disable-model-invocation: true`)**：防止 Agent 在常规对话或日常编码中擅自接管或重构工程配置；唯有在用户显式要求使用 `project-quality` 时方可执行。
- **清晰的技术债务边界**：严格区分“质量基础设施缺失”、“当前变更代码问题”与“既有历史债务”，聚焦于当前任务，禁止擅自发起大范围无关重构或随意滥用 ignore 抑制警告。

#### 2. [`no-negative-echo`](./no-negative-echo)
*交付物语言净化：消除项目持久化资产中的“过程残留与否定回声”*

确保提交信息、代码注释与文档始终表述“当前系统是什么”，而不是记录开发过程中经历的误解、被否决的方案或来回纠偏的对话痕迹。

- **基于采纳事实构建语言 (Accepted-State Wording)**：全面清除进入持久层（Git Commit、PR 描述、代码注释、文件名、测试用例名称、Release Notes、交接文档）的沟通过程残留（如避免使用 `feature_no_service`、`// 改用此方法因为之前方案被否定`）。
- **双工作模式支持**：
  - **生成模式 (Generation Mode)**：在撰写新的提交、注释与文档时，直接采用积极正向、描述最终系统的领域词汇。
  - **审查模式 (Review Mode)**：作为代码提交或交付交接前的最后一道检查防线，审查准备提交的 diff，定位并重写隐藏的否定回声。
- **语义完整与架构约束保留**：严格区分“偶然的沟通残留”与“真实的领域排他性约束”（如安全禁止规则、架构决策记录 ADR、防回归测试）。在净化表达的同时，确保系统的架构不变量与所有权边界不被弱化。
- **轻量确定性扫描工具**：内置 Python 辅助脚本（`scripts/scan_echo.py`），支持在代码仓库中对指定的否定短语进行字面规则扫描。

---

### 安装与使用

#### 推荐方式：通过 Skills Manager 安装

可以直接使用各 Skill 对应的 Git 子路径进行精准安装：

```bash
# 安装 project-quality 技能
skills-manager-cli skills install https://github.com/ygq-future/custom-skills/tree/main/project-quality

# 安装 no-negative-echo 技能
skills-manager-cli skills install https://github.com/ygq-future/custom-skills/tree/main/no-negative-echo
```

#### 手动安装

克隆仓库后，将对应的技能目录拷贝至您所使用的 Agent 技能存放目录中：

```bash
git clone https://github.com/ygq-future/custom-skills.git
cp -r custom-skills/project-quality ~/.local/share/skills/  # 请根据实际 Agent 配置路径调整
cp -r custom-skills/no-negative-echo ~/.local/share/skills/
```

---

### 仓库目录结构

```text
custom-skills/
├── project-quality/             # 工程质量保障与统一门禁技能
│   ├── SKILL.md                 # 核心说明与严格触发规范
│   ├── agents/openai.yaml       # 针对 Codex 等客户端的调用策略配置
│   ├── assets/prettier/         # 共享代码格式化规则模板
│   └── references/              # 各技术栈语言深度配置规范与参考指南
└── no-negative-echo/            # 交付物语言净化与去过程残留技能
    ├── SKILL.md                 # 核心指导原则与正向表达重构指南
    ├── references/examples.md   # 典型场景重写正反例对照表
    ├── scripts/scan_echo.py     # 违禁残留词汇确定性检查脚本
    └── evals/evals.json         # 技能效果评估用例集
```
