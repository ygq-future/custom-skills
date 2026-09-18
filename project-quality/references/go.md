# Go

Detect `go.mod`, `go.work`, module boundaries, toolchain directives, build tags, cgo, and supported GOOS/GOARCH. Run checks per owned module; a root `./...` pattern is not proof that nested modules are covered.

## Choose coverage

- Use gofmt as the formatting owner, or an existing compatible formatter that includes its behavior. `gofmt -l` lists violations but does not by itself fail on a nonempty list; the gate must convert that result to failure without rewriting files. Enumerate owned Go files safely.
- `go vet ./...` covers suspicious constructs beyond compilation. It is not comprehensive static analysis; see [vet](https://pkg.go.dev/cmd/vet).
- Reuse Staticcheck or a configured aggregator when semantic diagnostics are needed. [SA1019](https://staticcheck.dev/docs/checks/#SA1019) detects deprecated API references. Inspect actual enabled checks, especially unused analysis, rather than assuming defaults cover every diagnostic family.
- golangci-lint is justified when its selected analyzers add useful coverage or it already owns the workflow. Do not also invoke standalone copies of the same analyzers unless their scopes differ intentionally. Verify configuration schema/tool compatibility with the Go version.
- Use `go test ./...` and `go build ./...` for the declared module/target matrix. Tests run only a subset of vet by default; do not infer a complete vet pass. Race tests are useful on supported execution targets when appropriate to the project, not a universal cross-compilation command.

## Gate shape and boundaries

Use an existing task runner or small script to aggregate formatting, vet/static checks, tests, build, and module validation. Go has no built-in `go quality` subcommand. Declare build tags and cgo prerequisites consistently across analysis, tests, and build; cross-compiling does not execute target tests.

Check manifest consistency using the selected Go version's supported check/diff mode or an isolated copy. `go mod tidy` mutates manifests and belongs outside the check-only path unless its changes are detected in isolation. `go mod verify` checks cached module integrity, not whether imports and go.mod/go.sum are tidy. See the [module command reference](https://go.dev/ref/mod#go-mod-tidy).

Go compilation rejects many unused/type errors but does not expose a generic compiler-warning switch. Map remaining families to vet/static analysis. [gopls analyzers](https://go.dev/gopls/analyzers) may differ from the selected batch checker; document uncovered editor diagnostics. Revalidate rule ownership when upgrading the aggregator or Go toolchain.
