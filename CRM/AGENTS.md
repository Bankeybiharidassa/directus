# 🤖 agents.md — CLI ↔ GUI Mapping

## 📌 Doel

Deze module beschrijft hoe elke functie beschikbaar is in zowel de Command Line Interface (CLI) als in de Graphical User Interface (GUI), conform het Nucleus-ontwikkelmodel.

Alle CLI-functies moeten óf 1-op-1 terugkomen in de GUI, óf als bundeling op logische plekken beschikbaar zijn.

---

## 🗝️ AUTHENTICATIE & RBAC (G1)

| Functie                   | CLI Command                | GUI Locatie          |
| ------------------------- | -------------------------- | -------------------- |
| Nieuwe gebruiker aanmaken | `nucleus user add`         | Beheer > Gebruikers  |
| MFA verplichten           | `nucleus user enforce-mfa` | Beheer > Beveiliging |
| IP-whitelist instellen    | `nucleus ip whitelist add` | Beheer > Beveiliging |

---

## 👥 CRM / PARTNERSTRUCTUUR (G2 / G4.2)

| Functie                     | CLI Command                     | GUI Locatie    |
| --------------------------- | ------------------------------- | -------------- |
| Klant toevoegen             | `nucleus customer add`          | CRM > Klanten  |
| Partner hiërarchie wijzigen | `nucleus partner reassign`      | CRM > Partners |
| Relatie exporteren          | `nucleus crm export --type=pdf` | CRM > Export   |
| EDI bericht versturen       | `nucleus edi send`              | CRM > EDI      |

---

## 📄 DOCUMENTGENERATOR (G4.1)

| Functie                | CLI Command                       | GUI Locatie             |
| ---------------------- | --------------------------------- | ----------------------- |
| Rapport genereren      | `nucleus doc create --case 001`   | Documenten > Nieuw      |
| Factuur PDF exporteren | `nucleus invoice export --id 455` | Facturen > Download     |
| Managementrapport      | `nucleus report --mgmt`           | Rapportage > Management |

---

## 🛠️ SUPPORTDESK + ASSETS (G4.3)

| Functie                 | CLI Command                       | GUI Locatie            |
| ----------------------- | --------------------------------- | ---------------------- |
| Ticket aanmaken         | `nucleus ticket create`           | Support > Nieuw Ticket |
| Asset sync starten      | `nucleus asset sync --source=all` | Beheer > Assets        |
| Vulnerability per asset | `nucleus asset vulns <hostname>`  | Assets > Details       |
| Tenable assets bekijken | `nucleus tenable assets`          | Beheer > Assets        |

---

## ✉️ DMARC ANALYSER (G4.6)

| Functie       | CLI Command                      | GUI Locatie              |
| ------------- | -------------------------------- | ------------------------ |
| DMARC rapport | `nucleus dmarc report <domain>`  | Beheer > Mail > DMARC    |
| Domein koppelen | `nucleus dmarc add-domain`       | CRM > Mail > DMARC       |
| Abuse melden | `nucleus dmarc abuse <tenant> <domain> <ip> <contact>` | CRM > Mail > DMARC |
| Status bijwerken | `nucleus dmarc abuse-status <id> <status>` | CRM > Mail > DMARC |

---

## 🌐 CMS & PORTAL (G4.4)

| Functie                 | CLI Command                    | GUI Locatie         |
| ----------------------- | ------------------------------ | ------------------- |
| Pagina aanmaken         | `nucleus page create`          | CMS > Pagina's      |
| Pagina publiceren       | `nucleus page publish <slug>`  | CMS > Publiceren    |
| Portaltoegang intrekken | `nucleus portal revoke <user>` | Portal > Gebruikers |

---

## 🔒 CORE FUNCTIONALITEIT / NUCLEUS

| Functie          | CLI Command             | GUI Locatie              |
| ---------------- | ----------------------- | ------------------------ |
| Logging export   | `nucleus log export`    | Beheer > Logs            |
| Config herladen  | `nucleus config reload` | Beheer > Instellingen    |
| API-instellingen | `nucleus config set-api` | Beheer > Instellingen    |
| BS-check draaien | `nucleus check --bs`    | Beheer > Systeemcontrole |
| Security scan    | `python scripts/security_scan.py` | Beheer > Security Scan |
| Certificaat aanvragen | `python scripts/acme_cli.py request <email> <hosts>` | Beheer > Certificaten |

