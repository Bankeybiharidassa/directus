# System-Level Package Requirements (Ubuntu/Debian)

build-essential
libssl-dev
python3-pip
python3-venv
nvm (install Node.js 22 and optionally 18)
Node.js 22 (via `nvm install 22`)
npm
git
curl
unzip
jq
nmap
Use `nvm use 22` for the main development flow. Node 18 can be enabled with
`nvm use 18` for legacy modules. Set `PNPM_IGNORE_NODE_VERSION=true` and
`NPM_CONFIG_ENGINE_STRICT=false` when running `npm test` under Node 18.
Load the polyfill when using Node 18:
```
export NODE_OPTIONS="--import=$(pwd)/scripts/fs-glob-polyfill.js"
```
to provide `fs.glob` during tests.
Jest is installed locally in `CRM/node_backend` via `npm install` (legacy backend)
Install the Python backend requirements for the legacy services with:

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
