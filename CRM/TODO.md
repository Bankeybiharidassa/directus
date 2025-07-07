# TODO List

* [x] Check availability of extensive admin panel where all settings (system and super user) are reflected in logical grouped tabs. Designed and implemented basic admin page and backend route.
* [x] Ensure there is an installerscript which installs and setup the basics, creates the superuser and makes sure the superuser has 10 grace logins before MFA is forced.
* [x] Registration with MFA done through web GUI.
* [x] Status page shows status of all API services and jobs.
* [x] check of yubikeys are supported by default with correct code. code references/dev info @ https://github.com/yubico. keep in mind that if pam modules will be implemented, there is no physical access, only ssh and vnc! So these need to be allways excempt from yubikey authentication as mandatory step. till we have tested and confirmed with a low ranking account with no impact, to be working over ssh
* [x] make sure that masterkeys can be generated and private keys be stored in the yubikey. design choise is at your side to choose either pgp or certificate functions of the yubikey. Webauthn is only for authentication at web end an option. not for low level key generation or dependencies
  
* [x] Added yubikey utility script and tests.check if code is valid and functional with correct logics
* [x] check and improve keycloak integration. note license parts in documentation. Add keycloak integration wizard to admin panel. more info: https://github.com/keycloak/keycloak. make sure it has it's reflecting controls available in the admin panel. Make keycloak the primairy user,partner,distri,employees and admins. Superadmin level should stay out of here, so there is always a fall back in disaster situations
* [x] create a backup module in the admin section with :
    * [x] create full system settings backup system
    * [x] create full system backup system
    * [x] create full data and incremental backup system
    * [x] create a backup system for the secrets and certificates. also add an export function for public keys
* [x] Rework the hierarchy from nucleus - partner - enduser to nucleus - distri - partner - enduser. Make sure this change reflects everywhere. also in the rbac, api, invoicing modules, discount modules, customer groups. Add functions in api so distri can send in electronic messages/api/webhook to add resellers,endusers, subscriptions, changes to subscriptions, extending subscriptions. Same is valid for partners at their level (partner level and their customers) but also partners should be able to inject electronic messages/api/webhook instructs. all these functions should be also available in listings of the data (show)
Ticketing should be designed same way. alerting as well. except alerting is only downwards and never incoming from channel.
* [x] verify and rework the api to ensure it contains all functions to be able to supply these extra commands/options/features.
* [x] Tenable integration module beschikbaar op alle niveaus met documentatie en tests.
* [x] add a full dmarc analyser per domain available per customer (multiple customer domains possible), reflect this also for partners in overall status, distri, and in all have api functions designed in the api. enduser and partner can see details. all above just general metrics. below you will find more detailed buildinstructs. process them, reorder them, update all relevant documentation to reflect this dmarc module
* [x] create a "support call - authorize remote access" option in end-user, partner and distri levels. from internal only supportrole and auditrole can "login as" and access the data. support can alter (tracked and traced in logs), auditor can only view. create the proper api entries for these functions, buttons/checkboxes, documentation etc.
* [x] Restrict external API access with ip and fqdn whitelisting. ip's as ip or as cidr . fqdn including wildcard (*.domain.ext) . localhost is allways allowed, local ip is allways allowed and local segment is allways allowed if it's a private range ip. Access to this whitelist is only for admin panel. But default support request ticket template should be build for distributors and partners. endusers only thru partner request (for enduser : please contact your partner <partnername> )
* [x] Since install is initiated from git, we have to be carefull with updates in production. so we have to get an integrated OTAP established where updates are first staged into Test, after approval to accept. there functional operator tests need to be done. After operator approval we can move the update to production stage, but we have to ensure full rollback options for at least 2 approved running versions in production. So even if an error is detected later on, we always can revert to max 2 running versions prior. For database changes, this means always the need for backwardscompatibility for 2 full versions! Same for all API call changes! work in closed loops: Design, design tests, build design, test design, verify, rework, retest, verify till all is done
* [x] Create an update script, callable from admin panel, which obeys above rules!
* [x] integrate acme/let's encrypt certificate request system into CRM. make it possible to request certificates for all hostnames in use ( eg. api, customer, nucleus, www, mail) with key reuse. this last part is important for keeping tlsa records allright.
* [x] GUI : Make sure the gui side is mature, professional, template driven. All pages and subpages should be accessible depending on the RBAC user level. Make sure we have Frontends for Admin - Company - Distributors - Partners - Endusers. Categories Entries and Pages logically and make sure all features available for a role are available and accessible. Create 1 default professional mature template and one example template with embedded instructions for changing it. Make the templates top down structure, so all will match same layout/colorsettings. Distributors and Partners can have their own template set, where they can change colors, fonts and logo. This to enable whitelabel reselling at all levels.
* [x] Added user menu to all dashboards with profile and security links
* [x] Login page : Each frontend needs to have a suitable professional looking login page. Easy editable by admin in layout, logo, color,etc
* [x] Admin pages : System, Settings, Users, Groups, RBAC, Import/export/mappings  availability sensor indicators of services, statistics, logs.
* [x] Company pages : Internal news, CRM, CMS, Finance, Import/export, Email, Agenda, Knowledgebase, Support.
* [x] Support pages : Overview, Tickets, Knowledgebase, Remote control, logs (company only), Integrations
* [x] Public facing Frontpage : Professional looking frontpage for anonymous visitors (maybe @ different app instance & port?)
* [x] Logged in End-Users pages : Overview, Products in use, Reports, Assets, Tickets, Change my products, Profile & Security settings
* [x] Logged in Distributors : Overview, Resellers, Endusers, Reports, Assets, Tickets, EDI, Profile & Security Settings
* [x] Logged in Partners : Overview, Endusers, Reports, Assets, Tickets, EDI, Profile & Security Settings
* [x] Logged in Company user : All available for the user RBAC level + Profile & Security Settings
* [x] If I missed essenstial pages, please add them. my notes are guidelines , no laws. law is : work in closed loops of design, take notes, design test, take notes, build, rework test to find errors in the build, test, evaluate results, execute all syntax tests, fucntionality tests, logic tests, interoperatibility tests between other components, api, etc. Test with lowlevel html viewer if you get html or api responses. work till you get the html responses as you can expect from a working website, where you detect more then an empty page, but you should see all elements which should be there at that specific page.
* [ ] 
```crm
# CRM Integration Module — Final Build Specification (DMARC Analyzer)

## 🎯 Purpose
Integrate the DMARC Analyzer with existing CMS/CRM systems to:
- Provide per-tenant DMARC analytics
- Allow external access to statistics via authenticated API
- Enable abuse reporting and configuration via CRM frontend

---

## ✅ Core Features

### 1. Tenant & User Sync
- [x] API-based import of tenant and user metadata from external CRM
- [x] Webhook or cron-based sync support
- [x] Duplicate check and merge logic

### 2. Domain & Mail Profile Assignment
* [x] Map CRM domain records to DMARC Analyzer tenants
* [x] Assign IMAP/SMTP configs per domain or contact
* [x] Auto-create placeholder configs for new CRM tenants

### 3. Statistics Exposure
- [x] Provide per-domain, per-category stats via REST API:
   - Pass/fail count
   - Report volume
   - Abuse contacts matched
   - Complaint rate
- [x] Support JSON and CSV output
- [x] Enforce RBAC filtering (CRM sees only its own tenants)

### 4. Abuse Reporting API
* [x] Pre-fill complaint forms with CRM data (contact owner, domain, IP)
* [x] Send via secure webhook or direct email from Analyzer
* [x] Allow feedback loop back into CRM (status: sent / responded / actioned)

### 5. Configuration Access
- [ ] CRM users (admin/helpdesk level) can update:
   - IMAP credentials
   - Folder name
   - OAuth profiles (MS365 only with admin rights)

---

## 🧩 Technical
- Language: PHP for frontend, Python (Flask) for API layer
- Auth: Token-based (JWT) with optional IP restriction
- API Spec: OpenAPI 3.1 compatible
- Endpoint prefix: `/api/crm/`
- Format: JSON (default), fallback to XML or CSV
- Rate limiting + audit logging enabled by default

---

## 🧪 Testing
- [ ] API input validation (no overposting or injection)
- [ ] CRM access control (test role scoping)
 - [x] Multi-tenant isolation test (CRM A cannot access CRM B)
- [ ] Report injection test (1000 CRM events to API)
- [ ] CSV export sanity check (large domain sets)

---

## 📄 Docs
- [ ] `/docs/CRM_API.md` → full endpoint list and usage
- [ ] `/docs/README.md` → CRM section
- [ ] `/docs/CHANGELOG.md` → CRM module addition
- [ ] `/docs/TODO.md` → enhancements list

---

## 🔚 Exit Criteria
- [ ] All endpoints tested and authenticated
- [ ] CRM can read, write, and sync with DMARC Analyzer
- [ ] Multi-tenant logic confirmed
- [ ] Stats and complaints flow validated end-to-end
```
* [x] Design and build internal security suite for this CMS/CRM and it's underlaying (ubuntu) linux os
  - `security_scan.py` now performs package and binary checks, CVE lookups, bandit whitebox analysis and a simple blackbox port scan. Results are cached encrypted so Codex and operators can run consistent scans. Docs, agents and changelog updated accordingly.


