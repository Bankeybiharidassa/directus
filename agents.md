# Codex Agent Instructions

The Nucleus CRM project uses a strict closed-loop workflow.
Agents must:

1. Record every code change in `changelog.md` with a numbered pass.
2. Track unresolved items in `todo.md`.
3. Run `npm test` whenever dependencies or code change.

Governance rules forbid touching upstream Directus code outside the `CRM/` and `extensions/` directories.
Current prompt roles: **system**, **developer**, **user**.

For detailed CLI↔GUI mapping see `CRM/AGENTS.md`.

