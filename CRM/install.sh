#!/usr/bin/env bash
set -euo pipefail

LOGFILE=/var/log/nucleus_install.log
mkdir -p "$(dirname "$LOGFILE")"
touch "$LOGFILE"
exec > >(tee -a "$LOGFILE") 2>&1

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root" >&2
  exit 1
fi

APP_BASE=/opt/nucleus-platform
APP_PORT=8000
AUTH_PORT=3001

CRED_FILE=$HOME/.nucleus_install_cache
[ -f "$CRED_FILE" ] && source "$CRED_FILE"
touch "$CRED_FILE" && chmod 600 "$CRED_FILE"
trap 'rm -f "$CRED_FILE"' EXIT

prompt(){
  local var=$1 msg=$2
  if [ -z "${!var:-}" ]; then
    read -r -p "$msg" "$var"
    printf 'export %s=%q\n' "$var" "${!var}" >> "$CRED_FILE"
  fi
}
prompt_secret(){
  local var=$1 msg=$2
  if [ -z "${!var:-}" ]; then
    read -r -s -p "$msg" "$var"; echo
    printf 'export %s=%q\n' "$var" "${!var}" >> "$CRED_FILE"
  fi
}
step(){ echo; echo "==== $1 ===="; }

step "[1/8] System update and dependencies"
apt update
apt upgrade -y
apt install -y git curl wget unzip sudo nano mariadb-server mariadb-client python3 python3-pip python3-venv nginx ufw gh
if ! command -v node >/dev/null; then
  curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
  apt install -y nodejs
fi
npm install -g yarn >/dev/null 2>&1 || true
systemctl enable --now mariadb

step "[2/8] Database setup"
MYSQL_OPTS=(-u root)
if mysql "${MYSQL_OPTS[@]}" -e "SELECT 1" >/dev/null 2>&1; then
  echo "MariaDB root has no password"
else
  while true; do
    prompt_secret DB_ROOT_PW "Enter MariaDB root password: "
    MYSQL_OPTS=(-u root -p"$DB_ROOT_PW")
    if mysql "${MYSQL_OPTS[@]}" -e "SELECT 1" >/dev/null 2>&1; then
      break
    fi
    echo "Incorrect password"
  done
fi

prompt DB_NAME "Database name [nucleus]: "
DB_NAME=${DB_NAME:-nucleus}
prompt DB_USER "Database user [nucleus]: "
DB_USER=${DB_USER:-nucleus}
prompt_secret DB_PASS "Database user password: "

if ! mysql "${MYSQL_OPTS[@]}" -e "USE \`${DB_NAME}\`" >/dev/null 2>&1; then
  mysql "${MYSQL_OPTS[@]}" -e "CREATE DATABASE \`${DB_NAME}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
fi
if ! mysql "${MYSQL_OPTS[@]}" -e "SELECT User FROM mysql.user WHERE User='${DB_USER}'" | grep -q "${DB_USER}"; then
  mysql "${MYSQL_OPTS[@]}" -e "CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';"
fi
mysql "${MYSQL_OPTS[@]}" -e "GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${DB_USER}'@'localhost'; FLUSH PRIVILEGES;"

step "[3/8] Clone repository"
prompt GH_REPO "GitHub repo (owner/repo): "
prompt GH_USER "GitHub username: "
prompt_secret GH_TOKEN "GitHub token (PAT): "
REPO_NAME=$(basename "$GH_REPO")
APP_DIR=$APP_BASE/$REPO_NAME
PY_ENV=$APP_DIR/venv

if [ -d "$APP_DIR/.git" ]; then
  echo "Repository already exists at $APP_DIR, pulling latest changes"
  git -C "$APP_DIR" pull https://${GH_USER}:${GH_TOKEN}@github.com/${GH_REPO}.git
else
  mkdir -p "$APP_BASE"
  git clone https://${GH_USER}:${GH_TOKEN}@github.com/${GH_REPO}.git "$APP_DIR"
  chown -R $SUDO_USER:$SUDO_USER "$APP_DIR" || true
fi

step "[4/8] Configure environment and install dependencies"
cd "$APP_DIR"
mkdir -p "$APP_DIR/logs"
if [ ! -f config/.env.template ]; then
  cat >config/.env.template <<'EOF'
DB_HOST=localhost
DB_USER=nucleus
DB_PASS=change_me
IMAP_HOST=imap.yourdomain.tld
IMAP_USER=
IMAP_PASSWORD=
SOPHOS_URL=
SOPHOS_TOKEN=
TENABLE_URL=
TENABLE_TOKEN=
PORT=3001
EOF
fi

if [ ! -f .env ]; then
  cp config/.env.template .env
  sed -i "s/^DB_HOST=.*/DB_HOST=localhost/" .env
  sed -i "s/^DB_USER=.*/DB_USER=${DB_USER}/" .env
  sed -i "s/^DB_PASS=.*/DB_PASS=${DB_PASS}/" .env
  sed -i "s/^PORT=.*/PORT=${AUTH_PORT}/" .env
else
  echo ".env already exists, skipping creation"
fi

if [ ! -d "$PY_ENV" ]; then
  python3 -m venv --system-site-packages "$PY_ENV"
