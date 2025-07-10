import test from 'node:test';
import assert from 'node:assert/strict';
import register from '../../extensions/auth/keycloak/index.js';
let called = false;
const auth = { loginWithCredentials: async () => { called = true; } };
const init = (_name, fn) => { fn({ authentication: auth }); };
register({ init });
await auth.login({ email: 'a@example.com' }).catch(() => {});
await test('keycloak auth overrides login', () => {
  assert.ok(called);
});
