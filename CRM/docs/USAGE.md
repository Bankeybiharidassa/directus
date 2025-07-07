# Usage Guide

## Asset Sync

### CLI

```bash
python scripts/asset_cli.py sync --source=all
```

### GUI

Import and render `AssetSyncButton` from `frontend/components` to provide a button that triggers the sync.

## API Configuration

### CLI

```bash
python scripts/config_cli.py set-api --key YOUR_KEY --model gpt-4
python scripts/config_cli.py get-api
```

### GUI

Use `ApiConfigForm` from `frontend/components` to edit and save the API settings.

## Customers Page

### GUI

Render `CustomersPage` from `frontend/pages` to show a list of customers fetched from the backend.

## Security Scan

### CLI

```bash
python scripts/security_scan.py
```

This command performs several checks:

- Package versions are compared against Ubuntu Security Notices and the public CVE database.
- Critical binaries such as `bash` and `ssh` are validated and looked up in the CVE database.
- A Bandit whitebox scan is run on the repository.
- A simple port scan tests common services for open ports.

Results are cached in `security_cache.enc` using Fernet encryption. Set `SEC_SCAN_KEY` to reuse the cache on multiple runs.

### GUI

Open **Admin > Security Scan** in the React frontend and press **Run Security Scan**. The output includes package, binary, whitebox and blackbox results in JSON format.
