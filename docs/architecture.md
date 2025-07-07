# Nucleus CRM Architecture

The platform consists of a React frontend, a FastAPI backend and a Node.js service for OTP authentication.
Data is stored in a SQL database. External integrations like Sophos, Tenable and DMARC analyzer run as separate workers.
Extensions live under /extensions and are loaded by Directus.
