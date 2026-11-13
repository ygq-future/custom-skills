# Project Init Conventions & Starter Templates

Reference specifications for `project-init`. Adapt commands and paths to the actual resolved stack—never paste placeholder commands that fail execution.

---

## 1. Standard Repository Topology

```text
<project-root>/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                  # PR / main push -> runs root quality gate
│   │   └── release.yml             # v*.*.* tag -> version parity + quality + draft release from out/
│   └── release-note/
│       └── template.md             # Canonical release notes structure
├── docs/                           # ONLY home for project Markdown docs (besides root README.md & AGENTS.md)
│   ├── architecture.md             # Module boundaries, data flow, and core invariants
│   ├── quality.md                  # Quality contract, LSP Gate matrix & exemptions (managed by project-quality)
│   ├── adr/                        # Architecture Decision Records (.gitkeep or 0001-*.md)
│   └── tasks/                      # Vertical task slices (.gitkeep; consumed by breakdown & impl)
├── apps/                           # [Multi-project only] Runnable services/frontends (e.g. apps/web, apps/server)
├── packages/                       # [Multi-project only] Shared schemas, contracts, UI primitives, SDKs
├── scripts/                        # [When needed] Native-stack root runner (NEVER add a foreign scripting language)
├── out/                            # [GITIGNORED] SINGLE root for ALL build, cache, coverage, PID & log artifacts
│   ├── bin/                        # Compiled native executables (Go, C/C++, CLI binaries)
│   ├── dist/                       # Bundled web assets, packages, wheels, release archives
│   ├── target/                     # Rust Cargo target-dir
│   ├── build/                      # CMake / Gradle / TS intermediate compilation outputs
│   ├── coverage/                   # Unit/integration coverage reports
│   ├── run/                        # Managed service state (<service>.json: pid, port, startedAt)
│   └── logs/                       # Background daemon stdout/stderr logs (<service>.log)
├── .editorconfig                   # UTF-8, LF, indent & trailing-whitespace rules
├── .gitattributes                  # LF line-ending normalization across OSes
├── .gitignore                      # Ignores /out/, dependencies, secrets (.env*), IDE caches
├── .xerjignore                     # [When xerj installed] Excludes /out/, lockfiles, minified/SVG bloat
├── AGENTS.md                       # Authoritative Agent engineering contract
└── README.md                       # Human-facing quickstart, architecture pointer & root commands
```

---

## 2. Redirecting Stack Outputs Strictly into Root `out/`

Never leave default `dist/`, `build/`, `target/`, `bin/`, or `coverage/` folders at the repo root or nested inside `apps/*` / `packages/*`. Wire native tool configs to `<repo-root>/out/...`:

| Ecosystem | Native Redirection Configuration |
| :--- | :--- |
| **Vite / Vitest (Single App)** | `build.outDir: 'out/dist'`, `test.coverage.reportsDirectory: 'out/coverage'` in `vite.config.ts`. |
| **Vite / TS (Monorepo `apps/<name>`)** | `build.outDir: '../../out/dist/<name>'` (with `emptyOutDir: true`), `compilerOptions.outDir: "../../out/build/<name>"`, `tsBuildInfoFile: "../../out/build/<name>.tsbuildinfo"`. |
| **Next.js / Framework Locked Dir** | Where a framework requires an in-package cache dir during dev, export release/static bundles to `out/dist/<name>` and gitignore framework caches explicitly without exposing root clutter. |
| **Rust / Cargo & Tauri v2** | Create `.cargo/config.toml` at workspace root: `[build]\ntarget-dir = "out/target"`. In `tauri.conf.json`, set `build.frontendDist` to point into `out/dist/...` as appropriate. |
| **Go (`go.mod`)** | Compile binaries exclusively with `go build -o out/bin/<app>[.exe] ./cmd/<app>` and write coverage to `out/coverage/coverage.out` (`mkdir -p out/bin out/coverage` first). Never run bare `go build` that drops binaries in the root directory. |
| **Python (`uv` / `pytest`)** | `uv build --out-dir out/dist`; in `pyproject.toml`: `[tool.pytest.ini_options] cache_dir = "out/build/pytest_cache"` and `[tool.coverage.run] data_file = "out/coverage/.coverage"`, `html.directory = "out/coverage/html"`. |
| **C / C++ (`CMake`)** | Always pass `-B out/build` (`cmake -S . -B out/build -DCMAKE_RUNTIME_OUTPUT_DIRECTORY=out/bin`). |
| **JVM (`Gradle`)** | In `settings.gradle.kts` / root `build.gradle.kts`: `allprojects { layout.buildDirectory.set(rootProject.layout.projectDirectory.dir("out/build/${project.name}")) }`. |

