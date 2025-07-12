import test from 'node:test';
import assert from 'node:assert/strict';
import register from '../../extensions/auth/keycloak/index.js';

let called = false;
const auth = {
  loginWithCredentials: async (creds) => {
    if (creds.access_token === 'abc123') {
      called = true;
    }
  },
};

global.fetch = async () => ({ ok: true, json: async () => ({ access_token: 'abc123' }) });
process.env.KEYCLOAK_URL = 'http://kc';

const init = (_name, fn) => {
  fn({ authentication: auth });
};

register({ init });

await auth.login({ email: 'a@example.com', password: 'pw' });

await test('keycloak auth fetches token and logs in', () => {
  assert.ok(called);
});
