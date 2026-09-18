# Git and CI Quality

Apply the project's convention before choosing a validator. Git integration supports the source gate; it does not replace it.

## Commit messages

Inspect contributor rules, validator configuration, and representative recent commits. Prefer the documented convention over guessed patterns. For new projects without a convention, Conventional Commits is a reasonable default; record allowed types/scopes and any merge/revert exceptions. Do not rewrite history to fit a new convention.

Use the existing validator or a maintained solution compatible with the existing runtime. In Node projects, commitlint is an option; a different ecosystem need not gain Node solely for this. Any custom validator must be small, match the declared grammar, and be exercised against valid and invalid messages, including multiline bodies and the project's exceptions.

Expose message-file and commit-range validation through the quality interface (arguments or named tasks). Before committing, validate the actual proposed message; the source gate cannot infer a future message. In CI, validate the real incoming range with available base/head commits. Handle initial commits, shallow checkouts, merge commits, and squash workflows explicitly; validating only HEAD can miss earlier invalid messages. If policy governs the squash title, validate that field and document how it becomes the commit message.

See [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) and [commitlint CI setup](https://commitlint.js.org/guides/ci-setup.html) for grammar and range integration. Verify APIs/options for the selected validator version.

## Local hooks

Inspect existing hook manager and repository `core.hooksPath` before editing. Reuse them; preserve existing hook actions. Configure locally to the repository, document fresh-clone activation, and do not change global Git settings.

| Event | Responsibility |
| --- | --- |
| pre-commit | Fast checks of staged content, or the full gate if inexpensive |
| commit-msg | Validate the supplied message file |
| pre-push | Full gate, or the documented expensive checks delegated from pre-commit |

Hooks call shared quality tasks. A staged check must inspect the index version and handle partial staging safely; testing the working tree alone can validate code absent from the commit. Prefer proven existing staged-file handling or an isolated index snapshot. Do not auto-stage formatting changes or overwrite unstaged edits. Keep hook checks non-mutating.

Verify activation, executable bits where relevant, quoting/paths, and failure propagation by invoking with realistic fixture inputs. Do not create a real commit or push just to test a hook. Installation is separate from the read-only gate. A hook file in Git is not proof that fresh clones run it. See [Git hooks](https://git-scm.com/docs/githooks) for event arguments and execution rules.

If there is no Git repository yet, record integration as pending. Initialize it only when Git initialization is part of the user's project-setup request; invoking this skill alone does not request `git init`. Hooks are bypassable, so the Agent's checks and CI remain necessary. Never use `--no-verify` as remediation.

## CI

Reuse the detected provider and existing workflows. Where no provider/remote exists, deliver the local gate and document CI as pending provider selection; avoid guessing a hosting platform.

Bootstrap pinned tools and restore locked dependencies, then call the canonical gate with explicit matrix targets and Git event context. Keep rule selections and stage composition in repository tasks, not duplicated workflow command lists. A required aggregate job must fail if any required matrix job fails, is cancelled, or is unexpectedly skipped. Caches must not conceal missing checks.

Cover pull requests and protected-branch changes according to project policy. Check CI syntax and run locally possible checks; verify remote results when available. Creating workflow files does not establish protected-branch required checks. Report remote enforcement as unverified until observed; change hosted settings only within the user's authorization.

For multi-platform projects, use the same root quality interface per explicit target and a documented aggregate CI result. Follow the contract's declared pre-commit and CI-only responsibilities. A missing pre-commit result blocks committing; a pending CI-only result blocks the merge/release stage that requires it. Do not downgrade either automatically to optional. A project that requires every platform before commit needs a way to verify an uncommitted workspace snapshot, as described in the contract.
