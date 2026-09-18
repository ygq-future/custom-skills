# Quality Contract

Use this contract for every stack. Capabilities describe outcomes, not mandatory separate tools or separate processes. One verified command may satisfy several rows.

## Coverage matrix

Record each row in the project quality document (or the response for audit-only work), with columns: **capability | provider/configuration | command/task | files/modules/targets | enforcement phase/severity | status/evidence**.

| Capability | Required assessment |
| --- | --- |
| Formatting / format check | A consistent owner per file type and a non-mutating check |
| Syntax / compile | Parse or compile real project inputs with their build context |
| Type check | Compiler or ecosystem checker; document dynamic/untyped gaps |
| Lint | Applicable correctness and project-convention rules |
| Compiler warnings | Enabled categories, severity, and failing exit behavior |
| Deprecated / obsolete API | References to deprecated APIs, not just deprecated tool configuration |
| Static analysis | Semantic/dataflow diagnostics beyond parsing and build success |
| Unused / unreachable / suspicious code | Explicit rule ownership and enabled coverage |
| Tests | Real discovered tests, required suites, runtime warnings, and prerequisites |
| Build validation | Production/release or library artifact for supported target scope |
| Dependency / manifest / configuration | Consistent manifests/locks, valid project/tool configuration, reproducible resolution |
| Commit message validation | Existing convention or chosen convention, message/range inputs |
| Git hooks | Installed and executable local integration with defined responsibilities |
| CI Quality Gate | Shared entrypoint and required scope on the actual CI platform |

Use statuses **verified**, **configured but unverified**, **missing**, **blocked**, **partial**, or **not applicable (reason)**. Identify evidence separately from enforcement: a command can execute successfully while covering only part of a capability. Absence of tests is a gap, not successful testing. A blank starter may defer tests until behavior exists; record that limitation without inventing trivial tests or enabling pass-with-no-tests globally.

For such a starter, report **bootstrap infrastructure verified; application tests pending** if the other applicable checks pass. State the activation condition in agent instructions: adding the first behavior requires a real test task before that implementation is complete. Once behavior exists, missing tests remain a gap; the starter exception does not apply to an existing untested application.

For interpreted apps, validate import/package/runtime preparation instead of inventing a compiler. For public libraries, assess API/source/binary compatibility against an explicit release baseline when that is part of their support contract. Configuration validation includes meaningful framework/build schema checks; JSON/YAML parsing alone does not prove configuration semantics. Vulnerability/license scans are separate risk-policy capabilities; add them when appropriate, not as a substitute for manifest validation.

## Mandatory Web Search for version selection

This procedure is mandatory when recommending, introducing, replacing, upgrading, or choosing to pin a version of any quality tool, library, plugin, analyzer, formatter, test runner, or hook/commit validator. It applies during audits as well as implementation, across every language profile.

1. Read the project's actual resolved versions and constraints from manifests, lockfiles, wrappers, toolchain files, and available version commands. Include runtime/SDK/compiler, framework, build system, package manager, host tools, and relevant plugins. Distinguish declared ranges from installed/resolved versions.
2. **Perform Web Search for this selection task**, using the tool name, the project's relevant versions, and release/compatibility terms. Find the latest stable candidates and their supported version ranges. Model knowledge, this skill's examples, a previously installed release, or an unverified `latest` tag cannot substitute for the search. Existing search evidence from the same task may be reused while the relevant constraints remain unchanged.
3. Open the primary sources behind the results: official release notes, compatibility matrices, versioned documentation, or maintainer-published package metadata. Verify runtime/engine requirements, peer dependencies, compiler/framework/build-plugin compatibility, and configuration migrations as applicable. Registry/CLI metadata can supplement Web Search, but does not replace it. Search snippets and publication dates alone do not prove compatibility or that a release is newest.
4. Select the **latest stable compatible version within the project's declared constraints**, not automatically the latest overall major. Exclude prereleases unless requested or already required by the project. Verify the combination of tools/plugins, not each package independently. Do not upgrade the project's runtime/framework or bypass peer-dependency checks merely to install a newer quality tool. If an older version must remain under project policy or migration scope, document the newer compatible candidate and the concrete reason for retaining the older version; never label it latest.
5. Record the search date, relevant project versions, selected version, primary-source URLs, compatibility basis, and any deliberate retention/deferment in the quality document or audit report. Pin/lock the chosen release using the project's normal mechanism, then perform actual installation/configuration and Quality Gate validation when implementation is authorized. Documentation establishes expected compatibility; successful execution is separate evidence.

If Web Search is unavailable, fails, or yields insufficient compatibility evidence, mark version selection **blocked/unverified**. Do not recommend or install a guessed version, silently fall back to a remembered old release, or claim to have found the latest compatible release. Continue independent inspection and safe existing checks, and report the missing evidence.

Running an already established, pinned Quality Gate without making a version-selection decision does not require a fresh search or dependency update. This policy governs selection; the gate itself remains reproducible and does not search for or install latest releases at runtime.

## Diagnostic parity

Aim for the useful union of **Compiler + Language Server + IDE + Official Static Analyzer**. Enumerate the relevant diagnostic families: deprecated/obsolete, warnings, unused symbols/imports, unreachable and suspicious code, nullability, unchecked casts/operations, compatibility, type errors, API compatibility, and framework diagnostics.

For each relevant family:

