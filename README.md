
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

Run tests with:

```bash
npm test
```

## Testing the GUI

Run `scripts/gui_loop.sh` to install dependencies, launch the services and
execute the headless browser checks via `scripts/headless_check.js`. Results are
stored in the `logs/` directory.

