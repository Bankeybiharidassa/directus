# Extensions Directory

This folder is reserved for Directus extensions that are independent from the CRM modules under `CRM/extensions`.
Place custom interfaces, modules or plugins here so Directus can load them automatically.

This workspace contains the Directus extensions for the Nucleus platform.
Every package exports a `register()` function so Directus can load the routes
automatically. The most important packages are:

| Extension | Purpose |
|-----------|---------|
| `auth/keycloak` | OAuth2 login using Keycloak |
| `nucleus-auth` | Generic OAuth2 token exchange |
| `nucleus-crm` | Simple customer listing API |
| `nucleus-contracts` | Contract creation and termination |
| `nucleus-docs` | PDF/CSV document generation |
| `nucleus-edi` | Parse basic EDI XML messages |
| `nucleus-support` | Tickets and asset inventory |
| `nucleus-mail-ingest` | Periodic IMAP mail parsing |
| `nucleus-portal` | Public landing page |
| `nucleus-core` | Maintenance routes such as log export |
| `nucleus-api` | Asset sync and remote control helpers |
| `nucleus-dmarc` | DMARC report handling |
| `nucleus-sophos` | Sophos Central status endpoint |
| `nucleus-tenable` | Example Tenable asset data |
| `nucleus-suppliers` | Supplier registration demo |
| `nucleus-ui` | Generated theme stylesheet |

Refer to `docs/inventory.md` and the individual READMEs for details.
