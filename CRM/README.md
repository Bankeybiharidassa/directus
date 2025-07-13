# 📘 Nucleus CMS Platform — README (EN)

## 🗭 Project Overview

A modular, securely designed CMS/CRM/Supportdesk platform built in accordance with ISO 27001 and NIS2 guidelines. Developed with a complete OTAP structure and a strict 0% BS policy.

**Modules:**

1. Auth & RBAC (G1)

   * Keycloak integration via wizard
2. Customers/Partners/Distributors/Suppliers (G2)
3. Contract Management (G3)

   * Create and terminate contracts
4. Document Generator (G4.1)
5. CRM & Partner Structure (G4.2)

   * modify hierarchy to reflect this one: nucleus admins - distributors - partners - endusers ; make sure this is reflected over all modules and api structures and rbac
   * Manage distributors, partners and endusers
   * Register suppliers
   * EDI messaging between distributors and partners
6. Support Desk + Assets (G4.3)

   * Create tickets and list view
   * Register assets and list view
   * Track asset vulnerabilities
   * Mail sync via IMAP
7. CMS + Public Portal (G4.4)

   * Create and publish pages
   * Revoke portal access
8. Core: Nucleus Kernel (RBAC, encryption, logging)
   * Logging export
   * Config reload
   * API settings management
   * BS-check system scan
   * Security scan via CLI
   * Certificate request (ACME)
9. Tenable Integration (G4.5)
10. DMARC Analyzer (G4.6)

    * CRM integration for tenant statistics and domain assignment

## 🏠 Architecture

```
 [React Frontend]  <--REST-->  [FastAPI Backend]  <--DB-->  [SQLite/MySQL]
                             \--Auth-->  [Node.js Service]
```

## 🔐 Security by Design

* 🔑 Native support for YubiKey, certificates, IP + TOTP
* 📌 Full logging (audit-ready)
* 🛡 Granular RBAC for all actions/data
* 🔒 Encrypted-at-rest for all sensitive data
* 🔍 OTAP with testing and vulnerability checks

## ⚙️ Technical Details

The application consists of a Python backend (FastAPI) for all CRM/Support APIs, a small Node.js service for OTP-based authentication, and a React frontend. By default, SQLite is used during testing, but MySQL/MariaDB, PostgreSQL, and MSSQL are supported. External syncs like Sophos Central and Tenable.io/sc are available via CLI or GUI.

* Frontend: React
* Backend: FastAPI (Python) + Node.js (auth)
* DB choice: MySQL/MariaDB (default), PostgreSQL, MSSQL, SQLite
* Syncs: Sophos Central (partner & customer API), Tenable.io/sc
* CRM field `sophos_api_mode` determines whether the partner or customer API is used
* CLI/GUI asset sync via `/assets/sync`
* Document export: PDF, TXT, CSV
* HTML login page available at `/core/login` posting to the Node auth service. Passing `role` customizes the heading and determines the post-login redirect.
* Role dashboards provide customer lists, tickets and asset views for distributors, partners, end users and company users.
* Public landing page available at `/core/frontpage` for anonymous visitors.
* Support portal page lists tickets, knowledgebase links and remote control options.

## 📂 Project Structure

```text
/backend
  /routes
  /models
  /services
  /security
/frontend
  /components
  /pages
/tests
  *.py
scripts/
  sophos_sync.py
  tenable_sync.py
config/
  .env.template
  settings.yaml
```

## 🧚 OTAP Structure

| Phase | Description                 | Status |
| ----- | --------------------------- | ------ |
| O     | Development                 | ✅      |
| T     | Testing (unit + functional) | ✅      |
| A     | Acceptance Integration      | ✅      |
| P     | Production Deployment       | ✅      |

All code is automatically tested within CI. Pull requests without passing tests are not accepted.
Closed-loop QC: Development follows strict loops of design → build → test → verify → rework until operator approval.

## 🔄 Installation

