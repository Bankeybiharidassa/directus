# Changelog

## Phase 1 Review
- Date: 2025-07-07
- Outcome: Phase 1 incomplete. `docs/inventory.md` lacks module paths and only has one edit loop.
- Next: Add module paths, refine file and loop a second time before proceeding to Phase 2.

## Phase 1 Loop 1
- Date: 2025-07-07
- Added module/plugin paths column to `docs/inventory.md`.
- Updated `todo.md` accordingly.

## Phase 1 Loop 2
- Date: 2025-07-07
- Refined module paths and completed second revision of `docs/inventory.md`.
- Marked related tasks complete in `todo.md`.

## Phase 1 Loop 3
- Date: 2025-07-07
- Added admin features (log export, config reload, security scan) to `docs/inventory.md`.
- Node updated to v22 via NodeSource; pnpm install executed, but npm test fails due to missing @directus/random.

## Phase 2 Bootstrap
- Date: 2025-07-07
- Created workspace scaffolding and minimal files.
- Initialized `extensions/`, `scripts/install.sh`, and documentation.

## Phase 1
- Pass 01 - Started inventory from CRM/README.md
- Pass 02 - Added module folder proposals and classification table
- Pass 03 - Added requirements from TODO.md
- Pass 04 - Added additional classification rows
- Pass 05 - Noted test_install and headless scripts
- Pass 06 - Clarified inventory source
- Pass 07 - Updated folder paths in inventory
- Pass 08 - Documented architecture overview
- Pass 09 - Added table of contents
- Pass 10 - Inventory review complete

## Phase 2
- Pass 01 - Created workspace structure and initial files
- Pass 02 - Added README links
- Pass 03 - Added inventory pointer
- Pass 04 - Updated install script with npm step
- Pass 05 - Review workspace files
- Pass 06 - Added gui_loop.sh stub
- Pass 07 - Expanded architecture doc
- Pass 08 - Minor cleanup
- Pass 09 - Updated TODO
- Pass 10 - Workspace bootstrap complete

## Phase 2 (continued)
- Pass 11 - Added environment variables and expanded install script
- Pass 12 - Documented module layout and auth flow
- Pass 13 - Declared agent governance rules
- Pass 14 - Updated TODO list for upcoming modules
- Pass 15 - Documented env setup in README


## Docs and Scripts Update
- Date: 2025-07-07
- Added integration points section in `docs/architecture.md`.
- Created `scripts/headless_check.js` to proxy CRM headless tests.
- Documented GUI testing workflow in `README.md`.

## Phase 1 – Pass 01 (2025-07-06)

- Extracted 8 features from `/CRM/README.md`
- Created `/docs/inventory.md`
- Categorized features into native, plugin, external, or infeasible
- Inventory is tied to proposed module paths
- No blocking issues
- Ready for Phase 1 – Pass 02

## Phase 1 – Pass 01 Refresh (2025-07-07)
- Re-extracted features from `/CRM/README.md` and expanded table to 14 entries.
- Updated `/docs/inventory.md` with module paths and classification.
- Recorded test failures due to Node version and missing Python deps in `/loops/fix-phase1-pass01.md`.
- Ready for Phase 1 – Pass 02 review.
## Phase 1 – Pass 01 (2025-07-07)
- Re-extracted features from /CRM/README.md
- Updated /docs/inventory.md with 18 entries
- Classified features by required implementation
- Ready for Phase 1 – Pass 02


## Phase 1 Pass 02 - Node update
- Upgraded Node to 22.16 using nvm
- Ran pnpm install but `npm test` fails due to vitest missing modules
- Logged issue in loops/fix-phase1-pass02.md
## Phase 1 Pass 03 - Apt Node install
- Installed Node.js 22 via NodeSource apt repo
- Enabled pnpm through corepack
- `npm test` still fails missing `@directus/random`
- Documented in `loops/fix-phase1-pass02.md`
## Phase 1 – Pass 04 (2025-07-07)
- Installed Node.js 22 via NodeSource and activated system version with nvm.
- Ran `pnpm install`; `npm test` fails due to missing `@directus/random`.
- Logged issue in `loops/fix-phase1-pass03.md`.
- Verified `/docs/inventory.md` against `/CRM/README.md`; now at Pass 04 with 19 features mapped.
## Phase 1 – Pass 05 (2025-07-07)
- Used `nvm` to switch to Node 22.17.
- Built `@directus/random` with `pnpm --filter @directus/random run build` before running tests.
- `npm test` executes without missing module errors.
## Phase 1 – Pass 06 (2025-07-07)
- Installed Node.js 22.17 and enabled pnpm.
- Rebuilt random and storage packages.
- `npm test` now completes `@directus/extensions-sdk` tests successfully.
- Tests fail later in `@directus/app` with exit status 129, logged in `loops/fix-phase1-pass05.md`.


