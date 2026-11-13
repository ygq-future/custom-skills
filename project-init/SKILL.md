---
name: project-init
description: "USER-INITIATED ONLY. Bootstrap or standardize an Agent-ready repository: clean topology, single out/ artifact root, Git/.github, root lifecycle, XERJ, Quality Gate, and initial commit."
disable-model-invocation: true
---

# Project Init

Bootstrap a brand-new repository—or standardize an early/unstructured repository—into a clean, self-verifying Agent engineering workspace.

## Invocation Policy

- **Only the user may initiate this skill** (`/project-init` or an explicit request to initialize/standardize a repository with `project-init`). Never self-select during feature work, bug fixes, or routine quality runs.
- An explicit invocation of `project-init` **also authorizes chaining the sibling `project-quality` skill** for Step 5 within the same setup task without prompting twice.
- **Mode selection**:
  - **Greenfield Mode** (no `.git` or unborn `HEAD` with zero commits): Executes Steps 1–7 end-to-end and creates **one** initial baseline `git commit` **only after** the full Quality Gate passes (`exit 0`). Never `git push` unless explicitly instructed.
  - **Standardize Mode** (repository already has commits): Upgrades layout, `out/` redirection, `.github/`, root lifecycle, XERJ, and Quality Gate non-destructively, verifies the gate, and **leaves all changes uncommitted** for user review.

## Bootstrap Pipeline

Always read [templates-and-conventions.md](references/templates-and-conventions.md) before generating configs, scripts, or workflows.

### 1. Inspect & Confirm Blueprint
- Inspect directory contents, installed toolchains, and existing manifests.
- If the directory is empty or stack/topology choices are ambiguous, ask in **one brief round** with recommended defaults: (a) tech stack & package manager, (b) single-project vs. multi-project (`apps/` + `packages/`), and (c) optional `LICENSE` (omit `LICENSE` unless specified; create `.env.example` only if runtime env config exists).
- When installing third-party dependencies or quality tools, verify latest stable compatible versions via Web Search per `project-quality` rules—never guess versions from memory.

### 2. Enforce Clean Topology, `docs/` Consolidation & Single `out/` Root
- **Root Markdown Whitelist**: Only `README.md` (plus explicit locale variants like `README_CN.md`) and `AGENTS.md` belong at the repository root. Place **all** other Markdown docs (`architecture.md`, `quality.md`, `adr/`, `tasks/`, `guides/`) strictly inside `docs/`. Never create hidden root planning folders (`.tasks/`, `.plan/`, `.notes/`).
- **Single Build & Runtime Output Directory (`out/`)**:
  - **FORBID** root or per-package output sprawl (`dist/`, `build/`, `target/`, `debug/`, `release/`, `bin/`, `coverage/`).
  - Route **every** build artifact, compiler cache, binary, test report, PID lock, and background log into gitignored subdirectories under root `out/` (`out/dist/`, `out/bin/`, `out/target/`, `out/build/`, `out/coverage/`, `out/run/`, `out/logs/`) using each toolchain's native config (see reference).
- **Hollow Skeleton & Smoke Test Only (Zero Business Features)**:
  - **Single-project**: Use minimal idiomatic stack layout (`src/`, or `cmd/` + `internal/` for Go).
  - **Multi-project**: Group targets under `apps/<service>` and shared contracts/SDKs under `packages/<pkg>` (or workspace `crates/` / `internal/`).
  - Scaffold **only** a hollow framework stub (e.g., version/metadata export or minimal health/no-op entrypoint) **plus one real smoke unit test** so the initial Quality Gate runs genuine tests, and define one **Application Version SSOT**. **Do NOT implement product business logic or pending task specs (`docs/tasks/` or Issues) during initialization**—keep any existing task items untouched as `pending`.

### 3. Initialize Git Baseline & `.github/` Governance
- Run `git init -b main` if `.git/` is missing.
- Write `.gitattributes` (`* text=auto eol=lf`; `.bat`/`.cmd`/`.ps1` `eol=crlf`), `.editorconfig`, and `.gitignore` (ignoring `/out/`, dependency dirs, `.env*` with `!.env.example`, and OS/editor temporaries).
- Scaffold `.github/` (never use `&` or shell metacharacters in workflow filenames):
  - `.github/workflows/ci.yml` (`permissions: contents: read`): Runs on `pull_request` and `push` to `main`; sets up pinned toolchains and invokes the **single root `quality` command**.
  - `.github/workflows/release.yml` (`permissions: contents: write`): Runs on `v*.*.*` tags; enforces tag-to-SSOT version parity + root `quality` gate, reads `.github/release-note/`, and packages artifacts from `out/` (defaulting to a safe `draft: true` release skeleton until publishing targets are finalized).
  - `.github/release-note/template.md`: Standard release-note template (`Highlights`, `Breaking Changes`, `Features`, `Fixes`, `Upgrade Notes`).

