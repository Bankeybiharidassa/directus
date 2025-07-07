<!-- markdownlint-disable MD013 -->
# Nucleus CRM – Inventory (Pass 04)


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
| Email sync via IMAP | 🚧 External worker required | `extensions/nucleus-mail-ingest/` |
| CMS & public portal | 🔧 Plugin/module required | `extensions/nucleus-portal/` |
| DMARC analyzer & tenant stats | 🔧 Plugin/module required | `extensions/nucleus-dmarc/` |
| Audit logging & encrypted storage | 🔧 Plugin/module required | `extensions/nucleus-core/` |
| Config via GUI + `.env` | ✅ Native Directus (partially) | Use Directus settings with env overrides |
| Role dashboards & menus | 🔧 Plugin/module required | `extensions/nucleus-ui/` |
| API for asset sync & remote control | 🔧 Plugin/module required | `extensions/nucleus-api/` |

| MFA with YubiKey, certificates, IP + TOTP | 🔧 Plugin/module required | `extensions/nucleus-auth/` |
| Role-based login page & redirect | 🔧 Plugin/module required | `extensions/nucleus-auth/` |
| Public landing page | 🔧 Plugin/module required | `extensions/nucleus-ui/` |
| Support portal remote control | 🔧 Plugin/module required | `extensions/nucleus-support/` |
