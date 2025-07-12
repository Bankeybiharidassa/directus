export default function registerKeycloakAuth({ init }) {
  init('auth', ({ authentication }) => {
    authentication.login = async function (credentials) {
      const baseUrl = process.env.KEYCLOAK_URL;
      if (!baseUrl) {
        throw new Error('KEYCLOAK_URL not configured');
      }
      const params = new URLSearchParams({
        grant_type: 'password',
        client_id: process.env.KEYCLOAK_CLIENT_ID ?? 'directus',
        client_secret: process.env.KEYCLOAK_CLIENT_SECRET ?? '',
        username: credentials.email,
        password: credentials.password,
      });
      const res = await fetch(`${baseUrl}/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: params.toString(),
      });
      if (!res.ok) {
        throw new Error(`Keycloak login failed: ${res.status}`);
      }
      const data = await res.json();
      credentials.access_token = data.access_token;
      return this.loginWithCredentials(credentials);
    };
  });
}
