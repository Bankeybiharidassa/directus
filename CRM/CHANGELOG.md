# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Initial TODO list describing missing parts of the platform.
- This changelog to track issues and fixes.
- Basic FastAPI backend with user and customer routes.
- Placeholder endpoints for cases, docs, mail and assets.
- Tests covering new endpoints.
- Ticket model and API routes with tests.
- Asset model and CRUD endpoints with tests.
- Partner model and hierarchy management endpoints with tests.
- Page model with publish and portal revoke endpoints plus tests.
- Vulnerability model and asset endpoints to track vulnerabilities with tests.
- Contract model with CRUD and close endpoints plus tests.
- MFA enforcement endpoint with TOTP verification and tests.
- IP whitelist model, endpoints and enforcement with tests.
- Core routes for log export, config reload and BS check with tests.
- Role model with assignment endpoints and role-based access control tests.
- API config model with endpoints and tests to store API key and selected model.
- Asset sync endpoint with CLI script, GUI button and tests.
- Sophos and Tenable sync scripts now implement sample integrations.
- Asset sync endpoint creates assets from these scripts with count feedback.
- Admin dashboard now includes profile and security sections so menu links work.
- Sophos Partner and Customer API clients with tests.
- Document generator endpoint produces real PDF using FPDF with tests.
- Invoice export and management report endpoints with tests.
- Usage guide documenting CLI and GUI features.
- Customer export endpoint returning PDF with test.
- Case model with CRUD and search endpoints enforcing namespace filter with tests.
- Node.js authentication service with OTP and login counter.
- React login component calling the Node backend.
- IMAP mail sync storing message metadata with tests.
- Test suite cleanup fixture drops tables after each test to ensure isolation.
- Comprehensive README with architecture, setup and OTAP statement.
- AGENTS.md expanded with validated CLI ↔ GUI mappings.
- CONTRIBUTING guidelines and CODEOWNERS added.
- QC-4 validation verifying all modules and tests.
- Configuration loader reading `config/settings.yaml` and applying environment variables.
- React customer list component and page.
- CLI scripts refactored with `main()` functions and tests added.
- Sophos and Tenable sync scripts now read API URLs and tokens from environment.
- Installation script installs dependencies and initialises the database.
- Maintenance script with system update, hardening and git sync menu.
- `sophos_api_mode` veld toegevoegd aan het Customer-model om partner- of customer-workflow vast te leggen.
- Pylint run integrated with pytest; docstrings added to distributor and case routes.

## [1.0.1] - 2025-06-24
### Added
- Production-ready configuration templates.
- Updated build trace with commit and module test status.
- Documentation revised for deployment procedures.
### Changed
- settings.yaml now uses environment variables for sensitive data.
- OTAP status marked production ready.



### Known Issues
None.

### 2025-06-30
- Verified README and TODO updates, ran full test suite.
- All Python and Node.js tests passing.
- Dependencies installed for tests; codex loop log saved.
- System health check script and unit test added.

### 2025-06-30 - Admin features
- Admin panel page with grouped tabs added.
- Installer script now creates Node auth superuser with 10 grace logins.
- Web GUI for MFA registration implemented.
- Service status endpoint and page added with tests.

### 2025-07-01 - YubiKey utilities
- Added helper script `scripts/yubikey.py` to detect YubiKey presence and manage keys.
- Test suite expanded with `test_yubikey.py`.
- TODO updated to mark YubiKey tasks complete.

### 2025-07-02 - Keycloak and backups
- Added Keycloak configuration endpoints and wizard page.
- Distributor model introduced with API endpoints.
- Backup utility script implemented with tests.

### 2025-07-02 - Test expansions
- Expanded YubiKey, Keycloak and backup tests including negative paths.
- Added system and incremental backup helpers.

### 2025-07-03 - Tenable integration
- Tenable service and API routes added.
- CLI script now uses service implementation.
- Tests and documentation for Tenable integration added.

### 2025-07-04 - DMARC module
- DMARC service, API route and CLI implemented.
- Tests and documentation updated.
- CRM DMARC stats API with CSV output added.

### 2025-07-05 - CRM domain mapping
- Domain model introduced with tenant linkage and IMAP fields.
- CRM domain API for adding and listing domains.
- Customer creation now seeds a placeholder domain.

### 2025-07-07 - DMARC RBAC and SMTP
- Added SMTP fields to Domain model and API.
- Enforced tenant RBAC header on CRM DMARC endpoint.
- Multi-tenant isolation test implemented.

### 2025-07-08 - DMARC abuse reporting
- Added abuse report model and API route.
- CLI command `dmarc abuse` implemented with tests.
- Documentation and TODO updated.
- Webhook notification and status update endpoints implemented.