1. Identify the producer and project version, including IDE plugins and project-specific analyzers when visible.
2. Find its supported batch CLI or an equivalent rule. Check the actual severity, file inclusion, classpath/type information, target, generated inputs, and exit semantics.
3. Enable useful missing diagnostics in the selected owner. Warnings in output are not automatically failures; use native severity/threshold settings or structured diagnostic reports with a tested adapter.
4. Verify representative findings reach the root gate with a nonzero exit. For a claimed deprecated check, use a real supported deprecation marker/reference, not an unrelated syntax error.
5. Record residual gaps by diagnostic family and producer. An IDE extension being installed, or an LSP starting successfully, is not batch diagnostic evidence. Do not script fragile editor automation or parse localized log text and call it full parity.

Use semantic correctness rules as the default. Do not equate every optional IDE style suggestion with a mandatory warning or enable every experimental/pedantic rule. Choose explicit rule sets and target versions so upgrades do not silently redefine the contract.

## Warnings and historical debt

The target is no unaccepted warnings or errors in the declared scope. New diagnostics block completion/commit, including deprecation. Never treat a warning-bearing build as clean merely because its exit code is zero.

For existing repositories, capture findings before changing configuration where practical. Attribute with an unchanged-base run under the same tool versions/configuration, or specific source/history evidence; diagnostics newly exposed by stronger rules can concern historical code. Do not blame the current change solely because a rule was just enabled.

If historical debt cannot be fixed within scope, preserve its visibility and keep the gate failing until the project has an explicit accepted baseline/exception policy. Do not create or expand an accepted baseline merely to obtain green status. Reuse an existing policy; otherwise report a concrete bounded baseline proposal for the owner to accept. Infrastructure work can be delivered as blocked without committing through a failed gate.

A permitted baseline identifies diagnostic IDs and stable file/symbol fingerprints, reason, owner, and review/removal condition. Enforce no new findings and remove resolved entries through a separate reviewed maintenance change; do not use a total warning count, changed-lines-only filtering, or a blanket directory exclusion as a substitute. If the tool cannot enforce a reliable ratchet, report the limitation and leave strict checks failing rather than claiming enforcement.

An accepted historical baseline yields **pass against baseline**, never **zero diagnostics**. A narrowly justified false positive or compatibility exception follows the project's established approval policy and includes evidence, exact scope, and review condition. Generated/vendor exclusions must describe ownership and generator validation; do not hide maintained source under them. Infrastructure/environment warnings also need attribution and disposition, not silent discarding.

## Entrypoint semantics

Define enforcement phases explicitly. The full default command is the complete pre-commit gate for all owned modules and declared development targets, including all applicable core capabilities. Additional platform/device/release configurations may be CI-only when the project's support policy puts them there; they use the same interface with explicit target arguments and remain required before merge/release. This is an upfront contract decision, not a runtime skip or an affected-files shortcut. Preserve existing stronger requirements; do not move a failed pre-commit check to CI merely to permit a commit. Label local success with CI pending accurately rather than claiming all-platform success.

If the project requires every platform before commit, establish a way to validate the final uncommitted tree (for example available runners consuming an identified workspace snapshot). Bind results to the exact content and configuration. If only commit-triggered CI is available, report that as an infrastructure blocker for this stronger requirement instead of constructing a circular commit prerequisite.

- Use the project's existing runner/runtime. Check commands do not reformat, auto-fix, rewrite locks, install hooks, or update baselines. Build/cache/generated outputs are permitted in their declared locations; tracked source/configuration changes must be detected and explained. Offer fixes as separate commands.
- Pin dependencies/toolchains using the ecosystem's supported mechanism. Put bootstrap/locked dependency restore in documented prerequisites or a reproducible CI setup step. The gate checks required tooling exists and fails clearly if not; it must not silently skip or fetch an unpinned latest tool.
- Propagate every failing child exit code. Shell pipelines, background jobs, log capture, and PowerShell native commands need explicit handling; PowerShell error preferences alone do not guarantee native exit propagation. Avoid success masking (`|| true`, unchecked last exit status, CI continue-on-error).
- Default to the complete declared scope. Include nested packages, tests, build scripts, framework files, and required generated inputs. Incremental caches are valid only with inputs covering configuration, tools, dependency locks, targets, and baselines.
- Define supported configurations rather than testing every theoretical combination. Cover required build tags, features, architectures, framework variants, and public API baselines. Do not select impossible combinations just to use an all-targets flag.
- For platform-specific or service-dependent work, the root interface dispatches documented jobs/targets. An unsupported host for the requested target reports partial/blocked rather than skipping successfully. CI must aggregate every required CI job; a local result cannot stand in for the full CI result.
- Keep tasks acyclic: a hook may invoke the gate, but the gate must not invoke Git commit/push or the hook recursively. Git validation takes explicit event context; its absence in the default source gate is documented and covered at commit/CI time.

## Verification evidence

Inspect configuration resolution and task discovery, then run the real commands. Check test discovery/counts and files analyzed, not only exit zero. An empty glob, missing workspace, or build task marked skipped can produce false success.

A fail-fast gate is valid. During an audit/setup verification, run safe downstream checks individually if an earlier failure prevents assessing them, or record them as not executed. Never infer their success from the first failing stage; an aggregate that continues must still return nonzero if any stage fails.

When adding/changing orchestration or diagnostic enforcement, use isolated temporary fixtures/copies to demonstrate representative success and failure: format violation, a compiler/type error, a warning/deprecation diagnostic, and a failing test where applicable. Select probes for the capabilities being claimed; no need to retest every unchanged upstream rule. Confirm the aggregate exits nonzero, then restore the fixture and confirm the success case. Never inject probes into unrelated user edits. Remove only your own temporary artifacts.

Run the full gate after the final changes. Record command, working directory, tool versions, target scope, outcome, residual findings, and unavailable checks. A dry-run, configuration parse, or written CI file alone is not execution evidence. If remote CI cannot be run, report local verification and remote status separately.
