# fix-phase3-pass15
Installed dependencies under Node 18 using `NPM_CONFIG_ENGINE_STRICT=false`.
`pnpm install` succeeds and CRM node_backend tests pass via `npm test --prefix node_backend`.
Monorepo tests still fail due to missing `@directus/random` which depends on Node 22 features.
