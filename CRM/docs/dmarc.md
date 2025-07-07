# DMARC Module

Deze module analyseert DMARC-rapporten per domein en toont de statistieken in het CRM.

- API: `/dmarc/{domain}`
- CLI: `nucleus dmarc report <domain>`
- GUI: Beheer > Mail > DMARC

## CRM integratie

- API: `/api/crm/dmarc/{tenant_id}/{domain}?format=json|csv`
- CLI: `nucleus dmarc crm-report <tenant_id> <domain> [--format=csv]`
- API: `/api/crm/domains/` (POST) en `/api/crm/domains/{tenant_id}` (GET)
 - Voor RBAC moet de header `X-CRM-Tenant` overeenkomen met de tenant ID.
 - Domeinen ondersteunen nu IMAP- en SMTP-velden.
- API: `/api/crm/dmarc/abuse` (POST)
 - Parameters: `tenant_id`, `domain`, `ip`, `contact`
- CLI: `nucleus dmarc abuse <tenant_id> <domain> <ip> <contact>`
- API: `/api/crm/dmarc/abuse/{id}` (PUT) om status te wijzigen
- CLI: `nucleus dmarc abuse-status <id> <status>`

