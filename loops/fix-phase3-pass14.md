# fix-phase3-pass14
Built workspace packages `@directus/random` and `@directus/storage` using pnpm under Node 18 with `NPM_CONFIG_ENGINE_STRICT=false`.
`npm test` now runs but fails in `@directus/sdk` because `fs.glob` is undefined in Node 18.
Upstream packages appear to require Node 22 features.
