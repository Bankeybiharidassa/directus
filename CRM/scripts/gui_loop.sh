#!/usr/bin/env bash
set -euo pipefail

bash test_install.sh > /tmp/test_install.log 2>&1 &
SERV_PID=$!
# Wait for services to come up
sleep 10

node scripts/headless_check.js > logs/headless.log 2>&1 || true

roles=(admin support company distributor partner enduser)
for role in "${roles[@]}"; do
  lynx -accept_all_cookies -dump "http://127.0.0.1:8000/core/login?role=${role}" > "logs/lynx_${role}.txt" || true
done

kill $SERV_PID
sleep 2
pkill -f uvicorn || true
pkill -f node || true
