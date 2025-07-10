#!/usr/bin/env bash
set -euo pipefail

LOGFILE=/var/log/nucleus/install.log
mkdir -p "$(dirname "$LOGFILE")"
exec > >(tee -a "$LOGFILE") 2>&1

DIRECTUS_DIR=${DIRECTUS_DIR:-directus-app}

step() { echo "==> $1"; }

step "Installing Directus"
if ! command -v directus >/dev/null 2>&1; then
  npm install -g directus
fi

step "Creating project in $DIRECTUS_DIR"
if [ ! -d "$DIRECTUS_DIR" ]; then
  npx directus init "$DIRECTUS_DIR"
fi

step "Copying extensions"
mkdir -p "$DIRECTUS_DIR/extensions"
EXT_SRC="$(dirname "$0")/../extensions"
for ext in "$EXT_SRC"/*; do
  [ -d "$ext" ] || continue
  cp -r "$ext" "$DIRECTUS_DIR/extensions/" 2>/dev/null || true
done

step "Configuring environment"
if [ ! -f "$DIRECTUS_DIR/.env" ]; then
  cp .env.example "$DIRECTUS_DIR/.env"
fi

step "Done"
echo "Run 'npx directus start $DIRECTUS_DIR' to launch Directus"
