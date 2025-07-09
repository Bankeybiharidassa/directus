import test from 'node:test';
import assert from 'node:assert/strict';
import passport from '../../CRM/extensions/nucleus-auth/node_modules/passport/lib/index.js';
import register from '../../CRM/extensions/nucleus-auth/index.js';
process.env.OAUTH_AUTH_URL = 'http://auth';
process.env.OAUTH_TOKEN_URL = 'http://token';
process.env.NUCLEUS_CLIENT_ID = 'id';
process.env.NUCLEUS_SECRET = 'secret';
process.env.OAUTH_CALLBACK_URL = 'http://callback';
register({services:{logger:{info:()=>{}}}});

test('strategy', () => {
  assert.ok(passport._strategies['nucleus-oauth']);
});
