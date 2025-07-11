import test from 'node:test';
import assert from 'node:assert/strict';
import passport from 'passport';
import register from '../../extensions/nucleus-auth/index.js';

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
