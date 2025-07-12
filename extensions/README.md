# Extensions Directory

This folder is reserved for Directus extensions that are independent from the CRM modules under `CRM/extensions`.
Place custom interfaces, modules or plugins here so Directus can load them automatically.

This workspace now contains a Keycloak authentication extension under
`extensions/auth/keycloak`. It implements a login flow that exchanges the user's
credentials for a token via the configured Keycloak server before delegating to
Directus. See `docs/inventory.md` for other planned packages.
