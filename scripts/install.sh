
#!/bin/bash
# Install Directus CRM extensions and register local modules
set -e

LOG_DIR=/var/log/nucleus
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/install.log"

# Ensure Node.js 22 is active for installation
if command -v nvm >/dev/null 2>&1; then
  nvm install 22 >> "$LOG_FILE" 2>&1
  nvm use 22 >> "$LOG_FILE" 2>&1
  nvm alias default 22 >> "$LOG_FILE" 2>&1
fi

# Load environment values if present
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "Installing dependencies..." | tee "$LOG_FILE"
pnpm install --silent >> "$LOG_FILE" 2>&1

# Install node_backend dependencies for tests
if [ -d CRM/node_backend ]; then
  echo "Installing CRM node_backend dependencies" | tee -a "$LOG_FILE"
  npm install --prefix CRM/node_backend --silent >> "$LOG_FILE" 2>&1
fi

for EXT in extensions/*; do
  if [ -d "$EXT" ]; then
    echo "Registering extension $EXT" | tee -a "$LOG_FILE"
    npx directus extension install "$EXT" >> "$LOG_FILE" 2>&1 || true
  fi
done

echo "Setup complete." | tee -a "$LOG_FILE"