fi
source "$PY_ENV/bin/activate"
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
deactivate
apt install -y python3-fastapi python3-uvicorn python3-sqlalchemy \
  python3-httpx python3-pyotp python3-fpdf python3-yaml \
  python3-psutil python3-cryptography python3-requests python3-pytest \
  python3-pytest-cov python3-pytest-mock python3-pytest-asyncio \
  python3-pytest-xdist

npm install --prefix node_backend
[ -f frontend/package.json ] && npm install --prefix frontend || true

source "$PY_ENV/bin/activate"
python <<PYEOF
from backend import settings
from backend.database import Base, engine
settings.apply_env()
Base.metadata.create_all(bind=engine)
PYEOF
deactivate

step "[5/8] Run tests"
source "$PY_ENV/bin/activate"
if ! python -m pytest --version >/dev/null 2>&1; then
  echo "Pytest missing from venv, linking system pytest"
  if command -v pytest >/dev/null 2>&1; then
    ln -sf "$(command -v pytest)" "$PY_ENV/bin/pytest"
    "$PY_ENV/bin/pytest" tests 2>&1 | tee -a "$APP_DIR/logs/pytest.log"
  else
    echo "System pytest not found, aborting tests"
  fi
else
  python -m pytest tests 2>&1 | tee -a "$APP_DIR/logs/pytest.log"
fi
npm test --prefix node_backend --silent 2>&1 | tee -a "$APP_DIR/logs/node_test.log"
deactivate

step "[6/8] Configure networking"
if ! ufw status | grep -q "Status: active"; then
  ufw allow OpenSSH
  ufw allow ${APP_PORT}
  ufw allow 'Nginx Full'
  ufw --force enable
fi

if [ ! -f /etc/nginx/sites-available/nucleus ]; then
  prompt DOMAIN "Domain for HTTPS (leave blank to skip): "
  if [ -n "$DOMAIN" ]; then
    cat >/etc/nginx/sites-available/nucleus <<NGINX
server {
    listen 80;
    server_name ${DOMAIN};
    location / {
        proxy_pass http://127.0.0.1:${APP_PORT};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
NGINX
    ln -sf /etc/nginx/sites-available/nucleus /etc/nginx/sites-enabled/nucleus
    systemctl restart nginx
  fi
fi

step "[7/8] Create admin user"
prompt ADMIN_USER "Admin username: "
prompt_secret ADMIN_PASS "Admin password: "
source "$PY_ENV/bin/activate"
python <<PYEOF
from backend import settings
from backend.database import SessionLocal, Base, engine
from backend.models import User, Role, UserRole
settings.apply_env()
Base.metadata.create_all(bind=engine)
db=SessionLocal()
user=db.query(User).filter_by(username="${ADMIN_USER}").first()
if not user:
    user=User(username="${ADMIN_USER}", password="${ADMIN_PASS}")
    db.add(user); db.commit(); db.refresh(user)
role=db.query(Role).filter_by(name="admin").first()
if not role:
    role=Role(name="admin")
    db.add(role); db.commit(); db.refresh(role)
if not db.query(UserRole).filter_by(user_id=user.id, role_id=role.id).first():
    db.add(UserRole(user_id=user.id, role_id=role.id)); db.commit()
db.close()
PYEOF
deactivate

cat <<'NODE' >node_backend/create_node_admin.js
const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcryptjs');
const path = require('path');
const dbPath = process.env.AUTH_DB || path.join(__dirname, 'auth.db');
const db = new sqlite3.Database(dbPath);
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
  db.run('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', [user, hash], () => db.close());
});
NODE
node node_backend/create_node_admin.js "$ADMIN_USER" "$ADMIN_PASS"
rm node_backend/create_node_admin.js

# use SERVICE_USER env var or default to a dedicated account
USER_NAME=${SERVICE_USER:-nucleus}

# ensure service user exists (defaults to "nucleus")
if ! id "$USER_NAME" >/dev/null 2>&1; then
  echo "Creating service user $USER_NAME"
  groupadd -f "$USER_NAME"
  useradd -r -g "$USER_NAME" -s /usr/sbin/nologin "$USER_NAME"
  usermod -aG adm "$USER_NAME" || true
fi

step "[8/9] Setup systemd services"
mkdir -p /var/log/nucleus
chown "$USER_NAME" /var/log/nucleus || true
"$APP_DIR/scripts/set_permissions.sh" "$APP_DIR" "$USER_NAME"
sed "s|/opt/nucleus-platform/CRM|$APP_DIR|g; s|8000|$APP_PORT|g; s|User=nucleus|User=$USER_NAME|" services/nucleus_backend.service \
  >/etc/systemd/system/nucleus-backend.service
sed "s|/opt/nucleus-platform/CRM|$APP_DIR|g; s|User=nucleus|User=$USER_NAME|" services/nucleus_auth.service \
  >/etc/systemd/system/nucleus-auth.service
systemctl daemon-reload
systemctl enable --now nucleus-backend.service
systemctl enable --now nucleus-auth.service

step "[9/9] Finished"
cat <<INFO
Installation complete!
Application directory: $APP_DIR
Services started: nucleus-backend and nucleus-auth
Manage them via scripts/manage_services.sh or systemctl.
Login via http://${DOMAIN:-<server-ip>}:${APP_PORT} or through Nginx domain if configured.
INFO
