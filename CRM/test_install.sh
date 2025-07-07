#!/usr/bin/env bash
set -euo pipefail
LOGFILE=/var/log/nucleus/test_install.log
mkdir -p "$(dirname "$LOGFILE")"
: > "$LOGFILE"

# Activate or create venv
if [ ! -d venv ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r backend/requirements.txt >>"$LOGFILE" 2>&1
npm install --production --prefix node_backend >>"$LOGFILE" 2>&1

# Launch backend and auth services
python3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 >>"$LOGFILE" 2>&1 &
BACKEND_PID=$!
node node_backend/index.js >>"$LOGFILE" 2>&1 &
AUTH_PID=$!

check_port() {
  local port=$1
  for _ in {1..15}; do
    if curl -fs "http://127.0.0.1:$port/health" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done
  return 1
}

if ! check_port 8000 || ! curl -fs http://127.0.0.1:3001/status >/dev/null 2>&1; then
  echo "Services failed to start" | tee -a "$LOGFILE"
  kill $BACKEND_PID $AUTH_PID
  exit 1
fi

echo "Backend on http://127.0.0.1:8000" | tee -a "$LOGFILE"
echo "Auth on http://127.0.0.1:3001" | tee -a "$LOGFILE"
echo "Use lynx http://127.0.0.1:8000/core/login" | tee -a "$LOGFILE"
wait
