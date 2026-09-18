# Android overlay

Load with Kotlin/Java. Inspect AGP/Gradle/JDK compatibility, SDK levels, product flavors, build types, Compose, generated resources/code, and device-test requirements.

## Choose coverage

Use the Android Gradle plugin's [Android Lint](https://developer.android.com/studio/write/lint) for Android-specific API availability, resources, manifest, and framework analysis. Ordinary compilation/assembly is not a full lint pass. Run wrapper lint tasks for the declared variants, such as `:app:lintDebug` where that task actually exists; a default lint task is not proof that every supported variant ran.

Inspect lint severity, `warningsAsErrors`, `abortOnError`, disabled/check-only rules, test/generated-source scope, and baseline files. Warnings must reach a failing gate under the shared contract. Do not regenerate a baseline to absorb current-change findings. Android API availability checks complement compiler deprecation diagnostics; neither subsumes the other.

Reuse Kotlin/Java formatting and compiler analysis. Add detekt or another analyzer only for explicit gaps that compiler plus Android Lint do not cover. For Compose or framework-specific checks, verify compatible plugin/library lint integration and actual reports rather than assuming framework dependencies automatically run all IDE inspections.

## Gate shape and boundaries

A root Gradle quality task can depend on format checks, relevant compile/lint/analyzer tasks, JVM unit tests, and required assembly. Inspect existing `check`, `test`, and `build` task dependencies first to avoid duplicate invocation or missing subprojects.

Record which variants and SDK targets the gate validates. Validate merged manifests, resources, dependency/configuration files, and the relevant production artifact. Avoid requiring signing credentials when an unsigned validation artifact satisfies the contract; do not silently replace a required release check with debug success.

Instrumented tests need an emulator/device and form a separate declared job when required. Lack of an SDK/device means blocked/partial verification, not passing skipped tests. Android Studio can expose inspections absent from Gradle lint; name the remaining diagnostic families and any version mismatch.
