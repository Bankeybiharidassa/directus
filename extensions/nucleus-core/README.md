# Nucleus Core Extension

Provides common utilities and logging for the Nucleus CRM plugins.
The extension exposes several maintenance endpoints:

* `GET /core/log/export` – download the Directus log
* `POST /core/config/reload` – reload the configuration
* `GET /core/api/settings` – return example API settings
* `POST /core/bs-check` – run a basic system check
* `POST /core/security-scan` – start a security scan
* `POST /core/cert/request` – request an ACME certificate

The extension also logs a startup message when loaded.
