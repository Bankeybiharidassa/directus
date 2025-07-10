# open-closed-loop_pass50
Switched to Node 22 using nvm and reinstalled all dependencies with `pnpm install` to solve the workspace protocol error.
Ran `npm test` which still fails in `@directus/extensions-sdk` with vitest exit code 129.
Installed required Python packages and executed `pytest` which passes all 94 tests.
Logs saved as `logs/pnpm_install_pass50.log`, `logs/npm_pass50.log`, `logs/pytest_pass50.log`.
