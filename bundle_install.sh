#!/bin/bash
# install_directus_keycloak.sh
# VPS Installatie van Directus (fork) en Keycloak met nginx + Let's Encrypt

set -e

### CONFIG
DOMAIN_DIRECTUS="directus.example.com"
DOMAIN_KEYCLOAK="auth.example.com"
EMAIL_ACME="admin@example.com"
GIT_REPO="https://github.com/Bankeybiharidassa/directus"
DIRECTUS_DIR="/var/www/directus"
KEYCLOAK_DIR="/opt/keycloak"

### 1. Packages
apt update
apt install -y curl gnupg2 ca-certificates lsb-release apt-transport-https software-properties-common nginx certbot python3-certbot-nginx nodejs npm git mariadb-server openjdk-17-jdk unzip

### 2. NodeJS 22 installeren via NodeSource
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs

### 3. Keycloak installeren (zonder docker)
useradd -r -d "$KEYCLOAK_DIR" -s /sbin/nologin keycloak || true
mkdir -p "$KEYCLOAK_DIR"
cd "$KEYCLOAK_DIR"
curl -LO https://github.com/keycloak/keycloak/releases/download/24.0.3/keycloak-24.0.3.zip
unzip keycloak-24.0.3.zip
mv keycloak-24.0.3/* .
rm -rf keycloak-24.0.3*
chown -R keycloak:keycloak "$KEYCLOAK_DIR"

# Keycloak configureren
$KEYCLOAK_DIR/bin/kc.sh build

cat <<EOF >/etc/systemd/system/keycloak.service
[Unit]
Description=Keycloak
After=network.target

[Service]
Type=simple
User=keycloak
Group=keycloak
ExecStart=$KEYCLOAK_DIR/bin/kc.sh start --hostname=$DOMAIN_KEYCLOAK --http-port=8080
Environment=JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reexec
systemctl daemon-reload
systemctl enable --now keycloak

### 4. Directus fork klonen
mkdir -p "$DIRECTUS_DIR"
git clone "$GIT_REPO" "$DIRECTUS_DIR"
cd "$DIRECTUS_DIR"
corepack enable
corepack prepare pnpm@latest --activate
pnpm install

# Directus .env aanmaken
cp .env.example .env

### 5. Directus service maken
cat <<EOF >/etc/systemd/system/directus.service
[Unit]
Description=Directus Node.js App
After=network.target

[Service]
Type=simple
WorkingDirectory=$DIRECTUS_DIR
ExecStart=/usr/bin/pnpm start
Restart=on-failure
User=www-data
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reexec
systemctl daemon-reload
systemctl enable --now directus

### 6. nginx configuratie
cat <<EOF >/etc/nginx/sites-available/directus
server {
    listen 80;
    server_name $DOMAIN_DIRECTUS;
    location / {
        proxy_pass http://localhost:8055;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

cat <<EOF >/etc/nginx/sites-available/keycloak
server {
    listen 80;
    server_name $DOMAIN_KEYCLOAK;
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/directus /etc/nginx/sites-enabled/directus
ln -sf /etc/nginx/sites-available/keycloak /etc/nginx/sites-enabled/keycloak

nginx -t && systemctl reload nginx

### 7. Certbot
certbot --nginx -d "$DOMAIN_DIRECTUS" -d "$DOMAIN_KEYCLOAK" --email "$EMAIL_ACME" --agree-tos --non-interactive

### 8. Klaar
systemctl status keycloak --no-pager
systemctl status directus --no-pager

echo "✅ Directus beschikbaar op https://$DOMAIN_DIRECTUS"
echo "✅ Keycloak beschikbaar op https://$DOMAIN_KEYCLOAK"
