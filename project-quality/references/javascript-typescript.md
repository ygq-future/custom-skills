# JavaScript / TypeScript

Load for JS/TS source, including build/test configuration and workspaces. Inspect package-manager locks, workspace boundaries, compiler references, module resolution, runtime targets, and generated type prerequisites.

## Choose coverage

- Reuse one formatter per file scope. For frontend Prettier setup, apply the template and Tailwind requirements below. Use check mode; disable linter formatting rules that conflict with the formatting owner.
- For TS, use the project's compiler in project mode. `tsc --noEmit -p tsconfig.json` fits a simple project; project-reference/composite builds need a compatible build-mode task and generated declarations. A bundler's transpilation does not prove type checking. JS can use `checkJs`/JSDoc where appropriate; do not migrate JS to TS just to satisfy a matrix row.
- Reuse the linter if it provides required semantics. With ESLint, configure type-aware rules only for files with valid project/type context. Biome, Oxlint, or another existing checker is sufficient only for the demonstrated rule coverage in that version; speed or parsing TS is not proof of typed/deprecated diagnostics.
- Choose explicit checks for unused imports/symbols, unreachable code, nullability/type safety, suspicious promises and casts as applicable. Assign overlapping unused rules to one owner. Inspect TS strictness and project scope before widening it in a legacy repository. TypeScript's `allowUnreachableCode: false` diagnoses syntactic unreachable code; it does not provide full dataflow reachability. See [TSConfig](https://www.typescriptlang.org/tsconfig/).
- TS does not normally fail `tsc` for JSDoc `@deprecated` references. With typed ESLint, [`@typescript-eslint/no-deprecated`](https://typescript-eslint.io/rules/no-deprecated/) adds this semantic check; verify its project context and actual rule activation. Record missing third-party annotations and uncovered JS references as limits.
- Make lint warnings fail (for ESLint, `eslint . --max-warnings 0`), and use real test-run mode rather than watch mode. Validate the production bundle or library artifact separately.

## Frontend Prettier standard

Use [the Prettier template](../assets/prettier/prettierrc.json) as the default for new frontend formatting setup. Copy it to `.prettierrc.json` when no Prettier configuration exists. Its option values are the shared standard; keep the template as their single source of truth. See [Prettier options](https://prettier.io/docs/options) for their semantics.

For an existing project, inspect the effective configuration first, including shared configs, overrides, and EditorConfig. Merge into its existing configuration format rather than creating a competing file. Preserve intentional project conventions under the existing-project policy and report differences from this template. Do not replace an effective alternative formatter solely to apply a Prettier template or format the entire codebase as an incidental change.

### Tailwind CSS

The base template has no plugins. When the frontend project uses Tailwind CSS, `prettier-plugin-tailwindcss` is required in its Prettier setup: add a compatible development dependency and merge `"plugins": ["prettier-plugin-tailwindcss"]` into the configuration. Preserve other plugins, avoid duplicates, and place the Tailwind plugin last. Without Tailwind, omit this dependency and plugin entry.

Check the installed versions against the [official plugin documentation](https://github.com/tailwindlabs/prettier-plugin-tailwindcss). Current releases require Prettier 3 and ESM loading. For Tailwind v4, set `tailwindStylesheet` to the actual CSS entrypoint; for v3, set `tailwindConfig` when its configuration is outside the default location. Paths are relative to the Prettier configuration. Configure `tailwindFunctions` only for class helpers actually used by the project.

If an existing Tailwind frontend uses another formatter, treat adopting Prettier plus this plugin as a formatting-ownership decision: report the required change and resolve it within the authorized scope, rather than running competing formatters or claiming an alternative satisfies this explicit plugin requirement. In audit-only mode, report the gap without installing anything.

Wire the repository's pinned Prettier check into the format stage of the unified gate, with write/fix mode separate. Verify configuration resolution and, for Tailwind, a representative class-sorting check. An installed plugin alone does not prove the gate loads it.

## Gate shape and boundaries

Reuse package scripts behind `npm run quality`, `pnpm quality`, or the project's equivalent. Resolve the package manager from repository evidence. Invoke all intended workspace packages and fail on missing required scripts; do not let an if-present/empty workspace filter create a passing gate. Generate framework declarations before their consumers.

Use frozen/immutable install semantics appropriate to the package manager in bootstrap/CI to validate locks. Check manifest, export/type entrypoints, runtime engine constraints, and relevant framework/config schemas. A dependency vulnerability scan is not a replacement for these checks.

Editor suggestions and language-service plugins may have no CLI equivalent. Record the specific rule family and extension rather than claiming parity from `tsc`. Add the React overlay when applicable; research the official equivalent for Vue, Svelte, Angular, or other frameworks instead of assuming plain TS covers their templates.
