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

