#!/usr/bin/env bash
set -euo pipefail


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="/opt/nucleus-platform/CRM"
CHANGES_BASE="$(dirname "$REPO_DIR")/changed_local"
mkdir -p "$REPO_DIR" "$CHANGES_BASE"


if [ "$EUID" -ne 0 ]; then
  echo "Please run as root" >&2
  exit 1
fi

cd "$REPO_DIR"
if [ ! -d .git ]; then
  echo "No repository found in $REPO_DIR"
  read -r -p "GitHub repo (owner/repo): " GH_REPO
  read -r -p "GitHub username: " GH_USER
  read -r -s -p "GitHub token (PAT): " GH_TOKEN; echo
  git clone "https://${GH_USER}:${GH_TOKEN}@github.com/${GH_REPO}.git" "$REPO_DIR"
  cd "$REPO_DIR"
fi

if [ -z "${GH_REPO:-}" ]; then
  GH_REPO=$(git remote get-url origin | sed -E 's|.*github.com[:/](.+)\.git|\1|' || true)
fi
if [ -z "${GH_USER:-}" ]; then
  read -r -p "GitHub username: " GH_USER
fi
if [ -z "${GH_TOKEN:-}" ]; then
  read -r -s -p "GitHub token (PAT): " GH_TOKEN; echo
fi

if [ -n "$(git status --porcelain)" ]; then
  ts="$(date +%Y%m%d-%H%M%S)"
  dest="$CHANGES_BASE/$ts"
  mkdir -p "$dest"
  git diff > "$dest/changes.patch"
  git ls-files --others --exclude-standard -z | while IFS= read -r -d '' f; do
    mkdir -p "$dest/$(dirname "$f")"
    cp -a "$f" "$dest/$f"
  done
  git stash push -u -m "update_now_$ts"
fi

# push any local commits so they are logged before pulling updates
current_branch=$(git rev-parse --abbrev-ref HEAD)
git push "https://${GH_USER}:${GH_TOKEN}@github.com/${GH_REPO}.git" "HEAD:${current_branch}" || true

git pull "https://${GH_USER}:${GH_TOKEN}@github.com/${GH_REPO}.git" "$current_branch" --ff-only

# reinstall dependencies only when missing to avoid overwriting system packages
missing_packages=()
while read -r pkg; do
    pkg_name=$(echo "$pkg" | cut -d'=' -f1 | cut -d'<' -f1 | cut -d'>' -f1)
    if ! python3 -m pip show "$pkg_name" >/dev/null 2>&1; then
        missing_packages+=("$pkg")
    fi
done < "$REPO_DIR/backend/requirements.txt"
if [ ${#missing_packages[@]} -ne 0 ]; then
    python3 -m pip install --break-system-packages "${missing_packages[@]}"
fi
npm install --production --prefix "$REPO_DIR/node_backend"

# remove old bytecode that may reference outdated paths
find "$REPO_DIR" -name '*.pyc' -delete

# determine service user from systemd unit if available
SERVICE_USER=$(awk -F= '/^User=/ {print $2; exit}' /etc/systemd/system/nucleus-backend.service 2>/dev/null || echo nucleus)

# create the user when missing
if ! id "$SERVICE_USER" >/dev/null 2>&1; then
    echo "Creating user $SERVICE_USER"
    groupadd -f "$SERVICE_USER"
    useradd -r -g "$SERVICE_USER" -s /usr/sbin/nologin "$SERVICE_USER"
    usermod -aG adm "$SERVICE_USER" || true
fi

"$REPO_DIR/scripts/set_permissions.sh" "$REPO_DIR" "$SERVICE_USER"

echo "Update completed."
