#!/usr/bin/env bash
set -euo pipefail

LOG_DIR=/var/log/nucleus
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/install_directus.log"

# Activate Node 18 via nvm when available
if command -v nvm >/dev/null 2>&1; then
  nvm install 18 >>"$LOG_FILE" 2>&1
  nvm use 18 >>"$LOG_FILE" 2>&1
fi

# Allow pnpm to run under Node 18
export PNPM_IGNORE_NODE_VERSION=true
export NODE_OPTIONS="--import=$(pwd)/scripts/fs-glob-polyfill.js"

echo "Installing monorepo dependencies via pnpm" | tee "$LOG_FILE"
pnpm install --silent >>"$LOG_FILE" 2>&1

if [ -d CRM/node_backend ]; then
  echo "Installing CRM node_backend deps" | tee -a "$LOG_FILE"
  npm install --prefix CRM/node_backend --silent >>"$LOG_FILE" 2>&1
fi

echo "Installation complete" | tee -a "$LOG_FILE"
