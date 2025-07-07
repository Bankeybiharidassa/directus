#!/bin/bash
set -e

SERVICES=(nucleus-backend.service nucleus-auth.service)

usage(){
  echo "Usage: $0 {start|stop|restart|status}" >&2
  exit 1
}

[ $# -eq 1 ] || usage

for svc in "${SERVICES[@]}"; do
  case $1 in
    start) systemctl start "$svc";;
    stop) systemctl stop "$svc";;
    restart) systemctl restart "$svc";;
    status) systemctl status "$svc";;
    *) usage;;
  esac
done