## 🎯 Objective
Audit the entire DMARC Analyzer codebase for flaws related to:
- Code integrity and consistency
- Security vulnerabilities
- Stress/load endurance

Every issue found must be logged in TODO, tested, fixed, and retested until the system is 100% green.

---

## 🔍 Audit Scope

### Code Integrity
- [ ] Check for undefined functions, unused variables
- [ ] Verify all modules import cleanly (no runtime errors)
- [ ] Confirm all expected files/folders are present
- [ ] Remove any placeholder logic or temporary code

### Security Checks
- [ ] Escape all input in PHP forms (XSS/HTML injection)
- [ ] Sanitize and parameterize all SQL queries (avoid SQLi)
- [ ] Validate IMAP/OAuth token scopes and usage
- [ ] Encrypt secrets, tokens, passwords securely (AES-256, Sodium)
- [ ] Check file upload handling (ZIP/GZ parsing, path traversal)
- [ ] Verify RBAC enforcement at all endpoints

### Load & Stress Tests
- [ ] Run synthetic load on IMAP parser (simulate 1000 reports)
- [ ] Simulate multiple concurrent users per tenant
- [ ] Process large `.zip` and `.tar.gz` files
- [ ] Monitor memory usage and peak behavior

---

## 📄 Reporting
- [ ] Log all flaws in `/docs/TODO.md` with tag `[AUDIT]`
- [ ] Each fix must:
   - Be committed
   - Include a test case
   - Be marked in `/docs/CHANGELOG.md`

---

## ✅ Exit Conditions
- ✅ All modules pass syntax, import, and logic tests
- ✅ No unescaped inputs or insecure DB operations
- ✅ All endpoints RBAC-protected and safe
- ✅ TODO.md = empty or contains only future features
- ✅ CHANGELOG.md fully reflects fixes and stability improvements

> Start: traverse `/api/`, `/web/`, `/tests/`, `/docs/`
> Loop: test → log issue → fix → retest → mark complete
> Do not exit until all flaws resolved and all tests green
