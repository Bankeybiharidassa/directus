Node Test Environment Workarounds
================================

`pnpm` refuses to run when the runtime Node version does not match the engine requirement declared in `package.json`. Since we keep the root engines value at `22` but run tests under Node 18, the following environment variable is used:

```
export PNPM_IGNORE_NODE_VERSION=true
```

After setting this variable and running `pnpm install`, `npm test` executes the individual package test scripts. Some upstream packages fail due to missing `vitest` or other dependencies which are outside the CRM scope.

To provide Node 22 APIs missing in Node 18, we load `scripts/fs-glob-polyfill.js` using `NODE_OPTIONS`:

```
export NODE_OPTIONS="--import=$(pwd)/scripts/fs-glob-polyfill.js"
```

This polyfills `fs.glob` for packages like `@directus/sdk` during tests.
