# Python

Inspect supported Python versions, package layout, environment/lock manager, typing/stub coverage, test runner, and packaging backend. Load each owned package, including tests and scripts.

## Choose coverage

- Retain an effective formatter/linter combination. Ruff can own formatting and lint, or lint alongside an existing formatter with matching settings. Its [formatter](https://docs.astral.sh/ruff/formatter/) and [linter](https://docs.astral.sh/ruff/linter/) are distinct checks; neither replaces semantic typing. Avoid duplicate import/format rule ownership.
- Select one primary semantic checker compatible with the project (for example existing mypy, Pyright, or another verified maintained checker). Check plugin/stub needs before migration. In Pyright, explicitly inspect `reportDeprecated`, unused and unnecessary-code diagnostics, and diagnostic severity; defaults do not imply strict enforcement. See [Pyright configuration](https://github.com/microsoft/pyright/blob/main/docs/configuration.md).
- Syntax validation or byte compilation can supplement coverage where the linter/checker does not parse all shipped modules. They do not establish runtime import success or type safety. Runtime tests must discover real tests and run in the declared environment.
- Static deprecated-API detection depends on annotations/stubs and checker support. Runtime warnings only cover executed paths. Configure the test runner's warning policy so relevant `DeprecationWarning`, `FutureWarning`, and other project warnings fail; baseline third-party noise narrowly under the shared contract. Python suppresses some warning categories by default; see [warning control](https://docs.python.org/3/library/warnings.html).

## Gate shape and boundaries

A runner-native `quality` task can compose `ruff format --check`, `ruff check`, the configured type checker, the existing test runner, and package/build validation. These are examples, not commands to install blindly. Avoid adding a second environment manager just to sequence them.

Validate `pyproject.toml`, lock consistency with the selected manager's check/locked mode, installed dependency compatibility where relevant, and wheel/sdist generation for distributed packages. For an unbundled script/service, use the project's meaningful import/runtime preparation instead of fabricating a distribution target.

Pylance/editor-only features, missing stubs, dynamic imports, and framework metaprogramming can leave gaps. Identify the actual diagnostic family; a successful mypy/Pyright run is not proof that every editor inspection or runtime deprecation is covered.
