#!/usr/bin/env bash
set -euo pipefail

# Correct file and directory permissions for the CRM project
# Usage: sudo ./scripts/set_permissions.sh [project_dir] [user]

TARGET_DIR="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
OWNER="${2:-}"
LOG_DIR="/var/log/nucleus"

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root" >&2
  exit 1
fi

if [ -z "$OWNER" ]; then
  if [ -f /etc/systemd/system/nucleus-backend.service ]; then
    OWNER=$(awk -F= '/^User=/ {print $2; exit}' /etc/systemd/system/nucleus-backend.service)
  fi
  OWNER=${OWNER:-nucleus}
fi

USER_NAME="$OWNER"

# Ensure ownership
chown -R "$USER_NAME":"$USER_NAME" "$TARGET_DIR"

# Directories need execute bit
find "$TARGET_DIR" -type d -exec chmod 755 {} \;
# Only update non-executable files so binaries keep their original x bit
find "$TARGET_DIR" -type f ! -perm /111 -exec chmod 644 {} \;
# Shell scripts remain executable
find "$TARGET_DIR/scripts" -type f -name '*.sh' -exec chmod 755 {} \;
# Ensure binaries inside bin/ directories keep the execute bit
find "$TARGET_DIR" -path '*/bin/*' -type f -exec chmod 755 {} \;

# Log directory for service logs
mkdir -p "$LOG_DIR"
touch "$LOG_DIR/sophos.log" "$LOG_DIR/tenable.log" "$LOG_DIR/dmarc.log" \
  "$LOG_DIR/acme.log" "$LOG_DIR/crm_sync.log"
chown -R "$USER_NAME":"$USER_NAME" "$TARGET_DIR/logs" "$LOG_DIR"
chmod 755 "$TARGET_DIR/logs" "$LOG_DIR"
chmod 664 "$LOG_DIR"/*.log

echo "Permissions corrected for $TARGET_DIR and $LOG_DIR (owner: $OWNER)"
