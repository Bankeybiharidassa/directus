
# Project Architecture

The repository contains a Directus-based platform with a modular CRM under the `CRM/` directory.
Core extensions reside in `extensions/` and are installed via `scripts/install.sh`.

# Nucleus CRM Architecture

The platform consists of a React frontend, a FastAPI backend and a Node.js service for OTP authentication.
Data is stored in a SQL database. External integrations like Sophos, Tenable and DMARC analyzer run as separate workers.
Extensions live under /extensions and are loaded by Directus.

