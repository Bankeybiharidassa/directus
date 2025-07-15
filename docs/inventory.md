<!-- markdownlint-disable MD013 -->
# Nucleus CRM – Inventory (Pass 08)
_Last updated: 2025-09-10_


The `CRM` folder is kept for legacy reference only. All listed modules are implemented as Directus extensions.
Extracted from: `/CRM/README.md`

| Feature | Category | Notes / Proposed Module |
|---------------------------------|----------------------------|---------------------------------------|
| Keycloak wizard for Auth & RBAC | ⚠️ Incomplete | `extensions/nucleus-auth/` |
| Hierarchical partners (admins→distributors→partners→endusers) | ⚠️ Incomplete | Schema + RBAC in `extensions/nucleus-crm/` |
| Contract lifecycle (create/terminate) | ⚠️ Incomplete | `extensions/nucleus-contracts/` |
| Document generator (PDF/TXT/CSV) | ⚠️ Incomplete | `extensions/nucleus-docs/` |
| EDI messaging between partners | ⚠️ Incomplete | `extensions/nucleus-edi/` |
| Supplier registration | ⚠️ Incomplete | `extensions/nucleus-suppliers/` |
| Support desk: tickets & assets | ⚠️ Incomplete | `extensions/nucleus-support/` |
| Asset vulnerabilities via Tenable | ⚠️ Incomplete | `extensions/nucleus-tenable/` |
| Sophos Central integration for asset sync | ✅ Implemented | `extensions/nucleus-sophos/` |
| `sophos_api_mode` selects partner or customer API | 🔧 Plugin/module required | `extensions/nucleus-sophos/` |
| Email sync via IMAP | ⚠️ Incomplete (external worker) | `extensions/nucleus-mail-ingest/` |
| CMS & public portal | ⚠️ Incomplete | `extensions/nucleus-portal/` |
| Portal access revocation | ⚠️ Incomplete | `extensions/nucleus-portal/` |
| DMARC analyzer & tenant stats | ⚠️ Incomplete | `extensions/nucleus-dmarc/` |
| Audit logging & encrypted storage | ⚠️ Incomplete (nucleus-core) | `extensions/nucleus-core/` |
| Granular RBAC for all actions & data | ⚠️ Incomplete | `extensions/nucleus-auth/` |
| Config via GUI + `.env` | ✅ Native Directus (partially) | Use Directus settings with env overrides |
| Role dashboards & menus | ⚠️ Incomplete | `extensions/nucleus-ui/` |
| API for asset sync & remote control | ⚠️ Incomplete | `extensions/nucleus-api/` |
| MFA with YubiKey, certificates, IP + TOTP | ⚠️ Incomplete | `extensions/nucleus-auth/` |
| Role-based login page & redirect | ⚠️ Incomplete | `extensions/nucleus-auth/` |
| Public landing page | ⚠️ Incomplete | `extensions/nucleus-ui/` |
| Customizable CSS themes via `frontend/templates` | ⚠️ Incomplete | `extensions/nucleus-ui/` |
| Support portal remote control | ⚠️ Incomplete | `extensions/nucleus-support/` |
| Knowledgebase links in support portal | ⚠️ Incomplete | `extensions/nucleus-support/` |
| Logging export | ⚠️ Incomplete | `extensions/nucleus-core/` |
| Config reload | ⚠️ Incomplete | `extensions/nucleus-core/` |
| API settings management | ⚠️ Incomplete | `extensions/nucleus-core/` |
| BS-check system scan | ⚠️ Incomplete | `extensions/nucleus-core/` |
| Security scan via CLI | ⚠️ Incomplete | `extensions/nucleus-core/` |
| Certificate request (ACME) | ✅ Implemented | `extensions/nucleus-core/` |
| Staged update and rollback script | ✅ Process | `CRM/scripts/update.py` |
| OTAP pipeline with automated testing & vulnerability checks | ✅ Process | Documented in `CRM/README.md` |
