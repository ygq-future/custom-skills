# C / C++

Detect the actual build system, compilers, standards, target platforms, presets/toolchains, generated headers, and vendored libraries. C and C++ have different applicable rules; retain real compilation context.

## Choose coverage

- Reuse clang-format or the existing formatting owner in a supported check mode, such as `--dry-run --Werror` for a compatible version. Restrict to owned source/header files and verify filename enumeration.
- Enable useful compiler warning categories in owned targets: GCC/Clang commonly start with `-Wall -Wextra -Wpedantic`, plus relevant deprecation/compatibility warnings; MSVC commonly starts with `/W4`. These are starting points, not a claim of all warnings. Promote the chosen warnings using the compiler's supported mechanism after applying the historical-debt policy. See [GCC warnings](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html).
- Build with actual definitions, includes, standard, and target ABI. Warning profiles and supported flags differ by compiler; do not impose GCC options on MSVC or propagate private warning policy to downstream consumers of a library.
- Add semantic/dataflow analysis only for gaps: an existing clang-tidy setup with a correct compilation database, compiler static analysis, or another established analyzer can provide it. [clang-tidy](https://clang.llvm.org/extra/clang-tidy/) check selection is separate from warning promotion; `--warnings-as-errors` does not enable additional checks. Compiler warnings also depend on the compilation command.
- MSVC [`/analyze`](https://learn.microsoft.com/en-us/cpp/build/reference/analyze-code-analysis?view=msvc-170) is an ecosystem-native choice. An analysis-only pass need not cover code-generation warnings. Do not stack equivalent analyzer families without a named gap.
- Run actual tests (for example the configured CTest suite) and a real link/build for the declared targets. Sanitizers add runtime diagnostics when compatible with the platform and project risks; they do not replace static analysis.

## Gate shape and boundaries

Use the build system's aggregate target/presets or existing script. A valid `compile_commands.json` must match generated headers, macros, include paths, and target configuration; stale/editor-only databases can produce misleading analysis. Analyze all owned translation units and ensure relevant headers are exercised. CMake compilation-database support depends on generator; do not assume every generator emits it.

Validate configure/generate steps, package/lock manifests, toolchain constraints, and meaningful build configurations. Distinguish configure success, analysis, test execution, and link success. Cross-compiled tests require a suitable runner; record unavailable target execution.

clangd and IDE inspections can differ from the selected compiler and analyzer. Explicitly assess deprecated declarations, unused/reachability, suspicious operations/casts, null-related analysis, and platform/API compatibility. Native languages do not provide a universal nullability guarantee. Public ABI compatibility needs a deliberate baseline/tool when part of the library contract.
