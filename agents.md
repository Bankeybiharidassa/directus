# Codex Agent Instructions

The Nucleus CRM project uses a strict closed-loop workflow.
Agents must:

1. Record every code change in `changelog.md` with a numbered pass.
2. Track unresolved items in `todo.md`.
3. Run `npm test` whenever dependencies or code change.

Codex operates at temperature **0.2** and performs closed-loop passes until all
tests pass or a blocking issue is logged. Each loop must update `trace.json` and
`changelog.md`.

Governance rules forbid touching upstream Directus code outside the `CRM/` and `extensions/` directories.
Current prompt roles: **system**, **developer**, **user**.

For detailed CLI↔GUI mapping see `CRM/AGENTS.md`.

