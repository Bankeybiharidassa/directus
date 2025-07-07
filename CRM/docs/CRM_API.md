# CRM API

## Sync endpoints

- `POST /api/crm/sync/import` – Import tenants and users from an external CRM.
  - Optional parameter `source_url` overrides `CRM_SYNC_URL` environment variable.
- CLI: `crm_sync import [--url=<crm url>]`

## Support endpoints

- `POST /support/authorize` – current user authorizes remote support access.
- `POST /support/revoke` – revoke previously granted access.
- `POST /support/login_as/{user_id}` – support or audit role impersonates a user when authorized.

## EDI endpoints

- `POST /edi/` – send an EDI message. Parameters: `sender_type`, `sender_id`, `receiver_type`, `receiver_id`, `content`.
- `GET /edi/` – list all EDI messages (admin only).

## Certificate endpoints

- `POST /certificates/request` – Request Let's Encrypt certificates for one or more hostnames. Body: `{ "hostnames": ["example.com"], "email": "admin@example.com" }`
