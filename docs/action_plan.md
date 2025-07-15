# Extension Implementation Plan

This document summarizes the remaining work required to complete the Nucleus CRM extensions. Each module must be implemented and verified in isolation before moving on.

## Audit Implementation Steps
The AUDIT.md file lists outstanding flaws. Follow these steps to bring all extensions to production quality:
1. Set up a local dev environment and run tests.
2. Replace in-memory data with Directus collections.
3. Enforce RBAC and partner hierarchy.
4. Implement real OAuth2 login via Keycloak.
5. Integrate external services for mail, Tenable, Sophos and DMARC.
6. Build app modules for CRM and Support.
7. Run automated and manual tests for each module.
8. Iterate until all tests pass.
9. Update docs and clean up code.

The original CRM folder is now legacy; all features are being migrated to extensions.

## nucleus-auth
- Integrate OAuth2 (Keycloak) fully.
- On callback create or update a Directus user and assign a role.
- Unit test: simulate OAuth verify and assert the user is provisioned.

## nucleus-crm
- Add collections to maintain partner hierarchy.
- Enforce role-based access so partners only see their own data.
- Test: create sample hierarchy and verify RBAC restrictions.

## nucleus-contracts
- Define contract schema and lifecycle hooks.
- Provide endpoint or flow to terminate contracts.
- Test: create and terminate a contract, checking status.

## nucleus-docs
- Generate PDFs using fpdf2 or similar.
- Endpoint `/extensions/nucleus-docs/:id/export` returns a document.
- Test: call export and validate PDF output.

## nucleus-edi
- Format records as EDI messages and send to partners.
- Test: mock send function and confirm segments are produced.

## nucleus-support
- Ticket and asset collections with automation hooks.
- Optionally ingest emails via nucleus-mail-ingest.
- Test: create ticket, update status, verify hooks fire.

## nucleus-tenable / nucleus-sophos
- Scheduled jobs to sync vulnerability and endpoint data.
- Store results in Directus collections.
- Tests: mock API responses and verify database updates.

## nucleus-mail-ingest
- Connect to IMAP and create support tickets from emails.
- Ensure idempotency and robust error logging.

## nucleus-ui / nucleus-portal
- Serve custom login page and public portal pages.
- Support theming through uploaded CSS.
- Tests: headless UI script navigates pages per role.

## nucleus-core
- Admin utilities: config reload, log export, system scan, ACME certificates.
- Tests for each utility ensuring commands run without error.

After implementing a feature, update documentation and run the full test suite:
`npm test` and `pytest`. Fix any failing tests before continuing.