### 4. Wire Root-Only Entrypoints (Zero Foreign Runtimes)
- **Zero-Foreign-Runtime Rule (HARD GATE)**: **NEVER introduce an extra language or runtime** (e.g., Python `.py` or `pre-commit` framework in a Go/Rust/TS repo; Node `package.json`/`husky` in a pure Go/Rust/Python repo) just to write build, quality, lifecycle, or Git-hook scripts—doing so pollutes a single-stack repo into a polyglot repo requiring extra linters/typecheckers. Always use the stack's **own** toolchain (`package.json` / `.mjs` for JS/TS, `go run ./scripts/ctl` for Go, `.cargo/config.toml` alias / `cargo xtask` for Rust, `uv run` for Python, Gradle/dotnet tasks for JVM/.NET; in true polyglot repos, reuse one runtime already in the app stack). Keep Git hooks as 3-line POSIX `#!/bin/sh` shims delegating to the native root command.
- **Match Entrypoint Shape to Target Archetype** (never add subdirectory `.sh`/`.ps1`/`.bat` scripts):
  - **Libraries, Plugins (CGO/FFI/Wasm), SDKs & CLI Tools (Non-Daemon)**: Expose **only** `build`, `test`, and `quality`—**NEVER** invent `start`/`stop`/`restart`/`status` daemon controllers when there is no long-running service.
  - **Single Frontend / Node App**: Manage `dev`, `build`, `test`, and `quality` solely via root `package.json` `scripts`—create zero wrapper scripts.
  - **Long-Running Services & Multi-Project Repos**: Expose root `dev` / `start [--daemon] [--only <svc>]`, `stop`, `restart`, `status`, and `quality` using the stack's native runner. Record `{ pid, port, cmd, startedAt }` in `out/run/<svc>.json` and daemon logs in `out/logs/<svc>.log`; `stop` kills **only** verified project process trees and confirms port release (never global `killall`/`taskkill /IM`), obeying Non-Intrusive Verification.

### 5. Establish Unified Quality & LSP Gate (`project-quality`)
- Load and execute the sibling `project-quality` skill workflow to wire formatting checks, compilation/type-checking, **headless local LSP CLI diagnostics** (`warning`/`info`/`hint` nonzero exit), linting, smoke tests, build output verification into `out/`, version-parity validation, Git hooks, and `docs/quality.md` behind the root `quality` command.

### 6. XERJ Onboarding & Canonical Documentation
- **XERJ Auto-Onboarding (when `xerj` CLI exists on host)**:
  1. Ensure `http://localhost:9200` responds (if unreachable, start `xerj --insecure --disable-feedback` in background and wait until ready).
  2. Write `.xerjignore` (excluding `out/`, dependency folders, lockfiles, `*.svg`, `*.min.*`) and verify via `xerj autoindex . --walk-only`.
  3. Inspect `xerj autoindex map --offset 999` to choose a unique `<prefix>`, run `xerj autoindex . --prefix <prefix> --no-graph --code-analyzer code --yes` (`exit=0|3`), and record `XERJ prefix: "<prefix>"` in `AGENTS.md`.
  *(If `xerj` is not installed on the host, skip cleanly without `.xerjignore` and note `XERJ: skipped (CLI not installed)`.)*
- Author concise, high-density `AGENTS.md` (stack, root commands, `docs/` & `out/` invariants, Version SSOT, XERJ prefix, Quality Gate rule), `README.md`, `docs/architecture.md`, and `docs/tasks/.gitkeep` + `docs/adr/.gitkeep`.

### 7. Full Gate Verification & Baseline Commit
1. Run the root `quality` command end-to-end (plus `start --daemon` → `status` → `stop` smoke check for runnable daemon services, and XERJ `Post-Edit Sync` if files changed after Step 6).
2. Confirm `exit 0`, zero compiler/LSP warnings or hints, all build/log outputs confined strictly inside `out/`, and zero stray root `.md` or build folders (`git status --short` shows `out/` ignored).
3. **Greenfield Mode only (unborn `HEAD` + Gate `exit 0`)**: Stage tracked baseline files (including any `docs/` planning docs already prepared) and run `git commit -m "chore: bootstrap project skeleton and quality gate"`.
4. **Completion Boundary**: Report the baseline commit hash, root commands, XERJ prefix, and Quality Gate status, then **stop and yield to the user**—do not proceed into feature/task implementation unless the user explicitly requested continuing past initialization in the same turn.
