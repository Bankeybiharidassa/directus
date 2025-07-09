
# Directus CRM Workspace

This repository bundles Directus with a Nucleus CRM example. The original `readme.md` provides upstream documentation.

- `CRM/` contains the custom CRM modules
- `extensions/` holds additional Directus extensions
- `scripts/install.sh` installs dependencies

# Nucleus CRM Extensions

This repository contains a modular Directus setup with the Nucleus CRM code in the `CRM/` directory.
Refer to [CRM/README.md](CRM/README.md) for full documentation.
See readme.md for Directus upstream instructions.
Detailed feature inventory lives in docs/inventory.md.

Copy `.env.example` to `.env` and adjust values before running `scripts/install.sh`.

## Build Instructions

Execute the installer script to install dependencies and enable all extensions:

```bash
./scripts/install.sh
```

Before running tests, build the workspace packages used in vitest:

```bash
pnpm --filter @directus/random run build
pnpm --filter @directus/storage run build
npm test
```

### Node.js 18 Compatibility

Run the workspace on Node 18 using `nvm` and bypass the engines check:

```bash
nvm use 18
export PNPM_IGNORE_NODE_VERSION=true
export NPM_CONFIG_ENGINE_STRICT=false
export NODE_OPTIONS="--import=$(pwd)/scripts/fs-glob-polyfill.js"
pnpm install
npm install --prefix CRM/node_backend
```

You can automate these commands using `scripts/install_directus.sh`:

```bash
./scripts/install_directus.sh
```

This loads a polyfill for `fs.glob` and installs Jest for the CRM backend before
executing `pnpm --workspace-root test` and `python3 -m pytest -q`.

## Testing the GUI

Run `scripts/gui_loop.sh` to install dependencies, launch the services and
execute the headless browser checks via `scripts/headless_check.js`. Results are
stored in the `logs/` directory.

