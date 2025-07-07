# Nucleus CRM – Inventory (Pass 01)

Extracted from: `/CRM/README.md`

| Feature                            | Category                  | Notes / Proposed Module         |
|------------------------------------|----------------------------|----------------------------------|
| Multi-tenant access per client     | 🔧 Plugin/module required  | `extensions/nucleus-auth/` + RBAC hook |
| OAuth2 for MS365 & NinjaOne        | 🔧 Plugin/module required  | `extensions/nucleus-auth/`       |
| Email ingestion via IMAP/XML       | 🚧 External worker required | `extensions/nucleus-mail-ingest/` |
| Audit logging                      | 🔧 Plugin/module required  | `extensions/nucleus-core/`       |
| CRM: clients, contacts, tickets    | 🔧 Plugin/module required  | Define schema in `nucleus-core/schema/` |
| Config via GUI + `.env`            | ✅ Native Directus (partially) | Extend via GUI collection override |
| Dashboards per tenant              | 🔧 Plugin/module required  | `extensions/nucleus-ui/`        |
| API: assign contacts, ticket stats | 🔧 Plugin/module required  | `extensions/nucleus-api/`       |
