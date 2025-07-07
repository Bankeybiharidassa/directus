# Nucleus CRM Feature Inventory

## Table of Contents
- [Modules and Features](#modules-and-features)
- [Schema / Entities](#schema--entities)
- [Authentication & Integrations](#authentication--integrations)
- [Workflows & RBAC](#workflows--rbac)
- [Feature Classification](#feature-classification)
- [Proposed Modules and Folders](#proposed-modules-and-folders)
- [Additional Design Points from TODO](#additional-design-points-from-todo)
- [Architecture Overview](#architecture-overview)
Built from CRM/README.md and documentation files.
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

| Feature | Category |
| --- | --- |
| Directus login, roles & permissions | ✅ Native Directus |
| Keycloak identity provider | 🔧 Plugin/extension |
| YubiKey authentication | 🔧 Plugin/extension |
| IP/FQDN whitelist | 🔧 Plugin/extension |
| Remote support login_as | 🔧 Plugin/extension |
| Support call authorization | 🔧 Plugin/extension |
| ACME certificate requests | 🔧 Plugin/extension |
| Let's Encrypt certificate service | 🔧 Plugin/extension |
| Customer/partner/distributor entities | 🔧 Plugin/extension |
| EDI messaging | 🔧 Plugin/extension |
| IMAP mail sync | 🚧 External worker |
| Contract management | 🔧 Plugin/extension |
| Document generator | 🔧 Plugin/extension |
| DMARC analytics | 🔧 Plugin/extension + 🚧 IMAP worker |
| Ticketing & assets | 🔧 Plugin/extension |
| Sophos and Tenable sync | 🚧 External worker |
| Public portal & CMS pages | ✅ Native Directus |
| Security scan utilities | 🚧 External worker |
| Backup system | 🚧 External worker |
| Update script with staging | 🔧 Plugin/extension |

No features were found that cannot be implemented within Directus using extensions or external workers.

## Proposed Modules and Folders

| Feature | Proposed Folder |
| --- | --- |
| Authentication (Keycloak, MFA) | `extensions/nucleus-auth` |
| CRM Core (customers, partners, distributors) | `extensions/nucleus-crm` |
| Contract Management | `extensions/nucleus-contracts` |
| Document Generator | `extensions/nucleus-docs` |
| Support Desk & Assets | `extensions/nucleus-support` |
| CMS & Public Portal | `extensions/nucleus-cms` |
| Tenable Integration | `extensions/nucleus-tenable` |
| DMARC Analyzer | `extensions/nucleus-dmarc` |
| Security Scan & Backup | `extensions/nucleus-maintenance` |
| Update Script & OTAP | `scripts/` |

Each folder lives under `/extensions` or `/scripts` depending on function.

## Additional Design Points from TODO
- Extensive admin panel with grouped tabs
- Install script granting 10 grace logins before MFA enforcement
- YubiKey support with master key storage
- Keycloak integration wizard and fallback superadmin
- Backup system for settings, data, and secrets
- Updated hierarchy: nucleus → distributors → partners → endusers
- Support call authorization with audit logging
- IP/FQDN whitelist for external API
- OTAP update workflow with rollback
- Let's Encrypt certificate requests
- Template-driven GUI with per-role dashboards
- `test_install.sh` spins up backend and auth for local `lynx` testing
- `headless_check.js` captures screenshots and menu traces

## Architecture Overview
- React frontend communicates via REST with FastAPI backend
- Backend stores data in SQL database (MySQL/MariaDB, PostgreSQL, MSSQL, or SQLite)
- Node.js service handles OTP authentication