---

Alle mappings worden getest binnen OTAP en elke release bevat een consistentiecontrole voor CLI↔GUI. Document wordt automatisch bijgewerkt bij buildversie-wijzigingen.
All agents respect closed-loop process

After each test or prompt execution:

Codex Instruction – No Assumptions, Validate Everything
Stop assuming correctness based on your own tests alone. Operator has observed flaws in your output. The only way to confirm correctness is to validate that your tests themselves are correct and complete.
# ✅ Codex Instruct: Full Lynx-Aided Closed-Loop GUI Verification for Nucleus Platform

## 🎯 Objective
Ensure that all CLI ↔ GUI mappings, role-based page/component/module access, and menu integrations are:
- Fully implemented
- Verified via test users per role
- Tested using `lynx` (TUI web browser)
- Documented with logs
- Hardened against privilege escalation or unauthorized access

## 🧭 Scope
- Create test users per role: `test-admin`, `test-supporter`, `test-employee`, `test-distributor`, `test-partner`, `test-enduser`
- Login via CLI or direct auth API
- Navigate frontend via `lynx` and simulate user behavior per role
- Trigger available menu items, modules, components and record:
  - Access OK
  - Redirect or Forbidden
  - Broken or Incomplete
- Validate menu correctness per role
- Validate pages/modules are wired to the correct permissions
- Test privilege escalation attempts via:
  - Direct URL input
  - Modified request headers
  - Cookie manipulation
- Record all attempts in log file (`logs/codex_loop_run_YYYYMMDD-HHMM.log`)
- Document test paths under `docs/loops/<role>.md`

---

## 📜 Instructions for Codex

1. 🔁 **Closed Loop Initialization**
   - Setup test harness for each of the 6 test roles
   - Prepare login automation (either via HTML login form or CLI auth API)

2. 🧪 **Run Test Suite per Role (Sequential)**
    # lynx & system preparation before testing!
     -### 🧠 Codex Instruct — Prepare Minimal Webserver for `lynx` Test Cycle

#### 📌 Context
To run the `lynx`-based role verification tests, Codex must ensure that both the `nucleus-auth` and `nucleus-backend` services are actively running. Because the standard `install.sh` and `patch-services.sh` scripts rely on full systemd-based service deployment, this may exceed the capabilities of the Codex virtual environment. Therefore, a minimal environment must be prepared.

---

#### 🪛 Task Summary for Codex

1. **Fork the Current Repository (Optional)**
   - If Codex runs in a test clone or virtual workspace, clone to a temporary folder.

2. **Scan and Parse**
   - Open `./install.sh` and `./scripts/patch-services.sh`.
   - Extract only the **service runtime**, **virtualenv activation**, and **database preparation** steps.
   - Ignore anything related to `systemctl`, `.service` files, or persistent install state.

3. **Create a new script: `./test_install.sh`**
   - This file must:
     - Setup virtualenv (if not already active)
     - Install Python requirements
     - Configure minimal database if required (assume mariadb is installed)
     - Launch both services manually:
       ```bash
       python3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 &
       node auth/index.js &
       ```
     - Wait for both services to respond (retry loop with curl or wait-on)