```bash
# copy and fill in the .env file
cp config/.env.template .env

# install dependencies and initialize the database
./scripts/install.sh

# install Python dependencies for tests
pip install -r backend/requirements.txt

Ensure optional Python packages like `fpdf2` and `psutil` are installed
to avoid runtime errors in document generation and system checks.

# start services in production mode via systemd
sudo systemctl start nucleus-backend.service
sudo systemctl start nucleus-auth.service
```

Service logs are written to `/var/log/nucleus/` for troubleshooting.
For development testing with the text browser `lynx`, run `./test_install.sh`.
Do not run `install.sh` or `scripts/patch_services.sh` during local tests; they are for production only.
This script sets up a virtualenv, installs dependencies and starts the backend
and auth services on localhost so you can browse to `http://127.0.0.1:8000/core/login`.
After launching the services you can run `node scripts/headless_check.js` to
generate screenshots and menu traces in the `logs/` directory.
For a full automated check, execute `scripts/gui_loop.sh` which starts the
services, runs the headless browser and stores `lynx` output for every role.
If the backend fails to start with a permission error for
`logs/integration/tenable.log`, your checkout still uses an old logging path.
Run `sudo ./scripts/update_now.sh` followed by
`sudo ./scripts/set_permissions.sh /opt/nucleus-platform/CRM <user>` to update
the code and reset permissions. `update_now.sh` now removes any `__pycache__`
files so outdated modules cannot reference `logs/integration/tenable.log`.
The mysterious path `/opt/nucleus-platform/CRM/-m` seen in some error logs
comes from the Python crash handler misreading the `-m` flag and can be ignored.

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.
For applying new releases, use the staged update process via
`scripts/update.py`. First run `update.py stage <repo>` to prepare and
test a build. After acceptance testing, run `update.py deploy` to push
it to production. Two backups are kept and `update.py rollback` can
restore the latest version.
If the services are missing on an existing install, run
`sudo ./scripts/patch_services.sh` to pull the latest code and (re)install the
systemd units without a full reinstall. The installer and patch script create
a dedicated service account when needed and use the `SERVICE_USER` environment
variable to override the default `nucleus` user.

### Directus Setup

The repository also contains a modular Directus instance. See
[docs/setup.md](docs/setup.md) for installation instructions and how to enable
the custom extensions.
After running `scripts/update_now.sh`, execute
`sudo ./scripts/set_permissions.sh /opt/nucleus-platform/CRM nucleus` to ensure
`/var/log/nucleus` remains writable for the Sophos integration.
For developers, additional info on Sophos integration is available in [docs/sophos.md](docs/sophos.md).


## 🎨 Frontend Templates
Default styling lives in `frontend/templates/default.css`. Copy this file to create custom themes. See `frontend/templates/example-theme.css` for instructions.
The login page at `/core/login` accepts a `role` query parameter so each frontend
can present a customized heading and submit the role back to the auth server
(e.g. `/core/login?role=partner`). The Node service reads this value and
redirects the user to `/core/<role>` after successful authentication.

## Pages & Menus
After logging in, each role (admin, distributor, partner, end user or company) lands on its own dashboard page. That page displays the appropriate menu for the role and every menu link points to an existing page or feature.

The typical flow is: user visits `/core/login`, signs in and is redirected to the role dashboard. From there the menu provides intuitive access to all features allowed for that role.


## 📋 Licenses & Third-Party Tools

* 🔓 Keycloak (GPL) with custom reference
* 📦 Documentation generated with open source tools

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the process. In short:
Fork this repo, create a feature branch, run `pytest` and the Node test suite.
Install packages with `pnpm install`, build the workspace packages using
`pnpm --workspace-root build`, then execute `pnpm --workspace-root test`.
Before opening a Pull Request, format and lint the Python code:
```bash
autoflake --remove-all-unused-imports -r backend/
isort backend/
black backend/
pylint --rcfile=.pylintrc backend/
```
Then open a Pull Request.

## 📢 Disclaimer

This software is not affiliated with OpenAI, Microsoft, Sophos, or Tenable. Use at your own risk, in accordance with applicable compliance regulations.
