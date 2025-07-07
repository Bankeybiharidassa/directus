#!/usr/bin/env bash
set -euo pipefail

UPDATED_PKGS_FILE=/tmp/updated_pkgs.txt
LOG_FILE=/var/log/maintenance.log
CHECKSUM_FILE=/var/lib/maintenance/checksums

mkdir -p "$(dirname "$CHECKSUM_FILE")"
touch "$LOG_FILE" "$CHECKSUM_FILE"

log() {
  echo "$(date '+%F %T') $*" | tee -a "$LOG_FILE"
}

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root" >&2
  exit 1
fi

env_file=/opt/nucleus-platform/.env
config_file=/opt/nucleus-platform/config/settings.yaml

checksum_file_update() {
  local file=$1
  [ -f "$file" ] || return
  local sum
  sum=$(md5sum "$file")
  grep -v " $file$" "$CHECKSUM_FILE" > "$CHECKSUM_FILE.tmp" && mv "$CHECKSUM_FILE.tmp" "$CHECKSUM_FILE"
  echo "$sum" >> "$CHECKSUM_FILE"
}

detect_config_changes() {
  for f in "$env_file" "$config_file"; do
    [ -f "$f" ] || continue
    local new_sum old_sum
    new_sum=$(md5sum "$f" | cut -d' ' -f1)
    old_sum=$(grep " $f$" "$CHECKSUM_FILE" | cut -d' ' -f1 || true)
    if [ -n "$old_sum" ] && [ "$new_sum" != "$old_sum" ]; then
      echo "Warning: $f was modified" >&2
      log "WARNING: $f was modified"
    fi
    checksum_file_update "$f"
  done
}

update_system() {
  log "Updating base system"
  apt update
  mapfile -t pkgs < <(apt list --upgradable 2>/dev/null | awk -F/ 'NR>1 {print $1}')
  if [ ${#pkgs[@]} -gt 0 ]; then
    DEBIAN_FRONTEND=noninteractive apt upgrade -y
    printf "%s\n" "${pkgs[@]}" > "$UPDATED_PKGS_FILE"
    log "Packages updated: ${pkgs[*]}"
    detect_config_changes
  else
    echo "System is already up to date."
    log "System already up to date"
    : > "$UPDATED_PKGS_FILE"
  fi
}

hardening_check() {
  log "Running hardening checks"
  if ! command -v ufw >/dev/null; then
    apt install -y ufw
  fi
  ufw status | grep -q active || ufw --force enable

  if grep -q '^PermitRootLogin\s\+no' /etc/ssh/sshd_config; then
    echo "SSH root login already disabled"
  else
    sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
    systemctl reload sshd
    echo "Disabled SSH root login"
  fi

  if ! dpkg -s unattended-upgrades >/dev/null 2>&1; then
    apt install -y unattended-upgrades
  fi

  for rule in \
    "net.ipv4.ip_forward=0" \
    "net.ipv4.conf.all.rp_filter=1" \
    "net.ipv4.conf.default.rp_filter=1"; do
    key=${rule%%=*}; val=${rule#*=}
    cur=$(sysctl -n "$key" 2>/dev/null || echo "")
    if [ "$cur" != "$val" ]; then
      sysctl -w "$key=$val" >/dev/null
      log "Set $key=$val"
    fi
  done
  detect_config_changes
}

git_pull() {
  local repo_path=/opt/nucleus-platform
  if [ ! -d "$repo_path/.git" ]; then
    echo "Invalid git repository: $repo_path"
    log "Repository missing: $repo_path"
    return 1
  fi
  if [ -n "$(git -C "$repo_path" status --porcelain)" ]; then
    echo "Warning: local changes detected in $repo_path. Proceed? (y/N)" >&2
    read -r ans
    if [ "$ans" != "y" ]; then
      log "Git pull cancelled due to local changes"
      return 0
    fi
  fi
  read -r -p "GitHub repo (owner/repo): " gh_repo
  read -r -p "GitHub username: " gh_user
  read -r -s -p "GitHub token (PAT): " gh_token
  echo
  if git -C "$repo_path" pull "https://${gh_user}:${gh_token}@github.com/${gh_repo}.git"; then
    log "Pulled $gh_repo into $repo_path"
    detect_config_changes
  else
    log "Git pull failed for $gh_repo"
  fi
}

restart_services() {
  [ ! -f "$UPDATED_PKGS_FILE" ] && { echo "No package update data - run system update first"; return; }
  local services=()
  for pkg in $(cat "$UPDATED_PKGS_FILE"); do
    svc_files=$(dpkg -L "$pkg" 2>/dev/null | grep -E '/systemd/system/.*\.service$' || true)
    for file in $svc_files; do
      svc=$(basename "$file")
      if systemctl restart "$svc" 2>/dev/null; then
        services+=("$svc")
      fi
    done
  done
  if [ ${#services[@]} -eq 0 ]; then
    echo "No services restarted."
    log "No services restarted"
  else
    echo "Restarted services: ${services[*]}"
    log "Restarted services: ${services[*]}"
  fi
}

while true; do
  echo "Please select an action:"
  echo "1) Update base system"
  echo "2) Run system hardening check"
  echo "3) Pull latest project updates"
  echo "4) Restart updated services"
  echo "5) Exit"
  read -r -p "Selection: " choice
  case $choice in
    1) update_system;;
    2) hardening_check;;
    3) git_pull;;
    4) restart_services;;
    5) exit 0;;
    *) echo "Invalid option";;
  esac
  echo
done
