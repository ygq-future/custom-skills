# .NET

Inspect solution/project membership, `global.json`, SDK and target frameworks, language (C#/VB/F#), nullable settings, central build properties/packages, analyzers, and `.editorconfig`. Roslyn-specific guidance primarily applies to C#/VB; map F# compiler/analyzer capabilities separately rather than assuming parity.

## Choose coverage

- Reuse SDK formatting checks, such as `dotnet format <solution> --verify-no-changes`, with suitable project scope and restore policy. Verify analyzer severities included by the command; formatting alone is not compilation or complete analysis. See [dotnet format](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-format).
- Build using the declared configuration/frameworks and enabled SDK/project analyzers. Inspect `EnableNETAnalyzers`, `AnalysisLevel`, ruleset/editorconfig severities, and `RunAnalyzersDuringBuild`. Do not add analyzer packages that duplicate the SDK's effective coverage.
- Compiler diagnostics cover obsolete APIs, type errors, and nullable warnings where supported/enabled. Establish explicit warning enforcement through build properties/arguments; inspect `NoWarn` and related overrides rather than trusting exit zero.
- [Code analysis](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview) distinguishes build-capable rules from IDE-only ones. Style rules may require `EnforceCodeStyleInBuild` and effective warning/error severities; turning that property on does not make every IDE rule run. Fill only demonstrated gaps.
- Execute the actual test projects with the repository's test runner/version. Verify discovery and framework coverage. Build validation includes relevant Release/target-framework compilation; use publish only when deployment compilation/trimming/AOT is part of the product contract.

## Gate shape and boundaries

Use an existing MSBuild target or repository runner under one quality entrypoint. Keep configuration/target arguments consistent across restore, format, build, and tests. A `--no-build` test invocation is valid only after building the same test targets/configuration; stale artifacts are not verification.

Use locked restore where locks are part of the project policy. Validate project/solution references, central package declarations, and SDK compatibility. Use a build that genuinely runs analyzers when verifying new rules; incremental no-op output does not demonstrate new diagnostics.

Distinguish compiler/analyzer warnings from MSBuild/NuGet warnings and verify the selected warnings-as-errors mechanism covers the intended producers. For public libraries, assess SDK package/API compatibility validation against the supported baseline. IDE-specific Roslyn/ReSharper/Rider inspections without a verified CLI counterpart remain explicit gaps.