### 2025-07-08 - CRM sync import
- CRM tenant and user sync endpoint with CLI script added.
- TODO updated to mark sync tasks complete.

### 2025-07-09 - Security scan
- Added `security_scan.py` script to verify installed packages against Ubuntu security notices.
- Encrypted cache allows fast offline checks in Codex and live environments.
- Documentation, TODO and agents updated; test added.
- Added admin panel button to run the security scan via new backend endpoint.

### 2025-07-10 - Security scan extended
- Security scan now validates critical binaries and queries the public CVE database.
- Includes Bandit whitebox scan and simple blackbox port scan.
- Admin docs and tests updated.

### 2025-07-11 - CI dependency fix
- Added `requests` to backend requirements to resolve missing module errors in tests.

### 2025-07-12 - API whitelist enhancement
- Added CIDR and FQDN pattern support for API whitelist entries.
- Authentication now accepts `X-Client-FQDN` header and falls back to reverse DNS.
- Updated tests and documentation.

### 2025-07-12 - Remote support access
- Users can authorize temporary remote support using `/support/authorize`.
- Support and audit roles can impersonate authorized users via `/support/login_as/{user_id}`.
- Added docs and tests.

### 2025-07-13 - README translation verification
- Root README converted fully to English and checked for consistency across modules.
- Full Python and Node test suites executed; all tests passing.
- Logged results in `logs/codex_loop_run_20250701-1300.log`.
### 2025-07-13 - Full code verification
- Verified README translation and ran flake8 lint plus full test suites. All checks passing.
- Logged results in `logs/codex_loop_run_20250701-1300.log`.

### 2025-07-14 - EDI messaging
- Added EDI message model with endpoints and CLI utility.
- Added tests for sending and listing EDI messages.


### 2025-06-30 - Security loop
- Performed bandit static analysis; resolved try/except pass in mail route.
- Re-ran Python and Node test suites 5 times each.

### 2025-07-01 - CRM sync password fix
- Replaced hardcoded password in CRM sync import with random token.
- Bandit scan verified clean results.

### 2025-07-01 - Security scan verification
- Pytest and Node tests executed; all passing.
- Bandit scan run with 16 high, 22 medium, 398 low issues reported.
- Logged results in `logs/codex_loop_run_20250701-1338.log`.

### 2025-07-01 - Security scan rework
- Added request timeouts to CLI scripts.
- Updated CLI tests for new parameters.
- Bandit scan rerun on project code shows zero high issues and three medium issues in tests.
### 2025-07-01 - Install script update
- Added instructions for locating GitHub PAT and repo format in install.sh

### 2025-07-15 - Update script
- Added `update.py` to manage staged deployments with automated backups.
### 2025-07-15 - OTAP update flow
- Update script now separates test, acceptance and production stages.
- Docs updated with staging and deployment commands.
### 2025-07-16 - Installer improvements
- Install script checks MariaDB root password, installs gh and skips existing configuration.
- Installer handles reruns and verifies DB config.
- Installer now runs tests via `python -m pytest` and stores Node test output.
- Installer auto-creates `config/.env.template` if missing before generating `.env`.
=======
### 2025-07-16 - ACME certificate integration
- Added ACME/Let's Encrypt certificate request API and CLI.
- Updated node dependencies to remove deprecation warnings.
- Install script now installs pytest before running tests.
### 2025-07-17 - Installer fix
- Install script uses --break-system-packages to support Debian-based environments with PEP 668.
### 2025-07-18 - Installer improvement
- Install script installs Python modules via apt instead of using --break-system-packages.

