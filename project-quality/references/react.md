# React overlay

Load with the JS/TS profile. Determine React version, framework, bundler, server/client boundaries, and whether compiler integration is in use.

Use framework-supported lint presets with compatible versions. The official [React hooks plugin](https://react.dev/reference/eslint-plugin-react-hooks) covers hooks rules and exposes React Compiler diagnostics; inspect the installed preset instead of assuming only two hook rules exist. Assess JSX/accessibility checks against current tooling and avoid duplicating them across linters. Static rules supplement component/integration tests; they do not establish UI behavior coverage.

## Next.js

Inspect the installed major version. [Next.js 16](https://nextjs.org/docs/app/guides/upgrading/version-16) removed `next lint` and automatic linting from `next build`; use a supported direct linter invocation. Check the project's actual version rather than copying that change into older projects.

The [TypeScript integration](https://nextjs.org/docs/app/api-reference/config/typescript) documents framework type checking and type generation. Generate required route types before standalone type checking when supported. Verify build-time checking is enabled, inspect options such as ignored build errors, and record what the framework language-service plugin adds beyond CLI checking. Do not assume `tsc` executes IDE plugins.

Run a production build to exercise routing, server/client constraints, and generated artifacts, plus the tests appropriate to the app. Avoid duplicating an identical compiler pass if an independently verified framework task already enforces it, but preserve a fast type task for development where useful. Build-time external services/secrets should be explicit prerequisites; unavailable ones yield blocked validation.

For other React frameworks, map their official CLI diagnostics and production task to the same contract. Rendering successfully in development is not evidence that framework diagnostics or production compilation pass.
