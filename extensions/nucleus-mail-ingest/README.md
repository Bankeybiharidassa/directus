# Nucleus Mail Ingest Extension

Connects to an IMAP server every hour and parses incoming XML messages.

Required environment variables:
- `IMAP_HOST`
- `IMAP_USER`
- `IMAP_PASSWORD`

Admins manage the connection settings under **Support → Mail Ingest**. Parsed messages are stored as tickets in the support module.
