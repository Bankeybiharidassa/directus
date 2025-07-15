
# Directus CRM Workspace

This repository bundles Directus with a set of Nucleus extensions. The original `readme.md` provides upstream documentation.

- `CRM/` holds the legacy CRM implementation used only for reference
- `extensions/` contains the active Directus extensions
- `scripts/install.sh` installs dependencies

# Nucleus CRM Extensions

The CRM directory is retained only for legacy reference. All new modules are implemented as Directus extensions under `extensions/`.
Legacy docs remain at [CRM/README.md](CRM/README.md) but no runtime code depends on them.
See readme.md for Directus upstream instructions.
Detailed feature inventory lives in docs/inventory.md.

Audit findings are summarized in AUDIT.md with a step-by-step plan. Outstanding tasks are listed in todo.md and expanded in docs/action_plan.md.

Custom extensions belong in the `extensions/` directory. A basic `nucleus-core`
plugin is included which logs a startup message when Directus loads.

Copy `.env.example` to `.env` and adjust values before running `scripts/install.sh`.

## Build Instructions

Execute the installer script to install dependencies and enable all extensions:

```bash
./scripts/install.sh
```

Alternatively run `./bundle_install.sh` as root for an automated server
setup. This installs Node 22, configures Keycloak and Directus services
and provisions HTTPS via Let's Encrypt.

Before running tests, build the workspace packages used in vitest:

```bash
pnpm --filter @directus/random run build
pnpm --filter @directus/storage run build
npm test
```

### Node.js 22 Runtime (Default)

Directus packages list Node 22 in their `engines` field. Use Node 22 for all
regular development and builds:

```bash
nvm use 22
pnpm install

# Trust mise version files to suppress warnings
mise trust .mise.toml
```

Always run `pnpm install` with Node 22 before executing `npm test`. Skipping this
step leads to `Unsupported URL Type "workspace:"` errors because `npm install`
cannot resolve workspace protocols.

`npm install` is not supported at the repository root because the monorepo uses
the `workspace:` protocol. Use `pnpm install` or run `scripts/install.sh` to
install all dependencies.
### Verifying extension structure
Run `node extensions/check_extensions.cjs` to list each extension and verify that required files are present.


### Node.js 18 Compatibility

Older CRM modules can still run on Node 18. Use `nvm` to switch and bypass the
package engines check:

```bash
nvm use 18
export PNPM_IGNORE_NODE_VERSION=true
export NPM_CONFIG_ENGINE_STRICT=false
export NODE_OPTIONS="--import=$(pwd)/scripts/fs-glob-polyfill.js"
pnpm install
npm install --prefix CRM/node_backend   # legacy backend tests only
```

`scripts/install_directus.sh` now uses Node 22 by default. If you need to run
the project under Node 18, execute the above commands manually instead of the
helper script.

This script loads a polyfill for `fs.glob` and installs Jest for the CRM backend
before executing `pnpm --workspace-root test` and `python3 -m pytest -q`.

## Testing the GUI

Run `CRM/test_install.sh` first to start the legacy backend and auth services locally.
After the services are active, execute `scripts/gui_loop.sh` to install
dependencies and run the headless browser checks via `scripts/headless_check.js`.
Results are stored in the `logs/` directory.

