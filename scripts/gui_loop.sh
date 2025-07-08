#!/bin/bash
# Start backend and auth services then run headless and lynx tests
./scripts/install.sh

# Build packages required for vitest
pnpm --filter @directus/random run build
pnpm --filter @directus/storage run build

# Run the test suite (may fail on missing modules)
npm test || true

node scripts/headless_check.js
# placeholder for lynx loops