---

## 3. Baseline Dotfiles

### `.gitattributes`
```gitattributes
* text=auto eol=lf
*.bat text eol=crlf
*.cmd text eol=crlf
*.ps1 text eol=crlf
*.png binary
*.jpg binary
*.webp binary
*.ico binary
*.woff2 binary
```

### `.editorconfig`
```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.{go,Makefile}]
indent_style = tab
indent_size = 4

[*.{py,rs,java,kt,cs,c,cpp,h,hpp}]
indent_size = 4

[*.{bat,cmd,ps1}]
end_of_line = crlf
```

### `.gitignore` Core Entries (append stack-specific caches)
```gitignore
# Unified build, cache, coverage, PID & daemon log root
/out/

# Dependencies
node_modules/
.venv/
vendor/

# Environment & secrets
.env
.env.*
!.env.example

# OS & editor noise
.DS_Store
Thumbs.db
*.swp
*.tmp
```

### `.xerjignore` (when `xerj` is available)
```gitignore
out/
node_modules/
.venv/
vendor/
*.min.js
*.min.css
*.map
*.svg
*.lock
package-lock.json
pnpm-lock.yaml
go.sum
```

---

## 4. Native-Stack Entrypoints & Lifecycle Contract (Zero Foreign Runtimes)

### Hard Rule: Zero Foreign Scripting Languages
**NEVER** introduce a second language/runtime solely to orchestrate builds, quality checks, packaging, or Git hooks—doing so turns a single-language repository into a polyglot repository and drags in an extra formatter/linter/typechecker stack (e.g., Python `.py` forcing Ruff + Basedpyright + Node onto a Go or Rust repo, or `package.json`/`husky` forcing Node onto a pure Go/Python repo).

| Repository Stack | Canonical Native Runner (Zero Extra Runtime) |
| :--- | :--- |
| **JS / TS / Frontend** | Root `package.json` `scripts` directly (add `scripts/ctl.mjs` using Node/Bun stdlib **only** for multi-process orchestration). |
| **Go / CGO** | Native Go command (`go run ./scripts/ctl <subcmd>` or `./cmd/devctl`) using Go stdlib (`os/exec`, `flag`)—cross-platform and checked by the repo's own `gofmt`/`go vet`/`gopls`. |
| **Rust** | `.cargo/config.toml` `[alias]` for simple repos, or native `cargo xtask` workspace binary crate when custom cross-platform scripting is required. |
| **Python** | `pyproject.toml` scripts / `uv run python scripts/ctl.py` inside the project's own `.venv`. |
| **JVM / .NET / C++** | Native build tool tasks (`./gradlew`, `dotnet`, `cmake --preset` / `ctest`), or an already-installed declarative runner (`Taskfile.yml` / `justfile`) without pulling in Python/Node. |
| **True Polyglot Repo** | Reuse **one** runtime already required by the application stack (e.g., Node `scripts/ctl.mjs` in a TS+Go repo)—never introduce a third language. |

