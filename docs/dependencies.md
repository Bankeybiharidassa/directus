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
`PNPM_IGNORE_NODE_VERSION=true` when running `npm test` under Node 18.
