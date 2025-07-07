
# Project Architecture

The repository contains a Directus-based platform with a modular CRM under the `CRM/` directory.
Core extensions reside in `extensions/` and are installed via `scripts/install.sh`.

# Nucleus CRM Architecture

The platform consists of a React frontend, a FastAPI backend and a Node.js service for OTP authentication.
Data is stored in a SQL database. External integrations like Sophos, Tenable and DMARC analyzer run as separate workers.
Extensions live under /extensions and are loaded by Directus.

## Integration Points

The CRM hooks into Directus only via supported extension mechanisms. Custom
endpoints and event handlers live in `/extensions` and are loaded at runtime.
The FastAPI backend exposes REST endpoints such as `/health` that Directus and
external services consume. The Node authentication service manages OTP login and
redirects users back to `/core/<role>` dashboards. CLI scripts under
`CRM/scripts/` mirror GUI operations as documented in `CRM/AGENTS.md`.

