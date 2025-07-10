# Nucleus OAuth2 Extension

This extension registers a Passport OAuth2 strategy to authenticate users via an external provider.

Environment variables required:
- `NUCLEUS_CLIENT_ID`
- `NUCLEUS_SECRET`
- `OAUTH_AUTH_URL`
- `OAUTH_TOKEN_URL`
- `OAUTH_CALLBACK_URL`

Once installed, admins can configure the OAuth2 credentials under **Settings → Auth Provider** in the Directus admin panel. The login page shows a **Sign in with Nucleus** button for users.