- **Git Hooks**: Keep local hooks (`pre-commit`, `commit-msg`) as minimal POSIX `#!/bin/sh` shims (`exec <native-root-quality-cmd>`) configured via `git config core.hooksPath .githooks` (or the ecosystem's own hook tool **only** when that ecosystem is already primary). Never add Python `pre-commit` (`pre-commit.com`) to non-Python repos or `husky` to non-Node repos.

### Match Commands to Project Archetype
- **Libraries, Plugins (CGO `.dll`/`.so`, FFI, Wasm), SDKs & CLI Tools**:
  - Expose **only** `build` (emitting into `out/bin/` or `out/dist/`), `test`, and `quality` (plus `pack` if needed).
  - **DO NOT** create `start`, `stop`, `restart`, `status`, `out/run/`, or `out/logs/` daemon scaffolding when there is no long-running background service.
- **Single Frontend Project**: Keep `dev`, `build`, `test`, and `quality` in root `package.json` `scripts`—create zero `scripts/ctl.*` files.
- **Long-Running Services & Multi-Service Repos**: Centralize process lifecycle in **one** root native controller exposing:
  1. **`start [--daemon] [--only <name>]` / `dev`**: Ensure `out/run/` and `out/logs/` exist; check `out/run/<name>.json` + port availability first; in `--daemon` mode spawn detached with output to `out/logs/<name>.log`, write `{ "name", "pid", "port", "startedAt" }` to `out/run/<name>.json`, poll readiness (`127.0.0.1:<port>` or health URL), print concise status, and exit `0` without stealing desktop focus.
  2. **`stop [--only <name>]`**: Read `out/run/<name>.json`, verify PID liveness, terminate **only** that process tree (Windows `taskkill /PID <pid> /T /F`; POSIX process group `-pid` `SIGTERM` → bounded wait → `SIGKILL`), wait until port closes, and remove `out/run/<name>.json`. **NEVER** invoke global name-based kills (`taskkill /IM node.exe`, `pkill python`, `killall go`).
  3. **`restart`**: Run `stop` followed by `start`.
  4. **`status`**: Inspect `out/run/*.json`, verify live PID + port state, and print `service | status | pid | port | log`.
  5. **`quality`**: Execute the unified `project-quality` gate across all modules (`quiet-on-success`, dumping full captured stdout/stderr immediately on nonzero exit).
---

## 5. `.github/` Starter Templates

### `.github/workflows/ci.yml`
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # Add pinned stack setup step(s) matching the repository toolchain (e.g., setup-node, setup-go, rust-toolchain, uv)
      # Restore locked dependencies (--frozen-lockfile / --locked / go mod download)
      - name: Run Unified Quality Gate
        run: <CANONICAL_ROOT_QUALITY_COMMAND>
```

### `.github/workflows/release.yml`
```yaml
name: Release

on:
  push:
    tags:
      - "v*.*.*"

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # Add pinned stack setup step(s) matching ci.yml
      - name: Verify Tag Matches Canonical Version SSOT & Run Quality Gate
        env:
          RELEASE_TAG: ${{ github.ref_name }}
        run: |
          <CANONICAL_VERSION_PARITY_CHECK_COMMAND>
          <CANONICAL_ROOT_QUALITY_COMMAND>
      - name: Build Release Artifacts into out/dist
        run: <CANONICAL_RELEASE_BUILD_COMMAND>
      - name: Create Draft GitHub Release
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          NOTES_FILE=".github/release-note/${GITHUB_REF_NAME}.md"
          if [ ! -f "$NOTES_FILE" ]; then
            NOTES_FILE=".github/release-note/template.md"
          fi
          gh release create "$GITHUB_REF_NAME" out/dist/* \
            --title "$GITHUB_REF_NAME" \
            --notes-file "$NOTES_FILE" \
            --draft
```

### `.github/release-note/template.md`
```markdown
## Highlights
- Brief summary of the most impactful user-facing or architectural improvements in this release.

## Breaking Changes
- None.

## Features
- Added ...

## Bug Fixes
- Fixed ...

## Upgrade & Verification Notes
- Canonical version verified against `RELEASE_TAG` and full Quality Gate passed.
```

---

## 6. Compact `AGENTS.md` Blueprint (~60–90 lines)

```markdown
# AGENTS.md

<One-sentence project purpose and pinned tech stack>.

## Canonical Commands
- Install / Sync: `<exact locked install command>`
- Dev / Start: `<root dev/start command>` (`--daemon` for background; *omit start/stop/status for libraries, plugins & CLIs*)
- Stop / Status: `<root stop command>` / `<root status command>` *(services/apps only)*
- Single Test: `<exact targeted test command>`
- **Unified Quality Gate**: `<exact root quality command>`

## Repository Topology & Hard Invariants
- **Root Markdown Policy**: Keep ONLY `README.md` and `AGENTS.md` at the repository root. Place all architecture, quality, ADR, and task docs under `docs/` (`docs/architecture.md`, `docs/quality.md`, `docs/adr/`, `docs/tasks/`). Never create hidden dot-directories for planning.
- **Unified `out/` Artifact Root**: Route ALL build outputs, binaries, target caches, coverage reports, PID files (`out/run/`), and daemon logs (`out/logs/`) under `out/`. Never emit `dist/`, `build/`, `target/`, or `bin/` at root or inside subprojects.
- **Root-Only Lifecycle**: Manage all subproject startup/shutdown and quality checks strictly from the repository root; never add per-subdirectory `.sh`/`.ps1`/`.bat` scripts.
- **Version SSOT**: `<canonical version file & field>` is the single source of truth for application version parity.

## Code Retrieval (XERJ)
- XERJ prefix: `"<unique-prefix>"` *(omit this section if XERJ is not configured)*

## Coding & Completion Gate
- Write behavioral tests at public interfaces/seams for every new capability or bug fix.
- During iteration, run targeted tests and incremental LSP diagnostics on changed files. Before handoff, run `<exact root quality command>` once on the final working tree (see `docs/quality.md` for full coverage matrix and debt policy), re-sync XERJ if configured, and execute `post-impl` convergence. Never suppress errors/linters or use `--no-verify`.
```