4. **Log Results**
   - Write a log to `/var/log/nucleus/test_install.log` with any startup errors.
   - Print URLs for lynx to visit (e.g., http://127.0.0.1:8000/core/login)

5. **Update the Closed-Loop Test Logic**
   - Codex must recognize that `lynx` tests require these servers to be running.
   - Before launching `lynx`, check that both ports (8000 for backend, auth fallback) are live.
   - If not, run `./test_install.sh` again.

6. **Security Notes**
   - Use `localhost` only, no binding to `0.0.0.0`
   - Log all stdout/stderr of the services into the same log file
   - Ensure temp users (test-admin, test-supporter, etc.) are seeded or created via API

7. **Documentation**
   - Codex must update `AGENTS.md`, `README.md` and `docs/loops/lynx_test.md` to reflect that `test_install.sh` must be run before any browser-based page verification.

---

#### ✅ Output Required from Codex

- `./test_install.sh` (generated based on `install.sh` logic)
- Log output in `/var/log/nucleus/test_install.log`
- Confirmation that both services respond on expected ports
- Lynx logs per role saved in `logs/lynx_test-<role>.log`
- Headless screenshots and menu traces saved by running `node scripts/headless_check.js`
- `scripts/gui_loop.sh` automates these steps by starting the services and running both headless and `lynx` checks for every role.
- Updated AGENTS.md and test loop docs

---

#### 🚫 Restrictions
- Do not modify or redeploy the actual `nucleus-auth` or `nucleus-backend` service units.
- Never bind services to public IPs or interfaces
- Do not remove existing install.sh logic

---

Once all steps succeed and each role’s lynx logs show correct menu/page/module availability, Codex can mark this verification cycle as ✅ green.
#
   For each role:
   - Login with correct credentials
   - Open GUI via `lynx http://localhost/core/login?role=<role>`
   - Follow redirects to dashboard
   - Visit each menu item (manual traversal)
   - Attempt broken links, hidden features, and known/expected paths
   - Record which components were accessible
   - Validate RBAC boundaries:
     - Cannot see menus/modules beyond privileges
     - Cannot perform actions outside assigned role
     - Proper redirects or 403 messages

4. 🔐 **Security Test Vector Validation**
   - For each role, attempt:
     - URL manipulation (e.g. `/core/admin` by `test-enduser`)
     - CSRF override (fake token)
     - Cookie injection (elevated session)
     - Form spoofing (submit action not visible in UI)
     - Privileged API access via raw HTTP (using `curl`)
   - Expected result: 403 / permission denied / logged attempt

5. 🗂 **Documentation & Logging**
   - Save interaction logs to: `logs/codex_gui_loop_<role>_YYYYMMDD.log`
   - For each role, generate a coverage map (`docs/loops/coverage_<role>.md`):
     - ✅ = Available + Working
     - 🔒 = Blocked as expected
     - ❌ = Broken / missing / inaccessible
   - Update `AGENTS.md` if mismatches found between CLI ↔ GUI mappings

6. 🧠 **Final Report**
   - Mark test status as ✅ green only when:
     - All GUI functions match CLI descriptions
     - Pages, menus, components work per role
     - No broken wires, redirects, or privileges exist
     - All log/test/doc files are committed and up to date

7. ⚠️ **DON'T Touch**:
   - `nucleus-auth` and `nucleus-backend` service config — already confirmed working

---

## 🧩 Tips
- Use `lynx -auth=<user>:<pass>` or scripted login session (session reuse)
- For debugging menu paths, use page source (`lynx -source <url>`) to ensure it's visible
- Validate frontend state change via cookies and browser cache by clearing session per role

---

## ✅ Exit Condition
This instruct completes **only** when all roles pass the GUI/RBAC/CLI consistency test and:
- All docs updated
- All logs written
- No security gaps remain
- All broken pages/components are fixed or marked as `TODO` and triaged

When there is a conflict between your tests and operator visual inspection of the local build, operator verification always takes precedence. Human verification and visual inspection determine correctness, not your internal assumptions or previously generated test results.

Therefore, review and rework your tests, and confirm their validity by matching them against operator checks and visual confirmations in the local build environment. Continue in closed loops until operator confirms correctness.

Review the output and logs in the GUI.
Adjust the prompt or update settings if the result was not satisfactory.
Re-run the prompt via F5 or perform a self‑test.
Only commit changes with F9 once the desired result has been confirmed.
Update AGENTS.md and CHANGELOG.md with any completed tasks.
Save the audit log as logs/codex_loop_run_YYYYMMDD-HHMM.log.
Detailed per-component loops are documented under docs/loops.


### Commitlog
- 2025-06-24: `sophos_api_mode` veld toegevoegd aan CRM.
- 2025-06-30: Tests run in closed loop; README and TODO verified.
- 2025-06-30: Dependencies installed; full test run logged.
- 2025-06-30: Added system_check script and tests.
- 2025-06-30: Admin panel, MFA registration GUI and status page implemented; installer updated.
- 2025-07-01: YubiKey utilities and tests added.
- 2025-07-02: Keycloak wizard, backup utilities and distributor model implemented.
- 2025-06-30: Extended tests for YubiKey, Keycloak and backup utilities; distributor hierarchy verified.
- 2025-06-30: Security loop executed with bandit scan and test repetitions; mail route logging improved.
- 2025-07-03: Tenable integration module and tests added.
- 2025-07-04: DMARC module with API, CLI and tests implemented.
- 2025-07-05: CRM DMARC stats endpoint and CLI added.
- 2025-07-06: CRM domain mapping endpoints implemented.
- 2025-07-07: DMARC RBAC header and SMTP fields added; tests updated.
- 2025-07-08: DMARC abuse reporting route, CLI and tests added.
- 2025-07-08: Webhook notification and feedback loop implemented.
- 2025-07-08: CRM sync import endpoint and CLI added.
- 2025-07-01: CRM sync password fix and bandit scan clean.
- 2025-07-09: Security scan script added with encrypted caching and tests.
- 2025-07-09: Security scan accessible via Admin panel and API endpoint.
- 2025-07-10: Security scan extended with binary checks, CVE lookup, bandit and port scan.
- 2025-07-11: Added requests dependency to backend for passing CI tests.
- 2025-07-12: Added FQDN and CIDR support for whitelist authentication; tests updated.
- 2025-07-12: Remote support authorization endpoints implemented.
- 2025-07-13: README translated to English; full test suite verified.
- 2025-07-13: Codebase verified post-translation with flake8 and tests.
- 2025-07-14: EDI messaging endpoints, CLI and tests implemented.
- 2025-07-01: Security scan verification and all tests passing.
- 2025-07-01: CLI scripts updated with request timeouts; bandit shows no high issues.
- 2025-07-01: Install script now explains repo and PAT input.
- 2025-07-15: Update script with staging and rollback added.
- 2025-07-15: OTAP flow refined; update script uses test and acceptance stages.
- 2025-07-16: Install script made idempotent with root password detection and gh support.
- 2025-07-16: Fix installer env template check and DB verification.
- 2025-07-16: Installer runs tests via python -m pytest and logs Node output.
- 2025-07-16: Installer creates default env template when missing.
- 2025-07-16: ACME certificate request API, CLI and tests added. Node packages updated.
- 2025-07-17: Installer handles PEP 668 by passing --break-system-packages to pip.
- 2025-07-18: Installer installs Python modules via apt instead of using --break-system-packages.
- 2025-07-19: Installer uses git pull when repo exists and virtualenv includes system packages.
- 2025-07-20: Installer adds pytest plugins and caches credentials during run.
- 2025-07-21: Added systemd service setup and management script.
- 2025-07-22: Patch script for service installation added; backend service path fixed.
- 2025-07-21: Installer fixes sqlite3 module path for Node admin creation.
- 2025-07-20: Installer symlinks system pytest when venv lacks the module.
- 2025-07-23: Database fallback to SQLite when no DB host configured.
- 2025-07-24: Backend and auth service logs stored in /var/log/nucleus.
- 2025-07-24: Updated PDF generation and support logging for deprecation fixes; safe tar extraction during rollback.
- 2025-07-25: Permission fix utility added.
- 2025-07-26: Auth service port fixed to avoid conflict with backend.
- 2025-07-27: Backend service now launches via `python -m uvicorn` to avoid 203/EXEC failures.
- 2025-07-27: Added root API endpoint returning info and docs link.
- 2025-07-28: Added update_now.sh for quick git pull with permissions check.
- 2025-07-29: update_now.sh prompts for GitHub credentials and clones the repo when absent.
- 2025-07-30: update_now.sh pulls to /opt/nucleus-platform/CRM.
- 2025-07-31: update_now.sh stores local changes in /opt/nucleus-platform/changed_local.
- 2025-07-27: Added root API endpoint returning info and docs link.
- 2025-07-28: CI pipeline creates `/var/log/nucleus` to avoid test permission errors.
- 2025-07-31: Added HTML admin login page and test.
- 2025-07-31: Login form now posts to server host instead of localhost.
- 2025-07-31: Login page falls back to local IP when host is 0.0.0.0; auth server logs in syslog format.
- 2025-07-02: Placeholder role dashboards and CSS templates added.
- 2025-07-31: Role dashboards fleshed out; login page customizable by role.
- 2025-07-31: Public front page and support portal added.
- 2025-07-31: update_now.sh pushes local commits before pulling to preserve logs.
- 2025-07-31: update_now.sh pushes HEAD to current branch before pull.
- 2025-07-31: Node server accepts form-encoded login data with new test.
- 2025-07-31: Auth server respects AUTH_DB env var; tests use separate DB.
- 2025-07-31: Install script creates auth DB in node_backend directory for consistent login.
- 2025-07-31: update_now.sh archives directories correctly when stashing local changes.
- 2025-08-01: Added update_admin.sh to reset admin accounts.
- 2025-08-02: Added CORS middleware and tests.
- 2025-08-02: update_admin.sh warns when venv missing and falls back to system Python.
- 2025-08-03: Documented service recovery steps using set_permissions.sh and npm install.
- 2025-08-03: Sophos logs moved to /var/log/nucleus; update_now.sh installs dependencies and auth service runs npm install.
- 2025-08-04: Node login redirects to admin page; /core/admin route added with tests.
- 2025-08-05: Added pylint lint test and basic fixes.
- 2025-08-06: Addressed pylint warnings and cleaned trailing newlines.
- 2025-08-07: set_permissions.sh creates `sophos.log` so services log to `/var/log/nucleus` without fallback.
- 2025-08-07: Pytest run with pylint integration; docstrings added to routes.
- 2025-08-08: set_permissions.sh accepts user arg; docs updated.
- 2025-08-08: update_now.sh checks installed Python packages before using pip.
- 2025-08-09: install.sh, patch_services.sh and update_now.sh create missing service user.
- 2025-08-10: Tenable service logs stored in `/var/log/nucleus`.
- 2025-08-11: All services log to `/var/log/nucleus`; set_permissions.sh creates log files.
- 2025-08-12: patch_services.sh and install.sh run set_permissions for log ownership.
- 2025-08-13: set_permissions.sh detects the service user from systemd when no user is supplied.
- 2025-08-14: fastapi and cryptography installed; tests rerun but fail due to missing packages like pyotp.
- 2025-08-15: Docstrings added for Asset, Case and Contract models; full tests pass.
- 2025-08-16: Refactored auth module imports and added docstrings.
- 2025-08-17: Added .pylintrc and CI autoformat with strict pylint scoring.
- 2025-08-18: Fixed pylint warnings across routes and services; updated tests.
- 2025-08-18: Installed dependencies and executed new test procedures; all tests pass.
- 2025-08-19: Centralised logging setup with syslog timestamps; backend tests updated.
- 2025-08-19: update_now.sh cleans __pycache__ to fix old log paths.
- 2025-08-20: install.sh and patch_services.sh default to the `nucleus` service
  user unless SERVICE_USER is set; README updated.
- 2025-08-21: UserMenu component added to dashboards; loops documented for each page group.
- 2025-07-05: Installed backend dependencies and reran full test suite; all tests pass.
- 2025-08-22: Pages and menus verified as per README; dependencies installed, tests run (86 Python, 4 Node); log saved.
- 2025-08-23: Full verification cycle completed; 86 Python and 4 Node tests passing.
- 2025-07-05: Automated test validation run; pytest and npm test passing.
- 2025-08-24: Added test_install script for lynx testing; docs updated and tests verified.
- 2025-08-25: Reverted role dashboard routing update; test_install.sh used for local testing without modifying production scripts.
- 2025-08-25: Verified `fpdf2`, `psutil` and `python3-typeshed` installed; all tests pass.
- 2025-08-24: Role dashboard routing fixed; Node auth redirects based on role and new pages added.
- 2025-08-27: Menu docs verified; security gaps noted in docs/loops
- 2025-08-27: RBAC tests added to ensure dashboards return 403 for unauthorized roles; security docs updated.
- 2025-09-07: .gitignore updated to ignore common binary assets.
