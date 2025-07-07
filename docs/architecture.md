
# Project Architecture

The repository contains a Directus-based platform with a modular CRM under the `CRM/` directory.
Core extensions reside in `extensions/` and are installed via `scripts/install.sh`.

# Nucleus CRM Architecture

The platform consists of a React frontend, a FastAPI backend and a Node.js service for OTP authentication.
Data is stored in a SQL database. External integrations like Sophos, Tenable and DMARC analyzer run as separate workers.
Extensions live under /extensions and are loaded by Directus.

## Module Layout

```
CRM/                # CRM specific React and FastAPI modules
extensions/         # Directus extensions (endpoints, hooks, interfaces)
scripts/            # Helper CLI scripts and installers
docs/               # User and developer documentation
```

Each extension can be enabled or disabled independently so deployments can remain lightweight.

## Integration Points

The CRM hooks into Directus only via supported extension mechanisms. Custom
endpoints and event handlers live in `/extensions` and are loaded at runtime.
The FastAPI backend exposes REST endpoints such as `/health` that Directus and
external services consume. The Node authentication service manages OTP login and
redirects users back to `/core/<role>` dashboards. CLI scripts under
`CRM/scripts/` mirror GUI operations as documented in `CRM/AGENTS.md`.

## Planned Authentication Flow

1. Users visit `/auth/login` served by the Node.js service.
2. Credentials and OTP tokens are validated against the FastAPI backend.
3. Upon success, the backend issues a signed JWT using `NUCLEUS_AUTH_SECRET` from the environment.
4. The JWT is stored in a Directus session and the user is redirected to the CRM dashboard.
5. Failed logins are logged to `/var/log/nucleus/auth.log` for review.

