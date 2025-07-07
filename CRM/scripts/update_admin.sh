#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PY_ENV="$PROJECT_DIR/venv"
NODE_DB="$PROJECT_DIR/node_backend/auth.db"

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root" >&2
  exit 1
fi

read -r -p "Admin username: " ADMIN_USER
read -r -s -p "New password: " ADMIN_PASS
echo

if [ -f "$PY_ENV/bin/activate" ]; then
  # Use project virtual environment when available
  source "$PY_ENV/bin/activate"
else
  echo "Warning: virtualenv not found at $PY_ENV, using system Python" >&2
fi
python <<PYEOF
from backend import settings
from backend.database import SessionLocal, Base, engine
from backend.models import User, Role, UserRole
settings.apply_env()
Base.metadata.create_all(bind=engine)
db = SessionLocal()
user = db.query(User).filter_by(username="${ADMIN_USER}").first()
if not user:
    user = User(username="${ADMIN_USER}", password="${ADMIN_PASS}")
    db.add(user)
else:
    user.password = "${ADMIN_PASS}"
role = db.query(Role).filter_by(name="admin").first()
if not role:
    role = Role(name="admin")
    db.add(role)
    db.flush()
if not db.query(UserRole).filter_by(user_id=user.id, role_id=role.id).first():
    db.add(UserRole(user_id=user.id, role_id=role.id))
db.commit()
db.close()
PYEOF
[ -f "$PY_ENV/bin/activate" ] && deactivate

cat <<'NODE' > "$PROJECT_DIR/node_backend/reset_node_admin.js"
const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcryptjs');
const db = new sqlite3.Database(process.env.AUTH_DB || 'auth.db');
const user = process.argv[2];
const pass = process.argv[3];
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    totp_secret TEXT,
    login_count INTEGER DEFAULT 0
  )`);
  const hash = bcrypt.hashSync(pass, 10);
  db.run('DELETE FROM users WHERE username = ?', [user], () => {
    db.run('INSERT INTO users (username, password) VALUES (?, ?)', [user, hash], () => db.close());
  });
});
NODE
node "$PROJECT_DIR/node_backend/reset_node_admin.js" "$ADMIN_USER" "$ADMIN_PASS"
rm "$PROJECT_DIR/node_backend/reset_node_admin.js"

echo "Admin account reset for $ADMIN_USER"
