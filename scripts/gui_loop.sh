#!/usr/bin/env bash
set -euo pipefail

# Proxy to the CRM implementation so role-based tests run via lynx
CRM_LOOP="CRM/scripts/gui_loop.sh"
if [[ -x "$CRM_LOOP" ]]; then
  exec "$CRM_LOOP" "$@"
else
  echo "Missing $CRM_LOOP" >&2
  exit 1
fi
