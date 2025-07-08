# TODO

## nucleus-auth
- Create authentication schema {status:in-progress} {priority:high} {blocked_by:none}

## nucleus-core
- Register each CRM extension in install.sh {status:in-progress} {priority:medium} {blocked_by:none}
- Automate building workspace packages before tests {status:in-progress} {priority:medium} {blocked_by:none}

## nucleus-api
- Add CI pipeline to run npm and vitest {status:in-progress} {priority:low} {blocked_by:#nucleus-core}
- Fix npm test failure in @directus/app (exit status 129) {status:in-progress} {priority:high} {blocked_by:none}

## nucleus-ui
- Setup role-based tests using lynx {status:in-progress} {priority:medium} {blocked_by:none}
- Document admin features in extensions modules {status:in-progress} {priority:low} {blocked_by:none}
- Implement customizable CSS themes via templates {status:todo} {priority:low} {blocked_by:none}

## repository
- Integrate with upstream Directus build {status:in-progress} {priority:medium} {blocked_by:none}
 - Ensure gui_loop.sh uses headless_check.js via proxy script {status:done} {priority:low} {blocked_by:none}
- Document extensions under /extensions {status:in-progress} {priority:low} {blocked_by:none}
- Enrich `docs/inventory.md` with module/plugin paths for each feature {status:done} {priority:low} {blocked_by:none}
- Revise `docs/inventory.md` to ensure classification table includes these paths {status:done} {priority:low} {blocked_by:none}
- Commit second revision to satisfy two-loop requirement {status:done} {priority:low} {blocked_by:none}
- Document updates in `changelog.md` {status:done} {priority:low} {blocked_by:none}
- Review inventory for completeness in Pass 02 {status:done} {priority:low} {blocked_by:none}
- Install Node 22 via apt using NodeSource repo {status:done} {priority:low} {blocked_by:none}
- Resolve vitest dependency errors during npm test {status:done} {priority:low} {blocked_by:none}
- Fix missing @directus/random module during npm test {status:done} {priority:high} {blocked_by:none}
- Fix missing @directus/storage module during npm test {status:done} {priority:high} {blocked_by:none}
- Implement staged update and rollback script {status:todo} {priority:low} {blocked_by:none}
