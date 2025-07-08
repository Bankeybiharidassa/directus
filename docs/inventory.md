<!-- markdownlint-disable MD013 -->
# Nucleus CRM – Inventory (Pass 07)
_Last updated: 2025-07-08_


Extracted from: `/CRM/README.md`

| Feature | Category | Notes / Proposed Module |
|---------------------------------|----------------------------|---------------------------------------|
| Keycloak wizard for Auth & RBAC | 🔧 Plugin/module required | `extensions/nucleus-auth/` |
| Hierarchical partners (admins→distributors→partners→endusers) | 🔧 Plugin/module required | Schema + RBAC in `extensions/nucleus-crm/` |
| Contract lifecycle (create/terminate) | 🔧 Plugin/module required | `extensions/nucleus-contracts/` |
| Document generator (PDF/TXT/CSV) | 🔧 Plugin/module required | `extensions/nucleus-docs/` |
| EDI messaging between partners | 🔧 Plugin/module required | `extensions/nucleus-edi/` |
| Support desk: tickets & assets | 🔧 Plugin/module required | `extensions/nucleus-support/` |
| Asset vulnerabilities via Tenable | 🔧 Plugin/module required | `extensions/nucleus-tenable/` |
| Sophos Central integration for asset sync | 🔧 Plugin/module required | `extensions/nucleus-sophos/` |
| `sophos_api_mode` selects partner or customer API | 🔧 Plugin/module required | `extensions/nucleus-sophos/` |
| Email sync via IMAP | 🚧 External worker required | `extensions/nucleus-mail-ingest/` |
| CMS & public portal | 🔧 Plugin/module required | `extensions/nucleus-portal/` |
| Portal access revocation | 🔧 Plugin/module required | `extensions/nucleus-portal/` |
| DMARC analyzer & tenant stats | 🔧 Plugin/module required | `extensions/nucleus-dmarc/` |
| Audit logging & encrypted storage | 🔧 Plugin/module required | `extensions/nucleus-core/` |
| Granular RBAC for all actions & data | 🔧 Plugin/module required | `extensions/nucleus-auth/` |
| Config via GUI + `.env` | ✅ Native Directus (partially) | Use Directus settings with env overrides |
| Role dashboards & menus | 🔧 Plugin/module required | `extensions/nucleus-ui/` |
| API for asset sync & remote control | 🔧 Plugin/module required | `extensions/nucleus-api/` |
| MFA with YubiKey, certificates, IP + TOTP | 🔧 Plugin/module required | `extensions/nucleus-auth/` |
| Role-based login page & redirect | 🔧 Plugin/module required | `extensions/nucleus-auth/` |
| Public landing page | 🔧 Plugin/module required | `extensions/nucleus-ui/` |
| Customizable CSS themes via `frontend/templates` | 🔧 Plugin/module required | `extensions/nucleus-ui/` |
| Support portal remote control | 🔧 Plugin/module required | `extensions/nucleus-support/` |
| Knowledgebase links in support portal | 🔧 Plugin/module required | `extensions/nucleus-support/` |
| Logging export | 🔧 Plugin/module required | `extensions/nucleus-core/` |
| Config reload | 🔧 Plugin/module required | `extensions/nucleus-core/` |
| API settings management | 🔧 Plugin/module required | `extensions/nucleus-core/` |
| BS-check system scan | 🔧 Plugin/module required | `extensions/nucleus-core/` |
| Security scan via CLI | 🔧 Plugin/module required | `extensions/nucleus-core/` |
| Certificate request (ACME) | 🔧 Plugin/module required | `extensions/nucleus-core/` |
| Staged update and rollback script | ✅ Process | `CRM/scripts/update.py` |
| OTAP pipeline with automated testing & vulnerability checks | ✅ Process | Documented in `CRM/README.md` |
