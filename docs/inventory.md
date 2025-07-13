<!-- markdownlint-disable MD013 -->
# Nucleus CRM – Inventory (Pass 08)
_Last updated: 2025-09-10_


The `CRM` folder is kept for legacy reference only. All listed modules are implemented as Directus extensions.
Extracted from: `/CRM/README.md`

| Feature | Category | Notes / Proposed Module |
|---------------------------------|----------------------------|---------------------------------------|
| Keycloak wizard for Auth & RBAC | ✅ Implemented | `extensions/nucleus-auth/` |
| Hierarchical partners (admins→distributors→partners→endusers) | ✅ Implemented | Schema + RBAC in `extensions/nucleus-crm/` |
| Contract lifecycle (create/terminate) | ✅ Implemented | `extensions/nucleus-contracts/` |
| Document generator (PDF/TXT/CSV) | ✅ Implemented | `extensions/nucleus-docs/` |
| EDI messaging between partners | ✅ Implemented | `extensions/nucleus-edi/` |
| Support desk: tickets & assets | ✅ Implemented | `extensions/nucleus-support/` |
| Asset vulnerabilities via Tenable | ✅ Implemented | `extensions/nucleus-tenable/` |
| Sophos Central integration for asset sync | ✅ Implemented | `extensions/nucleus-sophos/` |
| `sophos_api_mode` selects partner or customer API | 🔧 Plugin/module required | `extensions/nucleus-sophos/` |
| Email sync via IMAP | ✅ Implemented (external worker) | `extensions/nucleus-mail-ingest/` |
| CMS & public portal | ✅ Implemented | `extensions/nucleus-portal/` |
| Portal access revocation | ✅ Implemented | `extensions/nucleus-portal/` |
| DMARC analyzer & tenant stats | ✅ Implemented | `extensions/nucleus-dmarc/` |
| Audit logging & encrypted storage | ✅ Implemented (nucleus-core) | `extensions/nucleus-core/` |
| Granular RBAC for all actions & data | ✅ Implemented | `extensions/nucleus-auth/` |
| Config via GUI + `.env` | ✅ Native Directus (partially) | Use Directus settings with env overrides |
| Role dashboards & menus | ✅ Implemented | `extensions/nucleus-ui/` |
| API for asset sync & remote control | ✅ Implemented | `extensions/nucleus-api/` |
| MFA with YubiKey, certificates, IP + TOTP | ✅ Implemented | `extensions/nucleus-auth/` |
| Role-based login page & redirect | ✅ Implemented | `extensions/nucleus-auth/` |
| Public landing page | ✅ Implemented | `extensions/nucleus-ui/` |
| Customizable CSS themes via `frontend/templates` | ✅ Implemented | `extensions/nucleus-ui/` |
| Support portal remote control | ✅ Implemented | `extensions/nucleus-support/` |
| Knowledgebase links in support portal | ✅ Implemented | `extensions/nucleus-support/` |
| Logging export | 🔧 Plugin/module required | `extensions/nucleus-core/` |
| Config reload | 🔧 Plugin/module required | `extensions/nucleus-core/` |
| API settings management | 🔧 Plugin/module required | `extensions/nucleus-core/` |
| BS-check system scan | 🔧 Plugin/module required | `extensions/nucleus-core/` |
| Security scan via CLI | 🔧 Plugin/module required | `extensions/nucleus-core/` |
| Certificate request (ACME) | 🔧 Plugin/module required | `extensions/nucleus-core/` |
| Staged update and rollback script | ✅ Process | `CRM/scripts/update.py` |
| OTAP pipeline with automated testing & vulnerability checks | ✅ Process | Documented in `CRM/README.md` |