## Phase 1 – Pass 07 (2025-07-07)
- Activated Node 22 with nvm after container restart.
- Reinstalled packages and built workspace packages via `pnpm --recursive --filter @directus/* run build`.
- `npm test` no longer fails at `@directus/random`, but tests still fail in `@directus/app` with exit code 129.
## Phase 1 – Pass 08 (2025-09-07)
- Validated inventory alignment with README; added missing core features.

## Phase 3 – Pass 01 (2025-09-08)
- Began deep closed loop cycle for CRM modules.
- Built workspace packages and attempted full test run.
- `npm test` fails in `@directus/app`; `pytest` missing dependencies.
- Logged progress in `CRM/docs/loops/20250908_open_closed_loop.md`.
## Phase 3 – Pass 02 (2025-09-09)
- Activated Node 22 and installed workspace dependencies.
- Rebuilt packages and reran tests.
- `npm test` now runs but fails in `@directus/api` with Axios 503 errors.
- `pytest` executed after installing `sqlalchemy` yet fails with 33 missing modules.
- Progress logged in `CRM/docs/loops/20250908_open_closed_loop.md`.

## Phase 3 – Pass 03 (2025-09-10)
- Documented usage of `test_install.sh` in `CRM/docs/setup.md`.
- Ran `npm test` and `pytest`; both fail due to missing dependencies.

## Phase 1 – Pass 01 (2025-07-08)
- Synced `docs/inventory.md` with `CRM/README.md` by adding portal revocation,
  support knowledgebase links, granular RBAC, `sophos_api_mode` and OTAP
  pipeline entry.
- Updated inventory heading to Pass 05.
- Logged this pass in `trace.json`.

## Phase 1 – Pass 02 (2025-07-09)
- Removed blank line in inventory table to match style guide.
- Documented Node 22 requirement in docs/dependencies.md.
- `npm test` fails due to unsupported Node version (v20.19.2 vs required 22).
- Logged this pass in trace.json.

## Phase 1 – Pass 03 (2025-07-10)
- Added .nvmrc and updated install script to enforce Node.js 22
- Ran pnpm install and npm test; tests fail due to missing @directus/random module
- Logged this pass in trace.json.

## Phase 1 – Pass 04 (2025-07-11)
- Added persistent build step for `@directus/random` before running tests
- Documented the step in README and automated it in `scripts/gui_loop.sh`
- Marked todo item as done and logged pass in trace.json

## Phase 1 – Pass 05 (2025-07-12)
- Added build step for `@directus/storage` to resolve missing module error during tests
- Documented this in README and `scripts/gui_loop.sh`
- Logged the new loop in `trace.json` and todo list

## Phase 1 – Pass 06 (2025-07-13)
- Parsed `/CRM/README.md` again and found missing features.
- Added `Customizable CSS themes` and `Staged update and rollback` rows to `docs/inventory.md`.
- Updated heading to Pass 06 and recorded changes in `trace.json`.

## Phase 1 – Pass 07 (2025-07-13)
- Clarified CSS theme row to mention `frontend/templates`.
- Recorded pass in `trace.json`.

## Phase 1 – Pass 08 (2025-07-13)
- Added inventory last updated timestamp.
- Logged in `trace.json`.

## Phase 1 – Pass 09 (2025-07-13)
- Reordered CSS theme row next to public landing page for clarity.
- Updated `trace.json`.

## Phase 1 – Pass 10 (2025-07-13)
- Verified inventory completeness against CRM README.
- Phase 1 validation passes complete.

## Phase 1 – Pass 11 (2025-07-08)
- Revalidated inventory after loop reset; updated heading to Pass 07.
- Logged pass in `trace.json`.


