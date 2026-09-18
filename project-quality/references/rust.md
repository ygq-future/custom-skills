# Rust

Inspect workspace members/default-members, toolchain pin, MSRV, edition, build scripts, procedural macros, target triples, and supported feature sets.

## Choose coverage

- Prefer toolchain components: `cargo fmt --all -- --check`, `cargo check`, and `cargo clippy`. Use workspace/target arguments appropriate to the actual support contract.
- Clippy provides compiler plus semantic lint diagnostics; [`-- -D warnings`](https://doc.rust-lang.org/clippy/usage.html) elevates enabled warnings. It does not enable every optional lint group. Avoid automatically enabling all pedantic/restriction lints.
- The compiler's [deprecated lint](https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html#deprecated) is warn-by-default. Inspect crate/workspace allow attributes, lint tables, and command flags for unused, unreachable, compatibility, and deprecation coverage. Propagate the chosen warning policy to compile/test/build contexts that Clippy does not cover.
- Run real `cargo test` suites and a meaningful build (`cargo build --release` when release behavior matters). Preserve doc tests as required; verify the selected test arguments do not accidentally omit them.

## Gate shape and boundaries

A native task alias or existing runner can sequence these checks under one implemented `quality` entrypoint. Do not assume Cargo aliases can execute arbitrary shell chains portably; use the project's established alias/xtask/script pattern.

Use explicit workspace and feature/target scope, commonly `--workspace --all-targets` for checking where supported. Do not blindly use `--all-features`: mutually exclusive features require separate supported combinations. Default features, no-default-features, and minimum-version jobs belong in the contract when they are supported configurations. Cross-target compilation and target test execution are distinct.

Use locked resolution where the project's Cargo.lock policy requires it; distinguish lock reproducibility from offline cache availability. Inspect build scripts and generated inputs. Avoid duplicate identical compiler work where Clippy already enforces it, while retaining a useful fast check task.

rust-analyzer may report additional IDE diagnostics and analyze different features/targets. Record these limits; a Clippy pass is not proof of every editor diagnostic. Public-crate API compatibility against a release baseline is an additional capability when the project promises it, not something `cargo check` proves.
