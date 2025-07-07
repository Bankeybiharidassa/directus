#!/usr/bin/env bash
set -euo pipefail

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root" >&2
  exit 1
fi

APP_DIR=/opt/nucleus-platform/CRM
read -r -p "GitHub repo (owner/repo): " GH_REPO
read -r -p "GitHub username: " GH_USER
read -r -s -p "GitHub token (PAT): " GH_TOKEN; echo

if [ -d "$APP_DIR/.git" ]; then
  git -C "$APP_DIR" pull "https://${GH_USER}:${GH_TOKEN}@github.com/${GH_REPO}.git"
else
  git clone "https://${GH_USER}:${GH_TOKEN}@github.com/${GH_REPO}.git" "$APP_DIR"
fi

# service account to run the backend and auth services
USER_NAME=${SERVICE_USER:-nucleus}
APP_PORT=8000
AUTH_PORT=3001

# create service user when missing (defaults to "nucleus")
if ! id "$USER_NAME" >/dev/null 2>&1; then
  echo "Creating service user $USER_NAME"
  groupadd -f "$USER_NAME"
  useradd -r -g "$USER_NAME" -s /usr/sbin/nologin "$USER_NAME"
  usermod -aG adm "$USER_NAME" || true
fi

mkdir -p /var/log/nucleus
chown "$USER_NAME" /var/log/nucleus || true
sed "s|/opt/nucleus-platform/CRM|$APP_DIR|g; s|8000|$APP_PORT|g; s|User=nucleus|User=$USER_NAME|" "$APP_DIR/services/nucleus_backend.service" > /etc/systemd/system/nucleus-backend.service
sed "s|/opt/nucleus-platform/CRM|$APP_DIR|g; s|User=nucleus|User=$USER_NAME|" "$APP_DIR/services/nucleus_auth.service" > /etc/systemd/system/nucleus-auth.service

# ensure dependencies are installed
python3 -m pip install --break-system-packages -r "$APP_DIR/backend/requirements.txt"
npm install --production --prefix "$APP_DIR/node_backend"

# remove stale Python bytecode
find "$APP_DIR" -name '*.pyc' -delete

# ensure auth service uses dedicated port
if [ -f "$APP_DIR/.env" ]; then
  sed -i "s/^PORT=.*/PORT=${AUTH_PORT}/" "$APP_DIR/.env"
fi

# create log files and set ownership
"$APP_DIR/scripts/set_permissions.sh" "$APP_DIR" "$USER_NAME"

systemctl daemon-reload
systemctl enable --now nucleus-backend.service
systemctl enable --now nucleus-auth.service

echo "Services installed and running."