### 2025-07-19 - Installer bugfix
- Virtual environment includes system packages so pytest works.
- Repository updates via `git pull` when already present.
### 2025-07-20 - Installer enhancements
- Added pytest plugins via apt for coverage, mock, asyncio and xdist.
- Installer caches credentials in a temporary file and deletes it on completion.
### 2025-07-21 - Service management
- Installer now installs and enables systemd services for backend and auth.
- Added scripts/manage_services.sh helper.
### 2025-07-22 - Service patch script
- Added scripts/patch_services.sh for updating the repository and installing services without reinstall.
- Backend service ExecStart sets --app-dir to avoid ModuleNotFoundError.
### 2025-07-21 - Installer fix
- Node admin creation script runs within node_backend so sqlite3 module resolves.
- Installer symlinks system pytest into the virtualenv when missing.
### 2025-07-23 - Database fallback
- Apply_env now falls back to SQLite when DB host/user are unset.
### 2025-07-24 - Service logging
- Backend and auth services now log to /var/log/nucleus.
### 2025-07-24 - Deprecation warnings resolved
- Updated FPDF usage to use built-in Helvetica font and "text" parameter.
- Remote support logging now uses timezone-aware timestamps.
- Rollback process uses tarfile with data filter for Python 3.12+ compatibility.
### 2025-07-25 - Permission fix utility
- Added scripts/set_permissions.sh to reset ownership and permissions across the repository and /var/log/nucleus.
### 2025-07-26 - Port configuration fix
- Auth service now defaults to port 3001 to avoid conflict with backend on port 8000.
### 2025-07-27 - Backend service fix
- Updated nucleus_backend.service to run `python -m uvicorn` so the service doesn't fail with status 203/EXEC when the uvicorn executable is missing in the virtualenv.
### 2025-07-27 - API root endpoint
- Added `/` route returning API info and docs link.
### 2025-07-28 - Quick update script
- Added scripts/update_now.sh for fast git pull with permission fix.
### 2025-07-29 - Update script improvements
- update_now.sh now prompts for GitHub credentials and clones the repo if missing.
### 2025-07-30 - Update path fix
- update_now.sh pulls repository from /opt/nucleus-platform/CRM.
### 2025-07-31 - Update script fix
- update_now.sh sets CHANGES_BASE to avoid unbound variable error.
### 2025-07-31 - Update push before pull
- update_now.sh now pushes local commits before pulling updates.
### 2025-07-31 - Update push fix
- update_now.sh pushes HEAD to the current branch before pulling.
### 2025-07-31 - Form login fix
- Node auth server parses URL-encoded form bodies and tests cover it.
### 2025-07-31 - Test DB isolation
- Auth server uses `AUTH_DB` environment variable; tests run on a separate database to preserve real users.
### 2025-07-27 - API root endpoint
- Added `/` route returning API info and docs link.
### 2025-07-28 - CI log directory fix
- CI pipeline now creates `/var/log/nucleus` so tests can write logs.

### 2025-07-31 - Admin login page
- Added simple HTML login form at `/core/login` with corresponding test.

### 2025-07-31 - Login action fix
- Login form posts to Node auth service using current server host.

### 2025-07-31 - Login host detection
- Login form resolves server IP when requests use 0.0.0.0 or localhost.
- Node auth server logs in syslog-style format.
### 2025-07-02 - GUI placeholders
- Added dashboard components for distributors, partners, end users and companies.
- Added CSS template files and updated README.

### 2025-07-31 - GUI dashboards fleshed out
- Added asset, ticket and customer lists on role dashboards.
- `/core/login` now accepts a `role` parameter for customized headings.
- New tests cover login role heading.
### 2025-07-31 - Public and support pages
- Added `/core/frontpage` route with simple landing page and test.
- Created `SupportHome` React page and expanded dashboards with placeholder sections.
- Documentation and TODO updated to mark GUI tasks complete.
### 2025-07-31 - Auth DB path fix
- Auth service and installer now use same database location to prevent login failures.
### 2025-07-31 - Update stash directory fix
- update_now.sh uses `cp -a` to copy directories when archiving local changes.
### 2025-08-01 - Admin reset script
- Added update_admin.sh to reset admin accounts across databases.
### 2025-08-02 - CORS middleware
- Added CORSMiddleware to backend with configurable origins.
- New test verifies CORS headers.
### 2025-08-02 - Admin script fallback
- update_admin.sh now handles missing venv by warning and using system Python.
### 2025-08-03 - Service recovery steps
- Documented fix for service startup via set_permissions.sh and npm install.
- Test log saved as logs/codex_loop_run_20250702-2340.log.
### 2025-08-03 - Startup fixes
- Sophos integration logs now write to /var/log/nucleus.
- update_now.sh and patch_services.sh install dependencies after pulling.
- nucleus_auth.service ensures npm install runs before starting.

### 2025-08-04 - Login redirect
- Node auth server redirects HTML logins to /core/admin.
- Added /core/admin page with placeholder and tests.
### 2025-08-05 - Lint improvements
- Added pylint test storing results in logs.
- Fixed import order and docstrings in core modules.
### 2025-08-06 - Pylint cleanup
- Fixed DMARC route parameter naming conflict and added encoding specifier.
- Removed trailing blank lines in models and routes.
### 2025-08-08 - Update script check
- update_now.sh skips pip install when requirements already satisfied.
### 2025-08-07 - Sophos log permissions fix
- set_permissions.sh now creates `/var/log/nucleus/sophos.log` and sets correct permissions.
- Restored Sophos services to write directly to `/var/log/nucleus/sophos.log`.
### 2025-08-08 - Permissions script update
- set_permissions.sh accepts optional user argument and README/docs updated.

