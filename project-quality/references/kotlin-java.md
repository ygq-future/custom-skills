# Kotlin / Java

Inspect Gradle/Maven wrappers, JDK/toolchains, compiler and plugin versions, source sets, annotation processing, generated code, and modules. Add the Android overlay for Android; Kotlin Multiplatform requires platform-specific source-set checks beyond this JVM profile.

## Choose coverage

- Reuse a formatter/check task (for example existing Spotless, ktlint, or Java formatter integration). Assign one formatting owner per source type. detekt's formatting integration and standalone ktlint should not both enforce the same rules.
- Configure the real build's compiler tasks, including tests. Kotlin [compiler options](https://kotlinlang.org/docs/compiler-reference.html) include warning enforcement; `allWarningsAsErrors`/`-Werror` elevate emitted warnings, while additional warning options depend on compiler version. Inspect `-nowarn`, language/API version, and warning overrides. Do not paste newer compiler flags into older plugins.
- Java [javac](https://docs.oracle.com/en/java/javase/25/docs/specs/man/javac.html) supports `-Xlint:deprecation,removal,unchecked`, broader selected lint categories, and `-Werror`. Pass these through Gradle/Maven so classpaths, module paths, processors, and release targets remain valid; standalone javac over source paths is not an equivalent build.
- Kotlin null safety does not cover every Java platform-type hazard; javac does not provide comprehensive nullability or unused-symbol analysis. Fill demonstrated semantic gaps using the existing analyzer or an appropriate maintained integration, such as detekt with type resolution, Error Prone, or SpotBugs. Choose by language and actual uncovered rules; do not install all of them. Check compatible versions, analysis scope, and warning thresholds.
- Run test suites and artifact assembly through actual project tasks. `check`/`verify` may aggregate some checks, but inspect the graph to confirm formatting, static analysis, tests, and packaging are included.

## Gate shape and boundaries

Reuse the wrapper (`gradlew.bat` on Windows, `./gradlew` on POSIX, or Maven equivalent) with one aggregate task/profile. Declare task dependencies; do not assume textual task order solves generated-code dependencies. Validate build configuration, dependency locks/verification policy, version catalogs, and plugin resolution without updating them inside check mode.

Gradle's own deprecation warnings are separate from Java/Kotlin compiler diagnostics. Inspect both; `--warning-mode=fail` can enforce Gradle warnings when supported and consistent with the baseline policy. See [Gradle logging](https://docs.gradle.org/current/userguide/logging.html).

IntelliJ inspections exceed compiler/analyzer coverage. If the project already depends on an inspection profile, assess a supported [headless inspection](https://www.jetbrains.com/help/idea/command-line-code-inspector.html) or equivalent batch analyzer, including SDK, IDE availability, report failure handling, and licensing. Otherwise name the remaining inspection gaps. Installing an IDE is not a default prerequisite.

For published libraries, add source/binary API compatibility validation against an explicit supported release when needed. Compiling the library itself does not establish consumer compatibility.
