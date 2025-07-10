export default function registerKeycloakAuth({ init }) {
  init('auth', ({ authentication }) => {
    authentication.login = async function (credentials) {
      console.log('Keycloak login placeholder for', credentials.email);
      return this.loginWithCredentials(credentials);
    };
  });
}
