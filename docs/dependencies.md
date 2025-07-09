# System-Level Package Requirements (Ubuntu/Debian)

build-essential
libssl-dev
python3-pip
python3-venv
nvm (install Node.js 18)
npm
git
curl
unzip
jq
nmap
Use `nvm use 18` to activate Node.js 18 for all development and testing.
Some upstream Directus packages declare Node 22 in their `engines` field; set
`PNPM_IGNORE_NODE_VERSION=true` and `NPM_CONFIG_ENGINE_STRICT=false` when running
`npm test` under Node 18.
Load the Node 18 polyfill with:
```
export NODE_OPTIONS="--import=$(pwd)/scripts/fs-glob-polyfill.js"
```
to provide `fs.glob` during tests.
Jest is installed locally in `CRM/node_backend` via `npm install`.
Install the Python backend requirements for tests with:

```bash
pip install -r CRM/backend/requirements.txt
```

The backend requires the following packages:

- fastapi
- uvicorn
- sqlalchemy
- httpx
- pyotp
- fpdf2
- PyYAML
- psutil
- cryptography
- requests