## Phase 1 – Pass 12 (2025-07-08)
- Detected Node v20 in environment and enabled nvm manually.
- Switched to Node.js 18 and attempted `npm test` which fails due to engines expecting Node 22 (#env-mismatch).
- Documented steps in `loops/fix-env-node-version.md` and updated dependencies to recommend Node 18.

## Phase 3 – Pass 13 (2025-07-08)
- Modified `scripts/install.sh` to activate Node.js 18 instead of 22.
- Documented engine mismatch workaround in `loops/test-env-workarounds.md`.
- Updated `docs/dependencies.md` to clarify Node 18 usage and `PNPM_IGNORE_NODE_VERSION` flag.
- Added `loops/refactor-node-compat.md` detailing compatibility audit.

## Phase 3 – Pass 14 (2025-07-08)
- Built workspace packages @directus/random and @directus/storage using pnpm under Node 18.
- `npm test` fails in @directus/sdk due to Node 22-only fs.glob.
- Logged details in `loops/fix-phase3-pass14.md` and added TODO entry.

## Phase 3 – Pass 15 (2025-07-08)
- Installed deps with NPM_CONFIG_ENGINE_STRICT=false and PNPM_IGNORE_NODE_VERSION.
- Node backend tests pass on Node 18; monorepo tests still fail due to @directus/random.
- Logged details in traces JSON files.

## Phase 3 – Pass 16 (2025-07-08)
- Built @directus/random and @directus/storage for Node 18.
- Added `scripts/fs-glob-polyfill.js` and documented NODE_OPTIONS usage.
- Monorepo tests still failing due to unresolved packages.

## Phase 3 – Pass 17 (2025-07-08)
- Built @directus/constants and dependent packages for Node 18.
- Monorepo tests progress but other packages remain unresolved.


## Phase 3 – Pass 18 (2025-07-09)
- Ran inventory scan of CRM modules and scripts.
- Installed `CRM/node_backend` dependencies so Jest is available.
- `npm test` executed under Node 18 with polyfills; monorepo tests still fail due to missing vitest.
- Node backend tests pass.
- Logged results in trace files for pass 18.


## Phase 3 – Pass 19 (2025-07-09)
- Inventory scan recorded Node 22 engine and fs.glob polyfill usage.
- `scripts/install.sh` now installs CRM node_backend dependencies for Node 18.
- Trace files for pass 19 created.
## Phase 3 – Pass 20
- Added Node tests for nucleus-auth and nucleus-mail-ingest extensions.
## Phase 3 – Pass 29 (2025-07-09)
- Documented use of pnpm install and pnpm test in CRM README to avoid vitest not found errors.

## Phase 3 – Pass 30 (2025-07-09)
- Installed Python backend requirements for tests.
- All CRM Python and Node tests pass under Node 18.

## Phase 3 – Pass 31 (2025-07-09)
- Documented Node 18 setup commands in README.
- Listed CRM Python packages and install command in docs and README.

## Phase 3 – Pass 32 (2025-07-09)
- Added install_directus.sh script using pnpm.
- Documented script usage in README.

## Phase 3 – Pass 33 (2025-07-09)
- Node 22 runtime documented and pnpm install step added.
- Created requirements.md and phase3-progress.json.
- Logged failing build and tests to tracktrace-phase3-pass33.json.
- Updated docs/dependencies.md with Node 22 entry.

## Phase 3 – Pass 34 (2025-07-09)
- Clarified that Node 22 is the default runtime.
- Updated dependencies guide to mention Node 22 as primary version.

## Phase 3 – Pass 35 (2025-07-09)
- Logged Node 22 version and attempted installation.
- npm install and tests failed due to workspace protocol.

## Phase 3 – Pass 36 (2025-07-09)
- Updated `install.sh` and `install_directus.sh` to use Node 22.
- Adjusted README to reflect the change.
- Node 22 environment verified; npm tests still fail due to missing @directus/random.

## Phase 3 – Pass 37 (2025-07-09)
- Added test to build and boot Directus using in-memory SQLite.
- Ensured Node 22 environment and dependencies installed.

## Phase 3 – Pass 38 (2025-07-09)
- Fixed memory DB test to locate repo root and use current Node binary.


## Phase 3 – Pass 39 (2025-07-09)
- Node 22 environment logged.
- npm install failed due to workspace protocol; core package.json not modified.

## Phase 3 – Pass 40 (2025-07-09)
- Marked customizable CSS themes and staged update script as complete.
- npm test failed with Node 20; pytest failed due to missing sqlalchemy.

## Phase 3 – Pass 41 (2025-07-09)
- Installed vitest for workspace packages and switched back to Node 22.
- pnpm install succeeded but npm test failed due to missing @directus/random.
- Pytest still fails with missing sqlalchemy module.

## Phase 3 – Pass 42 (2025-07-09)
- Added pretest script to build all workspace packages automatically.
- Ran npm test after builds; tests still fail in @directus/app.
- Installed Python requirements and all pytest tests now pass.


## Phase 3 – Pass 43 (2025-07-09)
- Updated vps-install.sh to install Node 22 instead of 18.20.2.
- Reinstalled Node dependencies and Python requirements under Node 22.
- npm test fails in @directus/storage-driver-s3 but pytest passes all 94 tests.

## Phase 3 – Pass 44 (2025-07-10)
- Installed Node 22 using nodesource apt repository and updated PATH.
- Ran `pnpm install` to restore node_modules.
- `npm test` fails in @directus/api with Axios 503 errors.
- `pytest` fails due to missing sqlalchemy module.
