# fix-phase1-pass03
`npm test` fails after installing Node 22 and running `pnpm install`.
Vitest cannot find `@directus/random` during package tests.
Investigate monorepo build steps or missing dev dependencies.
Fixed in Pass 05 by building `@directus/random` with `pnpm --filter @directus/random run build` before running tests.
