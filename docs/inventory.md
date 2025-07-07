# Nucleus CRM Feature Inventory

This document summarizes all features described in the `/CRM` directory. Each feature is mapped against the Directus platform to determine whether it can be implemented natively, requires an extension, needs an external worker or is not feasible.

## Modules and Features

### G1 – Authentication & RBAC
- Keycloak wizard for external identity provider
- Multi‑factor authentication (TOTP, YubiKey)
- IP and FQDN whitelist
- Remote support login (`authorize`, `revoke`, `login_as`)
- ACME certificate request API

### G2 – Customers, Partners, Distributors, Suppliers
- Customer, partner, distributor and supplier records
- Hierarchical relations: **nucleus admins → distributors → partners → endusers**
- EDI messaging between distributors and partners
- Import tenants and users from external CRM
- Mail sync via IMAP per tenant

### G3 – Contract Management
- CRUD for contracts with termination workflow

### G4.1 – Document Generator
- PDF, TXT and CSV exports
- Invoice and management report generation

### G4.2 – CRM & Partner Structure
- Manage partners, distributors and end users
- View tenant statistics
- Assign domains with IMAP/SMTP details
- DMARC analytics per domain

### G4.3 – Support Desk & Assets
- Ticket system with list view
- Asset registration and vulnerability tracking
- Sophos Central integration

### G4.4 – CMS & Public Portal
- Page creation and publishing
- Role‑based dashboards and menus
- Public landing page and support portal

### G4.5 – Tenable Integration
- Sync assets and vulnerabilities from Tenable.io/sc

### G4.6 – DMARC Analyzer
- Domain mapping and per‑tenant statistics
- Abuse reporting and status updates

### Core Functions
- Logging export and configuration reload
- Security scan (packages, binaries, ports, Bandit)
- Backup utilities with full and incremental modes
- Update script with staging and rollback

## Schema / Entities
- Users and roles
- Customers, distributors, partners, end users
- Contracts, cases and tickets
- Assets and vulnerabilities
- Domains with IMAP/SMTP fields
- EDI messages
- IP whitelist
- Tenable and Sophos configuration
- DMARC reports and abuse entries

## Authentication & Integrations
- Keycloak for user management
- Node.js service for OTP login
- FastAPI backend for CRM APIs
- IMAP for mail fetching
- Tenable.io/sc and Sophos Central APIs
- Let’s Encrypt for certificate requests

## Workflows & RBAC
- Closed‑loop OTAP lifecycle: design → build → test → verify
- Roles: admin, company user, distributor, partner, end user, support, audit
- Each CLI command mirrored in the GUI
- Multi‑tenant isolation enforced via headers (`X-CRM-Tenant`)

## Feature Classification

| Feature | Category | Module/Plugin Path |
| --- | --- | --- |
| Directus login, roles & permissions | ✅ Native Directus | directus core |
| Keycloak identity provider | 🔧 Plugin/extension | CRM/extensions/nucleus-auth |
| YubiKey authentication | 🔧 Plugin/extension | CRM/extensions/nucleus-auth |
| IP/FQDN whitelist | 🔧 Plugin/extension | CRM/extensions/ip-whitelist |
| Remote support login_as | 🔧 Plugin/extension | CRM/extensions/remote-support |
| ACME certificate requests | 🔧 Plugin/extension | CRM/extensions/certbot |
| Customer/partner/distributor entities | 🔧 Plugin/extension | CRM/backend/models |
| EDI messaging | 🔧 Plugin/extension | CRM/extensions/edi-messaging |
| IMAP mail sync | 🚧 External worker | CRM/extensions/nucleus-mail-ingest |
| Contract management | 🔧 Plugin/extension | CRM/extensions/contract-manager |
| Document generator | 🔧 Plugin/extension | CRM/extensions/doc-generator |
| DMARC analytics | 🔧 Plugin/extension + 🚧 IMAP worker | CRM/extensions/dmarc, CRM/workers/imap-sync |
| Ticketing & assets | 🔧 Plugin/extension | CRM/extensions/ticketing |
| Sophos and Tenable sync | 🚧 External worker | CRM/workers/security-sync |
| Public portal & CMS pages | ✅ Native Directus | directus core |
| Security scan utilities | 🚧 External worker | CRM/workers/security-scan |
| Backup system | 🚧 External worker | CRM/extensions/backup |
| Update script with staging | 🔧 Plugin/extension | CRM/scripts/update.sh |

No features were found that cannot be implemented within Directus using extensions or external workers.
