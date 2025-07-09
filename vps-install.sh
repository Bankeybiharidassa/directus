#!/bin/bash
# === Nucleus CRM / Directus Installer for VPS ===
# Tested on: Ubuntu 22.04+ (non-Docker, bare metal)

set -e

# === Configuration ===
REPO_URL="https://github.com/Bankeybiharidassa/directus.git"
APP_DIR="/opt/nucleus"
DB_NAME="nucleus_crm"
DB_USER="nucleus"
DB_PASS="supersecurepass"
DB_HOST="localhost"
NODE_VERSION="18.20.2"

# === Ask for MariaDB root password ===
echo -n "Enter MariaDB root password: "
read -s MYSQL_ROOT_PASS
echo

# === Prepare system ===
echo "[+] Installing system dependencies..."
apt update && apt install -y git mariadb-server build-essential curl python3-pip unzip

# === Setup Node.js via NVM ===
echo "[+] Installing NVM and Node.js $NODE_VERSION..."
export NVM_DIR="$HOME/.nvm"
if [ ! -d "$NVM_DIR" ]; then
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
  source "$NVM_DIR/nvm.sh"
fi
source "$NVM_DIR/nvm.sh"
nvm install $NODE_VERSION
nvm use $NODE_VERSION

# === Clone Repo ===
echo "[+] Cloning repo to $APP_DIR..."
rm -rf "$APP_DIR"
git clone "$REPO_URL" "$APP_DIR"
cd "$APP_DIR"

# === Install Dependencies ===
echo "[+] Installing project dependencies..."
npm install

# === Setup Database ===
echo "[+] Configuring MariaDB..."
mysql -u root -p"$MYSQL_ROOT_PASS" <<EOF
CREATE DATABASE IF NOT EXISTS $DB_NAME;
CREATE USER IF NOT EXISTS '$DB_USER'@'$DB_HOST' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'$DB_HOST';
FLUSH PRIVILEGES;
EOF

# === Create Env File ===
echo "[+] Writing .env file..."
cat > .env <<EOF
KEY=supersecretkey
DB_CLIENT=mysql
DB_HOST=$DB_HOST
DB_PORT=3306
DB_DATABASE=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASS
WEBSOCKETS_ENABLED=true
PORT=8055
EOF

# === Run Migration and Start ===
echo "[+] Running DB migrations and starting Directus..."
npx directus bootstrap
npx directus start

# === Complete ===
echo "[✔] Nucleus CRM instance should now be running on http://localhost:8055"
echo "Login via web browser and create admin user."
