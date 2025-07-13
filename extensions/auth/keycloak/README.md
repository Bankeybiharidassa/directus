# Keycloak Auth Extension

Provides OAuth2 login using Keycloak. Configure `KEYCLOAK_URL`, `KEYCLOAK_CLIENT_ID`, and `KEYCLOAK_CLIENT_SECRET` environment variables. The extension overrides the Directus login to exchange user credentials for a Keycloak token and then logs into Directus using that access token.
