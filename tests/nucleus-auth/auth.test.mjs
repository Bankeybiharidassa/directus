import test from 'node:test';
import assert from 'node:assert/strict';
import passport from 'passport';
import register, { verifyToken, mapRole, exchangeToken } from '../../extensions/nucleus-auth/index.js';

// Reset strategy before each run
passport.unuse('nucleus-oauth');

const services = { logger: { info: () => {} } };

// Minimal env vars
process.env.OAUTH_AUTH_URL = 'http://auth';
process.env.OAUTH_TOKEN_URL = 'http://token';
process.env.NUCLEUS_CLIENT_ID = 'id';
process.env.NUCLEUS_SECRET = 'secret';
process.env.OAUTH_CALLBACK_URL = 'http://callback';

register({ services });

test('strategy registered', () => {
  assert.ok(passport._strategy('nucleus-oauth'));
});

test('invalid token', () => {
  assert.equal(verifyToken('bad'), null);
});

test('valid token', () => {
  const user = verifyToken('validtoken');
  assert.equal(user.role, 'admin');
});

test('role mapping', () => {
  assert.equal(mapRole('admin'), 'administrator');
  assert.equal(mapRole('unknown'), 'public');
});

test('token exchange', async () => {
  const data = await exchangeToken('good');
  assert.equal(data.access_token, 'validtoken');
  await assert.rejects(() => exchangeToken('bad'));
});
