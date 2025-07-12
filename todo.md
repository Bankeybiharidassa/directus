# TODO

## nucleus-auth
- Create authentication schema {status:done} {priority:high} {blocked_by:none}

## nucleus-core
- Register each CRM extension in install.sh {status:done} {priority:medium} {blocked_by:none}
 - Automate building workspace packages before tests {status:done} {priority:medium} {blocked_by:none}

## nucleus-api
- Add CI pipeline to run npm and vitest {status:done} {priority:low} {blocked_by:#nucleus-core}
- Fix npm test failure in @directus/app (exit status 129) {status:in-progress} {priority:high} {blocked_by:none}

## nucleus-ui
- Setup role-based tests using lynx {status:done} {priority:medium} {blocked_by:none}
- Document admin features in extensions modules {status:done} {priority:low} {blocked_by:none}
- Implement customizable CSS themes via templates {status:done} {priority:low} {blocked_by:none}

## repository
- Integrate with upstream Directus build {status:in-progress} {priority:medium} {blocked_by:none}
 - Ensure gui_loop.sh uses headless_check.js via proxy script {status:done} {priority:low} {blocked_by:none}
- Document extensions under /extensions {status:done} {priority:low} {blocked_by:none}
- Enrich `docs/inventory.md` with module/plugin paths for each feature {status:done} {priority:low} {blocked_by:none}
- Revise `docs/inventory.md` to ensure classification table includes these paths {status:done} {priority:low} {blocked_by:none}
- Commit second revision to satisfy two-loop requirement {status:done} {priority:low} {blocked_by:none}
- Document updates in `changelog.md` {status:done} {priority:low} {blocked_by:none}
- Review inventory for completeness in Pass 02 {status:done} {priority:low} {blocked_by:none}
- Install Node 22 via apt using NodeSource repo {status:done} {priority:low} {blocked_by:none}
- Resolve vitest dependency errors during npm test {status:done} {priority:low} {blocked_by:none}
- Fix missing @directus/random module during npm test {status:done} {priority:high} {blocked_by:none}
- Fix missing @directus/storage module during npm test {status:done} {priority:high} {blocked_by:none}
- Fix missing @directus/constants module during npm test {status:done} {priority:high} {blocked_by:none}
- Implement staged update and rollback script {status:done} {priority:low} {blocked_by:none}
- Adapt @directus/sdk tests for Node 18 or polyfill fs.glob {status:in-progress} {priority:medium} {blocked_by:none}
- Verify monorepo tests with Node 18 once fs.glob polyfill is added {status:in-progress} {priority:medium} {blocked_by:none}
- Install vitest for workspace packages to run monorepo tests {status:done} {priority:medium} {blocked_by:none}
- [pass20] Fix maintenance tests path
- [pass20] Created tests for nucleus-auth and mail-ingest
- [pass29] Document pnpm installation and test steps in README {status:done} {priority:low}
- [pass30] Install Python backend dependencies and run tests {status:done} {priority:low}
- [pass31] Document Node 18 test setup in README {status:done} {priority:low}
- [pass32] Add install_directus.sh script using pnpm {status:done} {priority:medium}
- [pass33] Build and test pipeline failing due to missing vitest modules and sqlalchemy {status:done}
- [pass34] Update docs to emphasize Node 22 as default runtime {status:done} {priority:low}
- [pass36] Update install scripts to use Node 22 {status:done} {priority:low}
 - Resolve npm install workspace protocol issues {status:done} {priority:high} {blocked_by:none}
- [pass37] Added build and boot memory DB tests {status:done} {priority:low}
- [pass38] Fix memory DB test path and node usage {status:done} {priority:low}
- Document running CRM/test_install.sh before GUI testing {status:done} {priority:low} {blocked_by:none}
- [pass50] Investigate vitest exit code 129 in extensions-sdk tests {status:open} {priority:medium} {blocked_by:none}
- [pass51] Created nucleus-core extension; npm test still fails with vitest exit code 129 {status:in-progress} {priority:medium} {blocked_by:none}

- [pass52] npm test fails in @directus/api due to port 503 error {status:open} {priority:medium}

- [pass53] npm test fails again in @directus/api with ERR_PNPM_RECURSIVE_RUN_FIRST_FAIL {status:open} {priority:medium}

- [pass54] npm test fails with Axios 503 in @directus/api {status:open} {priority:medium}
- [pass55] Add Keycloak auth extension and tests {status:done} {priority:low}
- [pass56] Scaffold remaining Directus extensions {status:done} {priority:low}
- [pass57] Migrated auth/mail ingest extensions to root {status:done} {priority:low}
- [pass58] Document full implementation plan for remaining extensions {status:done} {priority:low}
- [pass59] Install Python requirements to fix sqlalchemy error {status:done} {priority:low}
- [pass60] Replace placeholder Keycloak auth with real token exchange {status:done} {priority:low}
- [pass61] Flesh out docs, edi and portal extensions {status:done} {priority:low}

- [pass62] Add tests for nucleus-docs extension {status:done} {priority:low}
- [pass63] Verify extension structure and note npm test failure (exit code 129)
- [pass64] Add auth schema and token tests {status:done} {priority:low}
- [pass65] Add role mapping and token exchange route {status:done} {priority:low}
- [pass66] Configure mise to honor .nvmrc {status:done} {priority:low}
- [pass67] Document bundle_install.sh usage and validate script {status:done} {priority:low}
- [pass68] Trust mise config to remove warnings and update docs {status:done} {priority:low}
- [pass69] Replace placeholders in extensions with minimal routes; npm test fails (ERR_PNPM_RECURSIVE_RUN_FIRST_FAIL)
- [pass70] Document CRM folder as legacy; tests still failing
- [pass71] Add env-based theme support to nucleus-ui {status:done} {priority:low}