### 2025-08-09 - Service user checks
- install.sh ensures the service user exists and is added to the adm group.
- patch_services.sh creates the service user when missing.
- update_now.sh reads the service user from the systemd unit and creates it if necessary.
### 2025-08-10 - Tenable log path
- Tenable service writes logs to `/var/log/nucleus/tenable.log`.
### 2025-08-11 - Log directory unification
- All integration services now log to `/var/log/nucleus`.
- `set_permissions.sh` creates required log files with correct ownership.
### 2025-08-12 - Permission fix
- install.sh and patch_services.sh now call set_permissions.sh so service logs are created with the correct user ownership.
### 2025-08-13 - Permission script default
- set_permissions.sh reads the service user from the systemd backend unit when no user is provided.
### 2025-08-14 - Dependency check
- Verified fastapi and cryptography are installed; test run still fails due to missing packages like pyotp.
### 2025-08-15 - Lint cleanup
- Added module and class docstrings for asset, case and contract models.
- Installed backend and node dependencies to pass full test suite.
### 2025-08-16 - Auth refactor
- Reordered imports and added docstrings in `backend/security/auth.py`.
### 2025-08-17 - CI lint enforcement
- Added `.pylintrc` and integrated autoflake/isort/black with strict pylint scoring.
### 2025-08-18 - Pylint fixes
- Resolved broad exception warnings and unused arguments in routes.
- Refactored service logging setup and updated tests to use JSON payloads.
### 2025-08-18 - Test procedure update
- Installed dependencies via install.sh and ensured full Python and Node test suites pass.
### 2025-08-19 - Logging fix
- Unified service logging to use syslog timestamps.
- Updated backend services to avoid per-module log configuration.
### 2025-08-19 - Pycache cleanup
- update_now.sh and patch_services.sh delete *.pyc files to fix old logging paths

### 2025-08-20 - Service account default
- patch_services.sh and install.sh now default to the `nucleus` user unless
  `SERVICE_USER` is specified.
- README updated with service account instructions.
### 2025-08-21 - GUI user menu
- Introduced `UserMenu` React component showing profile and security links.
- Added menu to admin, company, distributor, partner, end user and support pages.
- Documented loops for each page group.
### 2025-07-05 - Test rerun
- Installed missing backend dependencies (fpdf2, psutil)
- Reran login page and full test suite; all tests passed.
### 2025-08-22 - README menu clarification
- Verified page menus and login flow; installed dependencies for tests; all tests passing (Python 86, Node 4).
### 2025-08-23 - Full verification
- Verified all modules and UI flows as per README. Ran 86 Python and 4 Node tests successfully.

### 2025-08-24 - Role dashboards routing
- Login form now includes hidden `role` field and Node server redirects to `/core/<role>`.
- Added backend routes for support, distributor, partner and enduser dashboards.
- Updated documentation and tests to cover role-based redirects.
### 2025-07-05 - Test validation
- Installed missing requirements and executed pytest and npm test; all tests passed.
- Added loop documentation and logs.

### 2025-07-05 - Full test suite rerun
- Re-executed 86 Python tests, 4 Node tests and linting.
- Generated new GUI dumps and log file.
### 2025-08-25 - Revert role dashboard routing
- Removed role dashboard redirects and related tests.
- Updated README and lynx test docs to avoid running install.sh or patch_services.sh.

### 2025-08-25 - Fix service crash on missing fpdf2
- Deferred `fpdf2` import in `backend/routes/docs.py` so services start even when
  the PDF library is absent.
- Crash was triggered after commit `346697a6a64` added new routes but the
  environment lacked the optional dependency.
### 2025-08-25 - Dependency verification
- Installed `fpdf2`, `psutil` and `python3-typeshed` in the production
  environment.
- Re-ran the full test suite to confirm services start correctly.
### 2025-08-26 - Permission fix
- set_permissions.sh now preserves executable files such as the virtualenv Python and node binaries to prevent service start failures.

### 2025-08-27 - Role menu verification
- Verified role dashboards and menus via headless tests.

### 2025-08-27 - RBAC enforcement tests
- Added pytest coverage ensuring each role cannot access other dashboards.
- Updated security loop docs to reflect 403 Forbidden responses.

### 2025-09-06 - Automated GUI loop script
- Added `scripts/gui_loop.sh` to run headless checks and `lynx` dumps in one command.
- Updated documentation and AGENTS.md to describe the new workflow.
\n### 2025-07-06 - Cycle 1
- Initial automated loop: tests and gui checks passed.

### 2025-07-06 - Cookie based login
- Node login now sets an `auth` cookie for HTML clients.
- Backend authentication reads this cookie when no Authorization header is present.
### 2025-09-07 - Gitignore update
- Added patterns to ignore common binary assets like images and PDFs.
